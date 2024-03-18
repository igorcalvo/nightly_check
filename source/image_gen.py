from datetime import date, timedelta
from pandas import DataFrame
from PIL import Image, ImageFont, ImageDraw

from source.constants import date_header, font_families, DATA_VISUALIZATION
from source.core.data_vis import (
    calculate_x_position,
    get_date_array,
    get_expected_value,
    get_fail_indexes_list,
    get_habit_data,
    get_rgb_color,
    get_weekdays_characters,
    generate_y_positions,
    segment_unit_into_list,
    text_list_max_len_to_pixels,
)
from source.utils import (
    align_right,
    cycle_index,
    flatten_list,
    get_value_from_df_by_row,
)


def new_image(size_x: int, size_y: int, background_color: tuple[int, int, int]):
    return Image.new("RGB", (size_x, size_y), background_color)


# 6 pixels / char + 1 @ 12
def write(
    image: Image.Image,
    position: tuple[int, int],
    text: str,
    color: tuple[int, int, int],
    font_family: str = "consolas",
    size: int = 12,
):
    draw = ImageDraw.Draw(image)
    draw.text(
        position, text, color, font=ImageFont.truetype(font_families[font_family], size)
    )


def write_category_header(
    image: Image.Image,
    position: tuple[int, int],
    category: str,
    max_category_len: int,
    square_size: int,
    square_border: int,
    squares: int,
    latest_date: str,
    dark_theme: bool,
):
    write(
        image,
        position,
        align_right(category.upper(), max_category_len),
        (
            DATA_VISUALIZATION.text
            if not dark_theme
            else DATA_VISUALIZATION.dark_theme_text
        ),
        "liberation",
    )
    habit_font_size_length = 7
    habit_font_size_spacing = 1
    magic_number = 5
    habit_font_constant = habit_font_size_length + habit_font_size_spacing
    oldest_date = date(
        int(latest_date.split("-")[0]),
        int(latest_date.split("-")[1]),
        int(latest_date.split("-")[2]),
    ) + timedelta(days=(-squares + 1))
    current_date = oldest_date
    initial_pos_x = position[0] + max_category_len * habit_font_constant + magic_number
    for s in range(squares):
        if current_date.day == 1 or (oldest_date - current_date).days % 7 == 0:
            write(
                image,
                (
                    calculate_x_position(initial_pos_x, s, square_size, square_border),
                    position[1],
                ),
                (
                    f"0{current_date.day}"
                    if current_date.day < 10
                    else str(current_date.day)
                ),
                (
                    DATA_VISUALIZATION.text
                    if not dark_theme
                    else DATA_VISUALIZATION.dark_theme_text
                ),
                "noto",
            )
        current_date += timedelta(days=+1)


def write_footer(
    image: Image.Image,
    position: tuple[int, int],
    square_size: int,
    square_border: int,
    squares: int,
    latest_date: str,
    weekdays_language: str,
    dark_theme: bool,
):
    days_of_the_week = get_weekdays_characters(weekdays_language)
    todays_index = date.fromisoformat(latest_date).weekday()
    for s in range(squares):
        write(
            image,
            (
                calculate_x_position(position[0], s, square_size, square_border),
                position[1],
            ),
            cycle_index(days_of_the_week, todays_index - squares + s + 1),
            (
                DATA_VISUALIZATION.text
                if not dark_theme
                else DATA_VISUALIZATION.dark_theme_text
            ),
            "noto",
        )


def draw_line_of_squares(
    image: Image.Image,
    position: tuple[int, int],
    square_size: int,
    square_border: int,
    squares: int,
    skipped: list[int],
    square_color: tuple[int, int, int],
    skipped_color: tuple[int, int, int],
):
    for square_index in range(squares):
        color = skipped_color if square_index in skipped else square_color
        for square_x_pixel in range(square_size):
            for square_y_pixel in range(square_size):
                image.putpixel(
                    (
                        position[0]
                        + square_index * (square_size + square_border)
                        + square_x_pixel,
                        position[1] + square_y_pixel,
                    ),
                    color,
                )


def write_all(
    image: Image.Image,
    categories: list[str],
    habits: list[list[str]],
    conditions: list[list[str]],
    data: DataFrame,
    position: tuple[int, int],
    squares: int,
    sqr_size: int,
    sqr_border: int,
    max_x_delta: int,
    text_squares_x_spacing: int,
    text_squares_y_offset: int,
    category_y_spacing: int,
    category_text_offset: tuple[int, int],
    graph_expected_value: bool,
    weekdays_language: str,
    dark_theme: bool,
):
    max_habit_len = max([len(h) for h in flatten_list(habits)])
    max_category_len = max([len(c) for c in categories])
    max_category_text_offset = text_list_max_len_to_pixels(categories)
    initial_pos = [position[0], position[1]]
    footer_text_offset = (12, 6)
    hues = segment_unit_into_list(len(categories))
    date_array = get_date_array(data, squares)

    for category_index, category in enumerate(categories):
        category_positions, next_category_position = generate_y_positions(
            (initial_pos[0], initial_pos[1]),
            sqr_size,
            2,
            len(habits[category_index]),
        )
        write_category_header(
            image,
            (
                initial_pos[0] + category_text_offset[0] - max_category_text_offset,
                category_positions[0][1] - category_text_offset[1],
            ),
            category,
            max_category_len,
            sqr_size,
            sqr_border,
            squares,
            get_value_from_df_by_row(date_header, -1, data),
            dark_theme,
        )
        for habit_index, habit in enumerate(habits[category_index]):
            expected_value = get_expected_value(habit, habits, conditions)
            habit_data = get_habit_data(
                data,
                date_array,
                squares,
                habit,
                expected_value if graph_expected_value else True,
            )
            fail_list = get_fail_indexes_list(
                habit_data, expected_value if graph_expected_value else True
            )
            hueOffset = (hues[1] - hues[0]) / (len(habits[category_index]) + 1)
            write(
                image,
                category_positions[habit_index],
                align_right(habit, max_habit_len),
                (
                    DATA_VISUALIZATION.text
                    if not dark_theme
                    else DATA_VISUALIZATION.dark_theme_text
                ),
            )
            draw_line_of_squares(
                image,
                (
                    initial_pos[0] + max_x_delta + text_squares_x_spacing,
                    category_positions[habit_index][1] - text_squares_y_offset,
                ),
                sqr_size,
                sqr_border,
                squares,
                fail_list,
                # GetRGBColor(0.5, 0.75, 1)
                # GetRGBColor(hues[category_index], saturations[habit_index], 1),
                get_rgb_color(hues[category_index] + habit_index * hueOffset, 0.85, 1),
                (
                    DATA_VISUALIZATION.skipped
                    if not dark_theme
                    else DATA_VISUALIZATION.dark_theme_skipped
                ),
            )
        initial_pos[1] = initial_pos[1] + next_category_position + category_y_spacing
        write_footer(
            image,
            (
                initial_pos[0]
                + max_x_delta
                + text_squares_x_spacing
                + ((sqr_size - footer_text_offset[0]) // 2),
                initial_pos[1] - category_y_spacing - footer_text_offset[1],
            ),
            sqr_size,
            sqr_border,
            squares,
            get_value_from_df_by_row(date_header, -1, data),
            weekdays_language,
            dark_theme,
        )


def generate_image(
    categories: list[str],
    habits: list[list[str]],
    conditions: list[list[str]],
    data_days: int,
    graph_expected_value: bool,
    weekdays_language: str,
    dark_theme: bool,
    data: DataFrame,
):
    flat_habit_list = flatten_list(habits)
    rows = len(flat_habit_list)
    categories_length = len(categories)
    squares = min([data_days, len(data.index)])
    max_x_delta = text_list_max_len_to_pixels(flat_habit_list)
    category_text_offset = (max_x_delta - 0, int(1.2 * DATA_VISUALIZATION.sqrSize))

    img = new_image(
        squares * (DATA_VISUALIZATION.sqrSize + DATA_VISUALIZATION.sqrBorder)
        + max_x_delta
        + DATA_VISUALIZATION.text_squares_x_spacing
        + 2 * DATA_VISUALIZATION.initial_x,
        rows
        * (
            DATA_VISUALIZATION.rows_y_spacing
            + DATA_VISUALIZATION.sqrSize
            + DATA_VISUALIZATION.sqrBorder
        )
        + (categories_length - 1)
        * (DATA_VISUALIZATION.category_y_spacing + DATA_VISUALIZATION.rows_y_spacing)
        + DATA_VISUALIZATION.initial_y,
        (
            DATA_VISUALIZATION.background
            if not dark_theme
            else DATA_VISUALIZATION.dark_theme_background
        ),
    )
    # DrawLineOfSquares(img, (2 * sqrSize, 2 * sqrSize), sqrSize, sqrBorder, days, [5, 10, 13], GetRGBColor(0.5, 0.75, 1), (150, 150, 150))
    write_all(
        img,
        categories,
        habits,
        conditions,
        data,
        (DATA_VISUALIZATION.initial_x, DATA_VISUALIZATION.initial_y),
        squares,
        DATA_VISUALIZATION.sqrSize,
        DATA_VISUALIZATION.sqrBorder,
        max_x_delta,
        DATA_VISUALIZATION.text_squares_x_spacing,
        DATA_VISUALIZATION.text_squares_y_offset,
        DATA_VISUALIZATION.category_y_spacing,
        category_text_offset,
        graph_expected_value,
        weekdays_language,
        dark_theme,
    )
    # img.show()
    # img.save(r'assets\data\test.png')
    return img

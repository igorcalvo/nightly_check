from datetime import date, timedelta
from PIL import Image, ImageFont, ImageDraw
import matplotlib.colors as clr

from .utils import flatten_list, align_right, cycle_index, get_value_from_df_by_row
from .core import get_header_data, get_date_array, get_fail_indexes_list, get_expeted_value, date_header

font_families = {
    "consolas": r"assets\fonts\consola.ttf",
    "roboto": r"assets\fonts\Roboto-Bold.ttf",
    "liberation": r"assets\fonts\LiberationMono-Bold.ttf",
    "noto": r"assets\fonts\NotoSansJP-Regular.otf",
}

def segment_unit_into_list(n: int, min_offset: float = 0, max_offset: float = 1) -> list:
    if n <= 0:
        raise Exception(f"SegmentUnitIntoList: n can't be <= 0. Got: {n}")
    elif min_offset >= max_offset or min_offset < 0 or max_offset > 1:
        raise Exception(f"SegmentUnitIntoList: Offsets out of range. Got min: {min_offset} and max: {max_offset}")
    length: float = ((max_offset - min_offset) / n) if n > 1 else 0
    result = [min_offset + length * i for i in range(n)]
    return result

def get_rgb_color(hue: float, saturation: float, value: float) -> tuple:
                                   # 0 to 1
    rgb_float = clr.hsv_to_rgb((hue, saturation, value))
    result = tuple(int(v * 255) for v in rgb_float)
    return result

def draw_line_of_squares(image, position: tuple, square_size: int, square_border: int, squares: int, skipped: list, square_color: tuple, skipped_color: tuple):
    for square_index in range(squares):
        color = skipped_color if square_index in skipped else square_color
        for square_x_pixel in range(square_size):
            for square_y_pixel in range(square_size):
                image.putpixel((position[0] + square_index * (square_size + square_border) + square_x_pixel, position[1] + square_y_pixel), color)

def new_image(size_x: int, size_y: int, background_color=(255, 255, 255)):
    return Image.new('RGB', (size_x, size_y), background_color)

# 6 pixels / char + 1 @ 12
def write(image, position: tuple, text: str, color: tuple, font_family: str = "consolas", size: int = 12):
    draw = ImageDraw.Draw(image)
    draw.text(
        position,
        text,
        color,
        font=ImageFont.truetype(font_families[font_family], size)
    )

def text_list_max_len_to_pixels(textList: list, font_size_length: int = 6, font_size_spacing: int = 1) -> int:
    return max([len(text) for text in textList]) * (font_size_length + font_size_spacing)

def generate_y_positions(initial_position: tuple, length: int, spacing: int, number: int) -> tuple:
    positions = [(initial_position[0], initial_position[1] + (length + spacing) * n) for n in range(number)]
    return positions, positions[-1][1] + length + spacing - initial_position[1]

def calculate_x_position(initial_pos_x, index, square_size, square_border):
    return initial_pos_x + index * (square_size + square_border)

def write_category_header(image, position: tuple, category: str, max_category_len: int, square_size: int, square_border: int, squares: int, latest_date: str):
    write(image, position, align_right(category.upper(), max_category_len), (0, 0, 0), "liberation")
    header_font_size_length = 7
    header_font_size_spacing = 1
    header_font_constant = header_font_size_length + header_font_size_spacing
    oldest_date = date(int(latest_date.split('-')[0]), int(latest_date.split('-')[1]), int(latest_date.split('-')[2])) + timedelta(days=(-squares + 1))
    current_date = oldest_date
    for s in range(squares):
        if current_date.day == 1 or (oldest_date - current_date).days % 7 == 0:
            initial_pos_x = position[0] + max_category_len * header_font_constant - 1
            if current_date.day < 10:
                initial_pos_x += header_font_constant
            write(image,
                  (calculate_x_position(initial_pos_x, s, square_size, square_border), position[1]),
                  f'0{current_date.day}' if current_date.day < 10 else str(current_date.day),
                  (0, 0, 0),
                  "noto")
        current_date += timedelta(days=+1)

def write_footer(image, position: tuple, square_size: int, square_border: int, squares: int, latest_date: str):
    # days_of_the_week = "STQQSSD"
    # days_of_the_week = "MTWTFSS"
    days_of_the_week = "月火水木金土日"
    todays_index = date.fromisoformat(latest_date).weekday()
    for s in range(squares):
        write(image,
              (calculate_x_position(position[0], s, square_size, square_border), position[1]),
              cycle_index(days_of_the_week, todays_index - squares + s + 1),
              (0, 0, 0),
              "noto")

def write_all(image, categories: list, header_list: list, conditions: list, data, position: tuple, squares: int, sqr_size: int, sqr_border: int, max_x_delta: int,
              text_squares_x_spacing: int, text_squares_y_offset: int, category_y_spacing: int, category_text_offset: tuple, graph_expected_value: bool):
    max_header_len = max([len(h) for h in flatten_list(header_list)])
    max_category_len = max([len(c) for c in categories])
    max_category_text_offset = text_list_max_len_to_pixels(categories)
    initial_pos = [position[0], position[1]]
    footer_text_offset = (12, 6)
    hues = segment_unit_into_list(len(categories))
    date_array = get_date_array(data, squares)

    for category_index, category in enumerate(categories):
        category_positions, next_category_position = generate_y_positions((initial_pos[0], initial_pos[1]), sqr_size, 2, len(header_list[category_index]))
        write_category_header(image,
                              (initial_pos[0] + category_text_offset[0] - max_category_text_offset,
                               category_positions[0][1] - category_text_offset[1]),
                              category,
                              max_category_len,
                              sqr_size,
                              sqr_border,
                              squares,
                              get_value_from_df_by_row(date_header, -1, data))
        for header_index, header in enumerate(header_list[category_index]):
            expected_value = get_expeted_value(header, header_list, conditions)
            header_data = get_header_data(data, date_array, squares, header, expected_value if graph_expected_value else True)
            fail_list = get_fail_indexes_list(header_data, expected_value if graph_expected_value else True)
            # print(header, header_data)
            hueOffset = (hues[1] - hues[0]) / (len(header_list[category_index]) + 1)
            write(image,
                  category_positions[header_index],
                  align_right(header, max_header_len),
                  (0, 0, 0))
            draw_line_of_squares(image,
                                 (initial_pos[0] + max_x_delta + text_squares_x_spacing,
                                  category_positions[header_index][1] - text_squares_y_offset),
                                 sqr_size,
                                 sqr_border,
                                 squares,
                                 fail_list,
                                 # GetRGBColor(0.5, 0.75, 1)
                                 # GetRGBColor(hues[category_index], saturations[header_index], 1),
                                 get_rgb_color(hues[category_index] + header_index * hueOffset, 0.85, 1),
                                 get_rgb_color(0, 0, 0.75))
        initial_pos[1] = initial_pos[1] + next_category_position + category_y_spacing
        write_footer(image,
                     (initial_pos[0] + max_x_delta + text_squares_x_spacing + ((sqr_size - footer_text_offset[0]) // 2),
                      initial_pos[1] - category_y_spacing - footer_text_offset[1]),
                     sqr_size,
                     sqr_border,
                     squares,
                     get_value_from_df_by_row(date_header, -1, data))

def generate_image(categories: list, header: list, conditions: list, data_days: int, graph_expected_value: bool, data):
    flat_header_list = flatten_list(header)
    initial_x = 25
    initial_y = 50
    rows = len(flat_header_list)
    rows_y_spacing = 2
    categories_length = len(categories)

    sqrSize = 20
    sqrBorder = 1
    squares = min([data_days, len(data.index)])

    max_x_delta = text_list_max_len_to_pixels(flat_header_list)

    text_squares_x_spacing = int(0.5 * sqrSize)
    text_squares_y_offset = int(0.25 * sqrSize)

    category_y_spacing = int(2 * sqrSize)
    category_text_offset = (max_x_delta - 0, int(1.2 * sqrSize))

    img = new_image(squares * (sqrSize + sqrBorder) + max_x_delta + text_squares_x_spacing + 2 * initial_x,
                    # rows * (rows_y_spacing + sqrSize + sqrBorder) + (categories_length - 1) * (category_y_spacing - rows_y_spacing) + initial_y)
                    rows * (rows_y_spacing + sqrSize + sqrBorder) + (categories_length - 1) * (category_y_spacing + rows_y_spacing) + initial_y)
    # DrawLineOfSquares(img, (2 * sqrSize, 2 * sqrSize), sqrSize, sqrBorder, days, [5, 10, 13], GetRGBColor(0.5, 0.75, 1), (150, 150, 150))
    write_all(img, categories, header, conditions, data, (initial_x, initial_y), squares, sqrSize, sqrBorder,
              max_x_delta, text_squares_x_spacing, text_squares_y_offset, category_y_spacing, category_text_offset, graph_expected_value)
    # img.show()
    # img.save(r'assets\data\test.png')
    return img
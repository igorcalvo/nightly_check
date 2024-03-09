from base64 import b64encode
from datetime import datetime, timedelta
from io import BytesIO
from matplotlib.colors import hsv_to_rgb
from pandas import DataFrame
from PIL.Image import Image

from source.constants import date_header
from source.core.data_in import get_matrix_data_by_header_indexes
from source.core.data_date import get_latest_date
from source.utils import get_value_from_df_by_value, to_lower_underscored


def get_date_array(data: DataFrame, squares: int) -> list[str]:
    latest_date_iso = get_latest_date(data)
    latest_date_value = datetime.fromisoformat(latest_date_iso)
    result = [
        (latest_date_value + timedelta(days=-day)).strftime("%Y-%m-%d")
        for day in range(squares)
    ]
    return result


def get_expected_value(
    habit: str, habit_list: list[list[str]], conditions: list[list[str]]
) -> bool:
    condition = get_matrix_data_by_header_indexes(conditions, habit_list, habit)
    return False if condition in ["=", "<=", "<"] else True


def get_habit_data(
    data: DataFrame,
    date_array: list,
    squares: int,
    habit: str,
    expected_value: bool = True,
) -> list[bool]:
    column_habit = to_lower_underscored(habit)
    habit_data = data[[date_header, column_habit]]
    habit_data = habit_data.reset_index()

    result = [not expected_value for item in range(squares)]
    for index, date_value in enumerate(date_array):
        try:
            data_value = get_value_from_df_by_value(date_header, date_value, habit_data)
            value = data_value[column_habit].values[0]
            if value == str(expected_value):
                result[index] = expected_value
        except:
            continue
    result.reverse()
    return result


def get_fail_indexes_list(habit_data: list, expected_value: bool = True) -> list[int]:
    result = []
    for index, item in enumerate(habit_data):
        if item != expected_value:
            result.append(index)
    return result


def image_bytes_to_base64(image: Image) -> str:
    in_memory_file = BytesIO()
    image.save(in_memory_file, format="PNG")
    in_memory_file.seek(0)
    img_bytes = in_memory_file.read()
    base64_bytes = b64encode(img_bytes)
    base64_str = base64_bytes.decode("ascii")
    return base64_str


def segment_unit_into_list(
    n: int, min_offset: float = 0, max_offset: float = 1
) -> list[float]:
    if n <= 0:
        raise Exception(f"SegmentUnitIntoList: n can't be <= 0. Got: {n}")
    elif min_offset >= max_offset or min_offset < 0 or max_offset > 1:
        raise Exception(
            f"SegmentUnitIntoList: Offsets out of range. Got min: {min_offset} and max: {max_offset}"
        )
    length: float = ((max_offset - min_offset) / n) if n > 1 else 0
    result = [min_offset + length * i for i in range(n)]
    return result


def get_rgb_color(hue: float, saturation: float, value: float) -> tuple:
    # 0 to 1
    rgb_float = hsv_to_rgb((hue, saturation, value))
    result = tuple([int(v * 255) for v in rgb_float])
    return result


def text_list_max_len_to_pixels(
    text_list: list[str], font_size_length: int = 6, font_size_spacing: int = 1
) -> int:
    return max([len(text) for text in text_list]) * (
        font_size_length + font_size_spacing
    )


def generate_y_positions(
    initial_position: tuple[int, int], length: int, spacing: int, number: int
) -> tuple:
    positions = [
        (initial_position[0], initial_position[1] + (length + spacing) * n)
        for n in range(number)
    ]
    return positions, positions[-1][1] + length + spacing - initial_position[1]


def calculate_x_position(
    initial_pos_x: int, index: int, square_size: int, square_border: int
):
    return initial_pos_x + index * (square_size + square_border)


def get_weekdays_characters(weekdays_language: str) -> str:
    match weekdays_language:
        case "en":
            return "MTWTFSS"
        case "pt":
            return "STQQSSD"
        case "jp":
            return "月火水木金土日"
        case _:
            return "月火水木金土日"

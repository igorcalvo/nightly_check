import matplotlib.colors as clr


def segment_unit_into_list(
    n: int, min_offset: float = 0, max_offset: float = 1
) -> list:
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
    rgb_float = clr.hsv_to_rgb((hue, saturation, value))
    result = tuple(int(v * 255) for v in rgb_float)
    return result


def text_list_max_len_to_pixels(
    textList: list, font_size_length: int = 6, font_size_spacing: int = 1
) -> int:
    return max([len(text) for text in textList]) * (
        font_size_length + font_size_spacing
    )


def generate_y_positions(
    initial_position: tuple, length: int, spacing: int, number: int
) -> tuple:
    positions = [
        (initial_position[0], initial_position[1] + (length + spacing) * n)
        for n in range(number)
    ]
    return positions, positions[-1][1] + length + spacing - initial_position[1]


def calculate_x_position(initial_pos_x, index, square_size, square_border):
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

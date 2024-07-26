import cv2 as cv
import matplotlib.colors as clr
import PIL.Image as im
from source.constants import (
    COLORS,
    ICON_PATHS,
    SETTINGS_DEFAULT_VALUES,
)
from source.core.theme import (
    get_default_theme,
    DEFAULT_COLORS,
    THEME,
    THEME_PROPS,
)


def get_paths() -> ICON_PATHS:
    path = ICON_PATHS()
    path.__init__()
    return path


def normalize_hue(hue: float, offset: float) -> float:
    new_hue = hue + offset
    if new_hue > 1:
        return new_hue - 1
    elif new_hue < 0:
        return new_hue + 1
    else:
        return new_hue


def is_hex_color(color: str) -> bool:
    if color in ["1234567890"] or "#" not in color:
        return False
    return True


def apply_hue_offset(hex_color: str, hue_offset: float) -> str:
    if not is_hex_color(hex_color):
        return hex_color

    hsv = clr.rgb_to_hsv(clr.to_rgb(hex_color))
    new_hue = normalize_hue(hsv[0], hue_offset)
    hsv[0] = new_hue
    return clr.rgb2hex(clr.hsv_to_rgb(hsv)) # type: ignore


def generate_icon(hue_offset: float, icon_path: str, output_path: str):
    icon = cv.imread(icon_path, cv.IMREAD_UNCHANGED)
    a = icon[:, :, 3]

    bgr = cv.imread(icon_path)
    hsv = cv.cvtColor(bgr, cv.COLOR_BGR2HSV)
    h, s, v = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]

    hsv_delta = 180 * hue_offset
    h2 = cv.add(h, hsv_delta)  # type: ignore
    hsv2 = cv.merge([h2, s, v])

    result = cv.cvtColor(hsv2, cv.COLOR_HSV2BGR)
    result = cv.merge([result[:, :, 0], result[:, :, 1], result[:, :, 2], a])
    cv.imwrite(output_path, result)


def populate_colors_dict(theme: THEME, hue_offset: float) -> dict:
    result = {}
    result[THEME_PROPS.BACKGROUND] = apply_hue_offset(theme.BACKGROUND, hue_offset)  # type: ignore
    result[THEME_PROPS.BORDER] = theme.BORDER
    result[THEME_PROPS.BUTTON] = tuple(apply_hue_offset(c, hue_offset) for c in theme.BUTTON)  # type: ignore
    result[THEME_PROPS.INPUT] = apply_hue_offset(theme.INPUT, hue_offset)  # type: ignore
    result[THEME_PROPS.SCROLL] = apply_hue_offset(theme.SCROLL, hue_offset)  # type: ignore
    result[THEME_PROPS.TEXT] = apply_hue_offset(theme.TEXT, hue_offset)  # type: ignore
    result[THEME_PROPS.TEXT_INPUT] = apply_hue_offset(theme.TEXT_INPUT, hue_offset)  # type: ignore
    return result


def get_cat_txt_color(bar_txt: str) -> str:
    if not is_hex_color(bar_txt):
        return bar_txt

    c1 = bar_txt
    c2 = DEFAULT_COLORS.cat_txt

    hsv1 = clr.rgb_to_hsv(clr.to_rgb(c1))
    hsv2 = clr.rgb_to_hsv(clr.to_rgb(c2))

    deltas = hsv2 - hsv1
    hsv3 = hsv1 + [0, deltas[1], 0]

    if hsv3[1] > 1:
        hsv3[1] = 1

    color = clr.to_hex(clr.hsv_to_rgb(hsv3)) # type: ignore
    return color


def init_ui(hue_offset: float, theme: str):
    ui_theme = get_theme(theme)
    base_color = ui_theme.BUTTON[1]
    updated_theme_color = apply_hue_offset(base_color, hue_offset)
    offset = image_hue_delta(im.open(ICON_PATHS.owl_icon_png_64), updated_theme_color)
    generate_icon(offset, ICON_PATHS.owl_icon_png_32, ICON_PATHS.colored_icon)
    generate_icon(offset, ICON_PATHS.owl_icon_png_64, ICON_PATHS.colored_msg_icon)
    theme_dict = populate_colors_dict(ui_theme, hue_offset)
    for k in theme_dict.keys():
        COLORS[k] = theme_dict[k]
    COLORS[THEME_PROPS.CATEGORY] = get_cat_txt_color(COLORS[THEME_PROPS.TEXT])
    # set_global_icon(ICON_PATHS.owl_icon_png_64)


def get_all_keys_for_themes() -> list[str]:
    # ['ACCENT1', 'ACCENT2', 'ACCENT3', 'BACKGROUND', 'BORDER', 'BUTTON', 'COLOR_LIST', 'DESCRIPTION', 'INPUT', 'PROGRESS', 'PROGRESS_DEPTH', 'SCROLL', 'SLIDER_DEPTH', 'TEXT', 'TEXT_INPUT']
    result = []
    result.sort()
    return result


def get_theme(theme: str) -> THEME:
    return get_default_theme()


def img_pixels(img: im.Image):
    pixels = img.load()
    width, height = img.size

    all_pixels = []
    for x in range(width):
        for y in range(height):
            cpixel = pixels[x, y] # type: ignore
            all_pixels.append(cpixel)

    return all_pixels


def avg_pixel(img: im.Image):
    pixels = img_pixels(img)
    count = 0
    avg = [0, 0, 0, 0]
    for px in pixels:
        if px[3] > 0:
            avg[0] = avg[0] + px[0]
            avg[1] = avg[1] + px[1]
            avg[2] = avg[2] + px[2]
            avg[3] = avg[3] + px[3]
            count += 1
    avg = (avg[0] / count, avg[1] / count, avg[2] / count, avg[3] / count)
    return avg


def image_hue_delta(img: im.Image, hex_color: str) -> float:
    avg = avg_pixel(img)
    hsv_img = clr.rgb_to_hsv(avg[:3])
    hsv_clr = clr.rgb_to_hsv(clr.to_rgb(hex_color))
    hsv_delta = hsv_clr[0] - hsv_img[0]
    return hsv_delta

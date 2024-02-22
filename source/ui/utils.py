from tkinter import Tk as tk_tk, font as tk_font
from PySimpleGUI import LOOK_AND_FEEL_TABLE
import matplotlib.colors as clr
import cv2 as cv

from source.constants import COLORS, PATHS
from source.core.theme import DEFAULT_COLORS, THEME, THEME_PROPS, get_default_theme

PATH = PATHS()
PATH.__init__()


def print_fonts():
    root = tk_tk()
    font_list = list(tk_font.families())
    font_list.sort()
    for f in font_list:
        print(f)
    root.destroy()


def normalize_hue(hue, offset):
    new_hue = hue + offset
    if new_hue > 1:
        return new_hue - 1
    elif new_hue < 0:
        return new_hue + 1
    else:
        return new_hue


def apply_hue_offset(hex_color: str, hue_offset: float) -> str:
    hsv = clr.rgb_to_hsv(clr.to_rgb(hex_color))
    new_hue = normalize_hue(hsv[0], hue_offset)
    hsv[0] = new_hue
    return clr.rgb2hex(clr.hsv_to_rgb(hsv))


def update_COLORS(hue_offset: float):
    for key in COLORS.keys():
        COLORS[key] = apply_hue_offset(COLORS[key], hue_offset)


def generate_icon(hue_offset: float):
    icon = cv.imread(PATH.standard_icon, cv.IMREAD_UNCHANGED)
    a = icon[:, :, 3]

    bgr = cv.imread(PATH.standard_icon)
    hsv = cv.cvtColor(bgr, cv.COLOR_BGR2HSV)
    h, s, v = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]

    hsv_delta = 180 * hue_offset
    h2 = cv.add(h, hsv_delta)  # type: ignore
    hsv2 = cv.merge([h2, s, v])

    result = cv.cvtColor(hsv2, cv.COLOR_HSV2BGR)
    result = cv.merge([result[:, :, 0], result[:, :, 1], result[:, :, 2], a])
    cv.imwrite(PATH.colored_icon, result)


def populate_colors_dict(theme: THEME, hue_offset) -> dict:
    result = {}
    result[THEME_PROPS.BACKGROUND] = apply_hue_offset(theme.BACKGROUND, hue_offset)  # type: ignore
    result[THEME_PROPS.BORDER] = theme.BORDER
    result[THEME_PROPS.BUTTON] = tuple(apply_hue_offset(c, hue_offset) for c in theme.BUTTON)  # type: ignore
    result[THEME_PROPS.INPUT] = apply_hue_offset(theme.INPUT, hue_offset)  # type: ignore
    result[THEME_PROPS.SCROLL] = apply_hue_offset(theme.SCROLL, hue_offset)  # type: ignore
    result[THEME_PROPS.TEXT] = apply_hue_offset(theme.TEXT, hue_offset)  # type: ignore
    result[THEME_PROPS.TEXT_INPUT] = apply_hue_offset(theme.TEXT_INPUT, hue_offset)  # type: ignore
    return result


def InitUi(hue_offset: float, theme: str):
    generate_icon(hue_offset)
    ui_theme = get_theme(theme)
    theme_dict = populate_colors_dict(ui_theme, hue_offset)
    # for k in theme_dict.keys():
    #     COLORS[k] = theme_dict[k]
    # change_look_and_feel(theme)
    update_COLORS(hue_offset)


def get_all_keys_for_themes():
    # ['ACCENT1', 'ACCENT2', 'ACCENT3', 'BACKGROUND', 'BORDER', 'BUTTON', 'COLOR_LIST', 'DESCRIPTION', 'INPUT', 'PROGRESS', 'PROGRESS_DEPTH', 'SCROLL', 'SLIDER_DEPTH', 'TEXT', 'TEXT_INPUT']
    result = []
    for theme in LOOK_AND_FEEL_TABLE.keys():
        for key in LOOK_AND_FEEL_TABLE[theme].keys():
            if key not in result:
                result.append(key)
    result.sort()
    return result


def get_theme(theme: str) -> THEME:
    return THEME(theme) if theme in LOOK_AND_FEEL_TABLE.keys() else get_default_theme()


def get_cat_txt_color(bar_txt: str):
    c1 = bar_txt
    c2 = DEFAULT_COLORS.cat_txt

    hsv1 = clr.rgb_to_hsv(clr.to_rgb(c1))
    hsv2 = clr.rgb_to_hsv(clr.to_rgb(c2))

    deltas = hsv2 - hsv1
    hsv3 = hsv1 + deltas

    for idx, v in enumerate(hsv3):
        if v > 1:
            hsv3[idx] = 1

    color = clr.to_hex(hsv3)
    return color

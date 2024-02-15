from tkinter import Tk as tk_tk, font as tk_font
import matplotlib.colors as clr
import cv2 as cv

from source.constants import COLORS, PATHS

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


def InitUi(hueOffset: float):
    generate_icon(hueOffset)
    update_COLORS(hueOffset)
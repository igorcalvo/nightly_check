import PySimpleGUI as sg
import tkinter as tk
import matplotlib.colors as clr

from core import GetMatrixDataByHeaderIndexes
from utils import PadString, Transpose

# | hue_offset | < 1
hue_offset = 0.0

# basis
bar_bkg = "#00274f"
bar_txt = "#b1d8ff"
win_bkg = "#002f5f"
cat_txt = "#dbedff"

def ApplyHueOffset(hexColor: str) -> str:
    hsv = clr.rgb_to_hsv(clr.to_rgb(hexColor))
    newHue = hsv[0] + hue_offset
    if newHue > 1:
        hsv[0] = newHue - 1
    elif newHue < 0:
        hsv[0] = newHue + 1
    else:
        hsv[0] = newHue
    return clr.rgb2hex(clr.hsv_to_rgb(hsv))

colors = {
    "bar_bkg":  ApplyHueOffset(bar_bkg),
    "bar_txt":  ApplyHueOffset(bar_txt),
    "win_bkg":  ApplyHueOffset(win_bkg),
    "cat_bkg":  ApplyHueOffset(win_bkg),
    "cat_txt":  ApplyHueOffset(cat_txt),
    "ckb_bkg":  ApplyHueOffset(bar_bkg),
    "ckb_txt":  ApplyHueOffset(bar_txt),
    "dnb_bkg":  ApplyHueOffset(bar_bkg),
    "dnb_txt":  ApplyHueOffset(bar_txt),
    "pop_bkg":  ApplyHueOffset(bar_txt),
    "pop_txt":  ApplyHueOffset(bar_bkg),
}

def PrintFonts():
    root = tk.Tk()
    fonts = list(tk.font.families())
    fonts.sort()
    for f in fonts:
        print(f)
    root.destroy()

def CreateCheckBoxes(descriptions: list, header: list) -> list:
    return [[(sg.Checkbox(text=PadString(' ' + item, 30),
                          default=False,
                          key=item,
                          size=15,
                          font=('Consolas', 11),
                          checkbox_color=colors["ckb_bkg"],
                          text_color=colors["ckb_txt"],
                          background_color=colors["win_bkg"],
                          pad=((15, 0), (2, 2)),
                          tooltip=GetMatrixDataByHeaderIndexes(descriptions, header, item)) if item != '' else sg.Text(PadString('', 37), background_color=colors["win_bkg"])) for item in splitList] for splitList in Transpose(header)]
#                                                                                               Fixes floating checkbox on a column
def CreateLayout(categories: list, header: list, descriptions: list, buttonText: str) -> list:
    #                        Spacing between categories
    categoryTitles = [sg.Text(PadString(c.upper(), 27),
                              text_color=colors["cat_txt"],
                              background_color=colors["cat_bkg"],
                              pad=((15, 0), (10, 10)),
                              font=("Helvetica", 11, "bold")) for c in categories]
    checkboxes = CreateCheckBoxes(descriptions, header)
    #                                   Button's distance from the left
    return [categoryTitles,
            checkboxes,
            [sg.Text(PadString("", 165), background_color=colors["win_bkg"]),
             sg.Button(buttonText, font=("Verdana", 9, "bold"), size=7,
                       button_color=(colors["dnb_bkg"], colors["dnb_txt"]))]]

def CreateWindow(categories: list, header: list, descriptions: list, buttonText: str):
    layout = CreateLayout(categories, header, descriptions, buttonText)
    return sg.Window(title="Argus",
                     icon="assets\icon64.ico",
                     layout=layout,
                     use_custom_titlebar=True,
                     titlebar_background_color=colors["bar_bkg"],
                     titlebar_text_color=colors["bar_txt"],
                     titlebar_icon="assets\icon16.png",
                     background_color=colors["win_bkg"],
                     size=(153 * len(categories), 40 * max(len(h) for h in header) + 70))

def PopUp(message: str):
    sg.PopupNoButtons(message,
             keep_on_top=True,
             auto_close=True,
             auto_close_duration=3,
             background_color=colors["pop_bkg"],
             text_color=colors["pop_txt"],
             no_titlebar=True,
             font=("Arial", 11, "bold"),
             line_width=500)
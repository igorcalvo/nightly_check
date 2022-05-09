import PySimpleGUI as sg
import tkinter as tk
import matplotlib.colors as clr

from core import GetMatrixDataByHeaderIndexes, ReadSettings
from utils import PadString, Transpose

# | hue_offset | < 1
hue_base = 0.59

# basis
bar_bkg = "#00274f"
bar_txt = "#b1d8ff"
win_bkg = "#002f5f"
cat_txt = "#dbedff"

def ApplyHueOffset(hexColor: str, hue_offset: float) -> str:
    hsv = clr.rgb_to_hsv(clr.to_rgb(hexColor))
    newHue = hsv[0] + hue_offset
    if newHue > 1:
        hsv[0] = newHue - 1
    elif newHue < 0:
        hsv[0] = newHue + 1
    else:
        hsv[0] = newHue
    return clr.rgb2hex(clr.hsv_to_rgb(hsv))

def UpdateColors(hue_offset: float):
    for key in colors.keys():
        colors[key] = ApplyHueOffset(colors[key], hue_offset)

colors = {
    "bar_bkg":  bar_bkg,
    "bar_txt":  bar_txt,
    "win_bkg":  win_bkg,
    "cat_bkg":  win_bkg,
    "cat_txt":  cat_txt,
    "ckb_bkg":  bar_bkg,
    "ckb_txt":  bar_txt,
    "dnb_bkg":  bar_bkg,
    "dnb_txt":  bar_txt,
    "pop_bkg":  bar_txt,
    "pop_txt":  bar_bkg,
    "sld_txt":  cat_txt,
    "sld_bkg":  win_bkg,
    "sld_sld":  bar_txt,
}

def PrintFonts():
    root = tk.Tk()
    fonts = list(tk.font.families())
    fonts.sort()
    for f in fonts:
        print(f)
    root.destroy()

def InitUi(settingsFileName: str):
    settings = ReadSettings(settingsFileName)
    hueOffset = float(settings[list(settings.keys())[0]])
    UpdateColors(hueOffset)

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
def CreateLayout(categories: list, header: list, descriptions: list, doneButtonText: str, styleButtonText: str) -> list:
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
            [sg.Button(styleButtonText,
                       font=("Verdana", 9, "bold"),
                       size=7,
                       button_color=(colors["dnb_bkg"], colors["dnb_txt"]),
                       pad=((15, 0), (10, 10))),
             sg.Text(PadString("", 150), background_color=colors["win_bkg"]),
             sg.Button(doneButtonText,
                       font=("Verdana", 9, "bold"),
                       size=7,
                       button_color=(colors["dnb_bkg"], colors["dnb_txt"]))]]

def CreateWindow(categories: list, header: list, descriptions: list, doneButtonText: str, styleButtonText: str):
    layout = CreateLayout(categories, header, descriptions, doneButtonText, styleButtonText)
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

def Style(styleButtonText: str, sliderTextKey: str, setButtonTextKey: str):
    return sg.Window(styleButtonText, [
        [sg.Text(PadString("Slide to change hue", 0),
                 background_color=colors["sld_bkg"],
                 text_color=colors["sld_txt"])],
        [sg.Slider(range=(-1, 1),
                   default_value=0,
                   resolution=0.01,
                   orientation='h',
                   enable_events=True,
                   key=sliderTextKey,
                   text_color=colors["sld_txt"],
                   background_color=colors["sld_bkg"],
                   trough_color=colors["sld_sld"])],
        [sg.Button(setButtonTextKey,
                   font=("Verdana", 9, "bold"),
                   size=7,
                   pad=((65, 0), (15, 15)),
                   key=setButtonTextKey,
                   button_color=(colors["dnb_bkg"], colors["dnb_txt"]))]
    ],
     return_keyboard_events=True,
     use_custom_titlebar=True,
     titlebar_background_color=colors["bar_bkg"],
     titlebar_text_color=colors["bar_txt"],
     titlebar_icon="assets\style16.png",
     background_color=colors["win_bkg"],
     ).Finalize()
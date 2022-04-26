import PySimpleGUI as sg
import tkinter as tk

from core import GetMatrixDataByHeaderIndexes
from utils import PadString, Transpose

bar_bkg = "#00274f"
bar_txt = "#b1d8ff"
win_bkg = "#002f5f"
cat_bkg = win_bkg
cat_txt = "#dbedff"
ckb_bkg = bar_bkg
ckb_txt = bar_txt
dnb_bkg = bar_bkg
dnb_txt = bar_txt

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
                          checkbox_color=ckb_bkg,
                          text_color=ckb_txt,
                          background_color=win_bkg,
                          pad=((15, 0), (2, 2)),
                          tooltip=GetMatrixDataByHeaderIndexes(descriptions, header, item)) if item != '' else sg.Text(PadString('', 37), background_color=win_bkg)) for item in splitList] for splitList in Transpose(header)]
#                                                                                               Fixes floating checkbox on a column
def CreateLayout(categories: list, header: list, descriptions: list, buttonText: str) -> list:
    #                        Spacing between categories
    categoryTitles = [sg.Text(PadString(c.upper(), 27),
                              text_color=cat_txt,
                              background_color=cat_bkg,
                              pad=((15, 0), (10, 10)),
                              font=("Helvetica", 11, "bold")) for c in categories]
    checkboxes = CreateCheckBoxes(descriptions, header)
    #                                   Button distance from the left
    return [categoryTitles, checkboxes, [sg.Text(PadString("", 165), background_color=win_bkg), sg.Button(buttonText,
                                                                                                          font=("Verdana", 9, "bold"),
                                                                                                          size=7,
                                                                                                          button_color=(dnb_bkg, dnb_txt))]]

def CreateWindow(categories: list, header: list, descriptions: list, buttonText: str):
    layout = CreateLayout(categories, header, descriptions, buttonText)
    return sg.Window(title="Argus",
                     icon="assets\icon64.ico",
                     layout=layout,
                     use_custom_titlebar=True,
                     titlebar_background_color=bar_bkg,
                     titlebar_text_color=bar_txt,
                     titlebar_icon="assets\icon16.png",
                     background_color=win_bkg,
                     size=(153 * len(categories), 40 * max(len(h) for h in header) + 70))

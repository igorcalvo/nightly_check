import PySimpleGUI as sg
import tkinter as tk
import matplotlib.colors as clr
import cv2 as cv
# w, h = sg.Window.get_screen_size()
from core import GetMatrixDataByHeaderIndexes
from utils import PadString, Transpose, FlattenList

categoryPixelLength = 10
checkboxPixelLength = 8
coloredIconPath = "assets\icons\iconColored.png"
# | hue_offset | < 1
hue_base = 0.59

# basis
bar_bkg = "#00274f"
bar_txt = "#b1d8ff"
win_bkg = "#002f5f"
cat_txt = "#dbedff"
sld_bkg = "#004080"

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
    "stl_bkg":  bar_bkg,
    "stl_txt":  bar_txt,
    "dtb_bkg":  bar_bkg,
    "dtb_txt":  bar_txt,
    "pop_bkg":  bar_txt,
    "pop_txt":  bar_bkg,
    "sld_txt":  cat_txt,
    "sld_bkg":  sld_bkg,
    "sld_sld":  bar_txt,
    "dat_txt":  cat_txt,
    "dat_bkg":  sld_bkg,
    "exp_txt":  bar_txt,
    "exp_bkg":  bar_bkg,
}

fonts = {
    "cat": ("Cascadia Mono", 13, "bold"),
    # "cat": ("Helvetica", 11, "bold"),
    "ckb": ('Consolas', 11),
    "btn": ("Verdana", 9, "bold"),
    "pop": ("Arial", 11, "bold")
}

def PrintFonts():
    root = tk.Tk()
    fontList = list(tk.font.families())
    fontList.sort()
    for f in fontList:
        print(f)
    root.destroy()

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

def GenerateIcon(hue_offset: float):
    icon = cv.imread("assets\icons\icon16.png", cv.IMREAD_UNCHANGED)
    a = icon[:, :, 3]

    bgr = cv.imread("assets\icons\icon16.png")
    hsv = cv.cvtColor(bgr, cv.COLOR_BGR2HSV)
    h = hsv[:, :, 0]
    s = hsv[:, :, 1]
    v = hsv[:, :, 2]

    hsvDelta = 180 * (hue_offset)
    h2 = cv.add(h, hsvDelta)
    hsv2 = cv.merge([h2, s, v])

    result = cv.cvtColor(hsv2, cv.COLOR_HSV2BGR)
    result = cv.merge([result[:,:,0], result[:,:,1], result[:,:,2], a])
    cv.imwrite(coloredIconPath, result)

def InitUi(hueOffset: float):
    GenerateIcon(hueOffset)
    UpdateColors(hueOffset)

def CreateCheckBoxes(descriptions: list, header: list, size: int) -> list:
    #                  magic number to align checkboxes when the previous column has fewer rows
    columnCorrection = 2 * size + 7
    return [[(sg.Checkbox(text=' ' + item,
                          default=False,
                          key=item,
                          size=size,
                          font=fonts["ckb"],
                          checkbox_color=colors["ckb_bkg"],
                          text_color=colors["ckb_txt"],
                          background_color=colors["win_bkg"],
                          pad=((15, 0), (2, 2)),
                          tooltip=GetMatrixDataByHeaderIndexes(descriptions, header, item)) if item != '' else sg.Text(PadString('', columnCorrection), background_color=colors["win_bkg"])) for item in splitList] for splitList in Transpose(header)]
#                                                                                                                      Fixes floating checkbox on a column
def CreateLayout(categories: list, header: list, descriptions: list, doneButtonText: str, styleButtonText: str, dataButtonText: str, longestText: int, windowsXSize: int, csvNotEmpty: bool) -> list:
    # 10 -> size 15 -> 37
    # 16 -> size 20 -> 47
    size = int(18 * longestText / 16)
    #                        Spacing between categories
# TODO                        1px error for 4 cat with pad = 14 - used to be 15
    categoryTitles = [sg.Text(PadString(c.upper(), int(longestText * checkboxPixelLength / categoryPixelLength) + 4),
                              text_color=colors["cat_txt"],
                              background_color=colors["cat_bkg"],
                              pad=((14, 10), (10, 10)),
                              font=fonts["cat"]) for c in categories]
    checkboxes = CreateCheckBoxes(descriptions, header, size)
    buttonSpacing = int(0.423 * windowsXSize / checkboxPixelLength)
#   TODO               may be missing linear component
    return [categoryTitles,
            checkboxes,
            [sg.Button(styleButtonText,
                       font=fonts["btn"],
                       size=7,
                       button_color=(colors["stl_bkg"], colors["stl_txt"]),
                       pad=((15, 0), (10, 10))),
    #                Button's distance from the left
             sg.Text(PadString("", buttonSpacing), background_color=colors["win_bkg"], font=fonts["ckb"]),
             sg.Button(dataButtonText,
                       font=fonts["btn"],
                       size=7,
                       disabled=not csvNotEmpty,
                       button_color=(colors["dtb_bkg"], colors["dtb_txt"])),
    #                Button's distance from the left
             sg.Text(PadString("", buttonSpacing), background_color=colors["win_bkg"], font=fonts["ckb"]),
             sg.Button(doneButtonText,
                       font=fonts["btn"],
                       size=7,
                       button_color=(colors["dnb_bkg"], colors["dnb_txt"]))]]

def MainWindow(categories: list, header: list, descriptions: list, doneButtonText: str, styleButtonText: str, dataButtonText: str, csvNotEmpty: bool):
    longestText = max([len(x) for x in FlattenList(header)])
    windowSize = (int(1.4 * checkboxPixelLength * longestText * len(categories) + 64), 40 * max([len(h) for h in header]) + 70)
#   TODO spacing + borders? missing
    layout = CreateLayout(categories, header, descriptions, doneButtonText, styleButtonText, dataButtonText, longestText, windowSize[0], csvNotEmpty)
    return sg.Window(title="Argus",
                     layout=layout,
                     use_custom_titlebar=True,
                     titlebar_background_color=colors["bar_bkg"],
                     titlebar_text_color=colors["bar_txt"],
                     titlebar_icon=coloredIconPath,
                     background_color=colors["win_bkg"],
                     size=windowSize)

def PopUp(message: str):
    sg.PopupNoButtons(message,
             keep_on_top=True,
             auto_close=True,
             auto_close_duration=3,
             background_color=colors["pop_bkg"],
             text_color=colors["pop_txt"],
             no_titlebar=True,
             font=fonts["pop"],
             line_width=len(message))

def StyleWindow(styleButtonText: str, sliderTextKey: str, previewWindowText: str, setButtonTextKey: str):
    return sg.Window(styleButtonText, [
        [sg.Text(PadString("Slide to change hue", 0),
                 background_color=colors["sld_bkg"],
                 text_color=colors["sld_txt"])],
        [sg.Slider(range=(-0.5, 0.5),
                   default_value=0,
                   resolution=0.001,
                   orientation='h',
                   enable_events=True,
                   key=sliderTextKey,
                   text_color=colors["sld_txt"],
                   background_color=colors["sld_bkg"],
                   trough_color=colors["sld_sld"],
                   size=(50, 23))],
        [[sg.Button(previewWindowText,
                   font=fonts["btn"],
                   size=7,
                   pad=((5, 0), (15, 15)),
                   key=previewWindowText,
                   button_color=(colors["dnb_bkg"], colors["dnb_txt"])),
          sg.Button(setButtonTextKey,
                    font=fonts["btn"],
                    size=7,
                    pad=((322, 0), (15, 15)),
                    key=setButtonTextKey,
                    button_color=(colors["dnb_bkg"], colors["dnb_txt"]))
          ]]
    ],
     return_keyboard_events=True,
     use_custom_titlebar=True,
     titlebar_background_color=colors["bar_bkg"],
     titlebar_text_color=colors["bar_txt"],
     titlebar_icon="assets\icons\style16.png",
     background_color=colors["sld_bkg"],
     relative_location=(-100, 0)
     ).Finalize()

def PreviewWindow(previewWindowText: str, previewCloseKey: str, hueOffset: float):
    return sg.Window(previewWindowText, [
        [sg.Text(PadString("Preview".upper(), 27),
                 text_color=ApplyHueOffset(colors["cat_txt"], hueOffset),
                 background_color=ApplyHueOffset(colors["cat_bkg"], hueOffset),
                 pad=((15, 0), (10, 10)),
                 font=fonts["cat"])],
        [sg.Checkbox(text=PadString(' ' + "Sample Text", 30),
                     default=False,
                     size=15,
                     font=fonts["ckb"],
                     checkbox_color=ApplyHueOffset(colors["ckb_bkg"], hueOffset),
                     text_color=ApplyHueOffset(colors["ckb_txt"], hueOffset),
                     background_color=ApplyHueOffset(colors["win_bkg"], hueOffset),
                     pad=((15, 0), (2, 2)),
                     tooltip="Sample tooltip")],
        [sg.Button("Close",
                   font=fonts["btn"],
                   size=7,
                   key=previewCloseKey,
                   pad=((65, 0), (15, 15)),
                   button_color=(ApplyHueOffset(colors["dnb_bkg"], hueOffset), ApplyHueOffset(colors["dnb_txt"], hueOffset)))]
    ],
     return_keyboard_events=True,
     use_custom_titlebar=True,
     titlebar_background_color=ApplyHueOffset(colors["bar_bkg"], hueOffset),
     titlebar_text_color=ApplyHueOffset(colors["bar_txt"], hueOffset),
     titlebar_icon="assets\icons\preview16.png",
     background_color=ApplyHueOffset(colors["win_bkg"], hueOffset),
     relative_location=(240, 0)
     ).Finalize()

def DataWindow(dataButtonText: str, exportImageFileNameKey: str, exportButtonText: str, scrollableImage: bool, imgBase64: str):
    layout = [
        [sg.Image(data=imgBase64)],
        [
            sg.InputText(key=exportImageFileNameKey, default_text='filename', enable_events=True, size=(20, 5)),
            sg.InputText(key=exportButtonText, do_not_clear=False, enable_events=True, visible=False),
            sg.FileSaveAs(
                button_text="Export",
                font=fonts["btn"],
                initial_folder='%HomeDrive%',
                file_types=(('PNG', '.png'), ('JPG', '.jpg')),
                pad=((5, 0), (5, 5)),
                button_color=(colors["exp_bkg"], colors["exp_txt"])
            )
        ]
    ]
    return sg.Window(dataButtonText, [
        # [sg.Column(layout, size=(200, 200), scrollable=True, key='Column')]
        [sg.Column(layout, scrollable=scrollableImage, key='Column')]
    ],
     return_keyboard_events=True,
     use_custom_titlebar=True,
     titlebar_background_color=colors["bar_bkg"],
     titlebar_text_color=colors["bar_txt"],
     titlebar_icon="assets\icons\data16.png",
     background_color=colors["dat_bkg"],
     relative_location=(0, 0)
     ).Finalize()

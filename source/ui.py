import PySimpleGUI as sg
import tkinter as tk
import matplotlib.colors as clr
import cv2 as cv
import os
# w, h = sg.Window.get_screen_size()
from .core import get_matrix_data_by_header_indexes
from .utils import pad_string, transpose, flatten_list

PARENT_DIR = os.path.abspath(os.path.join(os.getcwd(), os.pardir)).replace("\\", "/") + "/NightlyCheck"
CATEGORY_PIXEL_LENGTH = 10
CHECKBOX_PIXEL_LENGTH = 8
COLORED_ICON_PATH = f"{PARENT_DIR}/assets/icons/iconColored.png"
# | hue_offset | < 1
HUE_BASE = 0.59

# basis
bar_bkg = "#00274f"
bar_txt = "#b1d8ff"
win_bkg = "#002f5f"
cat_txt = "#dbedff"
sld_bkg = "#004080"

COLORS = {
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

FONTS = {
    "cat": ("Cascadia Mono", 13, "bold"),
    # "cat": ("Helvetica", 11, "bold"),
    "ckb": ('Consolas', 11),
    "btn": ("Verdana", 9, "bold"),
    "pop": ("Arial", 11, "bold")
}

def print_FONTS():
    root = tk.Tk()
    font_list = list(tk.font.families())
    font_list.sort()
    for f in font_list:
        print(f)
    root.destroy()

def apply_hue_offset(hex_color: str, hue_offset: float) -> str:
    hsv = clr.rgb_to_hsv(clr.to_rgb(hex_color))
    new_hue = hsv[0] + hue_offset
    if new_hue > 1:
        hsv[0] = new_hue - 1
    elif new_hue < 0:
        hsv[0] = new_hue + 1
    else:
        hsv[0] = new_hue
    return clr.rgb2hex(clr.hsv_to_rgb(hsv))

def update_COLORS(hue_offset: float):
    for key in COLORS.keys():
        COLORS[key] = apply_hue_offset(COLORS[key], hue_offset)

def generate_icon(hue_offset: float):
    icon = cv.imread(f"{PARENT_DIR}/assets/icons/icon16.png", cv.IMREAD_UNCHANGED)
    a = icon[:, :, 3]

    bgr = cv.imread(f"{PARENT_DIR}/assets/icons/icon16.png")
    hsv = cv.cvtColor(bgr, cv.COLOR_BGR2HSV)
    h = hsv[:, :, 0]
    s = hsv[:, :, 1]
    v = hsv[:, :, 2]

    hsv_delta = 180 * (hue_offset)
    h2 = cv.add(h, hsv_delta)
    hsv2 = cv.merge([h2, s, v])

    result = cv.cvtColor(hsv2, cv.COLOR_HSV2BGR)
    result = cv.merge([result[:, :, 0], result[:, :, 1], result[:, :, 2], a])
    cv.imwrite(COLORED_ICON_PATH, result)

def InitUi(hueOffset: float):
    generate_icon(hueOffset)
    update_COLORS(hueOffset)

def CreateCheckBoxes(descriptions: list, header: list, size: int) -> list:
    #                  magic number to align checkboxes when the previous column has fewer rows
    column_correction = 2 * size + 7
    return [[(sg.Checkbox(text=' ' + item,
                          default=False,
                          key=item,
                          size=size,
                          font=FONTS["ckb"],
                          checkbox_color=COLORS["ckb_bkg"],
                          text_color=COLORS["ckb_txt"],
                          background_color=COLORS["win_bkg"],
                          pad=((15, 0), (2, 2)),
                          tooltip=get_matrix_data_by_header_indexes(descriptions, header, item)) if item != '' else sg.Text(pad_string('', column_correction), background_color=COLORS["win_bkg"])) for item in splitList] for splitList in transpose(header)]
#                                                                                                                      Fixes floating checkbox on a column
def CreateMainLayout(categories: list, header: list, descriptions: list, done_button_text: str, style_button_text: str, data_button_text: str, edit_button_text: str, longest_text: int, windows_x_size: int, csv_not_empty: bool, is_neglected: bool) -> list:
    size = int(longest_text * 8 / CHECKBOX_PIXEL_LENGTH + 1)
    #                        Spacing between categories
    category_titles = [sg.Text(pad_string(c.upper(), int(longest_text * CHECKBOX_PIXEL_LENGTH / CATEGORY_PIXEL_LENGTH) + 3),
                               text_color=COLORS["cat_txt"],
                               background_color=COLORS["cat_bkg"],
                               pad=((15, 10), (10, 10)),
                               font=FONTS["cat"]) for c in categories]
    checkboxes = CreateCheckBoxes(descriptions, header, size)

    buttons_layout = [
        sg.Button(style_button_text,
                  font=FONTS["btn"],
                  size=7,
                  button_color=(COLORS["stl_bkg"], COLORS["stl_txt"]),
                  pad=(25, 0)),
        sg.Push(background_color=COLORS["win_bkg"]),
        sg.Button(data_button_text,
                  font=FONTS["btn"],
                  size=7,
                  disabled=not csv_not_empty,
                  button_color=(COLORS["dtb_bkg"], COLORS["dtb_txt"]),
                  ),
        sg.Push(background_color=COLORS["win_bkg"]),
        sg.Button(edit_button_text,
                  font=FONTS["btn"],
                  size=7,
                  disabled=not csv_not_empty,
                  button_color=(COLORS["dtb_bkg"], COLORS["dtb_txt"]),
                  ),
    ]

    done_button_layout = [
        sg.Push(background_color=COLORS["win_bkg"]),
        sg.Button(done_button_text,
                  font=FONTS["btn"],
                  size=7,
                  button_color=(COLORS["dnb_bkg"], COLORS["dnb_txt"]),
                  pad=(25, 0))
    ]
    buttons_layout.extend(done_button_layout)

    if not is_neglected:
        window_layout = [category_titles, checkboxes, buttons_layout]
    else:
        window_layout = [category_titles, checkboxes, done_button_layout]

    return window_layout

def MainWindow(categories: list, header: list, descriptions: list, done_button_text: str, style_button_text: str, data_button_text: str, edit_button_text: str, csv_not_empty: bool, is_neglected: bool):
    longest_text = max([len(x) for x in flatten_list(header)])
    window_size = (int((0.93 * longest_text * CHECKBOX_PIXEL_LENGTH + 60) * len(categories) - 15), 40 * max([len(h) for h in header]) + 75)
    layout = CreateMainLayout(categories, header, descriptions, done_button_text, style_button_text, data_button_text, edit_button_text, longest_text, window_size[0], csv_not_empty, is_neglected)
    return sg.Window(title="Argus",
                     layout=layout,
                     use_custom_titlebar=True,
                     titlebar_background_color=COLORS["bar_bkg"],
                     titlebar_text_color=COLORS["bar_txt"],
                     titlebar_icon=COLORED_ICON_PATH,
                     background_color=COLORS["win_bkg"],
                     size=window_size,
                     element_justification='c')

def PopUp(message: str, message_duration: int):
    sg.PopupNoButtons(message,
                      keep_on_top=True,
                      auto_close=True,
                      auto_close_duration=message_duration,
                      background_color=COLORS["pop_bkg"],
                      text_color=COLORS["pop_txt"],
                      no_titlebar=True,
                      font=FONTS["pop"],
                      line_width=len(message))

def StyleWindow(style_button_text: str, slider_text_key: str, preview_window_text: str, set_button_tex_key: str):
    return sg.Window(style_button_text, [
        [sg.Text(pad_string("Slide to change hue", 0),
                 background_color=COLORS["sld_bkg"],
                 text_color=COLORS["sld_txt"])],
        [sg.Slider(range=(-0.5, 0.5),
                   default_value=0,
                   resolution=0.001,
                   orientation='h',
                   enable_events=True,
                   key=slider_text_key,
                   text_color=COLORS["sld_txt"],
                   background_color=COLORS["sld_bkg"],
                   trough_color=COLORS["sld_sld"],
                   size=(50, 23))],
        [[sg.Button(preview_window_text,
                    font=FONTS["btn"],
                    size=7,
                    pad=((5, 0), (15, 15)),
                    key=preview_window_text,
                    button_color=(COLORS["dnb_bkg"], COLORS["dnb_txt"])),
          sg.Button(set_button_tex_key,
                    font=FONTS["btn"],
                    size=7,
                    pad=((322, 0), (15, 15)),
                    key=set_button_tex_key,
                    button_color=(COLORS["dnb_bkg"], COLORS["dnb_txt"]))
          ]]
    ],
                     return_keyboard_events=True,
                     use_custom_titlebar=True,
                     titlebar_background_color=COLORS["bar_bkg"],
                     titlebar_text_color=COLORS["bar_txt"],
                     titlebar_icon="assets\icons\style16.png",
                     background_color=COLORS["sld_bkg"],
                     relative_location=(-100, 0)
                     ).Finalize()

def PreviewWindow(preview_window_text: str, preview_close_key: str, hue_offset: float):
    return sg.Window(preview_window_text, [
        [sg.Text(pad_string("Preview".upper(), 27),
                 text_color=apply_hue_offset(COLORS["cat_txt"], hue_offset),
                 background_color=apply_hue_offset(COLORS["cat_bkg"], hue_offset),
                 pad=((15, 0), (10, 10)),
                 font=FONTS["cat"])],
        [sg.Checkbox(text=pad_string(' ' + "Sample Text", 30),
                     default=False,
                     size=15,
                     font=FONTS["ckb"],
                     checkbox_color=apply_hue_offset(COLORS["ckb_bkg"], hue_offset),
                     text_color=apply_hue_offset(COLORS["ckb_txt"], hue_offset),
                     background_color=apply_hue_offset(COLORS["win_bkg"], hue_offset),
                     pad=((15, 0), (2, 2)),
                     tooltip="Sample tooltip")],
        [sg.Button("Close",
                   font=FONTS["btn"],
                   size=7,
                   key=preview_close_key,
                   pad=((65, 0), (15, 15)),
                   button_color=(apply_hue_offset(COLORS["dnb_bkg"], hue_offset), apply_hue_offset(COLORS["dnb_txt"], hue_offset)))]
    ],
                     return_keyboard_events=True,
                     use_custom_titlebar=True,
                     titlebar_background_color=apply_hue_offset(COLORS["bar_bkg"], hue_offset),
                     titlebar_text_color=apply_hue_offset(COLORS["bar_txt"], hue_offset),
                     titlebar_icon="assets\icons\preview16.png",
                     background_color=apply_hue_offset(COLORS["win_bkg"], hue_offset),
                     relative_location=(240, 0)
                     ).Finalize()

def DataWindow(data_button_text: str, export_button_text: str, scrollable_image: bool, img_base64: str):
    layout = [
        [sg.Image(data=img_base64)],
        [
            sg.InputText(key=export_button_text, do_not_clear=False, enable_events=True, visible=False),
            sg.Push(),
            sg.FileSaveAs(
                button_text="Export",
                font=FONTS["btn"],
                initial_folder='%HomeDrive%',
                file_types=(('PNG', '.png'), ('JPG', '.jpg')),
                pad=((0, 5), (5, 5)),
                button_color=(COLORS["exp_bkg"], COLORS["exp_txt"])
            )
        ]
    ]
    return sg.Window(data_button_text, [
        # [sg.Column(layout, size=(200, 200), scrollable=True, key='Column')]
        [sg.Column(layout, scrollable=scrollable_image, key='Column')]
    ],
                     return_keyboard_events=True,
                     use_custom_titlebar=True,
                     titlebar_background_color=COLORS["bar_bkg"],
                     titlebar_text_color=COLORS["bar_txt"],
                     titlebar_icon="assets\icons\data16.png",
                     background_color=COLORS["dat_bkg"],
                     relative_location=(0, -15)
                     ).Finalize()

def NeglectedPopUp(accept_text: str, reject_text: str):
    layout = [
        [sg.Text("It looks like you haven't input yesterday's data. Would you like to add it now?",
                 text_color=COLORS["pop_txt"],
                 background_color=COLORS["pop_bkg"],
                 pad=((15, 15), (10, 10)),
                 font=FONTS["pop"])],
        [
            sg.Button(accept_text,
                      font=FONTS["btn"],
                      size=7,
                      key=accept_text,
                      pad=((15, 0), (15, 15)),
                      button_color=(COLORS["dnb_txt"], COLORS["dnb_bkg"])),
            sg.Text(pad_string("", 29),
                    text_color=COLORS["pop_txt"],
                    background_color=COLORS["pop_bkg"],
                    font=FONTS["pop"]),
            sg.Button(reject_text,
                      font=FONTS["btn"],
                      size=7,
                      key=reject_text,
                      pad=((0, 15), (15, 15)),
                      button_color=(COLORS["dnb_txt"], COLORS["dnb_bkg"]))
        ]
    ]
    return sg.Window("Yesterday",
                     layout,
                     return_keyboard_events=True,
                     use_custom_titlebar=True,
                     titlebar_background_color=COLORS["bar_bkg"],
                     titlebar_text_color=COLORS["bar_txt"],
                     titlebar_icon="assets\icons\yesterday16.png",
                     background_color=COLORS["pop_bkg"],
                     relative_location=(0, 0),
                     element_justification='c'
                     ).Finalize()

def DatePickerWindow(select_date_key: str, select_date_button_text: str):
    layout = [
        [sg.Text(
            text='Select a date:',
            text_color=COLORS["pop_txt"],
            background_color=COLORS["pop_bkg"],
            font=FONTS["pop"]
        )],
        [
            sg.InputText(key=select_date_key,
                         background_color=COLORS["pop_bkg"],
                         size=(20, 10)),
            sg.CalendarButton("Pick a date",
                              close_when_date_chosen=True,
                              target=select_date_key,
                              format='%Y-%m-%d',
                              size=(15, 1),
                              button_color=(COLORS["dnb_txt"], COLORS["dnb_bkg"])),
            sg.Button(select_date_button_text,
                      font=FONTS["btn"],
                      size=7,
                      key=select_date_button_text,
                      button_color=(COLORS["dnb_txt"], COLORS["dnb_bkg"]))
        ]
    ]
    return sg.Window("Pick a Date",
                     layout,
                     return_keyboard_events=True,
                     use_custom_titlebar=True,
                     titlebar_background_color=COLORS["bar_bkg"],
                     titlebar_text_color=COLORS["bar_txt"],
                     titlebar_icon="assets\icons\yesterday16.png",
                     background_color=COLORS["pop_bkg"],
                     relative_location=(0, 0),
                     element_justification='c'
                     ).Finalize()

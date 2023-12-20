import PySimpleGUI as sg
import tkinter as tk
import matplotlib.colors as clr
import cv2 as cv
from io import BytesIO
from PIL import Image
from base64 import b64decode
# w, h = sg.Window.get_screen_size()
from .core import get_matrix_data_by_header_indexes
from .utils import pad_string, transpose, safe_value_from_dict, safe_bool_from_array, safe_value_from_array, is_windows
from .constants import COLORS, FONTS, CHECKBOX_PIXEL_LENGTH, MESSAGES, PATHS
PATH = PATHS()
PATH.__init__()

def print_fonts():
    root = tk.Tk()
    font_list = list(tk.font.families())
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
    h = hsv[:, :, 0]
    s = hsv[:, :, 1]
    v = hsv[:, :, 2]

    hsv_delta = 180 * hue_offset
    h2 = cv.add(h, hsv_delta)
    hsv2 = cv.merge([h2, s, v])

    result = cv.cvtColor(hsv2, cv.COLOR_HSV2BGR)
    result = cv.merge([result[:, :, 0], result[:, :, 1], result[:, :, 2], a])
    cv.imwrite(PATH.colored_icon, result)

def InitUi(hueOffset: float):
    generate_icon(hueOffset)
    update_COLORS(hueOffset)

def CreateCheckBoxes(descriptions: list, header: list, sizes: list, default_values: list = []) -> list:
    #                  magic number to align checkboxes when the previous column has fewer rows
    return [[(sg.Checkbox(text=' ' + item,
                          default=False if len(default_values) == 0 else get_matrix_data_by_header_indexes(default_values, header, item),
                          key=item,
                          size=sizes[idx],
                          font=FONTS["ckb"],
                          checkbox_color=COLORS["ckb_bkg"],
                          text_color=COLORS["ckb_txt"],
                          background_color=COLORS["win_bkg"],
                          pad=((15, 0), (1, 1)),
                          tooltip=get_matrix_data_by_header_indexes(descriptions, header, item)) if item != '' else sg.Text(pad_string('', sizes[idx] + 2) if not is_windows() else 2 * sizes[idx] + 7, background_color=COLORS["win_bkg"], font=FONTS["cat"])) for idx, item in enumerate(splitList)] for splitList in transpose(header)]
#                                                                                                                      Fixes floating checkbox on a column
def CreateMainLayout(categories: list, header: list, descriptions: list, done_button_text: str, style_button_text: str, data_button_text: str, edit_button_text: str, windows_x_size: int, csv_not_empty: bool, is_sub_window: bool, default_values: list) -> list:
    longest_texts = [max([len(text) for text in col]) for col in header]
    sizes = [lt + 1 for lt in longest_texts]
    #                        Spacing between categories
    category_titles = [sg.Text(pad_string(cat.upper(), longest_texts[idx]),
    # category_titles = [sg.Text(cat.upper(), int(longest_texts[idx] * CHECKBOX_PIXEL_LENGTH / CATEGORY_PIXEL_LENGTH) + 3,
                               text_color=COLORS["cat_txt"],
                               background_color=COLORS["cat_bkg"],
                               pad=((20, 20), (10, 0)),
                               font=FONTS["cat"]) for idx, cat in enumerate(categories)]
    checkboxes = CreateCheckBoxes(descriptions, header, sizes, default_values)

    buttons_layout = [
        sg.Button(style_button_text,
                  font=FONTS["btn"],
                  size=7,
                  button_color=(COLORS["dnb_bkg"], COLORS["dnb_txt"]),
                  pad=(25, 0)),
        sg.Push(background_color=COLORS["win_bkg"]),
        sg.Button(data_button_text,
                  font=FONTS["btn"],
                  size=7,
                  disabled=not csv_not_empty,
                  button_color=(COLORS["dnb_bkg"], COLORS["dnb_txt"]),
                  ),
        sg.Push(background_color=COLORS["win_bkg"]),
        sg.Button(edit_button_text,
                  font=FONTS["btn"],
                  size=7,
                  disabled=not csv_not_empty,
                  button_color=(COLORS["dnb_bkg"], COLORS["dnb_txt"]),
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

    if not is_sub_window:
        window_layout = [category_titles, checkboxes, buttons_layout]
    else:
        window_layout = [category_titles, checkboxes, done_button_layout]

    return window_layout

def MainWindow(categories: list, header: list, descriptions: list, done_button_text: str, style_button_text: str, data_button_text: str, edit_button_text: str, csv_not_empty: bool, is_sub_window: bool, default_values: list = []):
    longest_texts = [max([len(text) for text in col]) for col in header]
    window_size = (((sum(longest_texts) + 60) * CHECKBOX_PIXEL_LENGTH), 40 * max([len(h) for h in header]) + 75)
    layout = CreateMainLayout(categories, header, descriptions, done_button_text, style_button_text, data_button_text, edit_button_text, window_size[0], csv_not_empty, is_sub_window, default_values)
    return sg.Window(title=MESSAGES.app_title,
                     layout=layout,
                     use_custom_titlebar=True,
                     titlebar_background_color=COLORS["bar_bkg"],
                     titlebar_text_color=COLORS["bar_txt"],
                     titlebar_icon=PATH.colored_icon,
                     background_color=COLORS["win_bkg"],
                     size=window_size,
                     element_justification='l')

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
        [sg.Text(pad_string(MESSAGES.hue, 0),
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
                     titlebar_icon=PATH.style_icon,
                     background_color=COLORS["sld_bkg"],
                     relative_location=(-100, 0)
                     ).Finalize()

def PreviewWindow(preview_window_text: str, preview_close_key: str, hue_offset: float):
    return sg.Window(preview_window_text, [
        [sg.Text(pad_string(MESSAGES.preview_text.upper(), 27),
                 text_color=apply_hue_offset(COLORS["cat_txt"], hue_offset),
                 background_color=apply_hue_offset(COLORS["cat_bkg"], hue_offset),
                 pad=((15, 0), (10, 10)),
                 font=FONTS["cat"])],
        [sg.Checkbox(text=pad_string(MESSAGES.preview_checkbox, 30),
                     default=False,
                     size=15,
                     font=FONTS["ckb"],
                     checkbox_color=apply_hue_offset(COLORS["ckb_bkg"], hue_offset),
                     text_color=apply_hue_offset(COLORS["ckb_txt"], hue_offset),
                     background_color=apply_hue_offset(COLORS["win_bkg"], hue_offset),
                     pad=((15, 0), (2, 2)),
                     tooltip=MESSAGES.preview_tooltip)],
        [sg.Button(MESSAGES.preview_close,
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
                     titlebar_icon=f"{DIR}/assets/icons/preview16.png",
                     background_color=apply_hue_offset(COLORS["win_bkg"], hue_offset),
                     relative_location=(240, 0)
                     ).Finalize()

def DataWindow(data_button_text: str, export_button_text: str, scrollable_image: bool, img_base64: str):
    width, height = Image.open(BytesIO(b64decode(img_base64))).size
    layout = [
        [sg.Image(data=img_base64)],
        [
            sg.InputText(key=export_button_text, do_not_clear=False, enable_events=True, visible=False),
            sg.FileSaveAs(
                button_text=export_button_text,
                font=FONTS["btn"],
                initial_folder="%HomeDrive%",
                file_types=(('PNG', '.png'), ('JPG', '.jpg')),
                pad=((width - 50, 5), (5, 5)),
                button_color=(COLORS["exp_bkg"], COLORS["exp_txt"])
            )
        ]
    ]
    return sg.Window(data_button_text, [
        [sg.Column(layout, scrollable=scrollable_image, key='Column')]
    ],
                     return_keyboard_events=True,
                     use_custom_titlebar=True,
                     titlebar_background_color=COLORS["bar_bkg"],
                     titlebar_text_color=COLORS["bar_txt"],
                     titlebar_icon=PATH.data_icon,
                     background_color=COLORS["dat_bkg"],
                     relative_location=(0, -15),
                     ).Finalize()

def NeglectedPopUp(accept_text: str, reject_text: str):
    layout = [
        [sg.Text(MESSAGES.neglected,
                 text_color=COLORS["neg_txt"],
                 background_color=COLORS["neg_bkg"],
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
                    text_color=COLORS["neg_txt"],
                    background_color=COLORS["neg_bkg"],
                    font=FONTS["pop"]),
            sg.Button(reject_text,
                      font=FONTS["btn"],
                      size=7,
                      key=reject_text,
                      pad=((0, 15), (15, 15)),
                      button_color=(COLORS["dnb_txt"], COLORS["dnb_bkg"]))
        ]
    ]
    return sg.Window(MESSAGES.neglected_title,
                     layout,
                     return_keyboard_events=True,
                     use_custom_titlebar=True,
                     titlebar_background_color=COLORS["bar_bkg"],
                     titlebar_text_color=COLORS["bar_txt"],
                     titlebar_icon=PATH.yesterday_icon,
                     background_color=COLORS["neg_bkg"],
                     relative_location=(0, 0),
                     element_justification='c'
                     ).Finalize()

def DatePickerWindow(select_date_key: str, select_date_button_text: str):
    layout = [
        [sg.Text(
            text=MESSAGES.date_text,
            text_color=COLORS["dtp_txt"],
            background_color=COLORS["dtp_bkg"],
            font=FONTS["pop"]
        )],
        [
            sg.InputText(key=select_date_key,
                         background_color=COLORS["dtp_bkg"],
                         size=20),
            sg.CalendarButton(MESSAGES.date_calendar,
                              close_when_date_chosen=True,
                              target=select_date_key,
                              format='%Y-%m-%d',
                              size=15,
                              button_color=(COLORS["dnb_txt"], COLORS["dnb_bkg"])),
            sg.Button(select_date_button_text,
                      font=FONTS["btn"],
                      size=7,
                      key=select_date_button_text,
                      button_color=(COLORS["dnb_txt"], COLORS["dnb_bkg"]))
        ]
    ]
    return sg.Window(MESSAGES.date_calendar,
                     layout,
                     return_keyboard_events=True,
                     use_custom_titlebar=True,
                     titlebar_background_color=COLORS["bar_bkg"],
                     titlebar_text_color=COLORS["bar_txt"],
                     titlebar_icon=PATH.yesterday_icon,
                     background_color=COLORS["dtp_bkg"],
                     relative_location=(0, 0),
                     element_justification='c'
                     ).Finalize()

def habit_init_key(key: str, row: int, sub_row: int = 0):
    return f'{key}_{row}' if sub_row == 0 else f'{key}_{row}_{sub_row}'

def HabitInitHabitLayout(category_row: int,
                         category: str,
                         habit_count: int,
                         habits_init_habit_key: str,
                         habits_init_question_key: str,
                         habits_init_track_frequency_key: str,
                         habits_init_message_key: str,
                         habits_init_condition_key: str,
                         habits_init_fraction_num_key: str,
                         habits_init_fraction_den_key: str,
                         values_dict: dict):
    return [[
        sg.InputText(key=habit_init_key(habits_init_habit_key, category_row, row),
                     background_color=COLORS["pop_bkg"],
                     size=20,
                     pad=(10, 0),
                     tooltip=MESSAGES.input_tooltip_habit,
                     default_text=safe_value_from_dict(habit_init_key(habits_init_habit_key, category_row, row), values_dict)),
        sg.InputText(key=habit_init_key(habits_init_question_key, category_row, row),
                     background_color=COLORS["pop_bkg"],
                     size=30,
                     tooltip=MESSAGES.input_tooltip_question,
                     default_text=safe_value_from_dict(habit_init_key(habits_init_question_key, category_row, row), values_dict)),
        sg.VerticalSeparator(color=COLORS["hbi_sep"]),
        sg.Checkbox(text=MESSAGES.input_tooltip_track,
                    default=safe_value_from_dict(habit_init_key(habits_init_track_frequency_key, category_row, row), values_dict, True),
                    key=habit_init_key(habits_init_track_frequency_key, category_row, row),
                    size=16,
                    font=FONTS["ckb"],
                    checkbox_color=COLORS["ckb_bkg"],
                    text_color=COLORS["ckb_txt"],
                    background_color=COLORS["win_bkg"],
                    pad=5,
                    tooltip=MESSAGES.input_tooltip_checkbox,
                    enable_events=True),
        sg.InputText(key=habit_init_key(habits_init_message_key, category_row, row),
                     background_color=COLORS["pop_bkg"],
                     size=60,
                     pad=((0, 10), (0, 0)),
                     tooltip=MESSAGES.input_tooltip_message,
                     default_text=safe_value_from_dict(habit_init_key(habits_init_message_key, category_row, row), values_dict),
                     visible=safe_value_from_dict(habit_init_key(habits_init_track_frequency_key, category_row, row), values_dict, True)),
        sg.Combo(values=['>', '<'],
                 default_value=safe_value_from_dict(habit_init_key(habits_init_condition_key, category_row, row), values_dict),
                 key=habit_init_key(habits_init_condition_key, category_row, row),
                 size=4,
                 pad=5,
                 auto_size_text=True,
                 background_color=COLORS["ckb_bkg"],
                 text_color=COLORS["ckb_txt"],
                 button_background_color=COLORS["dnb_bkg"],
                 button_arrow_color=COLORS["dnb_txt"],
                 font=FONTS["ckb"],
                 change_submits=True,
                 enable_events=True,
                 tooltip=MESSAGES.input_tooltip_combo,
                 visible=safe_value_from_dict(habit_init_key(habits_init_track_frequency_key, category_row, row), values_dict, True)),
        sg.InputText(key=habit_init_key(habits_init_fraction_num_key, category_row, row),
                     background_color=COLORS["pop_bkg"],
                     size=3,
                     default_text=safe_value_from_dict(habit_init_key(habits_init_fraction_num_key, category_row, row), values_dict),
                     visible=safe_value_from_dict(habit_init_key(habits_init_track_frequency_key, category_row, row), values_dict, True)),
        sg.Text("in", key=("spacing", row), background_color=COLORS["win_bkg"], visible=safe_value_from_dict(habit_init_key(habits_init_track_frequency_key, category_row, row), values_dict, True)),
        sg.InputText(key=habit_init_key(habits_init_fraction_den_key, category_row, row),
                     background_color=COLORS["pop_bkg"],
                     size=3,
                     default_text=safe_value_from_dict(habit_init_key(habits_init_fraction_den_key, category_row, row), values_dict),
                     visible=safe_value_from_dict(habit_init_key(habits_init_track_frequency_key, category_row, row), values_dict, True)),
        sg.Text(pad_string("days", 5), key=("spacing_days", row), background_color=COLORS["win_bkg"], visible=safe_value_from_dict(habit_init_key(habits_init_track_frequency_key, category_row, row), values_dict, True)),
    ] for row in range(habit_count)]

def HabitInitCategoryLayout(category_count: int,
                            habits_init_category_key: str,
                            habits_init_add_habit_text: str,
                            habits_init_del_habit_text: str,
                            habits_init_track_frequency_key: str,
                            habits_init_habit_key: str,
                            habits_init_question_key: str,
                            habits_init_message_key: str,
                            habits_init_condition_key: str,
                            habits_init_fraction_num_key: str,
                            habits_init_fraction_den_key: str,
                            values_dict: dict,
                            habit_count: list):
    button_padding = 15
    button_size = 10
    return [[
        [sg.HorizontalSeparator(color=COLORS["hbi_sep"])],
        [sg.InputText(key=habit_init_key(habits_init_category_key, row),
                      background_color=COLORS["pop_bkg"],
                      size=20,
                      pad=10,
                      tooltip=MESSAGES.input_tooltip_category,
                      default_text=safe_value_from_dict(habit_init_key(habits_init_category_key, row), values_dict)),
        sg.Text(pad_string("", 0), key=("spacing", row), background_color=COLORS["win_bkg"]),
        sg.Button(button_text=habits_init_add_habit_text,
                  key=habit_init_key(habits_init_add_habit_text, row),
                  font=FONTS["btn"],
                  size=button_size,
                  button_color=(COLORS["dnb_bkg"], COLORS["dnb_txt"]),
                  pad=(button_padding, 0)),
        sg.Button(button_text=habits_init_del_habit_text,
                  key=habit_init_key(habits_init_del_habit_text, row),
                  font=FONTS["btn"],
                  size=button_size,
                  button_color=(COLORS["dnb_bkg"], COLORS["dnb_txt"]),
                  pad=((0, button_padding), (0, 0)),
                  disabled=safe_bool_from_array(row - 1, habit_count))],
        HabitInitHabitLayout(row, safe_value_from_dict(habit_init_key(habits_init_category_key, row), values_dict),
                             safe_value_from_array(row - 1, habit_count), habits_init_habit_key,
                             habits_init_question_key, habits_init_track_frequency_key, habits_init_message_key,
                             habits_init_condition_key, habits_init_fraction_num_key, habits_init_fraction_den_key, values_dict),
        # layout = [[sg.Column(column_layout, scrollable=True,  vertical_scroll_only=True, size_subsample_height=5)]]
    ] for row in range(1, category_count + 1)]

def HabitsInitLayout(habits_init_cat_add: str,
                     habits_init_cat_remove: str,
                     habits_init_generate_text: str,
                     habits_init_categories_key: str,
                     habits_init_category_key: str,
                     habits_init_add_habit_text: str,
                     habits_init_del_habit_text: str,
                     habits_init_track_frequency_key: str,
                     habits_init_habit_key: str,
                     habits_init_question_key: str,
                     habits_init_message_key: str,
                     habits_init_condition_key: str,
                     habits_init_fraction_num_key: str,
                     habits_init_fraction_den_key: str,
                     category_count: int,
                     values_dict: dict,
                     habit_count: list):
    button_padding = 25
    button_font_size = (20, 2)
    layout = [
        HabitInitCategoryLayout(category_count, habits_init_category_key, habits_init_add_habit_text,
                                habits_init_del_habit_text, habits_init_track_frequency_key, habits_init_habit_key,
                                habits_init_question_key, habits_init_message_key, habits_init_condition_key,
                                habits_init_fraction_num_key, habits_init_fraction_den_key, values_dict, habit_count),
        [sg.HorizontalSeparator(color=COLORS["hbi_sep"])],
        [
            sg.Push(background_color=COLORS["win_bkg"]),
            sg.Button(habits_init_cat_add,
                      font=FONTS["btn"],
                      size=button_font_size,
                      button_color=(COLORS["hbc_bkg"], COLORS["hbc_txt"]),
                      pad=button_padding),
            sg.Button(habits_init_cat_remove,
                      font=FONTS["btn"],
                      size=button_font_size,
                      button_color=(COLORS["hbc_bkg"], COLORS["hbc_txt"]),
                      pad=((0, button_padding), (0, 0)),
                      disabled=category_count < 1),
            sg.Button(habits_init_generate_text,
                      font=FONTS["btn"],
                      size=button_font_size,
                      button_color=(COLORS["dnb_bkg"], COLORS["dnb_txt"]),
                      pad=((0, button_padding), (0, 0))),
            sg.Push(background_color=COLORS["win_bkg"])
        ],
    ]
    return layout
    # https://stackoverflow.com/questions/66351957/how-to-add-a-field-or-element-by-clicking-a-button-in-pysimplegui
    # https://github.com/PySimpleGUI/PySimpleGUI/issues/845

def HabitsInitWindow(layout: list):
    return sg.Window(
        MESSAGES.habits_title,
        layout,
        return_keyboard_events=True,
        use_custom_titlebar=True,
        titlebar_background_color=COLORS["bar_bkg"],
        titlebar_text_color=COLORS["bar_txt"],
        titlebar_icon=PATH.init_icon,
        background_color=COLORS["win_bkg"],
        relative_location=(0, 0),
        element_justification='l'
    ).Finalize()

def ReRenderHabitsInit(previous_windows: sg.Window,
                       habits_init_cat_add: str,
                       habits_init_cat_remove: str,
                       habits_init_generate_text: str,
                       habits_init_categories_key: str,
                       habits_init_category_key: str,
                       habits_init_add_habit_text: str,
                       habits_init_del_habit_text: str,
                       habits_init_track_frequency_key: str,
                       habits_init_habit_key: str,
                       habits_init_question_key: str,
                       habits_init_message_key: str,
                       habits_init_condition_key: str,
                       habits_init_fraction_num_key: str,
                       habits_init_fraction_den_key: str,
                       category_count: int,
                       values_dict: dict,
                       habit_count: list) -> sg.Window:
    variables_init_layout = HabitsInitLayout(habits_init_cat_add, habits_init_cat_remove, habits_init_generate_text, habits_init_categories_key,
                                             habits_init_category_key, habits_init_add_habit_text, habits_init_del_habit_text,
                                             habits_init_track_frequency_key, habits_init_habit_key, habits_init_question_key,
                                             habits_init_message_key, habits_init_condition_key, habits_init_fraction_num_key,
                                             habits_init_fraction_den_key, category_count, values_dict, habit_count)
    previous_windows.close()
    new_window = HabitsInitWindow(variables_init_layout)
    return new_window

import PySimpleGUI as sg
from tkinter import Tk as tk_tk, font as tk_font
import matplotlib.colors as clr
import cv2 as cv
from io import BytesIO
from PIL import Image
from base64 import b64decode
from .core import get_matrix_data_by_header_indexes, Settings
from .utils import flatten_and_wrap, flatten_list_1, pad_string, safe_value_from_dict, safe_bool_from_array,\
    safe_value_from_array, settings_key_to_text, habit_init_key
from .constants import COLORS, FONTS, MESSAGES, PATHS, SETTINGS_KEYS
# w, h = sg.Window.get_screen_size()
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
    h2 = cv.add(h, hsv_delta) # type: ignore
    hsv2 = cv.merge([h2, s, v])

    result = cv.cvtColor(hsv2, cv.COLOR_HSV2BGR)
    result = cv.merge([result[:, :, 0], result[:, :, 1], result[:, :, 2], a])
    cv.imwrite(PATH.colored_icon, result)

def InitUi(hueOffset: float):
    generate_icon(hueOffset)
    update_COLORS(hueOffset)

def CreateMainLayout(categories: list, headers: list, descriptions: list, done_button_text: str, style_button_text: str, data_button_text: str, edit_button_text: str, settings_button_text: str, csv_not_empty: bool, is_sub_window: bool, default_values: list) -> list:
    max_cat_header_count = max([len(cat) for cat in headers])
    columns = [
        sg.Column(
            flatten_and_wrap([
                [sg.Text(cat.upper(),
                    text_color=COLORS["cat_txt"],
                    background_color=COLORS["cat_bkg"],
                    pad=((20, 20), (10, 0)),
                    font=FONTS["cat"])],
                list([sg.Checkbox(text=' ' + item,
                    default=False if len(default_values) == 0 else bool(get_matrix_data_by_header_indexes(default_values, headers, item)),
                    key=item,
                    font=FONTS["ckb"],
                    checkbox_color=COLORS["ckb_bkg"],
                    text_color=COLORS["ckb_txt"],
                    background_color=COLORS["win_bkg"],
                    pad=((15, 0), (1, 1)),
                    tooltip=get_matrix_data_by_header_indexes(descriptions, headers, item))] for item in headers[idx_cat]),
                list([sg.Text(text=' ',
                    font=FONTS["ckb"],
                    text_color=COLORS["win_bkg"],
                    background_color=COLORS["win_bkg"],
                    pad=((15, 0), (1, 1)))] for i in range(max_cat_header_count - len(headers[idx_cat])))
            ]),
            background_color=COLORS["cat_bkg"],
            justification='l'
        ) for idx_cat, cat in enumerate(categories)
    ]

    buttons_layout = [
        sg.Button(style_button_text,
                  font=FONTS["btn"],
                  size=7,
                  button_color=(COLORS["dnb_bkg"], COLORS["dnb_txt"]),
                  pad=(25, (5, 15)),
                  tooltip=MESSAGES.style_button_tooltip,
                  ),
        sg.Push(background_color=COLORS["win_bkg"]),
        sg.Button(settings_button_text,
                  font=FONTS["btn"],
                  size=7,
                  button_color=(COLORS["dnb_bkg"], COLORS["dnb_txt"]),
                  pad=(0, (5, 15)),
                  tooltip=MESSAGES.settings_button_tooltip,
                  ),
        sg.Push(background_color=COLORS["win_bkg"]),
        sg.Button(data_button_text,
                  font=FONTS["btn"],
                  size=7,
                  disabled=not csv_not_empty,
                  button_color=(COLORS["dnb_bkg"], COLORS["dnb_txt"]),
                  pad=(0, (5, 15)),
                  tooltip=MESSAGES.data_button_tooltip,
                  ),
        sg.Push(background_color=COLORS["win_bkg"]),
        sg.Button(edit_button_text,
                  font=FONTS["btn"],
                  size=7,
                  disabled=not csv_not_empty,
                  button_color=(COLORS["dnb_bkg"], COLORS["dnb_txt"]),
                  pad=(0, (5, 15)),
                  tooltip=MESSAGES.edit_button_tooltip,
                  ),
    ]

    done_button_layout = [
        sg.Push(background_color=COLORS["win_bkg"]),
        sg.Button(done_button_text,
                  font=FONTS["btn"],
                  size=7,
                  button_color=(COLORS["dnb_bkg"], COLORS["dnb_txt"]),
                  pad=(25, (5, 15)),
                  tooltip=MESSAGES.done_button_tooltip,
                  ),
    ]

    if not is_sub_window:
        buttons_layout.extend(done_button_layout)
        window_layout = [columns, buttons_layout]
    else:
        window_layout = [columns, done_button_layout]

    return window_layout

def MainWindow(categories: list, header: list, descriptions: list, done_button_text: str, style_button_text: str, data_button_text: str, edit_button_text: str,
               settings_button_text: str, csv_not_empty: bool, is_sub_window: bool, default_values: list = []):
    layout = CreateMainLayout(categories, header, descriptions, done_button_text, style_button_text, data_button_text, edit_button_text, settings_button_text, csv_not_empty, is_sub_window, default_values)
    return sg.Window(title=MESSAGES.app_title,
                     layout=layout,
                     use_custom_titlebar=True,
                     titlebar_background_color=COLORS["bar_bkg"],
                     titlebar_text_color=COLORS["bar_txt"],
                     titlebar_icon=PATH.colored_icon,
                     background_color=COLORS["win_bkg"],
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

def StyleWindow(style_button_text: str, slider_text_key: str, preview_window_text: str, set_button_text: str, hue_offset: float):
    return sg.Window(style_button_text, [
        [sg.Text(pad_string(MESSAGES.hue, 0),
                 background_color=COLORS["sld_bkg"],
                 text_color=COLORS["sld_txt"])],
        [sg.Slider(range=(-0.5, 0.5),
                   default_value=hue_offset,
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
          sg.Button(set_button_text,
                    font=FONTS["btn"],
                    size=7,
                    pad=((322, 0), (15, 15)),
                    key=set_button_text,
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
                     titlebar_icon=PATHS.preview_icon,
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
                         text_color="#ffffff",
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

def HabitInitHabitLayout(row_in_habit_count: int,
                         category_row: int,
                         category: str,
                         habits_init_habit_key: str,
                         habits_init_question_key: str,
                         habits_init_track_frequency_key: str,
                         habits_init_message_key: str,
                         habits_init_condition_key: str,
                         habits_init_fraction_num_key: str,
                         habits_init_fraction_den_key: str,
                         values_dict: dict):
    layout = [
        sg.InputText(key=habit_init_key(habits_init_habit_key, category_row, row_in_habit_count),
                     background_color=COLORS["pop_bkg"],
                     size=20,
                     pad=(10, 0),
                     tooltip=MESSAGES.input_tooltip_habit,
                     default_text=safe_value_from_dict(habit_init_key(habits_init_habit_key, category_row, row_in_habit_count), values_dict)), # type: ignore
        sg.InputText(key=habit_init_key(habits_init_question_key, category_row, row_in_habit_count),
                     background_color=COLORS["pop_bkg"],
                     size=30,
                     tooltip=MESSAGES.input_tooltip_question,
                     default_text=safe_value_from_dict(habit_init_key(habits_init_question_key, category_row, row_in_habit_count), values_dict)), # type: ignore
        sg.VerticalSeparator(color=COLORS["hbi_sep"]),
        sg.Checkbox(text=MESSAGES.input_tooltip_track,
                    default=bool(safe_value_from_dict(habit_init_key(habits_init_track_frequency_key, category_row, row_in_habit_count), values_dict)),
                    key=habit_init_key(habits_init_track_frequency_key, category_row, row_in_habit_count),
                    size=16,
                    font=FONTS["ckb"],
                    checkbox_color=COLORS["ckb_bkg"],
                    text_color=COLORS["ckb_txt"],
                    background_color=COLORS["win_bkg"],
                    pad=5,
                    tooltip=MESSAGES.input_tooltip_checkbox,
                    enable_events=True),
        sg.InputText(key=habit_init_key(habits_init_message_key, category_row, row_in_habit_count),
                     background_color=COLORS["pop_bkg"],
                     size=60,
                     pad=((0, 10), (0, 0)),
                     tooltip=MESSAGES.input_tooltip_message,
                     default_text=safe_value_from_dict(habit_init_key(habits_init_message_key, category_row, row_in_habit_count), values_dict), # type: ignore
                     visible=bool(safe_value_from_dict(habit_init_key(habits_init_track_frequency_key, category_row, row_in_habit_count), values_dict))),
        sg.Combo(values=['>=', '>', '=', '<', '<='],
                 default_value=safe_value_from_dict(habit_init_key(habits_init_condition_key, category_row, row_in_habit_count), values_dict),
                 key=habit_init_key(habits_init_condition_key, category_row, row_in_habit_count),
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
                 visible=bool(safe_value_from_dict(habit_init_key(habits_init_track_frequency_key, category_row, row_in_habit_count), values_dict))),
        sg.InputText(key=habit_init_key(habits_init_fraction_num_key, category_row, row_in_habit_count),
                     background_color=COLORS["pop_bkg"],
                     size=3,
                     default_text=safe_value_from_dict(habit_init_key(habits_init_fraction_num_key, category_row, row_in_habit_count), values_dict), # type: ignore
                     visible=bool(safe_value_from_dict(habit_init_key(habits_init_track_frequency_key, category_row, row_in_habit_count), values_dict))),
        sg.Text("in", key=("spacing", row_in_habit_count), background_color=COLORS["win_bkg"], visible=bool(safe_value_from_dict(habit_init_key(habits_init_track_frequency_key, category_row, row_in_habit_count), values_dict))),
        sg.InputText(key=habit_init_key(habits_init_fraction_den_key, category_row, row_in_habit_count),
                     background_color=COLORS["pop_bkg"],
                     size=3,
                     default_text=safe_value_from_dict(habit_init_key(habits_init_fraction_den_key, category_row, row_in_habit_count), values_dict), # type: ignore
                     visible=bool(safe_value_from_dict(habit_init_key(habits_init_track_frequency_key, category_row, row_in_habit_count), values_dict))),
        sg.Text(pad_string("days", 5), key=("spacing_days", row_in_habit_count), background_color=COLORS["win_bkg"],
                visible=bool(safe_value_from_dict(habit_init_key(habits_init_track_frequency_key, category_row, row_in_habit_count), values_dict))),
    ]
    return layout

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

    layout = []
    for row in range(1, category_count + 1):
        category = [
            [sg.HorizontalSeparator(color=COLORS["hbi_sep"])],
            [sg.InputText(key=habit_init_key(habits_init_category_key, row),
                          background_color=COLORS["pop_bkg"],
                          size=20,
                          pad=10,
                          tooltip=MESSAGES.input_tooltip_category,
                          default_text=safe_value_from_dict(habit_init_key(habits_init_category_key, row), values_dict)), # type: ignore
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
        ]
        for habit in range(safe_value_from_array(row - 1, habit_count, 0)):
            habit_row = HabitInitHabitLayout(habit, row, safe_value_from_dict(habit_init_key(habits_init_category_key, row), values_dict), # type: ignore
                        habits_init_habit_key, habits_init_question_key, habits_init_track_frequency_key, habits_init_message_key,
                        habits_init_condition_key, habits_init_fraction_num_key, habits_init_fraction_den_key, values_dict)
            category.append(habit_row)
        layout.append(category)
    return layout

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
    show_scroll_bar = category_count + sum(flatten_list_1(habit_count)) > 20
    category_layout = HabitInitCategoryLayout(category_count, habits_init_category_key, habits_init_add_habit_text,
                      habits_init_del_habit_text, habits_init_track_frequency_key, habits_init_habit_key,
                      habits_init_question_key, habits_init_message_key, habits_init_condition_key,
                      habits_init_fraction_num_key, habits_init_fraction_den_key, values_dict, habit_count)
    layout = [
        [sg.Column(
            flatten_list_1(category_layout),
            scrollable=show_scroll_bar,
            vertical_scroll_only=show_scroll_bar,
            background_color=COLORS["win_bkg"],
            visible=category_count > 0
        )],
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

def HabitsInitWindow(layout: list) -> sg.Window:
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
        element_justification='l',
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

def SettingsWindowLayout(settings: Settings, settings_save_button_text: str, settings_cancel_button_text: str) -> list:
    checkbox_padding = 5
    sections_padding_y = 25
    sections_padding_x = 5
    text_input_size = 7

    appearance = [
        [
            sg.Text(
                text=MESSAGES.settings_section_appearance,
                text_color=COLORS["cat_txt"],
                background_color=COLORS["stg_bkg"],
                font=FONTS["cat"],
                pad=((sections_padding_x, 0), (sections_padding_y - 10, 5)),
            )
        ],
        [
            # I thought removing offset was more appropriate
            sg.Text(
                text=settings_key_to_text(SETTINGS_KEYS.hue_offset).replace("Offset", ""),
                text_color=COLORS["stg_txt"],
                background_color=COLORS["stg_bkg"],
                font=FONTS["pop"],
            ),
            sg.InputText(key=SETTINGS_KEYS.hue_offset,
                         do_not_clear=True,
                         enable_events=True,
                         visible=True,
                         font=FONTS["ckb"],
                         tooltip=MESSAGES.settings_tooltip_hueoffset,
                         default_text=str(settings.hue_offset),
                         size=text_input_size,
                         justification='r'
                         )
        ],
    ]

    data_visualization = [
        [
            sg.Text(
                text=MESSAGES.settings_section_data_visualization,
                text_color=COLORS["cat_txt"],
                background_color=COLORS["stg_bkg"],
                font=FONTS["cat"],
                pad=((sections_padding_x, 0), (sections_padding_y, 5)),
            )
        ],
        [
            sg.Text(
                text=settings_key_to_text(SETTINGS_KEYS.data_days),
                text_color=COLORS["stg_txt"],
                background_color=COLORS["stg_bkg"],
                font=FONTS["pop"],
            ),
            sg.InputText(key=SETTINGS_KEYS.data_days,
                         do_not_clear=True,
                         enable_events=True,
                         visible=True,
                         font=FONTS["ckb"],
                         tooltip=MESSAGES.settings_tooltip_days,
                         default_text=str(settings.data_days),
                         size=text_input_size,
                        justification='r'
                         ),
            sg.Text(
                text=pad_string('', 5),
                text_color=COLORS["stg_bkg"],
                background_color=COLORS["stg_bkg"],
                font=FONTS["ckb"],
            ),

            sg.Text(
                text=settings_key_to_text(SETTINGS_KEYS.weekdays_language),
                text_color=COLORS["stg_txt"],
                background_color=COLORS["stg_bkg"],
                font=FONTS["pop"],
            ),
            sg.Combo(values=['en', 'pt', 'jp'],
                     default_value=str(settings.weekdays_language),
                     key=SETTINGS_KEYS.weekdays_language,
                     size=4,
                     pad=5,
                     auto_size_text=True,
                     background_color=COLORS["stg_bkg"],
                     text_color=COLORS["stg_txt"],
                     button_background_color=COLORS["win_bkg"],
                     button_arrow_color=COLORS["cat_txt"],
                     font=FONTS["ckb"],
                     change_submits=True,
                     enable_events=True,
                     visible=True,
                     tooltip=MESSAGES.input_tooltip_combo,
                     ),
            sg.Text(
                text=pad_string('', 2),
                text_color=COLORS["stg_bkg"],
                background_color=COLORS["stg_bkg"],
                font=FONTS["ckb"],
            ),

            sg.Text(
                text=settings_key_to_text(SETTINGS_KEYS.graph_expected_value),
                text_color=COLORS["stg_txt"],
                background_color=COLORS["stg_bkg"],
                font=FONTS["pop"],
            ),
            sg.Checkbox(text='',
                        default=bool(settings.graph_expected_value),
                        key=SETTINGS_KEYS.graph_expected_value,
                        font=FONTS["pop"],
                        checkbox_color=COLORS["ckb_bkg"],
                        text_color=COLORS["ckb_txt"],
                        background_color=COLORS["stg_bkg"],
                        pad=((checkbox_padding, 0), (1, 1)),
                        tooltip=MESSAGES.settings_tooltip_expected
                        ),
            sg.Text(
                text=pad_string('', 2),
                text_color=COLORS["stg_bkg"],
                background_color=COLORS["stg_bkg"],
                font=FONTS["ckb"],
            ),

            sg.Text(
                text=settings_key_to_text(SETTINGS_KEYS.scrollable_image),
                text_color=COLORS["stg_txt"],
                background_color=COLORS["stg_bkg"],
                font=FONTS["pop"],
            ),
            sg.Checkbox(text='',
                        default=bool(settings.scrollable_image),
                        key=SETTINGS_KEYS.scrollable_image,
                        font=FONTS["pop"],
                        checkbox_color=COLORS["ckb_bkg"],
                        text_color=COLORS["ckb_txt"],
                        background_color=COLORS["stg_bkg"],
                        pad=((checkbox_padding, 0), (1, 1)),
                        tooltip=MESSAGES.settings_tooltip_scrollable
                        ),
        ],
    ]

    messages = [
        [
            sg.Text(
                text=MESSAGES.settings_section_messages,
                text_color=COLORS["cat_txt"],
                background_color=COLORS["stg_bkg"],
                font=FONTS["cat"],
                pad=((sections_padding_x, 0), (sections_padding_y, 5)),
            )
        ],
        [
            sg.Text(
                text=settings_key_to_text(SETTINGS_KEYS.display_messages),
                text_color=COLORS["stg_txt"],
                background_color=COLORS["stg_bkg"],
                font=FONTS["pop"],
            ),
            sg.Checkbox(text='',
                        default=bool(settings.display_messages),
                        key=SETTINGS_KEYS.display_messages,
                        font=FONTS["pop"],
                        checkbox_color=COLORS["ckb_bkg"],
                        text_color=COLORS["ckb_txt"],
                        background_color=COLORS["stg_bkg"],
                        pad=((checkbox_padding, 20), (1, 1)),
                        tooltip=MESSAGES.settings_tooltip_messages_show
                        ),
            sg.Text(
                text=pad_string('', 3),
                text_color=COLORS["stg_bkg"],
                background_color=COLORS["stg_bkg"],
                font=FONTS["ckb"],
            ),

            sg.Text(
                text=settings_key_to_text(SETTINGS_KEYS.random_messages),
                text_color=COLORS["stg_txt"],
                background_color=COLORS["stg_bkg"],
                font=FONTS["pop"],
            ),
            sg.Checkbox(text='',
                        default=bool(settings.random_messages),
                        key=SETTINGS_KEYS.random_messages,
                        font=FONTS["pop"],
                        checkbox_color=COLORS["ckb_bkg"],
                        text_color=COLORS["ckb_txt"],
                        background_color=COLORS["stg_bkg"],
                        pad=((checkbox_padding, 0), (1, 1)),
                        tooltip=MESSAGES.settings_tooltip_random
                        ),
            sg.Text(
                text=pad_string('', 7),
                text_color=COLORS["stg_bkg"],
                background_color=COLORS["stg_bkg"],
                font=FONTS["ckb"],
            ),

            sg.Text(
                text=settings_key_to_text(SETTINGS_KEYS.message_duration),
                text_color=COLORS["stg_txt"],
                background_color=COLORS["stg_bkg"],
                font=FONTS["pop"],
            ),
            sg.InputText(key=SETTINGS_KEYS.message_duration,
                         do_not_clear=True,
                         enable_events=True,
                         visible=True,
                         font=FONTS["ckb"],
                         tooltip=MESSAGES.settings_tooltip_duration,
                         default_text=str(settings.message_duration),
                         size=text_input_size,
                        justification='r'
                         ),
        ]
    ]

    buttons = [
        [
            sg.Text(
                text=pad_string('', 68),
                text_color=COLORS["stg_bkg"],
                background_color=COLORS["stg_bkg"],
                font=FONTS["ckb"],
            ),
            sg.Button(settings_cancel_button_text,
                      font=FONTS["btn"],
                      size=7,
                      pad=((5, 0), (30, 15)),
                      key=settings_cancel_button_text,
                      button_color=(COLORS["dnb_bkg"], COLORS["dnb_txt"]),
                      ),
            sg.Text(
                text=pad_string('', 5),
                text_color=COLORS["stg_bkg"],
                background_color=COLORS["stg_bkg"],
                font=FONTS["ckb"],
            ),
            sg.Button(settings_save_button_text,
                      font=FONTS["btn"],
                      size=7,
                      pad=((5, 0), (30, 15)),
                      key=settings_save_button_text,
                      button_color=(COLORS["dnb_bkg"], COLORS["dnb_txt"]),
                      ),
        ]
    ]

    layout = [appearance, data_visualization, messages, buttons]
    return layout

def SettingsWindow(settings: Settings, settings_button_text: str, settings_save_button_text: str, settings_cancel_button_text: str):
    layout = SettingsWindowLayout(settings, settings_save_button_text, settings_cancel_button_text)
    return sg.Window(title=settings_button_text,
                     layout=layout,
                     use_custom_titlebar=True,
                     titlebar_background_color=COLORS["bar_bkg"],
                     titlebar_text_color=COLORS["bar_txt"],
                     titlebar_icon=PATH.settings_icon,
                     background_color=COLORS["stg_bkg"],
                     size=(900, 360),
                     element_justification='l'
                     )

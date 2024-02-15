import PySimpleGUI as sg

from source.constants import COLORS, FONTS, MESSAGES, PATHS
from source.utils import (
    flatten_list_1,
    pad_string,
    safe_value_from_dict,
    safe_bool_from_array,
    safe_value_from_array,
    habit_init_key,
)

PATH = PATHS()
PATH.__init__()

def HabitInitHabitLayout(
    row_in_habit_count: int,
    category_row: int,
    category: str,
    habits_init_habit_key: str,
    habits_init_question_key: str,
    habits_init_track_frequency_key: str,
    habits_init_message_key: str,
    habits_init_condition_key: str,
    habits_init_fraction_num_key: str,
    habits_init_fraction_den_key: str,
    values_dict: dict,
):
    layout = [
        sg.InputText(
            key=habit_init_key(habits_init_habit_key, category_row, row_in_habit_count),
            background_color=COLORS["pop_bkg"],
            size=20,
            pad=(10, 0),
            tooltip=MESSAGES.input_tooltip_habit,
            default_text=safe_value_from_dict( # type: ignore
                habit_init_key(habits_init_habit_key, category_row, row_in_habit_count),
                values_dict,
            ),
        ),         sg.InputText(
            key=habit_init_key(
                habits_init_question_key, category_row, row_in_habit_count
            ),
            background_color=COLORS["pop_bkg"],
            size=30,
            tooltip=MESSAGES.input_tooltip_question,
            default_text=safe_value_from_dict( # type: ignore
                habit_init_key(
                    habits_init_question_key, category_row, row_in_habit_count
                ),
                values_dict,
            ),
        ),
        sg.VerticalSeparator(color=COLORS["hbi_sep"]),
        sg.Checkbox(
            text=MESSAGES.input_tooltip_track,
            default=bool(
                safe_value_from_dict(
                    habit_init_key(
                        habits_init_track_frequency_key,
                        category_row,
                        row_in_habit_count,
                    ),
                    values_dict,
                )
            ),
            key=habit_init_key(
                habits_init_track_frequency_key, category_row, row_in_habit_count
            ),
            size=16,
            font=FONTS["ckb"],
            checkbox_color=COLORS["ckb_bkg"],
            text_color=COLORS["ckb_txt"],
            background_color=COLORS["win_bkg"],
            pad=5,
            tooltip=MESSAGES.input_tooltip_checkbox,
            enable_events=True,
        ),
        sg.InputText(
            key=habit_init_key(
                habits_init_message_key, category_row, row_in_habit_count
            ),
            background_color=COLORS["pop_bkg"],
            size=60,
            pad=((0, 10), (0, 0)),
            tooltip=MESSAGES.input_tooltip_message,
            default_text=safe_value_from_dict(habit_init_key(habits_init_message_key, category_row, row_in_habit_count), values_dict),  # type: ignore
            visible=bool(
                safe_value_from_dict(
                    habit_init_key(
                        habits_init_track_frequency_key,
                        category_row,
                        row_in_habit_count,
                    ),
                    values_dict,
                )
            ),
        ),
        sg.Combo(
            values=[">=", ">", "=", "<", "<="],
            default_value=safe_value_from_dict(
                habit_init_key(
                    habits_init_condition_key, category_row, row_in_habit_count
                ),
                values_dict,
            ),
            key=habit_init_key(
                habits_init_condition_key, category_row, row_in_habit_count
            ),
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
            visible=bool(
                safe_value_from_dict(
                    habit_init_key(
                        habits_init_track_frequency_key,
                        category_row,
                        row_in_habit_count,
                    ),
                    values_dict,
                )
            ),
        ),
        sg.InputText(
            key=habit_init_key(
                habits_init_fraction_num_key, category_row, row_in_habit_count
            ),
            background_color=COLORS["pop_bkg"],
            size=3,
            default_text=safe_value_from_dict(habit_init_key(habits_init_fraction_num_key, category_row, row_in_habit_count), values_dict),  # type: ignore
            visible=bool(
                safe_value_from_dict(
                    habit_init_key(
                        habits_init_track_frequency_key,
                        category_row,
                        row_in_habit_count,
                    ),
                    values_dict,
                )
            ),
        ),
        sg.Text(
            "in",
            key=("spacing", row_in_habit_count),
            background_color=COLORS["win_bkg"],
            visible=bool(
                safe_value_from_dict(
                    habit_init_key(
                        habits_init_track_frequency_key,
                        category_row,
                        row_in_habit_count,
                    ),
                    values_dict,
                )
            ),
        ),
        sg.InputText(
            key=habit_init_key(
                habits_init_fraction_den_key, category_row, row_in_habit_count
            ),
            background_color=COLORS["pop_bkg"],
            size=3,
            default_text=safe_value_from_dict(habit_init_key(habits_init_fraction_den_key, category_row, row_in_habit_count), values_dict),  # type: ignore
            visible=bool(
                safe_value_from_dict(
                    habit_init_key(
                        habits_init_track_frequency_key,
                        category_row,
                        row_in_habit_count,
                    ),
                    values_dict,
                )
            ),
        ),
        sg.Text(
            pad_string("days", 5),
            key=("spacing_days", row_in_habit_count),
            background_color=COLORS["win_bkg"],
            visible=bool(
                safe_value_from_dict(
                    habit_init_key(
                        habits_init_track_frequency_key,
                        category_row,
                        row_in_habit_count,
                    ),
                    values_dict,
                )
            ),
        ),
    ]
    return layout


def HabitInitCategoryLayout(
    category_count: int,
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
    habit_count: list,
):
    button_padding = 15
    button_size = 10

    layout = []
    for row in range(1, category_count + 1):
        category = [
            [sg.HorizontalSeparator(color=COLORS["hbi_sep"])],
            [
                sg.InputText(
                    key=habit_init_key(habits_init_category_key, row),
                    background_color=COLORS["pop_bkg"],
                    size=20,
                    pad=10,
                    tooltip=MESSAGES.input_tooltip_category,
                    default_text=safe_value_from_dict( # type: ignore
                        habit_init_key(habits_init_category_key, row), values_dict
                    ),
                ),
                sg.Text(
                    pad_string("", 0),
                    key=("spacing", row),
                    background_color=COLORS["win_bkg"],
                ),
                sg.Button(
                    button_text=habits_init_add_habit_text,
                    key=habit_init_key(habits_init_add_habit_text, row),
                    font=FONTS["btn"],
                    size=button_size,
                    button_color=(COLORS["dnb_bkg"], COLORS["dnb_txt"]),
                    pad=(button_padding, 0),
                ),
                sg.Button(
                    button_text=habits_init_del_habit_text,
                    key=habit_init_key(habits_init_del_habit_text, row),
                    font=FONTS["btn"],
                    size=button_size,
                    button_color=(COLORS["dnb_bkg"], COLORS["dnb_txt"]),
                    pad=((0, button_padding), (0, 0)),
                    disabled=safe_bool_from_array(row - 1, habit_count),
                ),
            ],
        ]
        for habit in range(safe_value_from_array(row - 1, habit_count, 0)):
            habit_row = HabitInitHabitLayout(
                habit,
                row,
                safe_value_from_dict(habit_init_key(habits_init_category_key, row), values_dict), # type: ignore
                habits_init_habit_key,
                habits_init_question_key,
                habits_init_track_frequency_key,
                habits_init_message_key,
                habits_init_condition_key,
                habits_init_fraction_num_key,
                habits_init_fraction_den_key,
                values_dict,
            )
            category.append(habit_row)
        layout.append(category)
    return layout


def HabitsInitLayout(
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
    habit_count: list,
):
    button_padding = 25
    button_font_size = (15, 2)
    show_scroll_bar = category_count + sum(flatten_list_1(habit_count)) > 20
    category_layout = HabitInitCategoryLayout(
        category_count,
        habits_init_category_key,
        habits_init_add_habit_text,
        habits_init_del_habit_text,
        habits_init_track_frequency_key,
        habits_init_habit_key,
        habits_init_question_key,
        habits_init_message_key,
        habits_init_condition_key,
        habits_init_fraction_num_key,
        habits_init_fraction_den_key,
        values_dict,
        habit_count,
    )
    layout = [
        [
            sg.Column(
                flatten_list_1(category_layout),
                scrollable=show_scroll_bar,
                vertical_scroll_only=show_scroll_bar,
                background_color=COLORS["win_bkg"],
                visible=category_count > 0,
            )
        ],
        [sg.HorizontalSeparator(color=COLORS["hbi_sep"])],
        [
            sg.Push(background_color=COLORS["win_bkg"]),
            sg.Button(
                habits_init_cat_add,
                font=FONTS["btn"],
                size=button_font_size,
                button_color=(COLORS["hbc_bkg"], COLORS["hbc_txt"]),
                pad=button_padding,
            ),
            sg.Button(
                habits_init_cat_remove,
                font=FONTS["btn"],
                size=button_font_size,
                button_color=(COLORS["hbc_bkg"], COLORS["hbc_txt"]),
                pad=((0, button_padding), (0, 0)),
                disabled=category_count < 1,
            ),
            sg.Button(
                habits_init_generate_text,
                font=FONTS["btn"],
                size=button_font_size,
                button_color=(COLORS["dnb_bkg"], COLORS["dnb_txt"]),
                pad=((0, button_padding), (0, 0)),
            ),
            sg.Push(background_color=COLORS["win_bkg"]),
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
        element_justification="l",
    ).Finalize()


def ReRenderHabitsInit(
    previous_windows: sg.Window,
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
    habit_count: list,
) -> sg.Window:
    variables_init_layout = HabitsInitLayout(
        habits_init_cat_add,
        habits_init_cat_remove,
        habits_init_generate_text,
        habits_init_categories_key,
        habits_init_category_key,
        habits_init_add_habit_text,
        habits_init_del_habit_text,
        habits_init_track_frequency_key,
        habits_init_habit_key,
        habits_init_question_key,
        habits_init_message_key,
        habits_init_condition_key,
        habits_init_fraction_num_key,
        habits_init_fraction_den_key,
        category_count,
        values_dict,
        habit_count,
    )
    previous_windows.close()
    new_window = HabitsInitWindow(variables_init_layout)
    return new_window

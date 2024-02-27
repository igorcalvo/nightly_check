import PySimpleGUI as sg

from source.constants import (
    COLORS,
    FONTS,
    MESSAGES,
    HABITS_INIT,
    habit_init_width,
    height_coefficient,
)
from source.core.theme import THEME_PROPS
from source.utils import (
    flatten_list_1,
    pad_string,
    safe_value_from_dict,
    safe_bool_from_array,
    safe_value_from_array,
    habit_init_key,
)
from source.ui.utils import show_habit_init_scroll_bar, get_paths

ICON_PATHS = get_paths()


def HabitInitHabitLayout(
    row_in_habit_count: int,
    category_row: int,
    values_dict: dict,
    padding_x: int,
):
    padding_text = 10
    layout = [
        sg.Text(
            text=HABITS_INIT.label_habit,
            text_color=COLORS[THEME_PROPS.BUTTON][1],
            background_color=COLORS[THEME_PROPS.BACKGROUND],
            font=FONTS["pop"],
            pad=((2 * padding_x, 0), (0, 0)),
        ),
        sg.InputText(
            key=habit_init_key(HABITS_INIT.habit_key, category_row, row_in_habit_count),
            background_color=COLORS[THEME_PROPS.INPUT],
            text_color=COLORS[THEME_PROPS.TEXT_INPUT],
            size=20,
            pad=(10, 0),
            tooltip=MESSAGES.input_tooltip_habit,
            default_text=safe_value_from_dict(  # type: ignore
                habit_init_key(HABITS_INIT.habit_key, category_row, row_in_habit_count),
                values_dict,
            ),
        ),
        sg.Text(
            text=HABITS_INIT.label_habit_question,
            text_color=COLORS[THEME_PROPS.BUTTON][1],
            background_color=COLORS[THEME_PROPS.BACKGROUND],
            font=FONTS["pop"],
            pad=((padding_x, 0), (0, 0)),
        ),
        sg.InputText(
            key=habit_init_key(
                HABITS_INIT.question_key, category_row, row_in_habit_count
            ),
            background_color=COLORS[THEME_PROPS.INPUT],
            text_color=COLORS[THEME_PROPS.TEXT_INPUT],
            size=30,
            tooltip=MESSAGES.input_tooltip_question,
            default_text=safe_value_from_dict(  # type: ignore
                habit_init_key(
                    HABITS_INIT.question_key, category_row, row_in_habit_count
                ),
                values_dict,
            ),
        ),
        sg.VerticalSeparator(color=COLORS[THEME_PROPS.BUTTON][0]),
        sg.Checkbox(
            text=MESSAGES.input_tooltip_track,
            default=bool(
                safe_value_from_dict(
                    habit_init_key(
                        HABITS_INIT.track_frequency_key,
                        category_row,
                        row_in_habit_count,
                    ),
                    values_dict,
                )
            ),
            key=habit_init_key(
                HABITS_INIT.track_frequency_key, category_row, row_in_habit_count
            ),
            size=16,
            font=FONTS["btn"],
            checkbox_color=COLORS[THEME_PROPS.BUTTON][0],
            text_color=COLORS[THEME_PROPS.BUTTON][1],
            background_color=COLORS[THEME_PROPS.BACKGROUND],
            pad=5,
            tooltip=MESSAGES.input_tooltip_checkbox,
            enable_events=True,
        ),
        sg.Text(
            text=HABITS_INIT.label_message,
            text_color=COLORS[THEME_PROPS.BUTTON][1],
            background_color=COLORS[THEME_PROPS.BACKGROUND],
            font=FONTS["pop"],
            pad=((padding_text // 3, 0), (0, 0)),
            visible=bool(
                safe_value_from_dict(
                    habit_init_key(
                        HABITS_INIT.track_frequency_key,
                        category_row,
                        row_in_habit_count,
                    ),
                    values_dict,
                )
            ),
        ),
        sg.InputText(
            key=habit_init_key(
                HABITS_INIT.message_key, category_row, row_in_habit_count
            ),
            background_color=COLORS[THEME_PROPS.INPUT],
            text_color=COLORS[THEME_PROPS.TEXT_INPUT],
            size=60,
            pad=((padding_text, 0), (0, 0)),
            tooltip=MESSAGES.input_tooltip_message,
            default_text=safe_value_from_dict(habit_init_key(HABITS_INIT.message_key, category_row, row_in_habit_count), values_dict),  # type: ignore
            visible=bool(
                safe_value_from_dict(
                    habit_init_key(
                        HABITS_INIT.track_frequency_key,
                        category_row,
                        row_in_habit_count,
                    ),
                    values_dict,
                )
            ),
        ),
        sg.Text(
            text=HABITS_INIT.label_direction,
            text_color=COLORS[THEME_PROPS.BUTTON][1],
            background_color=COLORS[THEME_PROPS.BACKGROUND],
            font=FONTS["pop"],
            pad=((padding_text, 0), (0, 0)),
            visible=bool(
                safe_value_from_dict(
                    habit_init_key(
                        HABITS_INIT.track_frequency_key,
                        category_row,
                        row_in_habit_count,
                    ),
                    values_dict,
                )
            ),
        ),
        sg.Combo(
            values=["   >", "  >=", "  <=", "   <"],
            default_value=safe_value_from_dict(
                habit_init_key(
                    HABITS_INIT.condition_key, category_row, row_in_habit_count
                ),
                values_dict,
            ),
            key=habit_init_key(
                HABITS_INIT.condition_key, category_row, row_in_habit_count
            ),
            size=3,
            pad=((padding_text // 2, 0), (0, 0)),
            auto_size_text=True,
            background_color=COLORS[THEME_PROPS.INPUT],
            text_color=COLORS[THEME_PROPS.BUTTON][1],
            button_background_color=COLORS[THEME_PROPS.BUTTON][0],
            button_arrow_color=COLORS[THEME_PROPS.BUTTON][1],
            font=FONTS["pop"],
            change_submits=True,
            enable_events=True,
            tooltip=MESSAGES.input_tooltip_combo,
            visible=bool(
                safe_value_from_dict(
                    habit_init_key(
                        HABITS_INIT.track_frequency_key,
                        category_row,
                        row_in_habit_count,
                    ),
                    values_dict,
                )
            ),
        ),
        sg.InputText(
            key=habit_init_key(
                HABITS_INIT.fraction_num_key, category_row, row_in_habit_count
            ),
            background_color=COLORS[THEME_PROPS.INPUT],
            text_color=COLORS[THEME_PROPS.TEXT_INPUT],
            size=3,
            default_text=safe_value_from_dict(habit_init_key(HABITS_INIT.fraction_num_key, category_row, row_in_habit_count), values_dict),  # type: ignore
            justification="r",
            pad=((padding_text, 0), (0, 0)),
            visible=bool(
                safe_value_from_dict(
                    habit_init_key(
                        HABITS_INIT.track_frequency_key,
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
            background_color=COLORS[THEME_PROPS.BACKGROUND],
            text_color=COLORS[THEME_PROPS.BUTTON][1],
            font=FONTS["pop"],
            visible=bool(
                safe_value_from_dict(
                    habit_init_key(
                        HABITS_INIT.track_frequency_key,
                        category_row,
                        row_in_habit_count,
                    ),
                    values_dict,
                )
            ),
        ),
        sg.InputText(
            key=habit_init_key(
                HABITS_INIT.fraction_den_key, category_row, row_in_habit_count
            ),
            background_color=COLORS[THEME_PROPS.INPUT],
            text_color=COLORS[THEME_PROPS.TEXT_INPUT],
            size=3,
            default_text=safe_value_from_dict(habit_init_key(HABITS_INIT.fraction_den_key, category_row, row_in_habit_count), values_dict),  # type: ignore
            justification="r",
            visible=bool(
                safe_value_from_dict(
                    habit_init_key(
                        HABITS_INIT.track_frequency_key,
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
            background_color=COLORS[THEME_PROPS.BACKGROUND],
            text_color=COLORS[THEME_PROPS.BUTTON][1],
            font=FONTS["pop"],
            visible=bool(
                safe_value_from_dict(
                    habit_init_key(
                        HABITS_INIT.track_frequency_key,
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
    values_dict: dict,
    habit_count: list,
):
    padding_x = 25
    button_size = 15

    layout = []
    for row in range(1, category_count + 1):
        category = [
            [sg.HorizontalSeparator(color=COLORS[THEME_PROPS.BUTTON][0])],
            [
                sg.Text(
                    text=HABITS_INIT.label_category,
                    text_color=COLORS[THEME_PROPS.BUTTON][1],
                    background_color=COLORS[THEME_PROPS.BACKGROUND],
                    font=FONTS["pop"],
                    pad=((padding_x, 0), (0, 0)),
                ),
                sg.InputText(
                    key=habit_init_key(HABITS_INIT.category_key, row),
                    # background_color=COLORS[THEME_PROPS.BUTTON][1],
                    background_color=COLORS[THEME_PROPS.INPUT],
                    text_color=COLORS[THEME_PROPS.TEXT_INPUT],
                    size=20,
                    pad=10,
                    tooltip=MESSAGES.input_tooltip_category,
                    default_text=safe_value_from_dict(  # type: ignore
                        habit_init_key(HABITS_INIT.category_key, row), values_dict
                    ),
                ),
                sg.Button(
                    button_text=HABITS_INIT.add_habit_text,
                    key=habit_init_key(HABITS_INIT.add_habit_text, row),
                    font=FONTS["btn"],
                    size=button_size,
                    button_color=(
                        COLORS[THEME_PROPS.BUTTON][0],
                        COLORS[THEME_PROPS.BUTTON][1],
                    ),
                    pad=(padding_x, 0),
                ),
                sg.Button(
                    button_text=HABITS_INIT.del_habit_text,
                    key=habit_init_key(HABITS_INIT.del_habit_text, row),
                    font=FONTS["btn"],
                    size=button_size,
                    button_color=(
                        COLORS[THEME_PROPS.BUTTON][0],
                        COLORS[THEME_PROPS.BUTTON][1],
                    ),
                    pad=((0, padding_x), (0, 0)),
                    disabled=safe_bool_from_array(row - 1, habit_count),
                ),
            ],
        ]
        for habit in range(safe_value_from_array(row - 1, habit_count, 0)):
            habit_row = HabitInitHabitLayout(habit, row, values_dict, padding_x)
            category.append(habit_row)
        layout.append(category)
    return layout


def HabitsInitLayout(
    category_count: int,
    values_dict: dict,
    habit_count: list,
):
    button_padding = 25
    button_font_size = (15, 2)
    show_scroll_bar = show_habit_init_scroll_bar(category_count, habit_count)
    category_layout = HabitInitCategoryLayout(
        category_count,
        values_dict,
        habit_count,
    )
    layout = [
        [
            sg.Column(
                flatten_list_1(category_layout),
                scrollable=show_scroll_bar,
                vertical_scroll_only=show_scroll_bar,
                background_color=COLORS[THEME_PROPS.BACKGROUND],
                visible=category_count > 0,
                size=(
                    (None, None)
                    if not show_habit_init_scroll_bar(category_count, habit_count)
                    else (habit_init_width, round(height_coefficient * 1080))
                ),
            )
        ],
        [sg.HorizontalSeparator(color=COLORS[THEME_PROPS.BUTTON][0])],
        [
            sg.Push(background_color=COLORS[THEME_PROPS.BACKGROUND]),
            sg.Button(
                HABITS_INIT.cat_add,
                font=FONTS["btn"],
                size=button_font_size,
                button_color=(
                    COLORS[THEME_PROPS.BUTTON][0],
                    COLORS[THEME_PROPS.BUTTON][1],
                ),
                pad=button_padding,
            ),
            sg.Button(
                HABITS_INIT.cat_remove,
                font=FONTS["btn"],
                size=button_font_size,
                button_color=(
                    COLORS[THEME_PROPS.BUTTON][0],
                    COLORS[THEME_PROPS.BUTTON][1],
                ),
                pad=((0, button_padding), (0, 0)),
                disabled=category_count < 1,
            ),
            sg.Button(
                HABITS_INIT.generate_text,
                font=FONTS["btn"],
                size=button_font_size,
                button_color=(
                    COLORS[THEME_PROPS.BUTTON][0],
                    COLORS[THEME_PROPS.BUTTON][1],
                ),
                pad=((0, button_padding), (0, 0)),
            ),
            sg.Push(background_color=COLORS[THEME_PROPS.BACKGROUND]),
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
        titlebar_background_color=COLORS[THEME_PROPS.BUTTON][0],
        titlebar_text_color=COLORS[THEME_PROPS.BUTTON][1],
        titlebar_icon=ICON_PATHS.init_icon,
        background_color=COLORS[THEME_PROPS.BACKGROUND],
        relative_location=(0, 0),
        element_justification="l",
    ).Finalize()


def ReRenderHabitsInit(
    previous_windows: sg.Window,
    category_count: int,
    values_dict: dict,
    habit_count: list,
) -> sg.Window:
    variables_init_layout = HabitsInitLayout(
        category_count,
        values_dict,
        habit_count,
    )
    previous_windows.close()
    new_window = HabitsInitWindow(variables_init_layout)
    return new_window

import PySimpleGUI as sg

from source.constants import (
    habit_init_width,
    height_coefficient,
    COLORS,
    FONTS,
    HABITS_INIT,
    MESSAGES,
)
from source.core.theme import THEME_PROPS
from source.ui.utils import get_paths, show_habit_init_scroll_bar
from source.utils import (
    enabled_checkbox_default_value,
    flatten_list_1,
    habit_init_key,
    pad_string,
    safe_bool_from_array,
    safe_value_from_array,
    safe_value_from_dict,
)

ICON_PATHS = get_paths()


def HabitInitHabitLayout(
    row_in_habit_count: int,
    category_row: int,
    values_dict: dict,
    padding_x: int,
    file_exists: bool,
):
    padding_text = 10
    layout = [
        sg.Checkbox(
            text="",
            key=habit_init_key(
                HABITS_INIT.enabled_key, category_row, row_in_habit_count
            ),
            size=1,
            default=enabled_checkbox_default_value(safe_value_from_dict(habit_init_key(HABITS_INIT.enabled_key, category_row, row_in_habit_count), values_dict)),  # type: ignore
            checkbox_color=COLORS[THEME_PROPS.BUTTON][0],
            background_color=COLORS[THEME_PROPS.BACKGROUND],
            pad=((padding_text, 0), (0, 0)),
            tooltip=MESSAGES.settings_tooltip_enabled,
            enable_events=True,
            visible=file_exists,
        ),
        sg.Text(
            text=HABITS_INIT.label_habit,
            text_color=COLORS[THEME_PROPS.BUTTON][1],
            background_color=COLORS[THEME_PROPS.BACKGROUND],
            font=FONTS["pop"],
            pad=((padding_x // 2, 0), (0, 0)),
        ),
        sg.InputText(
            key=habit_init_key(HABITS_INIT.habit_key, category_row, row_in_habit_count),
            background_color=COLORS[THEME_PROPS.INPUT],
            text_color=COLORS[THEME_PROPS.TEXT_INPUT],
            size=20,
            pad=(10, 0),
            font=FONTS["pop"],
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
            pad=((padding_x // 2, 0), (0, 0)),
        ),
        sg.InputText(
            key=habit_init_key(
                HABITS_INIT.question_key, category_row, row_in_habit_count
            ),
            background_color=COLORS[THEME_PROPS.INPUT],
            text_color=COLORS[THEME_PROPS.TEXT_INPUT],
            size=35,
            font=FONTS["pop"],
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
            text="",
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
            size=0,
            font=FONTS["btn"],
            checkbox_color=COLORS[THEME_PROPS.BUTTON][0],
            text_color=COLORS[THEME_PROPS.BUTTON][1],
            background_color=COLORS[THEME_PROPS.BACKGROUND],
            pad=((5, 5), (0, 0)),
            tooltip=MESSAGES.input_tooltip_checkbox,
            enable_events=True,
        ),
        sg.InputText(
            key=habit_init_key(
                HABITS_INIT.message_key, category_row, row_in_habit_count
            ),
            background_color=COLORS[THEME_PROPS.INPUT],
            text_color=COLORS[THEME_PROPS.TEXT_INPUT],
            size=80,
            font=FONTS["pop"],
            pad=((padding_text + 5, 0), (0, 0)),
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
            font=FONTS["cat"],
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
            font=FONTS["pop"],
            default_text=safe_value_from_dict(habit_init_key(HABITS_INIT.fraction_num_key, category_row, row_in_habit_count), values_dict),  # type: ignore
            justification="c",
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
            font=FONTS["pop"],
            default_text=safe_value_from_dict(habit_init_key(HABITS_INIT.fraction_den_key, category_row, row_in_habit_count), values_dict),  # type: ignore
            justification="c",
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
    values_dict: dict, habit_count: list[int], file_exists: bool
):
    padding_x = 25
    button_size = 12
    padding_text = 30

    layout = []
    for row in range(1, len(habit_count) + 1):
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
                    size=16,
                    font=FONTS["cat"],
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
                    pad=((5 * padding_x, 0), (0, 0)),
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
                    pad=((padding_x, 0), (0, 0)),
                    disabled=safe_bool_from_array(row - 1, habit_count),
                ),
                sg.Text(
                    text=MESSAGES.input_tooltip_track,
                    text_color=COLORS[THEME_PROPS.BUTTON][1],
                    background_color=COLORS[THEME_PROPS.BACKGROUND],
                    font=FONTS["pop"],
                    pad=((padding_text // 2, 0), (0, 0)),
                    visible=True,
                    tooltip=MESSAGES.input_tooltip_checkbox,
                ),
                sg.Text(
                    text=HABITS_INIT.label_message,
                    text_color=COLORS[THEME_PROPS.BUTTON][1],
                    background_color=COLORS[THEME_PROPS.BACKGROUND],
                    font=FONTS["pop"],
                    pad=((0, 0), (0, 0)),
                    visible=True,
                    tooltip=MESSAGES.input_tooltip_message,
                ),
            ],
        ]
        for habit in range(safe_value_from_array(row - 1, habit_count, 0)):
            habit_row = HabitInitHabitLayout(
                habit, row, values_dict, padding_x, file_exists
            )
            category.append(habit_row)
        layout.append(category)
    return layout


def HabitsInitLayout(values_dict: dict, habit_count: list[int], file_exists: bool):
    category_count = len(habit_count)
    button_padding = 25
    button_size = (15, 2)
    load_data_button_size = (30, 1)
    show_scroll_bar = show_habit_init_scroll_bar(category_count, habit_count)
    category_layout = HabitInitCategoryLayout(
        values_dict,
        habit_count,
        file_exists,
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
                size=button_size,
                button_color=(
                    COLORS[THEME_PROPS.BUTTON][0],
                    COLORS[THEME_PROPS.BUTTON][1],
                ),
                pad=button_padding,
            ),
            sg.Button(
                HABITS_INIT.cat_remove,
                font=FONTS["btn"],
                size=button_size,
                button_color=(
                    COLORS[THEME_PROPS.BUTTON][0],
                    COLORS[THEME_PROPS.BUTTON][1],
                ),
                pad=((0, button_padding), (0, 0)),
                disabled=category_count < 1,
            ),
            sg.Button(
                button_text=(
                    HABITS_INIT.generate_text_alt
                    if file_exists
                    else HABITS_INIT.generate_text
                ),
                key=HABITS_INIT.generate_text,
                font=FONTS["btn"],
                size=button_size,
                button_color=(
                    COLORS[THEME_PROPS.BUTTON][0],
                    COLORS[THEME_PROPS.BUTTON][1],
                ),
                pad=((0, button_padding), (0, 0)),
            ),
            sg.Push(background_color=COLORS[THEME_PROPS.BACKGROUND]),
        ],
        [
            sg.Push(background_color=COLORS[THEME_PROPS.BACKGROUND]),
            sg.Button(
                HABITS_INIT.load_file_text,
                key=HABITS_INIT.load_file_key,
                font=FONTS["btn"],
                size=load_data_button_size,
                button_color=(
                    COLORS[THEME_PROPS.BUTTON][0],
                    COLORS[THEME_PROPS.BUTTON][1],
                ),
                pad=((0, 0), (0, button_padding)),
                visible=file_exists,
            ),
            sg.Push(background_color=COLORS[THEME_PROPS.BACKGROUND]),
        ],
    ]
    return layout
    # https://stackoverflow.com/questions/66351957/how-to-add-a-field-or-element-by-clicking-a-button-in-pysimplegui
    # https://github.com/PySimpleGUI/PySimpleGUI/issues/845


def HabitsInitWindow(layout: list[list]) -> sg.Window:
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
        finalize=True,
    )


def ReRenderHabitsInit(
    previous_windows: sg.Window,
    values_dict: dict,
    habit_count: list[int],
    file_exists: bool,
) -> sg.Window:
    variables_init_layout = HabitsInitLayout(values_dict, habit_count, file_exists)
    previous_windows.close()
    new_window = HabitsInitWindow(variables_init_layout)
    return new_window

import PySimpleGUI as sg
from PIL import Image

from source.constants import COLORS, FONTS, MESSAGES, TEXTS_AND_KEYS
from source.core.data_in import get_matrix_data_by_header_indexes
from source.core.data_vis import image_bytes_to_base64
from source.core.theme import THEME_PROPS
from source.ui.utils import get_paths
from source.utils import date_ymd_to_mdy, flatten_and_wrap, pad_string

ICON_PATHS = get_paths()


def CreateMainLayout(
    categories: list[str],
    habits: list[list[str]],
    descriptions: list[list[str]],
    csv_not_empty: bool,
    is_sub_window: bool,
    default_values: list,
) -> list:
    max_cat_habits_count = max([len(cat) for cat in habits])
    category_padding = ((20, 0), (10, 0))
    checkbox_padding = ((15, 0), (1, 1))
    checkbox_padlast = ((15, 15), (1, 1))

    columns = [
        sg.Column(
            flatten_and_wrap(
                [
                    [
                        sg.Text(
                            cat.upper(),
                            text_color=COLORS[THEME_PROPS.CATEGORY],
                            background_color=COLORS[THEME_PROPS.BACKGROUND],
                            pad=category_padding,
                            font=FONTS["cat"],
                        )
                    ],
                    list(
                        [
                            sg.Checkbox(
                                text=" " + item,
                                default=(
                                    False
                                    if len(default_values) == 0
                                    else bool(
                                        get_matrix_data_by_header_indexes(
                                            default_values, habits, item
                                        )
                                    )
                                ),
                                key=item,
                                font=FONTS["ckb"],
                                checkbox_color=COLORS[THEME_PROPS.BUTTON][0],
                                text_color=COLORS[THEME_PROPS.BUTTON][1],
                                background_color=COLORS[THEME_PROPS.BACKGROUND],
                                pad=(
                                    checkbox_padlast
                                    if idx_cat == int(len(categories) - 1)
                                    else checkbox_padding
                                ),
                                tooltip=get_matrix_data_by_header_indexes(
                                    descriptions, habits, item
                                ),
                            )
                        ]
                        for item in habits[idx_cat]
                    ),
                    list(
                        [
                            sg.Text(
                                text=" ",
                                font=FONTS["ckb"],
                                text_color=COLORS[THEME_PROPS.BACKGROUND],
                                background_color=COLORS[THEME_PROPS.BACKGROUND],
                                pad=checkbox_padding,
                            )
                        ]
                        for i in range(max_cat_habits_count - len(habits[idx_cat]))
                    ),
                ]
            ),
            background_color=COLORS[THEME_PROPS.BACKGROUND],
            justification="l",
        )
        for idx_cat, cat in enumerate(categories)
    ]

    buttons_layout = [
        sg.Button(
            TEXTS_AND_KEYS.settings_button_text,
            font=FONTS["btn"],
            size=7,
            button_color=(COLORS[THEME_PROPS.BUTTON][0], COLORS[THEME_PROPS.BUTTON][1]),
            pad=(25, (5, 15)),
            tooltip=MESSAGES.settings_button_tooltip,
        ),
        sg.Push(background_color=COLORS[THEME_PROPS.BACKGROUND]),
        sg.Button(
            TEXTS_AND_KEYS.data_button_text,
            font=FONTS["btn"],
            size=7,
            disabled=not csv_not_empty,
            button_color=(COLORS[THEME_PROPS.BUTTON][0], COLORS[THEME_PROPS.BUTTON][1]),
            pad=(0, (5, 15)),
            tooltip=MESSAGES.data_button_tooltip,
        ),
        sg.Push(background_color=COLORS[THEME_PROPS.BACKGROUND]),
        sg.Button(
            TEXTS_AND_KEYS.edit_button_text,
            font=FONTS["btn"],
            size=7,
            disabled=not csv_not_empty,
            button_color=(COLORS[THEME_PROPS.BUTTON][0], COLORS[THEME_PROPS.BUTTON][1]),
            pad=(0, (5, 15)),
            tooltip=MESSAGES.edit_button_tooltip,
        ),
    ]

    done_button_layout = [
        sg.Push(background_color=COLORS[THEME_PROPS.BACKGROUND]),
        sg.Button(
            TEXTS_AND_KEYS.done_button_text,
            font=FONTS["btn"],
            size=7,
            button_color=(COLORS[THEME_PROPS.BUTTON][0], COLORS[THEME_PROPS.BUTTON][1]),
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


def MainWindow(
    categories: list[str],
    habits: list[list[str]],
    descriptions: list[list[str]],
    csv_not_empty: bool,
    is_sub_window: bool,
    default_values: list[list] = [],
):
    layout = CreateMainLayout(
        categories,
        habits,
        descriptions,
        csv_not_empty,
        is_sub_window,
        default_values,
    )
    return sg.Window(
        title=MESSAGES.app_title,
        layout=layout,
        use_custom_titlebar=True,
        titlebar_background_color=COLORS[THEME_PROPS.BUTTON][0],
        titlebar_text_color=COLORS[THEME_PROPS.BUTTON][1],
        titlebar_icon=ICON_PATHS.colored_icon,
        background_color=COLORS[THEME_PROPS.BACKGROUND],
        element_justification="l",
    )


def IconWindow(message: str, message_duration: int):
    img = Image.open(ICON_PATHS.colored_msg_icon)
    base64_img = image_bytes_to_base64(img)
    layout = [
        [
            sg.Column(
                [
                    [
                        sg.Image(
                            data=base64_img,
                            background_color=COLORS[THEME_PROPS.BUTTON][1],
                        )
                    ]
                ],
                background_color=COLORS[THEME_PROPS.BUTTON][1],
            ),
            sg.Column(
                [
                    [
                        sg.Text(
                            text=message,
                            text_color=COLORS[THEME_PROPS.BUTTON][0],
                            background_color=COLORS[THEME_PROPS.BUTTON][1],
                            font=FONTS["pop"],
                        )
                    ]
                ],
                background_color=COLORS[THEME_PROPS.BUTTON][1],
            ),
        ]
    ]

    window = sg.Window(
        title="",
        background_color=COLORS[THEME_PROPS.BUTTON][1],
        no_titlebar=True,
        layout=layout,
        auto_close_duration=message_duration,
        auto_close=True,
        finalize=True,
    )
    window.read()
    window.TKroot.after(
        int(message_duration * 1000),
        lambda win=window: win.write_event_value(sg.WINDOW_CLOSED, None),
    )
    window.close()


def PopUp(message: str, message_duration: int, show_icon: bool):
    if show_icon:
        IconWindow(message, message_duration)
    else:
        sg.PopupNoButtons(
            message,
            keep_on_top=True,
            auto_close=True,
            auto_close_duration=message_duration,
            background_color=COLORS[THEME_PROPS.BUTTON][1],
            text_color=COLORS[THEME_PROPS.BUTTON][0],
            no_titlebar=True,
            font=FONTS["pop"],
            line_width=len(message),
            image=ICON_PATHS.colored_msg_icon,
        )


def NeglectedPopUp() -> sg.Window:
    layout = [
        [
            sg.Text(
                MESSAGES.neglected,
                text_color=COLORS[THEME_PROPS.BUTTON][1],
                background_color=COLORS[THEME_PROPS.BUTTON][0],
                pad=((15, 15), (10, 10)),
                font=FONTS["pop"],
            )
        ],
        [
            sg.Button(
                TEXTS_AND_KEYS.neglected_accept_text,
                font=FONTS["btn"],
                size=7,
                key=TEXTS_AND_KEYS.neglected_accept_text,
                pad=((15, 0), (15, 15)),
                button_color=(
                    COLORS[THEME_PROPS.BUTTON][1],
                    COLORS[THEME_PROPS.BUTTON][0],
                ),
            ),
            sg.Text(
                pad_string("", 29),
                text_color=COLORS[THEME_PROPS.BUTTON][1],
                background_color=COLORS[THEME_PROPS.BUTTON][0],
                font=FONTS["pop"],
            ),
            sg.Button(
                TEXTS_AND_KEYS.neglected_reject_text,
                font=FONTS["btn"],
                size=7,
                key=TEXTS_AND_KEYS.neglected_reject_text,
                pad=((0, 15), (15, 15)),
                button_color=(
                    COLORS[THEME_PROPS.BUTTON][1],
                    COLORS[THEME_PROPS.BUTTON][0],
                ),
            ),
        ],
    ]
    return sg.Window(
        MESSAGES.neglected_title,
        layout,
        return_keyboard_events=True,
        use_custom_titlebar=True,
        titlebar_background_color=COLORS[THEME_PROPS.BUTTON][0],
        titlebar_text_color=COLORS[THEME_PROPS.BUTTON][1],
        titlebar_icon=ICON_PATHS.yesterday_icon,
        background_color=COLORS[THEME_PROPS.BUTTON][0],
        relative_location=(0, 0),
        element_justification="c",
        finalize=True,
    )


def DatePickerWindow(yesterdays_date: str) -> sg.Window:
    layout = [
        [
            sg.Text(
                text=MESSAGES.date_text,
                text_color=COLORS[THEME_PROPS.BUTTON][1],
                background_color=COLORS[THEME_PROPS.BUTTON][0],
                font=FONTS["pop"],
            )
        ],
        [
            sg.InputText(
                key=TEXTS_AND_KEYS.select_date_key,
                default_text=yesterdays_date,
                size=20,
                background_color=COLORS[THEME_PROPS.INPUT],
                text_color=COLORS[THEME_PROPS.TEXT_INPUT],
                # background_color=COLORS[THEME_PROPS.BUTTON][0],
                # text_color="#ffffff",
            ),
            sg.CalendarButton(
                MESSAGES.date_calendar,
                close_when_date_chosen=True,
                target=TEXTS_AND_KEYS.select_date_key,
                format="%Y-%m-%d",
                size=15,
                button_color=(
                    COLORS[THEME_PROPS.BUTTON][1],
                    COLORS[THEME_PROPS.BUTTON][0],
                ),
                default_date_m_d_y=date_ymd_to_mdy(yesterdays_date),
            ),
            sg.Button(
                TEXTS_AND_KEYS.select_date_button_text,
                font=FONTS["btn"],
                size=7,
                key=TEXTS_AND_KEYS.select_date_button_text,
                button_color=(
                    COLORS[THEME_PROPS.BUTTON][1],
                    COLORS[THEME_PROPS.BUTTON][0],
                ),
            ),
        ],
    ]
    return sg.Window(
        MESSAGES.date_calendar,
        layout,
        return_keyboard_events=True,
        use_custom_titlebar=True,
        titlebar_background_color=COLORS[THEME_PROPS.BUTTON][0],
        titlebar_text_color=COLORS[THEME_PROPS.BUTTON][1],
        titlebar_icon=ICON_PATHS.yesterday_icon,
        background_color=COLORS[THEME_PROPS.BUTTON][0],
        relative_location=(0, 0),
        element_justification="c",
        finalize=True,
    )

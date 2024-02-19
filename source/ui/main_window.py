import PySimpleGUI as sg

from source.constants import COLORS, FONTS, MESSAGES, PATHS, TEXTS_AND_KEYS
from source.utils import flatten_and_wrap, pad_string
from source.core.data_in import get_matrix_data_by_header_indexes

PATH = PATHS()
PATH.__init__()


def CreateMainLayout(
    categories: list,
    headers: list,
    descriptions: list,
    csv_not_empty: bool,
    is_sub_window: bool,
    default_values: list,
) -> list:
    max_cat_header_count = max([len(cat) for cat in headers])
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
                            text_color=COLORS["cat_txt"],
                            background_color=COLORS["win_bkg"],
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
                                            default_values, headers, item
                                        )
                                    )
                                ),
                                key=item,
                                font=FONTS["ckb"],
                                checkbox_color=COLORS["bar_bkg"],
                                text_color=COLORS["bar_txt"],
                                background_color=COLORS["win_bkg"],
                                pad=(
                                    checkbox_padlast
                                    if idx_cat == int(len(categories) - 1)
                                    else checkbox_padding
                                ),
                                tooltip=get_matrix_data_by_header_indexes(
                                    descriptions, headers, item
                                ),
                            )
                        ]
                        for item in headers[idx_cat]
                    ),
                    list(
                        [
                            sg.Text(
                                text=" ",
                                font=FONTS["ckb"],
                                text_color=COLORS["win_bkg"],
                                background_color=COLORS["win_bkg"],
                                pad=checkbox_padding,
                            )
                        ]
                        for i in range(max_cat_header_count - len(headers[idx_cat]))
                    ),
                ]
            ),
            background_color=COLORS["win_bkg"],
            justification="l",
        )
        for idx_cat, cat in enumerate(categories)
    ]

    buttons_layout = [
        sg.Button(
            TEXTS_AND_KEYS.settings_button_text,
            font=FONTS["btn"],
            size=7,
            button_color=(COLORS["bar_bkg"], COLORS["bar_txt"]),
            pad=(25, (5, 15)),
            tooltip=MESSAGES.settings_button_tooltip,
        ),
        sg.Push(background_color=COLORS["win_bkg"]),
        sg.Button(
            TEXTS_AND_KEYS.data_button_text,
            font=FONTS["btn"],
            size=7,
            disabled=not csv_not_empty,
            button_color=(COLORS["bar_bkg"], COLORS["bar_txt"]),
            pad=(0, (5, 15)),
            tooltip=MESSAGES.data_button_tooltip,
        ),
        sg.Push(background_color=COLORS["win_bkg"]),
        sg.Button(
            TEXTS_AND_KEYS.edit_button_text,
            font=FONTS["btn"],
            size=7,
            disabled=not csv_not_empty,
            button_color=(COLORS["bar_bkg"], COLORS["bar_txt"]),
            pad=(0, (5, 15)),
            tooltip=MESSAGES.edit_button_tooltip,
        ),
    ]

    done_button_layout = [
        sg.Push(background_color=COLORS["win_bkg"]),
        sg.Button(
            TEXTS_AND_KEYS.done_button_text,
            font=FONTS["btn"],
            size=7,
            button_color=(COLORS["bar_bkg"], COLORS["bar_txt"]),
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
    categories: list,
    header: list,
    descriptions: list,
    csv_not_empty: bool,
    is_sub_window: bool,
    default_values: list = [],
):
    layout = CreateMainLayout(
        categories,
        header,
        descriptions,
        csv_not_empty,
        is_sub_window,
        default_values,
    )
    return sg.Window(
        title=MESSAGES.app_title,
        layout=layout,
        use_custom_titlebar=True,
        titlebar_background_color=COLORS["bar_bkg"],
        titlebar_text_color=COLORS["bar_txt"],
        titlebar_icon=PATH.colored_icon,
        background_color=COLORS["win_bkg"],
        element_justification="l",
    )


def PopUp(message: str, message_duration: int):
    sg.PopupNoButtons(
        message,
        keep_on_top=True,
        auto_close=True,
        auto_close_duration=message_duration,
        background_color=COLORS["bar_txt"],
        text_color=COLORS["bar_bkg"],
        no_titlebar=True,
        font=FONTS["pop"],
        line_width=len(message),
    )


def NeglectedPopUp():
    layout = [
        [
            sg.Text(
                MESSAGES.neglected,
                text_color=COLORS["bar_txt"],
                background_color=COLORS["bar_bkg"],
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
                button_color=(COLORS["bar_txt"], COLORS["bar_bkg"]),
            ),
            sg.Text(
                pad_string("", 29),
                text_color=COLORS["bar_txt"],
                background_color=COLORS["bar_bkg"],
                font=FONTS["pop"],
            ),
            sg.Button(
                TEXTS_AND_KEYS.neglected_reject_text,
                font=FONTS["btn"],
                size=7,
                key=TEXTS_AND_KEYS.neglected_reject_text,
                pad=((0, 15), (15, 15)),
                button_color=(COLORS["bar_txt"], COLORS["bar_bkg"]),
            ),
        ],
    ]
    return sg.Window(
        MESSAGES.neglected_title,
        layout,
        return_keyboard_events=True,
        use_custom_titlebar=True,
        titlebar_background_color=COLORS["bar_bkg"],
        titlebar_text_color=COLORS["bar_txt"],
        titlebar_icon=PATH.yesterday_icon,
        background_color=COLORS["bar_bkg"],
        relative_location=(0, 0),
        element_justification="c",
    ).Finalize()


def DatePickerWindow():
    layout = [
        [
            sg.Text(
                text=MESSAGES.date_text,
                text_color=COLORS["bar_txt"],
                background_color=COLORS["bar_bkg"],
                font=FONTS["pop"],
            )
        ],
        [
            sg.InputText(
                key=TEXTS_AND_KEYS.select_date_key,
                background_color=COLORS["bar_bkg"],
                text_color="#ffffff",
                size=20,
            ),
            sg.CalendarButton(
                MESSAGES.date_calendar,
                close_when_date_chosen=True,
                target=TEXTS_AND_KEYS.select_date_key,
                format="%Y-%m-%d",
                size=15,
                button_color=(COLORS["bar_txt"], COLORS["bar_bkg"]),
            ),
            sg.Button(
                TEXTS_AND_KEYS.select_date_button_text,
                font=FONTS["btn"],
                size=7,
                key=TEXTS_AND_KEYS.select_date_button_text,
                button_color=(COLORS["bar_txt"], COLORS["bar_bkg"]),
            ),
        ],
    ]
    return sg.Window(
        MESSAGES.date_calendar,
        layout,
        return_keyboard_events=True,
        use_custom_titlebar=True,
        titlebar_background_color=COLORS["bar_bkg"],
        titlebar_text_color=COLORS["bar_txt"],
        titlebar_icon=PATH.yesterday_icon,
        background_color=COLORS["bar_bkg"],
        relative_location=(0, 0),
        element_justification="c",
    ).Finalize()

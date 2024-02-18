import PySimpleGUI as sg

from source.constants import COLORS, FONTS, MESSAGES, PATHS
from source.utils import flatten_and_wrap, pad_string
from source.core.data_in import get_matrix_data_by_header_indexes

PATH = PATHS()
PATH.__init__()


def CreateMainLayout(
    categories: list,
    headers: list,
    descriptions: list,
    done_button_text: str,
    data_button_text: str,
    edit_button_text: str,
    settings_button_text: str,
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
                            background_color=COLORS["cat_bkg"],
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
                                checkbox_color=COLORS["ckb_bkg"],
                                text_color=COLORS["ckb_txt"],
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
            background_color=COLORS["cat_bkg"],
            justification="l",
        )
        for idx_cat, cat in enumerate(categories)
    ]

    buttons_layout = [
        sg.Button(
            settings_button_text,
            font=FONTS["btn"],
            size=7,
            button_color=(COLORS["dnb_bkg"], COLORS["dnb_txt"]),
            pad=(25, (5, 15)),
            tooltip=MESSAGES.settings_button_tooltip,
        ),
        sg.Push(background_color=COLORS["win_bkg"]),
        sg.Button(
            data_button_text,
            font=FONTS["btn"],
            size=7,
            disabled=not csv_not_empty,
            button_color=(COLORS["dnb_bkg"], COLORS["dnb_txt"]),
            pad=(0, (5, 15)),
            tooltip=MESSAGES.data_button_tooltip,
        ),
        sg.Push(background_color=COLORS["win_bkg"]),
        sg.Button(
            edit_button_text,
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
        sg.Button(
            done_button_text,
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


def MainWindow(
    categories: list,
    header: list,
    descriptions: list,
    done_button_text: str,
    data_button_text: str,
    edit_button_text: str,
    settings_button_text: str,
    csv_not_empty: bool,
    is_sub_window: bool,
    default_values: list = [],
):
    layout = CreateMainLayout(
        categories,
        header,
        descriptions,
        done_button_text,
        data_button_text,
        edit_button_text,
        settings_button_text,
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
        background_color=COLORS["pop_bkg"],
        text_color=COLORS["pop_txt"],
        no_titlebar=True,
        font=FONTS["pop"],
        line_width=len(message),
    )


def NeglectedPopUp(accept_text: str, reject_text: str):
    layout = [
        [
            sg.Text(
                MESSAGES.neglected,
                text_color=COLORS["neg_txt"],
                background_color=COLORS["neg_bkg"],
                pad=((15, 15), (10, 10)),
                font=FONTS["pop"],
            )
        ],
        [
            sg.Button(
                accept_text,
                font=FONTS["btn"],
                size=7,
                key=accept_text,
                pad=((15, 0), (15, 15)),
                button_color=(COLORS["dnb_txt"], COLORS["dnb_bkg"]),
            ),
            sg.Text(
                pad_string("", 29),
                text_color=COLORS["neg_txt"],
                background_color=COLORS["neg_bkg"],
                font=FONTS["pop"],
            ),
            sg.Button(
                reject_text,
                font=FONTS["btn"],
                size=7,
                key=reject_text,
                pad=((0, 15), (15, 15)),
                button_color=(COLORS["dnb_txt"], COLORS["dnb_bkg"]),
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
        background_color=COLORS["neg_bkg"],
        relative_location=(0, 0),
        element_justification="c",
    ).Finalize()


def DatePickerWindow(select_date_key: str, select_date_button_text: str):
    layout = [
        [
            sg.Text(
                text=MESSAGES.date_text,
                text_color=COLORS["dtp_txt"],
                background_color=COLORS["dtp_bkg"],
                font=FONTS["pop"],
            )
        ],
        [
            sg.InputText(
                key=select_date_key,
                background_color=COLORS["dtp_bkg"],
                text_color="#ffffff",
                size=20,
            ),
            sg.CalendarButton(
                MESSAGES.date_calendar,
                close_when_date_chosen=True,
                target=select_date_key,
                format="%Y-%m-%d",
                size=15,
                button_color=(COLORS["dnb_txt"], COLORS["dnb_bkg"]),
            ),
            sg.Button(
                select_date_button_text,
                font=FONTS["btn"],
                size=7,
                key=select_date_button_text,
                button_color=(COLORS["dnb_txt"], COLORS["dnb_bkg"]),
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
        background_color=COLORS["dtp_bkg"],
        relative_location=(0, 0),
        element_justification="c",
    ).Finalize()

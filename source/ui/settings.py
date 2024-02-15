import PySimpleGUI as sg

from source.constants import COLORS, FONTS, MESSAGES, PATHS, SETTINGS_KEYS
from source.core import Settings
from source.utils import pad_string, settings_key_to_text
from source.ui.utils import apply_hue_offset

PATH = PATHS()
PATH.__init__()


def StyleWindow(
    style_button_text: str,
    slider_text_key: str,
    preview_window_text: str,
    set_button_text: str,
    hue_offset: float,
):
    return sg.Window(
        style_button_text,
        [
            [
                sg.Text(
                    pad_string(MESSAGES.hue, 0),
                    background_color=COLORS["sld_bkg"],
                    text_color=COLORS["sld_txt"],
                )
            ],
            [
                sg.Slider(
                    range=(-0.5, 0.5),
                    default_value=hue_offset,
                    resolution=0.001,
                    orientation="h",
                    enable_events=True,
                    key=slider_text_key,
                    text_color=COLORS["sld_txt"],
                    background_color=COLORS["sld_bkg"],
                    trough_color=COLORS["sld_sld"],
                    size=(50, 23),
                )
            ],
            [
                [
                    sg.Button(
                        preview_window_text,
                        font=FONTS["btn"],
                        size=7,
                        pad=((5, 0), (15, 15)),
                        key=preview_window_text,
                        button_color=(COLORS["dnb_bkg"], COLORS["dnb_txt"]),
                    ),
                    sg.Button(
                        set_button_text,
                        font=FONTS["btn"],
                        size=7,
                        pad=((322, 0), (15, 15)),
                        key=set_button_text,
                        button_color=(COLORS["dnb_bkg"], COLORS["dnb_txt"]),
                    ),
                ]
            ],
        ],
        return_keyboard_events=True,
        use_custom_titlebar=True,
        titlebar_background_color=COLORS["bar_bkg"],
        titlebar_text_color=COLORS["bar_txt"],
        titlebar_icon=PATH.style_icon,
        background_color=COLORS["sld_bkg"],
        relative_location=(-100, 0),
    ).Finalize()


def PreviewWindow(preview_window_text: str, preview_close_key: str, hue_offset: float):
    return sg.Window(
        preview_window_text,
        [
            [
                sg.Text(
                    pad_string(MESSAGES.preview_text.upper(), 27),
                    text_color=apply_hue_offset(COLORS["cat_txt"], hue_offset),
                    background_color=apply_hue_offset(COLORS["cat_bkg"], hue_offset),
                    pad=((15, 0), (10, 10)),
                    font=FONTS["cat"],
                )
            ],
            [
                sg.Checkbox(
                    text=pad_string(MESSAGES.preview_checkbox, 30),
                    default=False,
                    size=15,
                    font=FONTS["ckb"],
                    checkbox_color=apply_hue_offset(COLORS["ckb_bkg"], hue_offset),
                    text_color=apply_hue_offset(COLORS["ckb_txt"], hue_offset),
                    background_color=apply_hue_offset(COLORS["win_bkg"], hue_offset),
                    pad=((15, 0), (2, 2)),
                    tooltip=MESSAGES.preview_tooltip,
                )
            ],
            [
                sg.Button(
                    MESSAGES.preview_close,
                    font=FONTS["btn"],
                    size=7,
                    key=preview_close_key,
                    pad=((65, 0), (15, 15)),
                    button_color=(
                        apply_hue_offset(COLORS["dnb_bkg"], hue_offset),
                        apply_hue_offset(COLORS["dnb_txt"], hue_offset),
                    ),
                )
            ],
        ],
        return_keyboard_events=True,
        use_custom_titlebar=True,
        titlebar_background_color=apply_hue_offset(COLORS["bar_bkg"], hue_offset),
        titlebar_text_color=apply_hue_offset(COLORS["bar_txt"], hue_offset),
        titlebar_icon=PATHS.preview_icon,
        background_color=apply_hue_offset(COLORS["win_bkg"], hue_offset),
        relative_location=(240, 0),
    ).Finalize()


def SettingsWindowLayout(
    settings: Settings, settings_save_button_text: str, settings_cancel_button_text: str
) -> list:
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
            sg.Text(
                text=settings_key_to_text(SETTINGS_KEYS.hue_offset),
                text_color=COLORS["stg_txt"],
                background_color=COLORS["stg_bkg"],
                font=FONTS["pop"],
            ),
            sg.InputText(
                key=SETTINGS_KEYS.hue_offset,
                do_not_clear=True,
                enable_events=True,
                visible=True,
                font=FONTS["ckb"],
                tooltip=MESSAGES.settings_tooltip_hueoffset,
                default_text=str(settings.hue_offset),
                size=text_input_size,
                justification="r",
            ),
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
            sg.InputText(
                key=SETTINGS_KEYS.data_days,
                do_not_clear=True,
                enable_events=True,
                visible=True,
                font=FONTS["ckb"],
                tooltip=MESSAGES.settings_tooltip_days,
                default_text=str(settings.data_days),
                size=text_input_size,
                justification="r",
            ),
            sg.Text(
                text=pad_string("", 5),
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
            sg.Combo(
                values=["en", "pt", "jp"],
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
                text=pad_string("", 2),
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
            sg.Checkbox(
                text="",
                default=bool(settings.graph_expected_value),
                key=SETTINGS_KEYS.graph_expected_value,
                font=FONTS["pop"],
                checkbox_color=COLORS["ckb_bkg"],
                text_color=COLORS["ckb_txt"],
                background_color=COLORS["stg_bkg"],
                pad=((checkbox_padding, 0), (1, 1)),
                tooltip=MESSAGES.settings_tooltip_expected,
            ),
            sg.Text(
                text=pad_string("", 2),
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
            sg.Checkbox(
                text="",
                default=bool(settings.scrollable_image),
                key=SETTINGS_KEYS.scrollable_image,
                font=FONTS["pop"],
                checkbox_color=COLORS["ckb_bkg"],
                text_color=COLORS["ckb_txt"],
                background_color=COLORS["stg_bkg"],
                pad=((checkbox_padding, 0), (1, 1)),
                tooltip=MESSAGES.settings_tooltip_scrollable,
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
            sg.Checkbox(
                text="",
                default=bool(settings.display_messages),
                key=SETTINGS_KEYS.display_messages,
                font=FONTS["pop"],
                checkbox_color=COLORS["ckb_bkg"],
                text_color=COLORS["ckb_txt"],
                background_color=COLORS["stg_bkg"],
                pad=((checkbox_padding, 20), (1, 1)),
                tooltip=MESSAGES.settings_tooltip_messages_show,
            ),
            sg.Text(
                text=pad_string("", 3),
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
            sg.Checkbox(
                text="",
                default=bool(settings.random_messages),
                key=SETTINGS_KEYS.random_messages,
                font=FONTS["pop"],
                checkbox_color=COLORS["ckb_bkg"],
                text_color=COLORS["ckb_txt"],
                background_color=COLORS["stg_bkg"],
                pad=((checkbox_padding, 0), (1, 1)),
                tooltip=MESSAGES.settings_tooltip_random,
            ),
            sg.Text(
                text=pad_string("", 7),
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
            sg.InputText(
                key=SETTINGS_KEYS.message_duration,
                do_not_clear=True,
                enable_events=True,
                visible=True,
                font=FONTS["ckb"],
                tooltip=MESSAGES.settings_tooltip_duration,
                default_text=str(settings.message_duration),
                size=text_input_size,
                justification="r",
            ),
        ],
    ]

    buttons = [
        [
            sg.Text(
                text=pad_string("", 68),
                text_color=COLORS["stg_bkg"],
                background_color=COLORS["stg_bkg"],
                font=FONTS["ckb"],
            ),
            sg.Button(
                settings_cancel_button_text,
                font=FONTS["btn"],
                size=7,
                pad=((5, 0), (30, 15)),
                key=settings_cancel_button_text,
                button_color=(COLORS["dnb_bkg"], COLORS["dnb_txt"]),
            ),
            sg.Text(
                text=pad_string("", 5),
                text_color=COLORS["stg_bkg"],
                background_color=COLORS["stg_bkg"],
                font=FONTS["ckb"],
            ),
            sg.Button(
                settings_save_button_text,
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


def SettingsWindow(
    settings: Settings,
    settings_button_text: str,
    settings_save_button_text: str,
    settings_cancel_button_text: str,
):
    layout = SettingsWindowLayout(
        settings, settings_save_button_text, settings_cancel_button_text
    )
    return sg.Window(
        title=settings_button_text,
        layout=layout,
        use_custom_titlebar=True,
        titlebar_background_color=COLORS["bar_bkg"],
        titlebar_text_color=COLORS["bar_txt"],
        titlebar_icon=PATH.settings_icon,
        background_color=COLORS["stg_bkg"],
        size=(900, 360),
        element_justification="l",
    )

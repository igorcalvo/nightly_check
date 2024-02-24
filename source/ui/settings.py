import PySimpleGUI as sg

from source.constants import (
    COLORS,
    FONTS,
    MESSAGES,
    PATHS,
    SETTINGS_DEFAULT_VALUES,
    SETTINGS_KEYS,
    TEXTS_AND_KEYS,
)
from source.core.theme import THEME_PROPS
from source.utils import pad_string, settings_key_to_text
from source.core.settings import Settings
from source.ui.utils import init_ui

PATH = PATHS()
PATH.__init__()


def PreviewWindow(new_hue: float, theme: str):
    init_ui(new_hue, theme)

    return sg.Window(
        TEXTS_AND_KEYS.preview_window_text,
        [
            [
                sg.Text(
                    pad_string(MESSAGES.preview_text.upper(), 27),
                    text_color=COLORS[THEME_PROPS.CATEGORY],
                    background_color=COLORS[THEME_PROPS.BACKGROUND],
                    pad=((15, 0), (10, 10)),
                    font=FONTS["cat"],
                )
            ],
            [
                sg.Checkbox(
                    text=pad_string(MESSAGES.preview_checkbox, 30),
                    default=False,
                    size=30,
                    font=FONTS["ckb"],
                    checkbox_color=COLORS[THEME_PROPS.BUTTON][0],
                    text_color=COLORS[THEME_PROPS.BUTTON][1],
                    background_color=COLORS[THEME_PROPS.BACKGROUND],
                    pad=((15, 0), (2, 2)),
                    tooltip=MESSAGES.preview_tooltip,
                )
            ],
            [
                sg.Button(
                    MESSAGES.preview_close,
                    font=FONTS["btn"],
                    size=7,
                    key=TEXTS_AND_KEYS.preview_close_key,
                    pad=((65, 0), (15, 15)),
                    button_color=(
                        COLORS[THEME_PROPS.BUTTON][0],
                        COLORS[THEME_PROPS.BUTTON][1],
                    ),
                )
            ],
        ],
        return_keyboard_events=True,
        use_custom_titlebar=True,
        titlebar_background_color=COLORS[THEME_PROPS.BUTTON][0],
        titlebar_text_color=COLORS[THEME_PROPS.BUTTON][1],
        titlebar_icon=PATHS.preview_icon,
        background_color=COLORS[THEME_PROPS.BACKGROUND],
        relative_location=(250, 20),
        auto_close_duration=3,
        auto_close=True,
        force_toplevel=True,
    ).Finalize()


def SettingsWindowLayout(
    settings: Settings,
) -> list:
    checkbox_padding = 5
    sections_padding_y = 25
    sections_padding_x = 25
    text_input_size = 7

    available_themes = sg.list_of_look_and_feel_values()
    available_themes.append(SETTINGS_DEFAULT_VALUES.theme)
    available_themes = sorted(available_themes)

    appearance = [
        [
            sg.Text(
                text=MESSAGES.settings_section_appearance,
                text_color=COLORS[THEME_PROPS.CATEGORY],
                background_color=COLORS[THEME_PROPS.BACKGROUND],
                font=FONTS["cat"],
                pad=((sections_padding_x, 0), (sections_padding_y - 10, 5)),
            )
        ],
        [
            sg.Text(
                text=settings_key_to_text(SETTINGS_KEYS.hue_offset),
                text_color=COLORS[THEME_PROPS.BUTTON][1],
                background_color=COLORS[THEME_PROPS.BACKGROUND],
                font=FONTS["pop"],
                pad=((sections_padding_x, sections_padding_x), (0, 0)),
            ),
            sg.Slider(
                range=(-0.5, 0.5),
                default_value=settings.hue_offset,
                resolution=0.001,
                orientation="h",
                enable_events=True,
                key=SETTINGS_KEYS.hue_offset,
                text_color=COLORS[THEME_PROPS.CATEGORY],
                background_color=COLORS[THEME_PROPS.SCROLL],
                trough_color=COLORS[THEME_PROPS.BUTTON][1],
                size=(50, 23),
            ),
            sg.Button(
                TEXTS_AND_KEYS.preview_window_text,
                font=FONTS["btn"],
                size=(20, 2),
                pad=((3 * sections_padding_x - 15, sections_padding_x), (15, 15)),
                key=TEXTS_AND_KEYS.preview_window_text,
                button_color=(
                    COLORS[THEME_PROPS.BUTTON][0],
                    COLORS[THEME_PROPS.BUTTON][1],
                ),
            ),
        ],
        [
            sg.Text(
                text=settings_key_to_text(SETTINGS_KEYS.theme),
                text_color=COLORS[THEME_PROPS.BUTTON][1],
                background_color=COLORS[THEME_PROPS.BACKGROUND],
                font=FONTS["pop"],
                pad=((sections_padding_x, sections_padding_x + 10), (0, 0)),
            ),
            sg.Combo(
                values=available_themes,
                default_value=settings.theme,
                key=SETTINGS_KEYS.theme,
                size=25,
                pad=20,
                auto_size_text=True,
                background_color=COLORS[THEME_PROPS.BACKGROUND],
                text_color=COLORS[THEME_PROPS.BUTTON][1],
                button_background_color=COLORS[THEME_PROPS.BACKGROUND],
                button_arrow_color=COLORS[THEME_PROPS.CATEGORY],
                font=FONTS["pop"],
                change_submits=True,
                enable_events=True,
                visible=True,
                tooltip=MESSAGES.settings_tooltip_theme,
            ),
            sg.Button(
                TEXTS_AND_KEYS.preview_themes_window_text,
                font=FONTS["btn"],
                size=15,
                pad=((2 * sections_padding_x + 15, 0), (15, 15)),
                key=TEXTS_AND_KEYS.preview_themes_window_text,
                button_color=(
                    COLORS[THEME_PROPS.BUTTON][0],
                    COLORS[THEME_PROPS.BUTTON][1],
                ),
            ),
        ],
    ]

    data_visualization = [
        [
            sg.Text(
                text=MESSAGES.settings_section_data_visualization,
                text_color=COLORS[THEME_PROPS.CATEGORY],
                background_color=COLORS[THEME_PROPS.BACKGROUND],
                font=FONTS["cat"],
                pad=((sections_padding_x, 0), (sections_padding_y, 5)),
            )
        ],
        [
            sg.Text(
                text=settings_key_to_text(SETTINGS_KEYS.data_days),
                text_color=COLORS[THEME_PROPS.BUTTON][1],
                background_color=COLORS[THEME_PROPS.BACKGROUND],
                font=FONTS["pop"],
                pad=((sections_padding_x, 0), (0, 0)),
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
                background_color=COLORS[THEME_PROPS.INPUT],
                text_color=COLORS[THEME_PROPS.TEXT_INPUT],
            ),
            sg.Text(
                text=pad_string("", 5),
                text_color=COLORS[THEME_PROPS.BACKGROUND],
                background_color=COLORS[THEME_PROPS.BACKGROUND],
                font=FONTS["ckb"],
            ),
            sg.Text(
                text=settings_key_to_text(SETTINGS_KEYS.weekdays_language),
                text_color=COLORS[THEME_PROPS.BUTTON][1],
                background_color=COLORS[THEME_PROPS.BACKGROUND],
                font=FONTS["pop"],
            ),
            sg.Combo(
                values=["en", "pt", "jp"],
                default_value=str(settings.weekdays_language),
                key=SETTINGS_KEYS.weekdays_language,
                size=4,
                pad=5,
                auto_size_text=True,
                background_color=COLORS[THEME_PROPS.BACKGROUND],
                text_color=COLORS[THEME_PROPS.BUTTON][1],
                button_background_color=COLORS[THEME_PROPS.BACKGROUND],
                button_arrow_color=COLORS[THEME_PROPS.CATEGORY],
                font=FONTS["ckb"],
                change_submits=True,
                enable_events=True,
                visible=True,
                tooltip=MESSAGES.settings_tooltip_day_of_week,
            ),
            sg.Text(
                text=pad_string("", 2),
                text_color=COLORS[THEME_PROPS.BACKGROUND],
                background_color=COLORS[THEME_PROPS.BACKGROUND],
                font=FONTS["ckb"],
            ),
            sg.Text(
                text=settings_key_to_text(SETTINGS_KEYS.graph_expected_value),
                text_color=COLORS[THEME_PROPS.BUTTON][1],
                background_color=COLORS[THEME_PROPS.BACKGROUND],
                font=FONTS["pop"],
            ),
            sg.Checkbox(
                text="",
                default=bool(settings.graph_expected_value),
                key=SETTINGS_KEYS.graph_expected_value,
                font=FONTS["pop"],
                checkbox_color=COLORS[THEME_PROPS.BUTTON][0],
                text_color=COLORS[THEME_PROPS.BUTTON][1],
                background_color=COLORS[THEME_PROPS.BACKGROUND],
                pad=((checkbox_padding, 0), (1, 1)),
                tooltip=MESSAGES.settings_tooltip_expected,
            ),
            sg.Text(
                text=pad_string("", 2),
                text_color=COLORS[THEME_PROPS.BACKGROUND],
                background_color=COLORS[THEME_PROPS.BACKGROUND],
                font=FONTS["ckb"],
            ),
            sg.Text(
                text=settings_key_to_text(SETTINGS_KEYS.scrollable_image),
                text_color=COLORS[THEME_PROPS.BUTTON][1],
                background_color=COLORS[THEME_PROPS.BACKGROUND],
                font=FONTS["pop"],
            ),
            sg.Checkbox(
                text="",
                default=bool(settings.scrollable_image),
                key=SETTINGS_KEYS.scrollable_image,
                font=FONTS["pop"],
                checkbox_color=COLORS[THEME_PROPS.BUTTON][0],
                text_color=COLORS[THEME_PROPS.BUTTON][1],
                background_color=COLORS[THEME_PROPS.BACKGROUND],
                pad=((checkbox_padding, 0), (1, 1)),
                tooltip=MESSAGES.settings_tooltip_scrollable,
            ),
        ],
    ]

    messages = [
        [
            sg.Text(
                text=MESSAGES.settings_section_messages,
                text_color=COLORS[THEME_PROPS.CATEGORY],
                background_color=COLORS[THEME_PROPS.BACKGROUND],
                font=FONTS["cat"],
                pad=((sections_padding_x, 0), (sections_padding_y, 5)),
            )
        ],
        [
            sg.Text(
                text=settings_key_to_text(SETTINGS_KEYS.display_messages),
                text_color=COLORS[THEME_PROPS.BUTTON][1],
                background_color=COLORS[THEME_PROPS.BACKGROUND],
                font=FONTS["pop"],
                pad=((sections_padding_x, 0), (0, 0)),
            ),
            sg.Checkbox(
                text="",
                default=bool(settings.display_messages),
                key=SETTINGS_KEYS.display_messages,
                font=FONTS["pop"],
                checkbox_color=COLORS[THEME_PROPS.BUTTON][0],
                text_color=COLORS[THEME_PROPS.BUTTON][1],
                background_color=COLORS[THEME_PROPS.BACKGROUND],
                pad=((checkbox_padding, 20), (1, 1)),
                tooltip=MESSAGES.settings_tooltip_messages_show,
            ),
            sg.Text(
                text=pad_string("", 3),
                text_color=COLORS[THEME_PROPS.BACKGROUND],
                background_color=COLORS[THEME_PROPS.BACKGROUND],
                font=FONTS["ckb"],
            ),
            sg.Text(
                text=settings_key_to_text(SETTINGS_KEYS.random_messages),
                text_color=COLORS[THEME_PROPS.BUTTON][1],
                background_color=COLORS[THEME_PROPS.BACKGROUND],
                font=FONTS["pop"],
            ),
            sg.Checkbox(
                text="",
                default=bool(settings.random_messages),
                key=SETTINGS_KEYS.random_messages,
                font=FONTS["pop"],
                checkbox_color=COLORS[THEME_PROPS.BUTTON][0],
                text_color=COLORS[THEME_PROPS.BUTTON][1],
                background_color=COLORS[THEME_PROPS.BACKGROUND],
                pad=((checkbox_padding, 0), (1, 1)),
                tooltip=MESSAGES.settings_tooltip_random,
            ),
            sg.Text(
                text=pad_string("", 7),
                text_color=COLORS[THEME_PROPS.BACKGROUND],
                background_color=COLORS[THEME_PROPS.BACKGROUND],
                font=FONTS["ckb"],
            ),
            sg.Text(
                text=settings_key_to_text(SETTINGS_KEYS.message_duration),
                text_color=COLORS[THEME_PROPS.BUTTON][1],
                background_color=COLORS[THEME_PROPS.BACKGROUND],
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
                background_color=COLORS[THEME_PROPS.INPUT],
                text_color=COLORS[THEME_PROPS.TEXT_INPUT],
            ),
        ],
    ]

    misc = [
        [
            sg.Text(
                text=MESSAGES.settings_section_misc,
                text_color=COLORS[THEME_PROPS.CATEGORY],
                background_color=COLORS[THEME_PROPS.BACKGROUND],
                font=FONTS["cat"],
                pad=((sections_padding_x, 0), (sections_padding_y, 5)),
            ),
        ],
        [
            sg.Text(
                text=settings_key_to_text(SETTINGS_KEYS.new_day_time),
                text_color=COLORS[THEME_PROPS.BUTTON][1],
                background_color=COLORS[THEME_PROPS.BACKGROUND],
                font=FONTS["pop"],
                pad=((sections_padding_x, 0), (0, 0)),
            ),
            sg.InputText(
                key=SETTINGS_KEYS.new_day_time,
                do_not_clear=True,
                enable_events=True,
                visible=True,
                font=FONTS["ckb"],
                tooltip=MESSAGES.settings_tooltip_new_day_time,
                default_text=str(settings.new_day_time),
                size=text_input_size,
                justification="r",
                background_color=COLORS[THEME_PROPS.INPUT],
                text_color=COLORS[THEME_PROPS.TEXT_INPUT],
            ),
        ],
    ]

    buttons = [
        [
            sg.Text(
                text=MESSAGES.settings_warning,
                text_color=COLORS[THEME_PROPS.BUTTON][1],
                background_color=COLORS[THEME_PROPS.BACKGROUND],
                font=FONTS["pop"],
                pad=((sections_padding_x, 0), (0, 0)),
            ),
            sg.Push(background_color=COLORS[THEME_PROPS.BACKGROUND]),
            sg.Button(
                TEXTS_AND_KEYS.settings_cancel_button_text,
                font=FONTS["btn"],
                size=7,
                pad=((5, 0), (30, 15)),
                key=TEXTS_AND_KEYS.settings_cancel_button_text,
                button_color=(
                    COLORS[THEME_PROPS.BUTTON][0],
                    COLORS[THEME_PROPS.BUTTON][1],
                ),
            ),
            sg.Text(
                text=pad_string("", 1),
                text_color=COLORS[THEME_PROPS.BACKGROUND],
                background_color=COLORS[THEME_PROPS.BACKGROUND],
                font=FONTS["ckb"],
            ),
            sg.Button(
                TEXTS_AND_KEYS.settings_save_button_text,
                font=FONTS["btn"],
                size=7,
                pad=((5, sections_padding_x), (30, 15)),
                key=TEXTS_AND_KEYS.settings_save_button_text,
                button_color=(
                    COLORS[THEME_PROPS.BUTTON][0],
                    COLORS[THEME_PROPS.BUTTON][1],
                ),
            ),
        ]
    ]

    layout = [appearance, data_visualization, messages, misc, buttons]
    return layout


def SettingsWindow(
    settings: Settings,
):
    layout = SettingsWindowLayout(
        settings,
    )
    return sg.Window(
        title=TEXTS_AND_KEYS.settings_button_text,
        layout=layout,
        use_custom_titlebar=True,
        titlebar_background_color=COLORS[THEME_PROPS.BUTTON][0],
        titlebar_text_color=COLORS[THEME_PROPS.BUTTON][1],
        titlebar_icon=PATH.settings_icon,
        background_color=COLORS[THEME_PROPS.BACKGROUND],
        size=(900, 540),
        element_justification="l",
        return_keyboard_events=True,
    )

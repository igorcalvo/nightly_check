from PySimpleGUI import WIN_CLOSED
from source.constants import FILE_NAMES, SETTINGS_KEYS, TEXTS_AND_KEYS
from source.core.data_out import save_settings_file
from source.core.settings import Settings
from source.loops.habit_init import Habit_Init_Loop
from source.ui.settings import PreviewWindow, SettingsWindow
from source.ui.utils import init_ui, preview_themes


def Settings_Loop(settings: Settings):
    settings_window = SettingsWindow(settings)

    hue_offset = settings.hue_offset
    old_hue_offset = settings.hue_offset

    theme = settings.theme
    old_theme = settings.theme

    while True:
        settings_event, settings_dict = settings_window.read()  # type: ignore
        if settings_event in [
            TEXTS_AND_KEYS.settings_save_button_text,
            TEXTS_AND_KEYS.settings_cancel_button_text,
            WIN_CLOSED,
        ]:
            if settings_event == TEXTS_AND_KEYS.settings_save_button_text:
                settings = Settings.from_dict(settings_dict)
                save_settings_file(FILE_NAMES.stg, settings)
            settings_window.close()
            break
        elif settings_event == SETTINGS_KEYS.hue_offset:
            hue_offset = settings_dict[SETTINGS_KEYS.hue_offset]
        elif settings_event == SETTINGS_KEYS.theme:
            theme = settings_dict[SETTINGS_KEYS.theme]
        elif settings_event == TEXTS_AND_KEYS.preview_themes_window_text:
            preview_themes()
        elif settings_event == TEXTS_AND_KEYS.edit_variables_button_text:
            Habit_Init_Loop(True)
        elif settings_event == TEXTS_AND_KEYS.preview_window_text:
            preview_window = PreviewWindow(hue_offset, theme)
            while True:
                preview_event, preview_values_dict = preview_window.read()  # type: ignore
                if (
                    preview_event == TEXTS_AND_KEYS.preview_close_key
                    or preview_event == WIN_CLOSED
                ):
                    preview_window.close()
                    break
    init_ui(old_hue_offset, old_theme)

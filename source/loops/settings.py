from source.constants import FILE_NAMES, SETTINGS_KEYS
from source.core.data_out import save_settings_file
from source.core.settings import Settings
from source.loops.habit_init import Habit_Init_Loop
from source.ui.utils import init_ui


def Settings_Loop(settings: Settings):
    hue_offset = settings.hue_offset
    old_hue_offset = settings.hue_offset
    theme = settings.theme
    old_theme = settings.theme

    settings = Settings.from_dict(settings_dict)
    save_settings_file(FILE_NAMES.stg, settings)

    hue_offset = settings_dict[SETTINGS_KEYS.hue_offset]

    theme = settings_dict[SETTINGS_KEYS.theme]

    preview_themes()

    Habit_Init_Loop(True)

    preview_window = PreviewWindow(hue_offset, theme)

    init_ui(old_hue_offset, old_theme)

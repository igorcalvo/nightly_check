from .utils import os_is_windows
from os import path, pardir

DIR = path.abspath(path.join(path.dirname(__file__), pardir))
data_folder_name = "data"
data_folder = path.abspath(path.join(DIR, data_folder_name))


class FILE_NAMES:
    csv = path.abspath(path.join(data_folder, "data.csv"))
    msg = path.abspath(path.join(data_folder, "msg.txt"))
    log = path.abspath(path.join(data_folder, "log.txt"))
    var = path.abspath(path.join(data_folder, "variables.csv"))
    stg = path.abspath(path.join(data_folder, "settings.json"))


class TEXTS_AND_KEYS:
    done_button_text = "Done"
    slider_text_key = "Slider"
    preview_close_key = "ClosePreview"
    data_button_text = "Data"
    export_button_text = "Export"
    neglected_accept_text = "Yes"
    neglected_reject_text = "No"
    edit_button_text = "Edit"
    settings_button_text = "Settings"
    preview_window_text = "Preview"
    settings_save_button_text = "Save"
    settings_cancel_button_text = "Cancel"
    select_date_button_text = "Select"
    select_date_key = "Date"


class HABITS_INIT:
    cat_add = "Add Category"
    cat_remove = "Remove Category"
    category_key = "NewCategory"
    add_habit_text = "+ Habit"
    del_habit_text = "- Habit"
    categories_key = "Categories"
    track_frequency_key = "Track Value"
    generate_text = "Generate File"
    habit_key = "Habit Value"
    question_key = "Question Value"
    message_key = "Message Value"
    condition_key = "Condition Value"
    fraction_num_key = "FracNum Value"
    fraction_den_key = "FracDen Value"


class SETTINGS_KEYS:
    hue_offset = "hue_offset"
    theme = "theme"
    data_days = "data_days"
    display_messages = "display_messages"
    graph_expected_value = "graph_expected_value"
    scrollable_image = "scrollable_image"
    message_duration = "message_duration"
    random_messages = "random_messages"
    weekdays_language = "weekdays_language"


class SETTINGS_DEFAULT_VALUES:
    hue_offset = 0
    theme = "Default"
    data_days = 21
    display_messages = True
    graph_expected_value = False
    scrollable_image = False
    message_duration = 5
    random_messages = True
    weekdays_language = "jp"


class MESSAGES:
    app_title = "Argus"
    hue = "Slide to change hue"
    preview_text = "Preview"
    preview_tooltip = "Sample tooltip"
    preview_checkbox = " " + "This window will close in 3s."
    preview_close = "Close"
    neglected_title = "Yesterday"
    neglected = "It looks like you haven't input yesterday's data. Would you like to add it now?"
    date_text = "Select a date:"
    date_calendar = "Pick a date"
    input_tooltip_track = "Track Frequency?"
    input_tooltip_habit = "Short word to represent a habit"
    input_tooltip_question = "Simple yes or no question to help you determine whether you have completed a task or not"
    input_tooltip_checkbox = "Enables message pop up if you fail to perform a task within a determined frequency"
    input_tooltip_message = "Message you'll get when you fail to complete the task within a defined frequency"
    input_tooltip_combo = "Pick with what you want to achieve in mind, not when you want to see a message (failure)"
    input_tooltip_category = "Short word to represent a collection of habits"
    habits_title = "Habits File Generator"
    settings_warning = "*** Changes will only take effect after restart ***"
    style_button_tooltip = "change app's hue"
    settings_button_tooltip = "edit settings"
    data_button_tooltip = "display past days' data"
    edit_button_tooltip = "edit a past day's entry"
    done_button_tooltip = "save and close app"
    settings_section_appearance = "APPEARANCE"
    settings_section_data_visualization = "DATA VISUALIZATION"
    settings_section_messages = "MESSAGES"
    settings_tooltip_hueoffset = "offset of hue according to base theme in the HSV schema (between -0.5 and +0.5)"
    settings_tooltip_days = "Number of back days to display data of"
    settings_tooltip_day_of_week = "Language to display weekday's symbols in"
    settings_tooltip_expected = (
        "Display data as according to expected or not instead of done or not"
    )
    settings_tooltip_scrollable = (
        "Enable window to be scrollable (useful if the number habits is high)"
    )
    settings_tooltip_messages_show = "Display a message before closing"
    settings_tooltip_random = (
        "Pick a message among candidates randomly instead of according to coded logic"
    )
    settings_tooltip_duration = "How many seconds the message is going to be displayed on the screen for before closing the app"
    settings_tooltip_theme = "Select a theme"


class PATHS:
    colored_icon = f"{DIR}/assets/icons/iconColored.png"
    standard_icon = f"{DIR}/assets/icons/icon16.png"
    style_icon = f"{DIR}/assets/icons/style16.png"
    data_icon = f"{DIR}/assets/icons/data16.png"
    yesterday_icon = f"{DIR}/assets/icons/yesterday16.png"
    init_icon = f"{DIR}/assets/icons/rocket16.png"
    preview_icon = f"{DIR}/assets/icons/preview16.png"
    settings_icon = f"{DIR}/assets/icons/cogwheel16.png"


class THEME_PROPS:
    ACCENT1 = "ACCENT1"
    ACCENT2 = "ACCENT2"
    ACCENT3 = "ACCENT3"
    BACKGROUND = "BACKGROUND"
    BORDER = "BORDER"
    BUTTON = "BUTTON"
    COLOR_LIST = "COLOR_LIST"
    DESCRIPTION = "DESCRIPTION"
    INPUT = "INPUT"
    PROGRESS = "PROGRESS"
    PROGRESS_DEPTH = "PROGRESS_DEPTH"
    SCROLL = "SCROLL"
    SLIDER_DEPTH = "SLIDER_DEPTH"
    TEXT = "TEXT"
    TEXT_INPUT = "TEXT_INPUT"


# ----------------------------------------------------------------------------------------------------------------------
wakeup_time = 14
date_header = "date"
already_filled_in_today_message = (
    "No message for you! You have already added your entry in today."
)
# ----------------------------------------------------------------------------------------------------------------------
# | hue_offset | < 1

COLORS = {
    "bar_bkg": "#00274f",
    "bar_txt": "#b1d8ff",
    "win_bkg": "#002f5f",
    "cat_txt": "#dbedff",
    "sld_bkg": "#004080",
}


class COLORS2:
    bar_bkg = "#00274f"
    bar_txt = "#b1d8ff"
    win_bkg = "#002f5f"
    cat_txt = "#dbedff"
    sld_bkg = "#004080"


FONTS = {
    "cat": ("Cascadia Mono" if os_is_windows() else "Liberation Mono", 13, "bold"),
    "ckb": ("Consolas" if os_is_windows() else "Noto Mono", 11),
    "btn": ("Verdana", 9, "bold"),
    "pop": ("Arial", 11, "bold"),
}

font_families = {
    "consolas": path.join(DIR, r"assets/fonts/consola.ttf"),
    "roboto": path.join(DIR, r"assets/fonts/Roboto-Bold.ttf"),
    "liberation": path.join(DIR, r"assets/fonts/LiberationMono-Bold.ttf"),
    "noto": path.join(DIR, r"assets/fonts/NotoSansJP-Regular.otf"),
}

from os import pardir, path

DIR = path.abspath(path.join(path.dirname(__file__), pardir))
data_folder_name = "data"
data_folder = path.abspath(path.join(DIR, data_folder_name))


class FILE_NAMES:
    csv = path.abspath(path.join(data_folder, "data.csv"))
    msg = path.abspath(path.join(data_folder, "messages.csv"))
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
    preview_window_text = "Preview Appearance"
    preview_themes_window_text = "Preview Themes"
    settings_save_button_text = "Save"
    settings_cancel_button_text = "Cancel"
    select_date_button_text = "Select"
    select_date_key = "Date"
    edit_variables_button_text = "Edit Variables"


class HABITS_INIT:
    cat_add = "Add Category"
    cat_remove = "Remove Category"
    category_key = "NewCategory"
    add_habit_text = "+ Habit"
    del_habit_text = "- Habit"
    categories_key = "Categories"
    track_frequency_key = "Track Value"
    generate_text = "Generate File"
    generate_text_alt = "Update File"
    load_file_text = "Load data from file"
    load_file_key = "Load File"
    habit_key = "Habit Value"
    question_key = "Question Value"
    message_key = "Message Value"
    condition_key = "Condition Value"
    fraction_num_key = "FracNum Value"
    fraction_den_key = "FracDen Value"
    label_category = "Category"
    label_habit = "Habit"
    label_habit_question = "Goal Question"
    label_message = "Encouraging Message"
    label_direction = "Ideal Frequency is: "
    enabled_key = "Enabled"
    clear_icon = "🧹"
    habit_clear_key = "ClearHabit"


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
    new_day_time = "new_day_time"
    show_data_vis_reminder = "show_data_vis_reminder"
    data_vis_reminder_days = "data_vis_reminder_days"
    data_vis_dark_theme = "data_vis_dark_theme"


class SETTINGS_DEFAULT_VALUES:
    hue_offset = 0
    theme = "Classic"
    data_days = 21
    display_messages = True
    graph_expected_value = False
    scrollable_image = False
    message_duration = 5
    random_messages = True
    weekdays_language = "jp"
    new_day_time = 6
    show_data_vis_reminder = True
    data_vis_reminder_days = 7
    data_vis_dark_theme = True


class MESSAGES:
    # app_title = "Argus"
    # app_title = "NightlyCheck"
    # app_title = "OwlPeek"
    app_title = "OwlCheck"
    hue = "Slide to change hue"
    preview_text = "Preview"
    preview_tooltip = "Sample tooltip"
    preview_checkbox = " " + "This window will close in 3s."
    preview_close = "Close"
    neglected_title = "Yesterday"
    neglected = "It looks like you haven't input yesterday's data. Would you like to add it now?"
    date_text = "Select a date:"
    date_calendar = "Pick a date"
    input_tooltip_track = "  Track?"
    input_tooltip_habit = "Short word to represent a habit"
    input_tooltip_question = "Simple yes or no question to help you determine whether you have completed a task or not"
    input_tooltip_checkbox = "Enables message pop up if you fail to perform a task within a determined frequency"
    input_tooltip_message = "Message you'll get when you fail to complete the task within a defined frequency"
    input_tooltip_combo = "Pick with what you want to achieve in mind (success), not when you want to see a message (failure)"
    input_tooltip_category = "Short word to represent a collection of habits"
    habits_title = "Habits File Generator"
    settings_warning = "*** Changes will only take effect after restart ***"
    style_button_tooltip = "change app's hue"
    settings_button_tooltip = "edit settings"
    data_button_tooltip = "display past days' data"
    data_export_tooltip = "export image to file"
    edit_button_tooltip = "edit a past day's entry"
    done_button_tooltip = "save and close app"
    settings_section_appearance = "APPEARANCE"
    settings_section_data_visualization = "DATA VISUALIZATION"
    settings_section_messages = "MESSAGES"
    settings_section_misc = "MISCELLANEOUS"
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
    settings_tooltip_new_day_time = (
        "Hour after which a new day starts - useful for people who sleep after midnight"
    )
    settings_tooltip_show_data_vis_reminder = (
        "Display popup periodically reminding you to check your data"
    )
    settings_tooltip_data_vis_reminder_days = (
        "How many days until the next reminder to check your data"
    )
    settings_data_vis_reminder_message = (
        "Have you recently checked how you are doing?\nMaybe you should check it."
    )
    settings_tooltip_enabled = "Toggles wether habit is enabled or not"
    settings_tooltip_datavis_darktheme = "Toggles dark theme on data visualization"


class ICON_PATHS:
    colored_icon = f"{DIR}/assets/icons/iconColored.png"
    colored_msg_icon = f"{DIR}/assets/icons/msgIconColored.png"
    standard_icon = f"{DIR}/assets/icons/icon16.png"
    style_icon = f"{DIR}/assets/icons/style16.png"
    data_icon = f"{DIR}/assets/icons/data16.png"
    yesterday_icon = f"{DIR}/assets/icons/yesterday16.png"
    init_icon = f"{DIR}/assets/icons/rocket16.png"
    preview_icon = f"{DIR}/assets/icons/preview16.png"
    settings_icon = f"{DIR}/assets/icons/cogwheel16.png"
    owl_icon_ico = f"{DIR}/assets/icons/owl/patrolling-owl.ico"
    owl_icon_png_32 = f"{DIR}/assets/icons/owl/patrolling-owl32.png"
    owl_icon_png_64 = f"{DIR}/assets/icons/owl/patrolling-owl64.png"


date_header = "date"


class MESSAGES_HEADERS:
    date = date_header
    category = "category"
    habit = "habit"
    message = "message"
    data_reminder = "data_reminder"


class VARIABLES_KEYS:
    enabled = "enabled"
    category = "category"
    habit = "habit"
    question = "question"
    message = "message"
    condition = "condition"
    frequency = "frequency"


class DATA_VISUALIZATION:
    initial_x = 25
    initial_y = 50
    rows_y_spacing = 2
    sqrSize = 20
    sqrBorder = 1
    text_squares_x_spacing = int(0.5 * sqrSize)
    text_squares_y_offset = int(0.25 * sqrSize)
    category_y_spacing = int(2 * sqrSize)
    background = (255, 255, 255)
    dark_theme_background = (70, 70, 70)
    text = (0, 0, 0)
    dark_theme_text = (220, 220, 220)
    skipped = (191, 191, 191)
    dark_theme_skipped = (150, 150, 150)


class HTTP:
    get = "GET"
    post = "POST"


class ROUTES:
    initial = "welcome"
    edit = "data"
    visual = "report"
    settings = "settings"
    close = "exit"

# ----------------------------------------------------------------------------------------------------------------------
variables_csv_header = "enabled,category,habit,question,message,condition,frequency"
messages_csv_header = f"{date_header},category,habit,message,data_reminder"
category_habit_separator = " - "
already_filled_in_today_message = (
    "No message for you! You have already added in an entry for today."
)
data_visualization_reminder_duration = 3
data_visualization_threshold = 60
# ----------------------------------------------------------------------------------------------------------------------
# | hue_offset | < 1

COLORS = {}

font_families = {
    "consolas": path.join(DIR, r"assets/fonts/consola.ttf"),
    "liberation": path.join(DIR, r"assets/fonts/LiberationMono-Bold.ttf"),
    "noto": path.join(DIR, r"assets/fonts/NotoSansJP-Regular.otf"),
}

from .utils import os_is_windows
import os

DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

data_folder_name = 'data'
data_folder = os.path.abspath(os.path.join(DIR, data_folder_name))
csv_file_name = os.path.abspath(os.path.join(data_folder, 'data.csv'))
msg_file_name = os.path.abspath(os.path.join(data_folder, 'msg.txt'))
log_file_name = os.path.abspath(os.path.join(data_folder, 'log.txt'))
variables_file_name = os.path.abspath(os.path.join(DIR, 'variables.csv'))
settings_file_name = os.path.abspath(os.path.join(DIR, 'settings.json'))

done_button_text = 'Done'
style_button_text = 'Style'
slider_text_key = 'Slider'
set_button_text_key = 'Set'
preview_window_text = 'Preview'
preview_close_key = 'ClosePreview'
data_button_text = 'Data'
export_button_text = 'Export'
neglected_accept_text = "Yes"
neglected_reject_text = "No"
edit_button_text = 'Edit'
settings_button_text = 'Settings'
settings_save_button_text = 'Save'
settings_cancel_button_text = 'Cancel'
select_date_button_text = 'Select'
select_date_key = 'Date'
habits_init_cat_add = 'Add Category'
habits_init_cat_remove = 'Remove Category'
habits_init_category_key = 'NewCategory'
habits_init_add_habit_text = '+ Habit'
habits_init_del_habit_text = '- Habit'
habits_init_categories_key = 'Categories'
habits_init_track_frequency_key = 'Track Value'
habits_init_generate_text = 'Generate File'
habits_init_habit_key = 'Habit Value'
habits_init_question_key = 'Question Value'
habits_init_message_key = 'Message Value'
habits_init_condition_key = 'Condition Value'
habits_init_fraction_num_key = 'FracNum Value'
habits_init_fraction_den_key = 'FracDen Value'

already_filled_in_today_message = "No message for you! You have already added your entry in today."
# ----------------------------------------------------------------------------------------------------------------------
wakeup_time = 14
date_header = "date"
# ----------------------------------------------------------------------------------------------------------------------
# | hue_offset | < 1

# basis
bar_bkg = "#00274f"
bar_txt = "#b1d8ff"
win_bkg = "#002f5f"
cat_txt = "#dbedff"
sld_bkg = "#004080"

COLORS = {
    "bar_bkg": bar_bkg,
    "bar_txt": bar_txt,
    "win_bkg": win_bkg,
    "cat_bkg": win_bkg,
    "cat_txt": cat_txt,
    "ckb_bkg": bar_bkg,
    "ckb_txt": bar_txt,
    "dnb_bkg": bar_bkg,
    "dnb_txt": bar_txt,
    "pop_bkg": bar_txt,
    "pop_txt": bar_bkg,
    "sld_txt": cat_txt,
    "sld_bkg": sld_bkg,
    "sld_sld": bar_txt,
    "dat_txt": cat_txt,
    "dat_bkg": sld_bkg,
    "exp_txt": bar_txt,
    "exp_bkg": bar_bkg,
    "neg_txt": bar_txt,
    "neg_bkg": bar_bkg,
    "dtp_txt": bar_txt,
    "dtp_bkg": bar_bkg,
    "hbc_txt": bar_bkg,
    "hbc_bkg": cat_txt,
    "hbi_sep": bar_bkg,
    "stg_bkg": win_bkg,
    "stg_txt": bar_txt,
}

FONTS = {
    "cat": ("Cascadia Mono" if os_is_windows() else "Liberation Mono", 13, "bold"),
    "ckb": ('Consolas' if os_is_windows() else "Noto Mono", 11),
    "btn": ("Verdana", 9, "bold"),
    "pop": ("Arial", 11, "bold")
}
# ----------------------------------------------------------------------------------------------------------------------
font_families = {
    "consolas": os.path.join(DIR, r"assets/fonts/consola.ttf"),
    "roboto": os.path.join(DIR, r"assets/fonts/Roboto-Bold.ttf"),
    "liberation": os.path.join(DIR, r"assets/fonts/LiberationMono-Bold.ttf"),
    "noto": os.path.join(DIR, r"assets/fonts/NotoSansJP-Regular.otf"),
}
# ----------------------------------------------------------------------------------------------------------------------
class SETTINGS_KEYS:
    hue_offset = "hue_offset"
    data_days = "data_days"
    display_messages = "display_messages"
    graph_expected_value = "graph_expected_value"
    scrollable_image = "scrollable_image"
    message_duration = "message_duration"
    random_messages = "random_messages"
    weekdays_language = "weekdays_language"

class MESSAGES:
    app_title = "Argus"
    hue = "Slide to change hue"
    preview_text = "Preview"
    preview_tooltip = "Sample tooltip"
    preview_checkbox = ' ' + "Sample Text"
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
    settings_warning = "Changes will only take effect after restart"
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
    settings_tooltip_expected = "Display data as according to expected or not instead of done or not"
    settings_tooltip_scrollable = "Enable window to be scrollable (useful if the number os habits is high)"
    settings_tooltip_messages_show = "Display a message before closing"
    settings_tooltip_random = "Pick a message among candidates randomly instead of according to coded logic"
    settings_tooltip_duration = "How long the message is going to be displayed on the screen before closing the app"

class PATHS:
    colored_icon = f"{DIR}/assets/icons/iconColored.png"
    standard_icon = f"{DIR}/assets/icons/icon16.png"
    style_icon = f"{DIR}/assets/icons/style16.png"
    data_icon = f"{DIR}/assets/icons/data16.png"
    yesterday_icon = f"{DIR}/assets/icons/yesterday16.png"
    init_icon = f"{DIR}/assets/icons/rocket16.png"
    preview_icon = f"{DIR}/assets/icons/preview16.png"
    settings_icon = f"{DIR}/assets/icons/cogwheel16.png"

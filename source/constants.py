from .utils import is_windows

data_folder = 'data'
csv_file_name = f'{data_folder}/data.csv'
msg_file_name = f'{data_folder}/msg.txt'
log_file_name = f'{data_folder}/log.txt'
variables_file_name = 'variables.csv'
settings_file_name = 'settings.json'

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
# ----------------------------------------------------------------------------------------------------------------------
wakeup_time = 14
date_header = "date"
# ----------------------------------------------------------------------------------------------------------------------
CATEGORY_PIXEL_LENGTH = 10
CHECKBOX_PIXEL_LENGTH = 8 if is_windows else 9
# | hue_offset | < 1
HUE_BASE = 0.59

# basis
bar_bkg = "#00274f"
bar_txt = "#b1d8ff"
win_bkg = "#002f5f"
cat_txt = "#dbedff"
sld_bkg = "#004080"

COLORS = {
    "bar_bkg":  bar_bkg,
    "bar_txt":  bar_txt,
    "win_bkg":  win_bkg,
    "cat_bkg":  win_bkg,
    "cat_txt":  cat_txt,
    "ckb_bkg":  bar_bkg,
    "ckb_txt":  bar_txt,
    "dnb_bkg":  bar_bkg,
    "dnb_txt":  bar_txt,
    "pop_bkg":  bar_txt,
    "pop_txt":  bar_bkg,
    "sld_txt":  cat_txt,
    "sld_bkg":  sld_bkg,
    "sld_sld":  bar_txt,
    "dat_txt":  cat_txt,
    "dat_bkg":  sld_bkg,
    "exp_txt":  bar_txt,
    "exp_bkg":  bar_bkg,
    "neg_txt":  bar_txt,
    "neg_bkg":  bar_bkg,
    "dtp_txt":  bar_txt,
    "dtp_bkg":  bar_bkg,
    "hbc_txt":  bar_bkg,
    "hbc_bkg":  cat_txt,
    "hbi_sep":  bar_bkg,
}

FONTS = {
    "cat": ("Cascadia Mono" if is_windows() else "Liberation Mono", 13, "bold"),
    "ckb": ('Consolas' if is_windows() else "Noto Mono", 11),
    "btn": ("Verdana", 9, "bold"),
    "pop": ("Arial", 11, "bold")
}
# ----------------------------------------------------------------------------------------------------------------------
import os
dirname = os.path.dirname(__file__)

font_families = {
    "consolas": os.path.join(dirname, r"assets/fonts/consola.ttf"),
    "roboto": os.path.join(dirname, r"assets/fonts/Roboto-Bold.ttf"),
    "liberation": os.path.join(dirname, r"assets/fonts/LiberationMono-Bold.ttf"),
    "noto": os.path.join(dirname, r"assets/fonts/NotoSansJP-Regular.otf"),
}
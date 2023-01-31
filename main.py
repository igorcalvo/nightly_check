import datetime

from source.ui import *
from source.core import *
from source.imggen import *

data_folder = 'data'
csv_file_name = f'{data_folder}\data.csv'
msg_file_name = f'{data_folder}\msg.txt'
log_file_name = f'{data_folder}\log.txt'
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
habits_init_add_habit_text = 'Add Habit'
habits_init_del_habit_text = 'Del Habit'
habits_init_categories_key = 'Categories'

values_dict = {}
hue_offset = 0

create_folder_if_doesnt_exist(data_folder)
create_file_if_doesnt_exist(log_file_name)
log = open(log_file_name, 'r+')
try:
    if not exists(variables_file_name):
        category_count = 0
        variables_init_layout = HabitsInitLayout(habits_init_cat_add, habits_init_cat_remove, habits_init_categories_key, habits_init_category_key, habits_init_add_habit_text, habits_init_del_habit_text, category_count, {})
        variables_init_window = HabitsInitWindow(variables_init_layout)
        while True:
            variables_init_event, variables_init_values_dict = variables_init_window.read()
            if variables_init_event == habits_init_cat_add:
                category_count += 1
                variables_init_layout = HabitsInitLayout(habits_init_cat_add, habits_init_cat_remove, habits_init_categories_key, habits_init_category_key, habits_init_add_habit_text, habits_init_del_habit_text, category_count, variables_init_values_dict)
                variables_init_window.close()
                variables_init_window = HabitsInitWindow(variables_init_layout)
            elif variables_init_event == habits_init_cat_remove:
                category_count -= 1
                variables_init_layout = HabitsInitLayout(habits_init_cat_add, habits_init_cat_remove, habits_init_categories_key, habits_init_category_key, habits_init_add_habit_text, habits_init_del_habit_text, category_count, variables_init_values_dict)
                variables_init_window.close()
                variables_init_window = HabitsInitWindow(variables_init_layout)
            elif variables_init_event == sg.WIN_CLOSED:
                variables_init_window.close()
                break
    verify_variables(variables_file_name)
    variables_file = read_csv(variables_file_name, csv_file_name)
    conditions, fractions, habit_messages, descriptions, header, categories = get_data(variables_file)

    if not exists(csv_file_name):
        cols = [to_lower_underscored(item) for item in flatten_list(header)]
        cols.insert(0, date_header)
        data = DataFrame(columns=cols)
    else:
        data = read_csv(csv_file_name, csv_file_name)
    variables = list(data.columns)
    variables.pop(0)
    data_from_date_to_list(data, '2023-01-12', header)
    verify_header_and_data(header, variables, csv_file_name, data)
    data = create_entry(data)
    # PrintFonts()
    settings = read_settings(settings_file_name)
    InitUi(settings.hue_offset)
    neglected = no_data_from_yesterday(data)
    if neglected:
        neglected_window = NeglectedPopUp(neglected_accept_text, neglected_reject_text)
        while True:
            neglected_event, neglected_values_dic = neglected_window.read()
            if neglected_event == neglected_accept_text:
                neglected_data_window = MainWindow(categories, header, descriptions, done_button_text, style_button_text,
                                                   data_button_text, edit_button_text, len(data) > 1, True)
                while True:
                    neglected_data_event, neglected_data_values_dict = neglected_data_window.read()
                    if neglected_data_event == done_button_text:
                        log_write(log, f"saving data from yesterday\n{neglected_data_values_dict}")
                        save_data(data, neglected_data_values_dict, csv_file_name, True)
                    if neglected_data_event == sg.WIN_CLOSED or neglected_data_event == done_button_text:
                        neglected_window.close()
                        break
            if neglected_event == sg.WIN_CLOSED or neglected_event == neglected_reject_text:
                neglected_window.close()
                break
    window = MainWindow(categories, header, descriptions, done_button_text, style_button_text, data_button_text,
                        edit_button_text, len(data) > 1, False)
    while True:
        event, values_dict = window.read()
        if event == style_button_text:
            style_window = StyleWindow(style_button_text, slider_text_key, preview_window_text, set_button_text_key)
            while True:
                style_event, style_values_dict = style_window.read()
                if style_event == slider_text_key:
                    hue_offset = style_values_dict[slider_text_key]
                elif style_event == preview_window_text:
                    preview_window = PreviewWindow(preview_window_text, preview_close_key, hue_offset)
                    while True:
                        preview_event, preview_values_dict = preview_window.read()
                        if preview_event == preview_close_key or preview_event == sg.WIN_CLOSED:
                            preview_window.close()
                            break
                elif style_event == set_button_text_key or style_event == sg.WIN_CLOSED:
                    if style_event == set_button_text_key:
                        settings.hue_offset = hue_offset
                        save_settings_file(settings, settings_file_name)
                    style_window.close()
                    break
        elif event == data_button_text:
            graph_data = read_csv(csv_file_name, csv_file_name)
            img = generate_image(categories, header, conditions, settings.data_days, settings.graph_expected_value, graph_data)
            data_window = DataWindow(data_button_text, export_button_text, settings.scrollable_image, image_bytes_to_base64(img))
            while True:
                data_event, data_values_dict = data_window.read()
                if data_event == export_button_text:
                    export_image_file_name = data_values_dict[export_button_text]
                    if export_image_file_name:
                        img.save(export_image_file_name)
                if data_event == sg.WIN_CLOSED or data_event == export_button_text:
                    data_window.close()
                    break
        elif event == edit_button_text:
            date_picker_window = DatePickerWindow(select_date_key, select_date_button_text)
            picked_date = datetime.today()
            while True:
                date_picker_event, date_picker_dict = date_picker_window.read()
                if date_picker_event == select_date_button_text or date_picker_event == sg.WIN_CLOSED:
                    picked_date = date_picker_dict[select_date_key]
                    data_from_date = data_from_date_to_list(data, picked_date, header)
                    edit_data_window = MainWindow(categories, header, descriptions, done_button_text, style_button_text,
                                                  data_button_text, edit_button_text, len(data) > 1, True, data_from_date)
                    while True:
                        edit_data_event, edit_data_values_dict = edit_data_window.read()
                        if edit_data_event == done_button_text:
                            log_write(log, f"saving data from date '{picked_date}'\n{edit_data_values_dict}")
                            save_data(data, edit_data_values_dict, csv_file_name, False, picked_date)
                        if edit_data_event == sg.WIN_CLOSED or edit_data_event == done_button_text:
                            edit_data_window.close()
                            break
                    date_picker_window.close()
                    break
        elif event == done_button_text or event == sg.WIN_CLOSED:
            if event == done_button_text:
                save_data(data, values_dict, csv_file_name)

                message = get_popup_message(conditions, fractions, habit_messages, header, data, msg_file_name)
                if message and settings.display_messages:
                    save_message_file(msg_file_name, header, message)
                    PopUp(message, settings.message_duration)
            break
    window.close()
except Exception as e:
    if __debug__:
        raise(e)
    else:
        e_type, e_obj, e_tb = exc_info()
        e_filename = path.split(e_tb.tb_frame.f_code.co_filename)[1]
        log_write(log, f"\n{e_obj} at line {e_tb.tb_lineno} of {e_filename}\n\n")
finally:
    finally_string = f"***** {date.today()} - {datetime.now().time().replace(microsecond=0)} *****\n"
    if values_dict is not None and any(values_dict.values()):
        log_write(log, f"{finally_string}{values_dict}\n\n")
    else:
        log_write(log, f"{finally_string}")
    log.close()

# TODO LIST - REAL
# better ui
#   columns instead of spacing text
#   better width formula
#   research how to make it look prettier
# ui for data init
# settings for day of the week
# ui for settings

# TODO LIST - OLD
# pop up after n days (settings) reminding to view data
# validate variables
#   duplicate columns
#   empty columns
#   handle empty tool tips
#   handle empty direction
#   handle empty frequency

# TAG FEATURE? LATEST TIME TAG
#   separate file

#   FUTURE
#   have an indicator on the side of each row based on frequencies:
#       all good
#       improving, but still bad
#       declining, but still good
#       all bad
#   ui for variables, very nani
#       if never ran, start this window
#       else have a button to edit it later
#   have some sort of readme?
#   write reddit post
#   (week challenge?!?!?!?!)
#       reward for completing challenge!!
#       or completing streaks(i.e. 30 days working out)
#
#   alerta baseado em tema conta mais:
#       exemplo: nao malhar e comer a mais
#       	 cel no trabalho e nao meditar
#       	 anime fap e jogar
# TODO fix ui
#
#   COMPILED CODE
#   run: python -m PyInstaller --onefile main.py
#   solution to assets problem: https://stackoverflow.com/q/31836104
#   improve code
#       remove unnecessary imports (from x import *)
#       remove commented out code
#   refer to: assets/reference/compiled.PNG
#       assets folder -> check if folder exists and maybe unzip automatically?
#       variables.txt -> handle msg, or create with ui
#       create data folder -> check if folder exists and maybe unzip automatically?
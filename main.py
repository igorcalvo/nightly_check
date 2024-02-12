import datetime

from source.ui import *
from source.core import *
from source.imggen import *
from source.constants import *

from traceback import format_exc

values_dict = {}

create_folder_if_doesnt_exist(data_folder)
create_file_if_doesnt_exist(log_file_name)
log = open(log_file_name, 'r+')
try:
    if not exists(variables_file_name):
        category_count = 0
        habit_count = []
        variables_init_layout = HabitsInitLayout(habits_init_cat_add, habits_init_cat_remove, habits_init_generate_text,
                                                 habits_init_categories_key, habits_init_category_key,
                                                 habits_init_add_habit_text, habits_init_del_habit_text,
                                                 habits_init_track_frequency_key, habits_init_habit_key,
                                                 habits_init_question_key, habits_init_message_key,
                                                 habits_init_condition_key, habits_init_fraction_num_key,
                                                 habits_init_fraction_den_key,category_count, {}, habit_count)
        variables_init_window = HabitsInitWindow(variables_init_layout)
        while True:
            variables_init_event, variables_init_values_dict = variables_init_window.read() # type: ignore
            if variables_init_event == habits_init_cat_add:
                category_count += 1
                habit_count.append(0)
            elif variables_init_event == habits_init_cat_remove:
                category_count -= 1
                habit_count.pop()
            elif habits_init_add_habit_text in variables_init_event:
                habit_count[habit_index_from_event(variables_init_event)] = habit_count[habit_index_from_event(variables_init_event)] + 1
            elif habits_init_del_habit_text in variables_init_event:
                habit_count[habit_index_from_event(variables_init_event)] = habit_count[habit_index_from_event(variables_init_event)] - 1
            elif variables_init_event == habits_init_generate_text:
                generate_variables(variables_file_name, variables_init_values_dict, habits_init_category_key, habits_init_habit_key,
                                   habits_init_question_key, habit_count, habits_init_message_key,
                                   habits_init_condition_key, habits_init_fraction_num_key, habits_init_fraction_den_key)
                variables_init_window.close()
                break
            elif variables_init_event == sg.WIN_CLOSED:
                variables_init_window.close()
                break

            if habits_init_track_frequency_key in variables_init_event\
                    or habits_init_del_habit_text in variables_init_event\
                    or habits_init_add_habit_text in variables_init_event\
                    or variables_init_event == habits_init_cat_remove\
                    or variables_init_event == habits_init_cat_add:
                variables_init_window = ReRenderHabitsInit(variables_init_window, habits_init_cat_add, habits_init_cat_remove,
                                                           habits_init_generate_text, habits_init_categories_key,
                                                           habits_init_category_key, habits_init_add_habit_text,
                                                           habits_init_del_habit_text, habits_init_track_frequency_key,
                                                           habits_init_habit_key, habits_init_question_key,
                                                           habits_init_message_key, habits_init_condition_key,
                                                           habits_init_fraction_num_key, habits_init_fraction_den_key,
                                                           category_count, variables_init_values_dict, habit_count)
    verify_variables(variables_file_name)
    variables_file = read_csv(variables_file_name, csv_file_name)
    conditions, fractions, habit_messages, descriptions, header, categories, disabled_headers = get_data(variables_file)

    if not exists(csv_file_name):
        cols = [to_lower_underscored(item) for item in flatten_list(header)]
        cols.insert(0, date_header)
        data = DataFrame(columns=cols)
    else:
        data = read_csv(csv_file_name, csv_file_name)
    variables = list(data.columns)
    variables.pop(0)
    verify_header_and_data(header, variables, csv_file_name, data, disabled_headers)
    data = create_entry(data)
    # print_fonts()
    settings = read_settings(settings_file_name)
    InitUi(settings.hue_offset)
    hue_offset = settings.hue_offset
    neglected = no_data_from_yesterday(data)
    if neglected:
        neglected_window = NeglectedPopUp(neglected_accept_text, neglected_reject_text)
        while True:
            neglected_event, neglected_values_dic = neglected_window.read() # type: ignore
            if neglected_event == neglected_accept_text:
                neglected_data_window = MainWindow(categories, header, descriptions, done_button_text,
                                                   style_button_text, data_button_text, edit_button_text,
                                                   settings_button_text, len(data) >= 1, True)
                while True:
                    neglected_data_event, neglected_data_values_dict = neglected_data_window.read() # type: ignore
                    if neglected_data_event == done_button_text:
                        log_write(log, f"\nsaving data from yesterday\n{neglected_data_values_dict}")
                        save_data(data, neglected_data_values_dict, csv_file_name, get_yesterday_date().isoformat())
                    if neglected_data_event == sg.WIN_CLOSED or neglected_data_event == done_button_text:
                        neglected_window.close()
                        break
            if neglected_event == sg.WIN_CLOSED or neglected_event == neglected_reject_text:
                neglected_window.close()
                break
    todays_data = todays_data_or_none(data, header)
    window = MainWindow(categories, header, descriptions, done_button_text, style_button_text, data_button_text,
                        edit_button_text, settings_button_text, len(data) > 0, False, todays_data) # type: ignore
    while True:
        event, values_dict = window.read() # type: ignore
        if event == style_button_text:
            style_window = StyleWindow(style_button_text, slider_text_key, preview_window_text, set_button_text_key, hue_offset)
            while True:
                style_event, style_values_dict = style_window.read() # type: ignore
                if style_event == slider_text_key:
                    hue_offset = style_values_dict[slider_text_key]
                elif style_event == preview_window_text:
                    preview_window = PreviewWindow(preview_window_text, preview_close_key, hue_offset)
                    while True:
                        preview_event, preview_values_dict = preview_window.read() # type: ignore
                        if preview_event == preview_close_key or preview_event == sg.WIN_CLOSED:
                            preview_window.close()
                            break
                elif style_event == set_button_text_key or style_event == sg.WIN_CLOSED:
                    if style_event == set_button_text_key:
                        settings.hue_offset = normalize_hue(settings.hue_offset, hue_offset)
                        save_settings_file(settings, settings_file_name)
                    style_window.close()
                    break
        elif event == data_button_text:
            graph_data = read_csv(csv_file_name, csv_file_name)
            img = generate_image(categories, header, conditions, settings.data_days, settings.graph_expected_value, settings.weekdays_language, graph_data)
            data_window = DataWindow(data_button_text, export_button_text, settings.scrollable_image, image_bytes_to_base64(img))
            while True:
                data_event, data_values_dict = data_window.read() # type: ignore
                if data_event == export_button_text:
                    export_image_file_name = data_values_dict[export_button_text]
                    if export_image_file_name:
                        img.save(export_image_file_name)
                if data_event == sg.WIN_CLOSED or data_event == export_button_text:
                    data_window.close()
                    break
        elif event == edit_button_text:
            date_picker_window = DatePickerWindow(select_date_key, select_date_button_text)
            picked_date = get_today_date() + timedelta(days=-1)
            while True:
                date_picker_event, date_picker_dict = date_picker_window.read() # type: ignore
                if date_picker_event == select_date_button_text or date_picker_event == sg.WIN_CLOSED:
                    if date_picker_event is None and date_picker_dict is None:
                        date_picker_window.close()
                        break
                    picked_date = date_picker_dict[select_date_key]
                    data_from_date = data_from_date_to_list(data, picked_date, header)
                    edit_data_window = MainWindow(categories, header, descriptions, done_button_text, style_button_text,
                                                  data_button_text, edit_button_text, settings_button_text,
                                                  len(data) > 0, True, data_from_date)
                    while True:
                        edit_data_event, edit_data_values_dict = edit_data_window.read() # type: ignore
                        if edit_data_event == done_button_text:
                            log_write(log, f"\nsaving data from date '{picked_date}'\n{edit_data_values_dict}")
                            save_data(data, edit_data_values_dict, csv_file_name, picked_date)
                        if edit_data_event == sg.WIN_CLOSED or edit_data_event == done_button_text:
                            edit_data_window.close()
                            break
                    date_picker_window.close()
                    break
        elif event == settings_button_text:
            settings_window = SettingsWindow(settings, settings_button_text, settings_save_button_text, settings_cancel_button_text)
            while True:
                settings_event, settings_dict = settings_window.read() # type: ignore
                if settings_event in [settings_save_button_text, settings_cancel_button_text, sg.WIN_CLOSED]:
                    if settings_event == settings_save_button_text:
                        settings = Settings.from_dict(settings_dict)
                        save_settings_file(settings, settings_file_name)
                    settings_window.close()
                    break
        elif event == done_button_text or event == sg.WIN_CLOSED:
            if event == done_button_text:
                data = save_data(data, values_dict, csv_file_name)
                message = get_popup_message(conditions, fractions, habit_messages, header, data, msg_file_name, settings.random_messages)
                if message and settings.display_messages:
                    save_message_file(msg_file_name, header, message)
                    PopUp(message, settings.message_duration)
            break
    window.close()
except Exception as e:
    if __debug__:
        raise(e)
#   python -O main.py
    else:
        log_write(log, f"\n{format_exc()}\n")
finally:
    finally_string = f"***** {date.today()} - {datetime.now().time().replace(microsecond=0)} *****\n"
    if values_dict is not None and any(values_dict.values()):
        log_write(log, f"{finally_string}{values_dict}\n\n")
    else:
        log_write(log, f"{finally_string}")
    log.close()

# format code and fix error warninggs
# change text hover to white? or bright color idk

# TODO Disallow 0 on denominator
# TODO Disallow duplicate value for habit and category
# TODO Disallow freq > 1
# validate variables
#   duplicate columns
#   empty columns
#   handle empty tool tips
#   handle empty direction
#   handle empty frequency
# TODO validate variables on form?
# break code into smaller files? (core and ui into regions?)

# TODO LIST - REAL
# better ui
#   columns instead of spacing text
#   better width formula
# pop up after n days (settings) reminding to view data

#   FUTURE
#   have an indicator on the side of each row based on frequencies:
#       all good
#       improving, but still bad
#       declining, but still good
#       all bad
#   have some sort of readme?
#   TODO write reddit post!!!!!
#   (week challenge?!?!?!?!)
#       reward for completing challenge!!
#       or completing streaks(i.e. 30 days working out)
#
#   alerta baseado em tema conta mais:
#       exemplo: nao malhar e comer a mais
#       	 cel no trabalho e nao meditar
#       	 anime fap e jogar

#
#   COMPILE
#   Distribute as .py, add assets and a good readme

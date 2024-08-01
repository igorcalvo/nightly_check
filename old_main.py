from datetime import datetime, date
from traceback import format_exc

from source.constants import (
    data_folder,
    data_visualization_reminder_duration,
    FILE_NAMES,
    MESSAGES,
    SETTINGS_DEFAULT_VALUES,
    TEXTS_AND_KEYS,
)
from source.core.data_in import (
    get_data,
    get_data_dataframe,
    read_csv,
    read_messages,
    read_settings,
)
from source.core.data_out import (
    create_folder_if_doesnt_exist,
    create_file_if_doesnt_exist,
    log_write,
    save_data,
    save_message_file,
)
from source.core.data_date import create_entries, todays_data_or_none
from source.core.habit_messages import (
    get_message_data,
    get_popup_message,
    should_show_data_visualization_reminder,
)
from source.core.validation import (
    no_data_from_yesterday,
    verify_variables,
    verify_header_and_data,
)
from source.loops.data_vis import Data_Vis_Loop
from source.loops.edit import Edit_Loop
from source.loops.habit_init import Habit_Init_Loop
from source.loops.neglected import Neglected_Loop
from source.loops.settings import Settings_Loop
from source.ui.utils import init_ui
from source.utils import file_not_exists

values_dict = {}
create_folder_if_doesnt_exist(data_folder)
create_file_if_doesnt_exist(FILE_NAMES.log)
log = open(FILE_NAMES.log, "r+")

try:
    variables_exists = not file_not_exists(FILE_NAMES.var)
    if not variables_exists:
        init_ui(SETTINGS_DEFAULT_VALUES.hue_offset, SETTINGS_DEFAULT_VALUES.theme)
        Habit_Init_Loop(variables_exists)


    # print_fonts()
    settings = read_settings(FILE_NAMES.stg)
    messages = read_messages(FILE_NAMES.msg, settings.new_day_time)
    init_ui(settings.hue_offset, settings.theme)
    data = create_entries(settings.new_day_time, data)
    show_data_vis_reminder = should_show_data_visualization_reminder(
        settings.show_data_vis_reminder,
        settings.data_vis_reminder_days,
        settings.new_day_time,
        messages,
    )

    neglected = no_data_from_yesterday(settings.new_day_time, data)
    if neglected:
        Neglected_Loop(categories, habits, descriptions, data, settings, log)

    if show_data_vis_reminder:
        PopUp(
            MESSAGES.settings_data_vis_reminder_message,
            data_visualization_reminder_duration,
            True,
        )

    todays_data = todays_data_or_none(settings.new_day_time, data, habits)
    window = MainWindow(
        categories,
        habits,
        descriptions,
        len(data) > 0,
        False,
        todays_data,  # type: ignore
    )

    while True:
        event, values_dict = window.read()  # type: ignore
        if event == TEXTS_AND_KEYS.data_button_text:
            Data_Vis_Loop(categories, habits, conditions, settings)
        elif event == TEXTS_AND_KEYS.edit_button_text:
            Edit_Loop(
                settings.new_day_time, categories, habits, descriptions, data, log
            )
        elif event == TEXTS_AND_KEYS.settings_button_text:
            Settings_Loop(settings)
        elif event == TEXTS_AND_KEYS.done_button_text or event == WIN_CLOSED:
            if event == TEXTS_AND_KEYS.done_button_text:
                data = save_data(data, values_dict, FILE_NAMES.csv)
                message_data = get_message_data(
                    habits, categories, conditions, fractions, habit_messages, data
                )
                message = get_popup_message(
                    settings.new_day_time,
                    settings.random_messages,
                    conditions,
                    habit_messages,
                    habits,
                    data,
                    messages,
                    message_data,
                )
                if message and settings.display_messages:
                    save_message_file(
                        FILE_NAMES.msg,
                        messages,
                        message,
                        show_data_vis_reminder,
                        settings.new_day_time,
                    )
                    PopUp(message, settings.message_duration, True)
            break
    window.close()
except Exception as e:
    if __debug__:
        raise (e)
    #   python -O main.py
    else:
        log_write(log, f"\n{format_exc()}\n")
finally:
    finally_string = (
        f"***** {date.today()} - {datetime.now().time().replace(microsecond=0)} *****\n"
    )
    if values_dict is not None and any(values_dict.values()):
        log_write(log, f"{finally_string}{values_dict}\n\n")
    else:
        log_write(log, f"{finally_string}")
    log.close()

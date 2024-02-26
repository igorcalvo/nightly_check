from datetime import datetime, date
from traceback import format_exc
from PySimpleGUI import WIN_CLOSED

from source.constants import (
    MESSAGES,
    data_folder,
    SETTINGS_KEYS,
    FILE_NAMES,
    HABITS_INIT,
    TEXTS_AND_KEYS,
    SETTINGS_DEFAULT_VALUES,
    data_visualization_reminder_duration,
)
from source.utils import file_not_exists
from source.core.data_in import (
    get_data_dataframe,
    read_csv,
    get_data,
    read_messages,
    read_settings,
)
from source.core.data_out import (
    create_folder_if_doesnt_exist,
    create_file_if_doesnt_exist,
    save_data,
    log_write,
    save_settings_file,
    save_message_file,
)
from source.core.data_date import (
    create_entries,
    todays_data_or_none,
    data_from_date_to_list,
    get_yesterday_date,
)
from source.core.settings import Settings
from source.core.data_vis import image_bytes_to_base64
from source.core.habit_messages import (
    get_popup_message,
    should_show_data_visualization_reminder,
)
from source.core.habit_init import habit_index_from_event, generate_variables
from source.core.validation import (
    verify_variables,
    verify_header_and_data,
    no_data_from_yesterday,
)
from source.ui.habit_init import HabitsInitLayout, HabitsInitWindow, ReRenderHabitsInit
from source.ui.utils import (
    init_ui,
    preview_themes,
)
from source.ui.main_window import NeglectedPopUp, MainWindow, PopUp, DatePickerWindow
from source.ui.data import DataWindow
from source.ui.settings import PreviewWindow, SettingsWindow
from source.image_gen import generate_image

values_dict = {}
create_folder_if_doesnt_exist(data_folder)
create_file_if_doesnt_exist(FILE_NAMES.log)
log = open(FILE_NAMES.log, "r+")

try:
    if file_not_exists(FILE_NAMES.var):
        category_count = 0
        habit_count = []
        init_ui(SETTINGS_DEFAULT_VALUES.hue_offset, SETTINGS_DEFAULT_VALUES.theme)

        variables_init_layout = HabitsInitLayout(category_count, {}, habit_count)
        variables_init_window = HabitsInitWindow(variables_init_layout)
        while True:
            variables_init_event, variables_init_values_dict = variables_init_window.read()  # type: ignore
            if variables_init_event == HABITS_INIT.cat_add:
                category_count += 1
                habit_count.append(0)
            elif variables_init_event == HABITS_INIT.cat_remove:
                category_count -= 1
                habit_count.pop()
            elif HABITS_INIT.add_habit_text in variables_init_event:
                habit_count[habit_index_from_event(variables_init_event)] = (
                    habit_count[habit_index_from_event(variables_init_event)] + 1
                )
            elif HABITS_INIT.del_habit_text in variables_init_event:
                habit_count[habit_index_from_event(variables_init_event)] = (
                    habit_count[habit_index_from_event(variables_init_event)] - 1
                )
            elif variables_init_event == HABITS_INIT.generate_text:
                generate_variables(
                    FILE_NAMES.var, variables_init_values_dict, habit_count
                )
                variables_init_window.close()
                break
            elif variables_init_event == WIN_CLOSED:
                variables_init_window.close()
                break

            if (
                HABITS_INIT.track_frequency_key in variables_init_event
                or HABITS_INIT.del_habit_text in variables_init_event
                or HABITS_INIT.add_habit_text in variables_init_event
                or variables_init_event == HABITS_INIT.cat_remove
                or variables_init_event == HABITS_INIT.cat_add
            ):
                variables_init_window = ReRenderHabitsInit(
                    variables_init_window,
                    category_count,
                    variables_init_values_dict,
                    habit_count,
                )

    verify_variables(FILE_NAMES.var)
    variables_file = read_csv(FILE_NAMES.var)

    (
        conditions,
        fractions,
        habit_messages,
        descriptions,
        habits,
        categories,
        disabled_habits,
    ) = get_data(variables_file)
    data = get_data_dataframe(habits)
    variables = list(data.columns)
    variables.pop(0)
    verify_header_and_data(habits, variables, FILE_NAMES.csv, data, disabled_habits)

    # print_fonts()
    settings = read_settings(FILE_NAMES.stg)
    messages = read_messages(FILE_NAMES.msg, settings.new_day_time)
    init_ui(settings.hue_offset, settings.theme)
    hue_offset = settings.hue_offset
    theme = settings.theme
    data = create_entries(settings.new_day_time, data)
    show_data_vis_reminder = should_show_data_visualization_reminder(
        settings.show_data_vis_reminder, settings.data_vis_reminder_days, messages
    )

    neglected = no_data_from_yesterday(settings.new_day_time, data)
    if neglected:
        neglected_window = NeglectedPopUp()
        while True:
            neglected_event, neglected_values_dic = neglected_window.read()  # type: ignore
            if neglected_event == TEXTS_AND_KEYS.neglected_accept_text:
                neglected_data_window = MainWindow(
                    categories,
                    habits,
                    descriptions,
                    len(data) >= 1,
                    True,
                )
                while True:
                    neglected_data_event, neglected_data_values_dict = neglected_data_window.read()  # type: ignore
                    if neglected_data_event == TEXTS_AND_KEYS.done_button_text:
                        log_write(
                            log,
                            f"\nsaving data from yesterday\n{neglected_data_values_dict}",
                        )
                        save_data(
                            data,
                            neglected_data_values_dict,
                            FILE_NAMES.csv,
                            get_yesterday_date(
                                settings.new_day_time,
                            ).isoformat(),
                        )
                    if (
                        neglected_data_event == WIN_CLOSED
                        or neglected_data_event == TEXTS_AND_KEYS.done_button_text
                    ):
                        neglected_window.close()
                        break
            if (
                neglected_event == WIN_CLOSED
                or neglected_event == TEXTS_AND_KEYS.neglected_reject_text
            ):
                neglected_window.close()
                break

    todays_data = todays_data_or_none(settings.new_day_time, data, habits)
    window = MainWindow(
        categories,
        habits,
        descriptions,
        len(data) > 0,
        False,
        todays_data,  # type: ignore
    )
    if show_data_vis_reminder:
        PopUp(
            MESSAGES.settings_data_vis_reminder_message,
            data_visualization_reminder_duration,
        )
    while True:
        event, values_dict = window.read()  # type: ignore
        if event == TEXTS_AND_KEYS.data_button_text:
            graph_data = read_csv(FILE_NAMES.csv)
            img = generate_image(
                categories,
                habits,
                conditions,
                settings.data_days,
                settings.graph_expected_value,
                settings.weekdays_language,
                graph_data,
            )
            data_window = DataWindow(
                settings.scrollable_image, image_bytes_to_base64(img)
            )
            while True:
                data_event, data_values_dict = data_window.read()  # type: ignore
                if data_event == TEXTS_AND_KEYS.export_button_text:
                    export_image_file_name = data_values_dict[
                        TEXTS_AND_KEYS.export_button_text
                    ]
                    if export_image_file_name:
                        img.save(export_image_file_name)
                if (
                    data_event == WIN_CLOSED
                    or data_event == TEXTS_AND_KEYS.export_button_text
                ):
                    data_window.close()
                    break
        elif event == TEXTS_AND_KEYS.edit_button_text:
            picked_date = str(get_yesterday_date(settings.new_day_time))
            date_picker_window = DatePickerWindow(picked_date)
            while True:
                date_picker_event, date_picker_dict = date_picker_window.read()  # type: ignore
                if (
                    date_picker_event == TEXTS_AND_KEYS.select_date_button_text
                    or date_picker_event == WIN_CLOSED
                ):
                    if date_picker_event is None and date_picker_dict is None:
                        date_picker_window.close()
                        break
                    picked_date = date_picker_dict[TEXTS_AND_KEYS.select_date_key]
                    data_from_date = data_from_date_to_list(data, picked_date, habits)
                    edit_data_window = MainWindow(
                        categories,
                        habits,
                        descriptions,
                        len(data) > 0,
                        True,
                        data_from_date,
                    )
                    while True:
                        edit_data_event, edit_data_values_dict = edit_data_window.read()  # type: ignore
                        if edit_data_event == TEXTS_AND_KEYS.done_button_text:
                            log_write(
                                log,
                                f"\nsaving data from date '{picked_date}'\n{edit_data_values_dict}",
                            )
                            save_data(
                                data, edit_data_values_dict, FILE_NAMES.csv, picked_date
                            )
                        if (
                            edit_data_event == WIN_CLOSED
                            or edit_data_event == TEXTS_AND_KEYS.done_button_text
                        ):
                            edit_data_window.close()
                            break
                    date_picker_window.close()
                    break
        elif event == TEXTS_AND_KEYS.settings_button_text:
            settings_window = SettingsWindow(settings)
            old_hue_offset = settings.hue_offset
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
        elif event == TEXTS_AND_KEYS.done_button_text or event == WIN_CLOSED:
            if event == TEXTS_AND_KEYS.done_button_text:
                data = save_data(data, values_dict, FILE_NAMES.csv)
                message = get_popup_message(
                    settings.new_day_time,
                    conditions,
                    fractions,
                    habit_messages,
                    habits,
                    categories,
                    data,
                    messages,
                    settings.random_messages,
                )
                if message and settings.display_messages:
                    save_message_file(
                        FILE_NAMES.msg, messages, message, show_data_vis_reminder
                    )
                    PopUp(message, settings.message_duration)
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

# ui habit init description for fields, just tooltip is too ambiguous
# ui to load habits.csv (load init habit)
# identidade visual: patrolling owl
# ship with scripts to run before shutdown
# more consistent typing list -> list[list[str]]
# sort imports

# MAJOR
#   *** Validation ***
#       Freq
#           Disallow 0 on denominator
#           Disallow duplicate value for habit and category
#           Disallow freq > 1
#       Variables
#           duplicate categories
#           duplicate headers
#           empty categories
#           handle empty tool tips
#           handle empty direction
#           handle empty frequency
#       validate variables on form even possible?
#   Indicator
#       have an indicator on the side of each row based on frequencies:
#           all good
#           improving, but still bad
#           declining, but still good
#           all bad

# FUTURE
#   (week challenge?!?!?!?!)
#       reward for completing challenge!!
#       or completing streaks(i.e. 30 days working out)
#
#   alerta baseado em tema conta mais:
#       exemplo: nao malhar e comer a mais
#       	 cel no trabalho e nao meditar
#       	 anime e jogar
#       for that, we'll have to link the habits somehow
#   migrate to Qt? -> fix icons in titlebar

#   COMPILE and SHIP
#       README.md
#       Reddit post HG, Producitivy, Linux
#       Capture video for clarity
#       Lots of screenshots
#       Distribute as .py, add assets

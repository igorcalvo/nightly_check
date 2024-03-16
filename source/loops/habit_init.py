from PySimpleGUI import WIN_CLOSED
from source.constants import FILE_NAMES, HABITS_INIT
from source.core.data_in import read_csv
from source.core.data_out import backup_data
from source.core.habit_init import (
    clear_habit_row,
    generate_variables,
    habit_index_from_event,
    variables_to_habitcount_and_dict,
)
from source.ui.habit_init import HabitsInitLayout, HabitsInitWindow, ReRenderHabitsInit

habit_count = []


def Habit_Init_Loop(variables_exists: bool):
    global habit_count
    variables_init_layout = HabitsInitLayout({}, habit_count, variables_exists)
    variables_init_window = HabitsInitWindow(variables_init_layout)
    while True:
        variables_init_event, variables_init_values_dict = variables_init_window.read()  # type: ignore
        if variables_init_event == HABITS_INIT.cat_add:
            habit_count.append(0)
        elif variables_init_event == HABITS_INIT.cat_remove:
            habit_count.pop()
        elif variables_init_event == WIN_CLOSED:
            variables_init_window.close()
            break
        elif HABITS_INIT.habit_clear_key in variables_init_event:
            row_key = variables_init_event.replace(HABITS_INIT.habit_clear_key, "")
            variables_init_values_dict = clear_habit_row(
                variables_init_values_dict, row_key
            )
        elif HABITS_INIT.add_habit_text in variables_init_event:
            habit_count[habit_index_from_event(variables_init_event)] = (
                habit_count[habit_index_from_event(variables_init_event)] + 1
            )
        elif HABITS_INIT.del_habit_text in variables_init_event:
            habit_count[habit_index_from_event(variables_init_event)] = (
                habit_count[habit_index_from_event(variables_init_event)] - 1
            )
        elif variables_init_event == HABITS_INIT.generate_text:
            if variables_exists:
                backup_data(FILE_NAMES.var, read_csv(FILE_NAMES.var))
            generate_variables(FILE_NAMES.var, variables_init_values_dict, habit_count)
            variables_init_window.close()
            break
        elif variables_init_event == HABITS_INIT.load_file_key:
            habit_count, variables_init_values_dict = variables_to_habitcount_and_dict(
                FILE_NAMES.var
            )
            variables_init_window = ReRenderHabitsInit(
                variables_init_window,
                variables_init_values_dict,
                habit_count,
                variables_exists,
            )
        if (
            HABITS_INIT.track_frequency_key in variables_init_event
            or HABITS_INIT.del_habit_text in variables_init_event
            or HABITS_INIT.add_habit_text in variables_init_event
            or HABITS_INIT.habit_clear_key in variables_init_event
            or variables_init_event == HABITS_INIT.cat_remove
            or variables_init_event == HABITS_INIT.cat_add
        ):
            variables_init_window = ReRenderHabitsInit(
                variables_init_window,
                variables_init_values_dict,
                habit_count,
                variables_exists,
            )

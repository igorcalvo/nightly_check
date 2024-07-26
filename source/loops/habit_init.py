from source.constants import FILE_NAMES
from source.core.data_in import read_csv
from source.core.data_out import backup_data
from source.core.habit_init import (
    generate_variables,
)

def Habit_Init_Loop(variables_exists: bool):
    if variables_exists:
        backup_data(FILE_NAMES.var, read_csv(FILE_NAMES.var))
    generate_variables(FILE_NAMES.var, variables_init_values_dict, habit_count)

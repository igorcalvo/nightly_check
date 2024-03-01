from pandas._libs.tslibs.period import freq_to_dtype_code
from source.core.data_in import read_csv
from source.utils import (
    habit_init_key,
    values_from_keyword,
    replace_commas_for_double_spaces,
    join_white_spaced_habit,
    flatten_list,
)
from source.constants import HABITS_INIT, VARIABLES_KEYS, variables_csv_header


def habit_index_from_event(event: str):
    number = event.split("_")[-1]
    return int(number) - 1


def variables_row(
    category: str,
    habit: str,
    tooltip: str,
    message: str,
    condition: str,
    numerator: str,
    denominator: str,
):
    condition = condition.strip()
    empty_conditions = ["", None, "-", "_", " "]
    valid_conditions = empty_conditions + [">=", ">", "=", "<", "<="]
    if condition not in valid_conditions:
        raise Exception(
            f"variables_row: condition '{condition}' not in valid_conditions: '{valid_conditions}'"
        )
    if condition in valid_conditions and numerator in ("", " ", "0"):
        condition = ""

    result = ""
    slap = (
        ",,"
        if condition in empty_conditions
        else f"{replace_commas_for_double_spaces(message)},{condition},{numerator}/{denominator}"
    )
    result += f"1,{category.lower()},{join_white_spaced_habit(habit.lower())},{tooltip},{slap}\n"
    return result


def generate_variables(
    variables_file_name: str,
    variables_init_values_dict: dict,
    habit_count: list,
):
    categories = values_from_keyword(
        HABITS_INIT.category_key, variables_init_values_dict
    )
    repeated_categories = flatten_list(
        [[categories[idx] for i in range(item)] for idx, item in enumerate(habit_count)]
    )
    habits = values_from_keyword(HABITS_INIT.habit_key, variables_init_values_dict)
    questions = values_from_keyword(
        HABITS_INIT.question_key, variables_init_values_dict
    )
    messages = values_from_keyword(HABITS_INIT.message_key, variables_init_values_dict)
    conditions = values_from_keyword(
        HABITS_INIT.condition_key, variables_init_values_dict
    )
    numerators = values_from_keyword(
        HABITS_INIT.fraction_num_key, variables_init_values_dict
    )
    denominators = values_from_keyword(
        HABITS_INIT.fraction_den_key, variables_init_values_dict
    )

    file_content = f"{variables_csv_header}\n"
    for i in range(len(repeated_categories)):
        row = variables_row(
            repeated_categories[i],
            habits[i],
            questions[i],
            messages[i],
            conditions[i],
            numerators[i],
            denominators[i],
        )
        file_content += row

    with open(variables_file_name, "w") as v:
        v.write(file_content)
        v.close()


def variables_to_habitcount_and_dict(
    variables_path: str,
) -> tuple[list[int], dict[str, str]]:
    variables = read_csv(variables_path)
    variables.to_csv(variables_path.replace("variables", "test"))

    categories = []
    habits = []
    dictionary = {}

    for index, row in variables.iterrows():
        if row[VARIABLES_KEYS.category] not in categories:
            categories.append(row[VARIABLES_KEYS.category])
            habits.append(0)
            dictionary[
                habit_init_key(
                    HABITS_INIT.category_key,
                    len(habits),
                    int(habits[-1]),
                )
            ] = row[VARIABLES_KEYS.category]

        track_freq = row[VARIABLES_KEYS.frequency] != ""
        numerator = "" if row[VARIABLES_KEYS.frequency] == "" else row[VARIABLES_KEYS.frequency].split("/")[0]  # type: ignore
        denominator = "" if row[VARIABLES_KEYS.frequency] == "" else row[VARIABLES_KEYS.frequency].split("/")[1]  # type: ignore

        habits[-1] = habits[-1] + 1
        key_row = len(habits)
        key_sub_row = int(habits[-1]) - 1

        dictionary[habit_init_key(HABITS_INIT.habit_key, key_row, key_sub_row)] = row[
            VARIABLES_KEYS.habit
        ]
        dictionary[habit_init_key(HABITS_INIT.question_key, key_row, key_sub_row)] = (
            row[VARIABLES_KEYS.question]
        )
        dictionary[
            habit_init_key(HABITS_INIT.track_frequency_key, key_row, key_sub_row)
        ] = track_freq
        dictionary[habit_init_key(HABITS_INIT.message_key, key_row, key_sub_row)] = row[
            VARIABLES_KEYS.message
        ]
        dictionary[habit_init_key(HABITS_INIT.condition_key, key_row, key_sub_row)] = (
            row[VARIABLES_KEYS.condition]
        )
        dictionary[
            habit_init_key(HABITS_INIT.fraction_num_key, key_row, key_sub_row)
        ] = numerator
        dictionary[
            habit_init_key(HABITS_INIT.fraction_den_key, key_row, key_sub_row)
        ] = denominator

    return (habits, dictionary)

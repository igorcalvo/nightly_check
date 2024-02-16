from source.utils import (
    values_from_keyword,
    replace_commas_for_double_spaces,
    join_white_spaced_header,
    flatten_list,
)


def habit_index_from_event(event: str):
    number = event.split("_")[-1]
    return int(number) - 1


def variables_row(
    category: str,
    header: str,
    tooltip: str,
    message: str,
    condition: str,
    numerator: str,
    denominator: str,
):
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
    result += f"1,{category.lower()},{join_white_spaced_header(header.lower())},{tooltip},{slap}\n"
    return result


def generate_variables(
    variables_file_name: str,
    variables_init_values_dict: dict,
    habits_init_category_key: str,
    habits_init_habit_key: str,
    habits_init_question_key: str,
    habit_count: list,
    habits_init_message_key: str,
    habits_init_condition_key: str,
    habits_init_fraction_num_key: str,
    habits_init_fraction_den_key: str,
):
    categories = values_from_keyword(
        habits_init_category_key, variables_init_values_dict
    )
    repeated_categories = flatten_list(
        [[categories[idx] for i in range(item)] for idx, item in enumerate(habit_count)]
    )
    habits = values_from_keyword(habits_init_habit_key, variables_init_values_dict)
    questions = values_from_keyword(
        habits_init_question_key, variables_init_values_dict
    )
    messages = values_from_keyword(habits_init_message_key, variables_init_values_dict)
    conditions = values_from_keyword(
        habits_init_condition_key, variables_init_values_dict
    )
    numerators = values_from_keyword(
        habits_init_fraction_num_key, variables_init_values_dict
    )
    denominators = values_from_keyword(
        habits_init_fraction_den_key, variables_init_values_dict
    )

    header = "enabled,category,header,tooltip,message,condition,frequency"
    file_content = f"{header}\n"
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

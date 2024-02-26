from pandas import DataFrame, read_csv as pandas_read_csv

from source.constants import FILE_NAMES, date_header, messages_csv_header
from source.core.data_date import create_entry, get_today_date
from source.utils import (
    replace_commas_for_double_spaces,
    replace_double_spaces_for_commas,
    flatten_list,
    to_capitalized,
    remove_duplicates,
    file_not_exists,
    to_lower_underscored,
)
from source.core.settings import Settings


def read_csv(file_name: str) -> DataFrame:
    with open(file_name, "r") as file:
        lines = file.readlines()
        file.close()
    header = lines[0].replace("\n", "").split(",")
    if file_name == FILE_NAMES.csv:
        content = [
            stringLine.replace("\n", "")
            .replace(",1", ",True")
            .replace(",0", ",False")
            .split(",")
            for stringLine in lines[1:]
        ]
    else:
        content = [
            replace_commas_for_double_spaces(stringLine).replace("\n", "").split(",")
            for stringLine in lines[1:]
        ]
        content = [
            [replace_double_spaces_for_commas(string) for string in habit_row]
            for habit_row in content
        ]
    df = DataFrame(content, columns=header)
    return df


def get_data_dataframe(habits: list) -> DataFrame:
    if file_not_exists(FILE_NAMES.csv):
        cols = [to_lower_underscored(item) for item in flatten_list(habits)]
        cols.insert(0, date_header)
        return DataFrame(columns=cols)
    else:
        return read_csv(FILE_NAMES.csv)


def group_by_category(dataframe: DataFrame, column: str) -> list[list]:
    enabled_column = "enabled"
    category_column = "category"
    capitalized_columns = ["habit"]
    categories = remove_duplicates(dataframe[category_column])
    result = []
    for category in categories:
        column_data = list(
            dataframe.loc[
                (dataframe[category_column] == category)
                & (dataframe[enabled_column] == "1")
            ][column]
        )
        result.append(
            [
                to_capitalized(x) if column in capitalized_columns else x
                for x in column_data
            ]
        )
    return result


def get_category(habit: str, habits: list[list[str]], categories: list[str]) -> str:
    for idx, cat in enumerate(habits):
        if habit in cat:
            return categories[idx]
    raise Exception(f"get_category: couldn't find category for {habit}")


def get_data(variables_file):
    fractions = group_by_category(variables_file, "frequency")
    conditions = group_by_category(variables_file, "condition")
    habit_messages = group_by_category(variables_file, "message")
    descriptions = group_by_category(variables_file, "tooltip")
    habits = group_by_category(variables_file, "habit")
    categories = remove_duplicates(
        flatten_list(group_by_category(variables_file, "category"))
    )
    disabled_habits = list(
        variables_file.loc[(variables_file["enabled"] == "0")]["habit"]
    )
    return (
        conditions,
        fractions,
        habit_messages,
        descriptions,
        habits,
        categories,
        disabled_habits,
    )


def get_matrix_data_by_header_indexes(
    other_matrix: list[list[str]], habit_matrix: list[list[str]], header_value: str
) -> str:
    for idx1, sublist in enumerate(habit_matrix):
        for idx2, item in enumerate(sublist):
            if item == header_value:
                return other_matrix[idx1][idx2]
    print(
        "get_matrix_data_by_header_indexes: Couldn't find description for: "
        + header_value
    )
    return ""


def read_settings(settings_file_name: str) -> Settings:
    settings: Settings = Settings()
    if file_not_exists(settings_file_name):
        with open(settings_file_name, "w") as s:
            s.write(settings.to_json())
            s.close()

    with open(settings_file_name, "r") as s:
        settings_file_content = s.read()
        settingsObj = Settings.from_json(settings_file_content)
        s.close()
    return settingsObj


def read_messages(messages_file_name: str, new_day_time: int) -> DataFrame:
    if file_not_exists(messages_file_name):
        messages = DataFrame(columns=messages_csv_header.split(","))
    else:
        messages = pandas_read_csv(FILE_NAMES.msg)
        messages.fillna("")

    today = get_today_date(new_day_time)
    if today not in list(messages[date_header].values):
        messages = create_entry(today, messages)

    return messages

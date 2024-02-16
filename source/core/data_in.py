from pandas import DataFrame
from os.path import exists

from source.constants import FILE_NAMES, date_header
from source.utils import (
    replace_commas_for_double_spaces,
    replace_double_spaces_for_commas,
    flatten_list,
    to_capitalized,
    remove_duplicates,
    file_not_exists,
    to_lower_underscored,
)
from source.core.validation import rid_message_file_of_blank_lines
from source.core.settings import Settings


def read_csv(file_name: str):
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


def get_data_dataframe(header: list) -> DataFrame:
    if file_not_exists(FILE_NAMES.csv):
        cols = [to_lower_underscored(item) for item in flatten_list(header)]
        cols.insert(0, date_header)
        return DataFrame(columns=cols)
    else:
        return read_csv(FILE_NAMES.csv)


def group_by_category(dataframe: DataFrame, column: str) -> list:
    enabled_column = "enabled"
    category_column = "category"
    capitalized_columns = ["header"]
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


def get_data(variables_file):
    fractions = group_by_category(variables_file, "frequency")
    conditions = group_by_category(variables_file, "condition")
    habit_messages = group_by_category(variables_file, "message")
    descriptions = group_by_category(variables_file, "tooltip")
    header = group_by_category(variables_file, "header")
    categories = remove_duplicates(
        flatten_list(group_by_category(variables_file, "category"))
    )
    disabled_headers = list(
        variables_file.loc[(variables_file["enabled"] == "0")]["header"]
    )
    return (
        conditions,
        fractions,
        habit_messages,
        descriptions,
        header,
        categories,
        disabled_headers,
    )


def get_matrix_data_by_header_indexes(
    other_matrix: list, header_matrix: list, header_value: str
) -> str:
    for idx1, sublist in enumerate(header_matrix):
        for idx2, item in enumerate(sublist):
            if item == header_value:
                return other_matrix[idx1][idx2]
    print(
        "get_matrix_data_by_header_indexes: Couldn't find description for: "
        + header_value
    )
    return ""


def read_past_messages(msg_file_name: str) -> tuple[list | None, str | None]:
    if not exists(msg_file_name):
        return None, None
    else:
        rid_message_file_of_blank_lines(msg_file_name)
        with open(msg_file_name, "r") as f:
            # lines = [l.split('\t')[-1].replace('\n', '') for l in f.readlines()]
            lines = [l.replace("\t\t", "\t").split("\t") for l in f.readlines()]
            f.close()
            return [f"{l[1]}\n{l[2]}" for l in lines], lines[-1][0]


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

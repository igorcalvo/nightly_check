from collections.abc import Iterable
from pandas import DataFrame
from os.path import exists, getsize
from sys import platform


def pad_string(string: str, length: int) -> str:
    return string.ljust(length)


def to_lower_underscored(string: str) -> str:
    return string.replace(" ", "_").lower()


def to_capitalized(string: str) -> str:
    dirty_fixes = {"GG": "GG"}
    return " ".join(
        [
            s.capitalize() if s not in dirty_fixes.keys() else dirty_fixes[s]
            for s in string.split(" ")
        ]
    )


def settings_key_to_text(key: str) -> str:
    return " ".join([c.capitalize() for c in key.split("_")])


def flatten_list(l: list) -> list:
    return [item for sublist in l for item in sublist]


def flatten_list_recursive(l: list, partial=[]) -> list:
    result = partial
    deeper = []
    for item in l:
        if type(item) == type([]):
            deeper.append(flatten_list_recursive(item, result))
        else:
            result.append(item)
    return result


def flatten_list_1(l: list) -> list:
    result = []
    for item in l:
        if type(item) == type([]):
            for i in item:
                result.append(i)
        else:
            result.append(item)
    return result


def wrap_list_items_in_list(l: list) -> list[list]:
    return [[item] for item in l]


def flatten_and_wrap(l: list) -> list[list]:
    flat_list = flatten_list_recursive(l, [])
    return wrap_list_items_in_list(flat_list)


def flatten_and_wrap_1(l: list) -> list[list]:
    flat_list = flatten_list_1(l)
    return wrap_list_items_in_list(flat_list)


def get_value_from_df_by_row(colName: str, row: int, data: DataFrame):
    return data.iloc[row, data.columns.get_loc(colName)]


def align_right(string: str, length: int) -> str:
    return string.rjust(length)


def cycle_index(obj, index):
    corrected_index = index
    if abs(index) > len(obj):
        div = abs(index) // len(obj)
        direction = 1 if index >= 0 else -1
        corrected_index = index - direction * div * len(obj)
    elif corrected_index == -len(obj):
        corrected_index = 0
    return obj[corrected_index]


def get_value_from_df_by_value(colName: str, value, data: DataFrame):
    return data.loc[data[colName] == value]


def remove_duplicates(arr: Iterable) -> list:
    seen = set()
    seen_add = seen.add
    return [x for x in arr if not (x in seen or seen_add(x))]


def df_row_from_date(df: DataFrame, date: str, date_header: str):
    row_from_date = df.loc[(df[date_header] == date)]
    return row_from_date


def safe_value_from_dict(key, dictionary: dict):
    if key in dictionary.keys():
        return dictionary[key]
    else:
        return None


def safe_bool_from_array(index, array: list):
    if array is None:
        return True

    if index < len(array):
        return array[index] < 1
    else:
        return False


def safe_value_from_array(index, array: list, default_value):
    if array is None:
        return 0

    if index < len(array):
        return array[index]
    else:
        return default_value


def habit_init_key(key: str, row: int, sub_row: int = 0):
    return f"{key}_{row}" if sub_row == 0 else f"{key}_{row}_{sub_row}"


def replace_commas_for_double_spaces(string: str) -> str:
    return string.replace(", ", "  ")


def replace_double_spaces_for_commas(string: str) -> str:
    return string.replace("  ", ", ")


def join_white_spaced_header(string: str) -> str:
    return string.replace(" ", "-")


def values_from_keyword(keyword: str, dictionary: dict):
    keys = [k for k in dictionary.keys() if keyword in k]
    keys.sort()
    values = [dictionary[key] for key in keys]
    return values


def os_is_windows() -> bool:
    return False if platform == "linux" else True


def file_not_exists(file_name) -> bool:
    return not exists(file_name) or getsize(file_name) == 0


def date_ymd_to_mdy(date_str: str) -> tuple[int, int, int]:
    date_list = date_str.split("-")
    return (int(date_list[1]), int(date_list[2]), int(date_list[0]))

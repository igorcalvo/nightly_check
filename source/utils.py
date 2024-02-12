from base64 import b64encode
from collections.abc import Iterable
from io import BytesIO
from pandas import DataFrame
from sys import platform

def group_list_if_char(flatList: list, ch: str) -> list:
    result = []
    separator_indexes = [i for i, x in enumerate(flatList) if x == ch]
    for i in range(len(separator_indexes) + 1):
        result.append([])
    index = 0
    for ind, item in enumerate(flatList):
        if item == ch:
            continue
        try:
            if ind + 1 > separator_indexes[index]:
                index += 1
        except:
            pass
        result[index].append(item)
    return result

def split_list(alist: list, parts: int = 1) -> list:
    length = len(alist)
    return [alist[i*length // parts: (i+1)*length // parts] for i in range(parts)]

def pad_string(string: str, length: int) -> str:
    return string.ljust(length)

def transpose(alist: list, emptyItem='') -> list:
    max_dims = [len(sublist) for sublist in alist]
    dim1 = len(alist)
    dim2 = max(max_dims)

    result = []
    for i in range(dim2):
        result.append([emptyItem for item in range(dim1)])

    for a in range(dim2):
        for b in range(dim1):
            value = emptyItem
            try:
                value = alist[b][a]
            except:
                pass
            finally:
                result[a][b] = value
    return result

def to_lower_underscored(string: str) -> str:
    return string.replace(' ', '_').lower()

def to_capitalized(string: str) -> str:
    dirty_fixes = {'GG': 'GG'}
    return ' '.join([s.capitalize() if s not in dirty_fixes.keys() else dirty_fixes[s] for s in string.split(' ')])

def settings_key_to_text(key: str) -> str:
    return ' '.join([c.capitalize() for c in key.split('_')])

def flatten_list(l: list) -> list:
    return [item for sublist in l for item in sublist]

def get_value_from_df_by_row(colName: str, row: int, data: DataFrame):
    return data.iloc[row, data.columns.get_loc(colName)]

def clean_df(data: DataFrame):
    return data.dropna().iloc[:-1]

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

def image_bytes_to_base64(image) -> str:
    in_memory_file = BytesIO()
    image.save(in_memory_file, format="PNG")
    in_memory_file.seek(0)
    img_bytes = in_memory_file.read()
    base64_bytes = b64encode(img_bytes)
    base64_str = base64_bytes.decode('ascii')
    return base64_str

def remove_duplicates(arr: Iterable) -> list:
    seen = set()
    seen_add = seen.add
    return [x for x in arr if not (x in seen or seen_add(x))]

def df_row_from_date(df: DataFrame, date: str, date_header: str):
    row_from_date = df.loc[(df[date_header] == date)]
    return row_from_date

def safe_value_from_dict(key, dictionary: dict, return_bool: bool = False):
    if key in dictionary.keys():
        return dictionary[key]
    else:
        return None if not return_bool else False

def safe_bool_from_array(index, array: list):
    if array is None:
        return True

    if index < len(array):
        return array[index] < 1
    else:
        return False

def safe_value_from_array(index, array: list):
    if array is None:
        return 0
    return array[index]

def habit_init_key(key: str, row: int, sub_row: int = 0):
    return f'{key}_{row}' if sub_row == 0 else f'{key}_{row}_{sub_row}'

def replace_commas_for_double_spaces(string: str) -> str:
    return string.replace(', ', '  ')

def replace_double_spaces_for_commas(string: str) -> str:
    return string.replace('  ', ', ')

def join_white_spaced_header(string: str) -> str:
    return string.replace(' ', '-')

def values_from_keyword(keyword: str, dictionary: dict):
    keys = [k for k in dictionary.keys() if keyword in k]
    keys.sort()
    values = [dictionary[key] for key in keys]
    return values

def os_is_windows() -> bool:
    return False if platform == 'linux' else True

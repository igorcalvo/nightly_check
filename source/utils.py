from base64 import b64encode
from io import BytesIO

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
    return ' '.join([s.capitalize() for s in string.split(' ')])

def flatten_list(l: list) -> list:
    return [item for sublist in l for item in sublist]

def get_value_from_df_by_row(colName: str, row: int, data):
    return data.iloc[row, data.columns.get_loc(colName)]

def clean_df(data):
    return data.dropna().iloc[:-1]

def align_right(string: str, length: int) -> str:
    return string.rjust(length)

def cycle_index(obj, index):
    corrected_index = index
    if abs(index) > len(obj):
        div = abs(index) // len(obj)
        direction = 1 if index >= 0 else -1
        corrected_index = index - direction * div * len(obj) - 1
    return obj[corrected_index]

def get_value_from_df_by_value(colName: str, value, data):
    return data.loc[data[colName] == value]

def image_bytes_to_base64(image) -> str:
    in_memory_file = BytesIO()
    image.save(in_memory_file, format="PNG")
    in_memory_file.seek(0)
    img_bytes = in_memory_file.read()
    base64_bytes = b64encode(img_bytes)
    base64_str = base64_bytes.decode('ascii')
    return base64_str

def remove_duplicates(arr: list) -> list:
    seen = set()
    seen_add = seen.add
    return [x for x in arr if not (x in seen or seen_add(x))]
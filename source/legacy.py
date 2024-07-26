from pandas import DataFrame
from sys import platform

def group_list_if_char(flatList: list, ch: str) -> list[list]:
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
    return [
        alist[i * length // parts : (i + 1) * length // parts] for i in range(parts)
    ]


def transpose(alist: list, emptyItem="") -> list:
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


def clean_df(data: DataFrame):
    return data.dropna().iloc[:-1]


def os_is_windows() -> bool:
    return False if platform == "linux" else True

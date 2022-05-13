
def GroupListIfChar(flatList: list, ch: str) -> list:
    result = []
    separatorIndexes = [i for i, x in enumerate(flatList) if x == ch]
    for i in range(len(separatorIndexes) + 1):
        result.append([])
    index = 0
    for ind, item in enumerate(flatList):
        if item == ch:
            continue
        try:
            if ind + 1 > separatorIndexes[index]:
                index += 1
        except:
            pass
        result[index].append(item)
    return result

def SplitList(alist: list, parts: int = 1) -> list:
    length = len(alist)
    return [alist[i*length // parts: (i+1)*length // parts] for i in range(parts)]

def PadString(string: str, length: int) -> str:
    return string.ljust(length)

def Transpose(alist: list, emptyItem='') -> list:
    maxDims = [len(sublist) for sublist in alist]
    dim1 = len(alist)
    dim2 = max(maxDims)

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

def ToLowerUnderScored(string: str) -> str:
    return string.replace(' ', '_').lower()

def FlattenList(l: list) -> list:
    return [item for sublist in l for item in sublist]

def GetValueFromDF(colName: str, row: int, data):
    return data.iloc[row, data.columns.get_loc(colName)]

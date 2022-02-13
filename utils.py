

def SplitList(alist: list, parts: int = 1) -> list:
    length = len(alist)
    return [alist[i*length // parts: (i+1)*length // parts] for i in range(parts)]

def PadString(string: str, length: int) -> str:
    return string.ljust(length)

def Transpose(alist: list, emptyItem = '') -> list:
    maxdims = [len(sublist) for sublist in alist]
    dim1 = len(alist)
    dim2 = max(maxdims)

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


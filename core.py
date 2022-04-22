from datetime import date, timedelta
from os.path import exists

# .csv

def CheckForTodaysEntry(lastDate: str) -> int:
    try:
        delta = date.today() - date.fromisoformat(lastDate)
    except:
        raise Exception("Can't parse the data, it needs to be in the format 'yyyy-mm-dd'. \nDatabase probably got corrupted.")
    return delta.days

def GetLatestDate(data) -> str:
    return data.iloc[-1]['date']

def CreateEntry(data):
    lastDate: str = GetLatestDate(data)
    deltaDays = CheckForTodaysEntry(data.iloc[-1]['date'])
    if deltaDays > 1:
        di = dict.fromkeys(data.columns.values, '')
        for day in range(deltaDays):
            newDate = date.fromisoformat(lastDate)
            di['date'] = str(newDate + timedelta(days=(day + 1)))
            data = data.append((di), ignore_index=True)
    return data

# .txt

def ParseHeader(field: str, tags: list) -> str:
    parts = field.split("_")
    for p in (parts):
        if (p in tags):
            parts.pop(parts.index(p))
    for i, p in enumerate(parts):
        parts[i] = p.replace("\n", "").capitalize()
    result = " ".join(parts)
    return result

def GroupListIfChar(flatList: list, ch: str) -> list:
    result = []
    separtorIndexes = [i for i, x in enumerate(flatList) if x == ch]
    for i in range(len(separtorIndexes) + 1):
        result.append([])
    index = 0
    for ind, item in enumerate(flatList):
        if item == ch:
            continue
        try:
            if ind + 1 > separtorIndexes[index]:
                index += 1
        except:
            pass
        result[index].append(item)
    return result

def ParseHeaderFile(content: list) -> tuple:
    setOfCategories = set([field.split('_')[0] for field in content])
    setOfCategories.remove('\n')
    tags = list(setOfCategories)
    tags.sort()

    header = []
    for line in content:
        header.append(ParseHeader(line, tags))
    return GroupListIfChar(header, ''), tags

def BackUpData(csvfileName: str, data):
    fileName = csvfileName.replace('.csv', '_' + str(date.today()) + '.csv')
    if exists(fileName):
        raise Exception("File " + fileName + " already exists.")
    data.to_csv(fileName, index=False)

# Combining both

def VerifyHeaderAndData(header: list, dataVariables: list, csvFileName: str, data):
    flatHeader = [item.lower().replace(' ', '_') for sublist in header for item in sublist]
    if len(flatHeader) < len(dataVariables):
        BackUpData(csvFileName, data)
        for h in dataVariables:
            if h not in flatHeader:
                print("header " + h + " was removed")
                data.drop(h, inplace=True, axis=1)
    elif len(flatHeader) > len(dataVariables):
        BackUpData(csvFileName, data)
        for h in flatHeader:
            if h not in dataVariables:
                print("header " + h + " was added")
                data[h] = [None for item in range(data.shape[0])]
    else:
        return


from datetime import date, timedelta

# .csv

def CheckForTodaysEntry(lastDate: str) -> int:
    delta = date.today() - date.fromisoformat(lastDate)
    return delta.days

def GetLatestDate(data) -> str:
    return data.iloc[-1]['date']

def CreateEntry(data):
    lastDate: str = GetLatestDate(data)
    deltaDays = CheckForTodaysEntry(data.iloc[-1]['date'])
    if deltaDays > 1:
        di = dict.fromkeys(data.columns.values, 'False')
        for day in range(deltaDays):
            newDate = date.fromisoformat(lastDate)
            di['date'] = str(newDate + timedelta(days=(day + 1)))
            data = data.append((di), ignore_index=True)
    return data

# .txt

def ParseHeader(header: str) -> str:
    tags = ["body", "mind", "addiction", "betterme", "social"]
    parts = header.split("_")
    for p in (parts):
        if (p in tags):
            parts.pop(parts.index(p))
    for i, p in enumerate(parts):
        parts[i] = p.replace("\n", "").capitalize()
    result = " ".join(parts)
    return result

def CombineListIfChar(flatList: list, ch: str) -> list:
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

def ParseHeaderFile(content: list) -> list:
    result = []
    for line in content:
        result.append(ParseHeader(line))
    return CombineListIfChar(result, '')

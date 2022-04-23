from datetime import date, timedelta
from os.path import exists
from utils import *

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
    deltaDays = None
    lastDate = None
    try:
        lastDate: str = GetLatestDate(data)
        deltaDays = CheckForTodaysEntry(data.iloc[-1]['date'])
    except:
        print("CreateEntry: .csv seems to be empty.")
    finally:
        deltaDays = 1 if deltaDays is None else deltaDays
        lastDate = (date.today() + timedelta(days=-1)).isoformat() if lastDate is None else lastDate

    if deltaDays > 0:
        di = dict.fromkeys(data.columns.values, '')
        for day in range(deltaDays):
            newDate = date.fromisoformat(lastDate)
            di['date'] = str(newDate + timedelta(days=(day + 1)))
            data = data.append((di), ignore_index=True)
    return data

def BackUpData(csvfileName: str, data):
    fileName = csvfileName.replace('.csv', '_' + str(date.today()) + '.csv')
    if exists(fileName):
        raise Exception("File " + fileName + " already exists.")
    data.to_csv(fileName, index=False)

def SaveData(data, checkboxDict: dict, csvFileName):
    for key in checkboxDict.keys():
        data.iloc[-1, data.columns.get_loc(ToLowerUnderScored(key))] = checkboxDict[key]
    data.to_csv(csvFileName, index=False)

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

def ParseHeaderFile(content: list) -> tuple:
    setOfCategories = set([field.split('_')[0] for field in content])
    setOfCategories.remove('\n')
    tags = list(setOfCategories)
    tags.sort()

    header = [ParseHeader(line.split(',')[0], tags) if line != '' else '' for line in content]
    descriptions = [line.split(',')[1].strip() if line.find(',') > -1 else '' for line in content]
    return tags, GroupListIfChar(header, ''), GroupListIfChar(descriptions, '')

def GetDescriptionText(descriptionMatrix: list, headerMatrix: list, headerValue: str) -> str:
    for idx1, sublist in enumerate(headerMatrix):
        for idx2, item in enumerate(sublist):
            if item == headerValue:
                return descriptionMatrix[idx1][idx2]
    print("GetDescriptionText: Couldn't find description for: " + headerValue)
    return ''

# Combining both

def VerifyHeaderAndData(header: list, dataVariables: list, csvFileName: str, data):
    flatHeader = [ToLowerUnderScored(item) for sublist in header for item in sublist]
    # if len(flatHeader) != len(dataVariables):
    if len([item for item in dataVariables if item not in flatHeader]) > 0 or len([item for item in flatHeader if item not in dataVariables]) > 0:
        BackUpData(csvFileName, data)
        for h in dataVariables:
            if h not in flatHeader:
                print("header " + h + " was removed")
                data.drop(h, inplace=True, axis=1)
        for h in flatHeader:
            if h not in dataVariables:
                print("header " + h + " was added")
                data[h] = [None for item in range(data.shape[0])]

from datetime import date, timedelta
from os.path import exists
from random import choice

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
            data = data.append(di, ignore_index=True)
    return data

def BackUpData(csvfileName: str, data):
    fileName = csvfileName.replace('.csv', '_' + str(date.today()) + '.csv')
    if exists(fileName):
        raise Exception(f"File {fileName} already exists.")
    data.to_csv(fileName, index=False)

def SaveData(data, checkboxDict: dict, csvFileName):
    for key in checkboxDict.keys():
        data.iloc[-1, data.columns.get_loc(ToLowerUnderScored(key))] = checkboxDict[key]
    data.to_csv(csvFileName, index=False)

# .txt

def ParseHeader(field: str, tags: list) -> str:
    parts = field.split("_")
    for p in parts:
        if p in tags:
            parts.pop(parts.index(p))
    for i, p in enumerate(parts):
        parts[i] = p.replace("\n", "").capitalize()
    result = " ".join(parts)
    return result

def ParseHeaderLine(content: list, index: int) -> list:
    return [line.split(';')[index].strip() if line.find(';') > -1 else '' for line in content]

def ParseHeaderFile(content: list) -> tuple:
    setOfCategories = set([field.split(';')[1].split('_')[0].strip() if field.find(';') > -1 else '\n' for field in content])
    setOfCategories.remove('\n')
    tags = list(setOfCategories)
    tags.sort()

    frequencies = ParseHeaderLine(content, 0)
    header = [ParseHeader(line.split(';')[1].strip(), tags) if line.find(';') > -1 else '' for line in content]
    descriptions = ParseHeaderLine(content, 2)
    habitMessages = ParseHeaderLine(content, 3)
    return GroupListIfChar(frequencies, ''), tags, GroupListIfChar(header, ''), GroupListIfChar(descriptions, ''), GroupListIfChar(habitMessages, '')

def GetMatrixDataByHeaderIndexes(otherMatrix: list, headerMatrix: list, headerValue: str) -> str:
    for idx1, sublist in enumerate(headerMatrix):
        for idx2, item in enumerate(sublist):
            if item == headerValue:
                return otherMatrix[idx1][idx2]
    print("GetMatrixDataByHeaderIndexes: Couldn't find description for: " + headerValue)
    return ''

# Combining both

def VerifyHeaderAndData(header: list, dataVariables: list, csvFileName: str, data):
    flatHeader = [ToLowerUnderScored(item) for sublist in header for item in sublist]
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

# Habit messages

def CalculateFrequency(dataFrequency: float, nominalFrequency: float, condition: str) -> bool:
    match condition:
        case '<':
            return dataFrequency < nominalFrequency
        case '>':
            return dataFrequency > nominalFrequency
        case _:
            raise Exception(f"CalculateFrequency: Condition {condition}{nominalFrequency} is not defined.")

def ParseFrequency(column: str, frequencies: list, header: list) -> tuple:
    freqString = GetMatrixDataByHeaderIndexes(frequencies, header, column)
    condition, fraction = tuple(freqString.split(','))
    return condition, int(fraction.split('/')[0]), int(fraction.split('/')[1])

def CheckHabit(column: str, frequencies: list, header: list, data) -> tuple:
    condition, num, den = ParseFrequency(column, frequencies, header)
    nominal = num/den
    if data.loc[:,ToLowerUnderScored(column)].count() >= den:
        trues = [1 if x is True else 0 for x in data.loc[:,ToLowerUnderScored(column)].tail(den)]
        frequency = sum(trues)/len(trues)
    else:
        return 0, 0
    return (frequency, nominal) if CalculateFrequency(frequency, num/den, condition) else (0, nominal)

def GetPopUpMessage(frequencies: list, habitMessages: list, header: list, data, previousMessage: str) -> str:
    flatHeader = FlattenList(header)
    messageData = [(CheckHabit(h, frequencies, header, data), h, GetMatrixDataByHeaderIndexes(habitMessages, header, h)) for h in flatHeader]
    candidateMessages = set([f'{GetMatrixDataByHeaderIndexes(header, habitMessages, m[2])}\n{m[2]}' if m[0][1] > 0 else '' for m in messageData])
    candidateMessages.remove('')
    if previousMessage != '' and len(candidateMessages) > 1:
        candidateMessages.remove(previousMessage)
    return choice(list(candidateMessages))

def ReadLatestMessage(msgFileName: str) -> str:
    if not exists(msgFileName):
        return ''
    else:
        with open(msgFileName, 'r') as f:
            lines = [l.split('\t') for l in f.readlines()]
            f.close()
            return f'{lines[-1][1]}\n{lines[-1][2]}'

def SaveMessageFile(msgFileName: str, todaysMessage: str):
    today = date.today().isoformat()
    message = todaysMessage.replace('\n', '\t')
    data = f'\n{today}\t{message}'
    if not exists(msgFileName):
        data = data.replace('\n', '')
    with open(msgFileName, 'a') as f:
        f.write(data)
        f.close()

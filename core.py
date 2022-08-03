from datetime import date, timedelta, datetime
from os.path import exists, getsize, isdir
from os import makedirs, path
from random import choice
from utils import *

import pandas as pd
import json

wakeup_time = 6
dateHeader = "date"

# .csv

def ReadCsv(fileName: str):
    with open(fileName, 'r') as file:
        lines = file.readlines()
        file.close()
    header = lines[0].replace('\n', '').split(',')
    content = [stringLine.replace('\n', '').split(',') for stringLine in lines[1:]]
    df = pd.DataFrame(content, columns=header)
    return df

def GroupByCategory(dataframe, column: str) -> list:
    categoryColumn = "category"
    captalizedColumns = ["header"]
    categories = RemoveDuplicates(dataframe[categoryColumn])
    result = []
    for category in categories:
        result.append([ToCapitalized(x) if column in captalizedColumns else x for x in list(dataframe.loc[dataframe[categoryColumn] == category][column])])
    return result

def GetData(variablesFile):
    fractions = GroupByCategory(variablesFile, "frequency")
    conditions = GroupByCategory(variablesFile, "condition")
    habitMessages = GroupByCategory(variablesFile, "message")
    descriptions = GroupByCategory(variablesFile, "tooltip")
    header = GroupByCategory(variablesFile, "header")
    categories = RemoveDuplicates(FlattenList(GroupByCategory(variablesFile, "category")))
    return conditions, fractions, habitMessages, descriptions, header, categories

def WriteCsv(fileName: str, data):
    cols = ','.join([col for col in data.columns])
    content = ''
    for index, row in data.iterrows():
        rowData = [str(item) for item in list(row)]
        content += f'\n{rowData}'.replace("[", "").replace("]", "").replace("'", "").replace(" ", "")
    with open(fileName, 'w') as dataFile:
        dataFile.seek(0)
        dataFile.write(f'{cols}')
        dataFile.write(f'{content}')
        dataFile.close()

def CheckForTodaysEntry(lastDate: str) -> int:
    try:
        # Fixes inputting data after midnight
        currentDate = date.today() + timedelta(days=-1) if datetime.now().hour < wakeup_time else date.today()
        delta = currentDate - date.fromisoformat(lastDate)
    except:
        raise Exception("Can't parse the data, it needs to be in the format 'yyyy-mm-dd'. \nDatabase probably got corrupted.")
    return delta.days

def GetLatestDate(data) -> str:
    return data.iloc[-1][dateHeader]

def CreateEntry(data):
    deltaDays = None
    lastDate = None
    try:
        lastDate = GetLatestDate(data)
        deltaDays = CheckForTodaysEntry(data.iloc[-1][dateHeader])
    except:
        print("CreateEntry: .csv seems to be empty.")
    finally:
        deltaDays = 1 if deltaDays is None else deltaDays
        # Fixes inputting data after midnight
        currentDate = date.today() + timedelta(days=-1) if datetime.now().hour < wakeup_time else date.today()
        lastDate = (currentDate + timedelta(days=-1)).isoformat() if lastDate is None else lastDate

    if deltaDays > 0:
        di = dict.fromkeys(data.columns.values, '')
        for day in range(deltaDays):
            newDate = date.fromisoformat(lastDate)
            di[dateHeader] = str(newDate + timedelta(days=(day + 1)))
            data = data.append(di, ignore_index=True)
    return data

def BackUpData(csvfileName: str, data):
    fileName = csvfileName.replace('.csv', '_' + str(date.today()) + '.csv')
    if exists(fileName):
        raise Exception(f"File {fileName} already exists.")
    WriteCsv(fileName, data)

def SaveData(data, checkboxDict: dict, csvFileName):
    for key in checkboxDict.keys():
        data.iloc[-1, data.columns.get_loc(ToLowerUnderScored(key))] = checkboxDict[key]
    WriteCsv(csvFileName, data)

# .txt

def GetMatrixDataByHeaderIndexes(otherMatrix: list, headerMatrix: list, headerValue: str) -> str:
    for idx1, sublist in enumerate(headerMatrix):
        for idx2, item in enumerate(sublist):
            if item == headerValue:
                return otherMatrix[idx1][idx2]
    print("GetMatrixDataByHeaderIndexes: Couldn't find description for: " + headerValue)
    return ''

def LogWrite(logFile, newLines: str):
    logFile.seek(0)
    content: list = logFile.readlines()
    content.insert(0, newLines)
    logFile.seek(0)
    logFile.write(''.join(content))

def CreteFolderIfDoesntExist(folderName: str):
    if not isdir(folderName):
        makedirs(folderName)

def CreateFileIfDoesntExist(fileName: str):
    if not exists(fileName):
        with open(fileName, 'w') as file:
            file.write('')
            file.close()

# Verifying

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

def VerifyVariables(variablesFileName):
    try:
        with open(variablesFileName, 'r') as file:
            lines = file.readlines()
            file.close()
        header = lines[0].replace('\n', '').split(',')
        content = [stringLine.replace('\n', '').split(',') for stringLine in lines[1:]]
        for idx, line in enumerate(content):
            if len(line) != len(header):
                raise Exception(f"VerifyVariables - Length of line {idx} and header is different from {len(header)}\n{line}")
            if line[0] == '' or line[1] == '':
                raise Exception(f"VerifyVariables - Cannot have empty value for line {idx} at the first two columns\n{line}")
        df = pd.DataFrame(content, columns=header)
    except Exception as e:
        raise e
# Habit messages

def CalculateFrequency(dataFrequency: float, nominalFrequency: float, condition: str) -> bool:
    match condition:
        case '<':
            return dataFrequency < nominalFrequency
        case '>':
            return dataFrequency > nominalFrequency
        # Skips this message
        case '':
            return True
        case _:
            raise Exception(f"CalculateFrequency: Condition {condition}{nominalFrequency} is not defined.")

def ParseFrequency(column: str, conditions: list, fractions: list, header: list) -> tuple:
    condition = GetMatrixDataByHeaderIndexes(conditions, header, column)
    fraction = GetMatrixDataByHeaderIndexes(fractions, header, column)
    if '/' not in fraction:
        return condition, 0, 1
    return condition, int(fraction.split('/')[0]), int(fraction.split('/')[1])

def CheckHabit(column: str, conditions: list, fractions: list, header: list, data) -> tuple:
    condition, num, den = ParseFrequency(column, conditions, fractions, header)
    nominal = num/den
    if data.loc[:, ToLowerUnderScored(column)].count() >= den:
        trues = [1 if x is True else 0 for x in data.loc[:, ToLowerUnderScored(column)].tail(den)]
        frequency = sum(trues)/len(trues)
    else:
        return 0, 0
    return (frequency, nominal) if CalculateFrequency(frequency, nominal, condition) else (0, nominal)

def DetermineSuccessfulToday(data, conditions: list, header: list, habitMessages: list) -> list:
    expectation = [[False if d == '>' else True for d in arr] for arr in conditions]

    reality = [[] for item in range(len(header))]
    for idx1, sublist in enumerate(header):
        for idx2, item in enumerate(sublist):
            reality[idx1].append(GetValueFromDFByRow(ToLowerUnderScored(header[idx1][idx2]), -1, data))

    missionAccomplishedMessages = []
    for idx1, sublist in enumerate(reality):
        for idx2, item in enumerate(sublist):
            if reality[idx1][idx2] == expectation[idx1][idx2]:
                missionAccomplishedMessages.append(habitMessages[idx1][idx2])
    return missionAccomplishedMessages

# TODO speed this method up (taking 11 sec before update)
def GetPopUpMessage(conditions: list, fractions: list, habitMessages: list, header: list, data, msgFileName: str) -> str | None:
    flatHeader = FlattenList(header)
    messageData = [(CheckHabit(h, conditions, fractions, header, data), h, GetMatrixDataByHeaderIndexes(habitMessages, header, h)) for h in flatHeader]

    candidateMessages = set([f"{GetMatrixDataByHeaderIndexes(header, habitMessages, m[2])}\n{m[2]}" if m[0][1] > 0 else '' for m in messageData])
    if len(candidateMessages.intersection({''})) > 0:
        candidateMessages.remove('')

    previousMessage = ReadLatestMessage(msgFileName)
    if previousMessage != '' and len(candidateMessages.intersection({previousMessage})) > 0:
        candidateMessages.remove(previousMessage)

    successMessages = DetermineSuccessfulToday(data, conditions, header, habitMessages)
    successesToRemove = [c for c in candidateMessages for s in successMessages if s in c]
    candidateMessages.difference_update(successesToRemove)

    # TODO Test no data tabs
    if len(candidateMessages) < 1:
        return None

    return choice(list(candidateMessages))

def ReadLatestMessage(msgFileName: str) -> str:
    if not exists(msgFileName):
        return ''
    else:
        with open(msgFileName, 'r') as f:
            # lines = [l.split('\t')[-1].replace('\n', '') for l in f.readlines()]
            lines = [l.replace('\t\t', '\t').split('\t') for l in f.readlines()]
            f.close()
            return f"{lines[-1][1]}\n{lines[-1][2]}"

def SaveMessageFile(msgFileName: str, todaysMessage: str):
    today = date.today().isoformat()
    message = '\t'.join(m + '\t' if len(m) < 8 else m for m in todaysMessage.split('\n'))
    data = f"\n{today}\t{message}"
    if not exists(msgFileName):
        data = data.replace('\n', '')
    with open(msgFileName, 'a') as f:
        f.write(data)
        f.close()

# Settings

class Settings:
    def __init__(self,
                 hueOffset: float = 0,
                 dataDays: int = 21,
                 displayMessages: bool = True,
                 graphExpectedValue: bool = False,
                 scrollableImage: bool = False,
                 ):
        self.hueOffset = hueOffset
        self.dataDays = dataDays
        self.displayMessages = displayMessages
        self.graphExpectedValue = graphExpectedValue
        self.scrollableImage = scrollableImage

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    @staticmethod
    def fromJSON(jsonString: str):
        json_dict = json.loads(jsonString)
        hueOffset = float(json_dict['hueOffset'])
        dataDays = int(json_dict['dataDays'])
        displayMessages = bool(json_dict['displayMessages'])
        graphExpectedValue = bool(json_dict['graphExpectedValue'])
        scrollableImage = bool(json_dict['scrollableImage'])
        return Settings(hueOffset,
                        dataDays,
                        displayMessages,
                        graphExpectedValue,
                        scrollableImage
                        )

def ReadSettings(settingsFileName: str) -> Settings:
    settings: Settings = Settings()
    if not exists(settingsFileName) or getsize(settingsFileName) == 0:
        with open(settingsFileName, 'w') as s:
            s.write(settings.toJSON())
            s.close()

    with open(settingsFileName, 'r') as s:
        settingsFileContent = s.read()
        settingsObj = Settings.fromJSON(settingsFileContent)
        s.close()
    return settingsObj

def SaveSettingsFile(settings: Settings, settingsFileName: str):
    with open(settingsFileName, 'w') as s:
        s.write(settings.toJSON())
        s.close()

#  Data Visualization

def GetDateArray(data, squares: int) -> list:
    latestDateIso = GetLatestDate(data)
    latestDateValue = datetime.fromisoformat(latestDateIso)
    result = [(latestDateValue + timedelta(days=-day)).strftime("%Y-%m-%d") for day in range(squares)]
    return result

def GetExpectedValue(header: str, headerList: list, conditions: list) -> bool:
    condition = GetMatrixDataByHeaderIndexes(conditions, headerList, header)
    return False if condition == '>' else True

def GetHeaderData(data, dateArray: list, squares: int, header: str, expectedValue: bool = True) -> list:
    columnHeader = ToLowerUnderScored(header)
    headerData = data[[dateHeader, columnHeader]]
    headerData = headerData.reset_index()

    result = [not expectedValue for item in range(squares)]
    for index, dateValue in enumerate(dateArray):
        try:
            dataValue = GetValueFromDFByValue(dateHeader, dateValue, headerData)
            value = dataValue[columnHeader].values[0]
            if value == str(expectedValue):
                result[index] = expectedValue
        except:
            continue
    result.reverse()
    return result

def GetFailIndexesList(headerData: list, expectedValue: bool = True) -> list:
    result = []
    for index, item in enumerate(headerData):
        if item != expectedValue:
            result.append(index)
    return result
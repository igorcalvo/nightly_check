from ui import *
from core import *

import pandas as pd

csvFileName = 'data.csv'
headerFileName = 'variables.txt'
msgFileName = 'msg.txt'
buttonText = 'Done'

log = open('log.txt', 'a')
valuesDic = ""
try:
    with open(headerFileName) as h:
        lines = h.readlines()
        frequencies, categories, header, descriptions, habitMessages = ParseHeaderFile(lines)
        h.close()

    if not exists(csvFileName):
        cols = [ToLowerUnderScored(item) for item in FlattenList(header)]
        cols.insert(0, 'date')
        data = pd.DataFrame(columns=cols)
    else:
        data = pd.read_csv(csvFileName)
    variables = list(data.columns)
    variables.pop(0)

    VerifyHeaderAndData(header, variables, csvFileName, data)
    data = CreateEntry(data)
    data.to_csv(csvFileName, index=False)

    # PrintFonts()
    window = CreateWindow(categories, header, descriptions, buttonText)
    while True:
        event, valuesDic = window.read()
        if event == buttonText or event == sg.WIN_CLOSED:
            if event == buttonText:
                latestMessage = ReadLatestMessage(msgFileName)
                todaysMessage = GetPopUpMessage(frequencies, habitMessages, header, data, latestMessage)
                SaveMessageFile(msgFileName, todaysMessage)
                PopUp(todaysMessage)
                SaveData(data, valuesDic, csvFileName)
            break
    window.close()
except Exception as e:
    log.write(f'***** {date.today()} *****\n\n{valuesDic}\n\n{e}\n\n{e.with_traceback}\n\n')
finally:
    log.close()


# TODO LIST
# -----------
# POP UP
#   style based on frequency difference

# DATA VISUALIZATION
#   have a button launch it
#   calendar like
#   colored squares for each header
#   same hue for each category

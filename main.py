from ui import *
from core import *

import pandas as pd

csvFileName = 'data.csv'
headerFileName = 'variables.txt'
buttonText = 'Done'
data = [] # is here just to supress error

log = open('log.txt', 'a')
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
                PopUp(GetPopUpMessage(frequencies, habitMessages, header, data))
            SaveData(data, valuesDic, csvFileName)
            break
    window.close()
except Exception as e:
    log.write(f'{date.today()}\t{data.iloc[-1]}\t{e}\n')
finally:
    log.close()


# TODO LIST
# -----------
# POP UP
#   change to window
#   style based on frequency difference
#   decide wether to keep it random or sort messages
#   code cleanup
#   TEST AND TEST SOME MORE

# DATA VISUALIZATION
#   have a button launch it
#   calendar like
#   colored squares for each header
#   same hue for each category

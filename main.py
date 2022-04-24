from ui import *
from core import *

import pandas as pd

csvFileName = 'data.csv'
headerFileName = 'variables.txt'
buttonText = 'Done'

with open(headerFileName) as h:
    lines = h.readlines()
    categories, header, descriptions = ParseHeaderFile(lines)
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
        # if event == buttonText:
        #     show popup
        SaveData(data, valuesDic, csvFileName)
        break
window.close()

# TODO LIST
# -----------

# FEATURE
#   pop up message on exit
#   based on configured expected habits
#       either streak based or interval on interval (3 in a row or 3 in 5)
#   automatically close popup after 1 or 2 sec
#   have a random or only the most important message show up

# DATA VISUALIZATION
#   have a button launch it
#   calendar like
#   colored squares for each header
#   same hue for each category

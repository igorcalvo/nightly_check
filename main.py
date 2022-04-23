from ui import *
from core import *

import pandas as pd
import PySimpleGUI as sg

message = "How was your day?"
csvFileName = 'data.csv'
headerFileName = 'variables.txt'

with open(headerFileName) as h:
    lines = h.readlines()
    categories, header, descriptions = ParseHeaderFile(lines)
    h.close()

data = pd.read_csv(csvFileName)
variables = list(data.columns)
variables.pop(0)

VerifyHeaderAndData(header, variables, csvFileName, data)
data = CreateEntry(data)
data.to_csv(csvFileName, index=False)

checkboxes = [[(sg.Checkbox(PadString(' ' + item, 30), default=False, key=item, font=('Consolas', 11), tooltip=GetDescriptionText(descriptions, header, item)) if item != '' else sg.Text(PadString('', 66))) for item in splitList] for splitList in Transpose(header)]
categoryTitles = [sg.Text(PadString(c.upper(), 59)) for c in categories]
layout = [[sg.Text(message)],  categoryTitles, checkboxes, [sg.Text(PadString("", 250)), sg.Button("OK")]]
# window = sg.Window(title="Argus", layout=layout, size=(600, 200))
window = sg.Window(title="Argus", layout=layout)

while True:
    event, valuesDic = window.read()
    if event == "OK" or event == sg.WIN_CLOSED:
        SaveData(data, valuesDic, csvFileName)
        break
window.close()

# TO LIST
# -----------
# LAYOUT
#   size pixels
#   checkbox
#   OK button
#   phrase
#   pop up message on exit
#   style
#   icon

# MISC
#   add sounds?
#   find phrases to display
#   double check headers

# DATA VISUALIZATION
#   calendar like
#   colored squares for each header

# DOWN THE ROAD
#   graphs clickable UI data insights
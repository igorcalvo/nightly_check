from ui import *
from utils import *
from core import *

import pandas as pd
import PySimpleGUI as sg

message = "How was your day?"
csvFileName = 'data.csv'
headerFileName = 'header.txt'

with open(headerFileName) as h:
    lines = h.readlines()
    header, categories = ParseHeaderFile(lines)
    h.close()

data = pd.read_csv(csvFileName)
variables = list(data.columns)
variables.pop(0)

VerifyHeaderAndData(header, variables, csvFileName, data)
data = CreateEntry(data)
data.to_csv(csvFileName, index=False)

checkboxes = [[(sg.Checkbox(PadString(' ' + item, 30), default=False, key=item, font=('Consolas', 11)) if item != '' else sg.Text(PadString('', 65))) for item in splitList] for splitList in Transpose(header)]
categoryTitles = [sg.Text(PadString(c.upper(), 59)) for c in categories]
layout = [[sg.Text(message)],  categoryTitles, checkboxes, [sg.Text(PadString("", 250)), sg.Button("OK")]]
# window = sg.Window(title="Argus", layout=layout, size=(600, 200))
window = sg.Window(title="Argus", layout=layout)

while True:
    event, values = window.read()
    if event == "OK" or event == sg.WIN_CLOSED:
        break
window.close()

# TO LIST
# -----------
# LAYOUT
#   size pixels
#   checkbox
#   control checkbox
#   exit button
#   phrase
#   pop up message on exit
#   style
#   icon

# LOGIC
#   save checkboxes to csv

# MISC
#   add sounds?
#   find phrases to display

# DOWN THE ROAD
#   graphs clickable UI data insights
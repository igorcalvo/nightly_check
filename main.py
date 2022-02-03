from ui import *
from utils import *

import pandas as pd
import PySimpleGUI as sg

csvFileName = 'data.csv'

data = pd.read_csv(csvFileName)
data = CreateEntry(data)
data.to_csv(csvFileName, index=False)

layout = [[sg.Text("Hello from PySimpleGUI")], [sg.Button("OK")]]
window = sg.Window("Demo", layout)

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
#   read variables from another csv
#   create new data.csv file if changed columns (preserve old data if possible)

# MISC
#   add sounds?
#   find phrases to display

# DOWN THE ROAD
#   graphs clickable UI data insights
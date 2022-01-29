from ui import *
from utils import *

import pandas as pd
import PySimpleGUI as sg

csvFileName = 'data.csv'

data = pd.read_csv(csvFileName)
data = CreateEntry(data)
data.to_csv(csvFileName, index=False)

# layout = [[sg.Text("Hello from PySimpleGUI")], [sg.Button("OK")]]
# window = sg.Window("Demo", layout)
#
# while True:
#     event, values = window.read()
#     # End program if user closes window or
#     # presses the OK button
#     if event == "OK" or event == sg.WIN_CLOSED:
#         break
#
# window.close()
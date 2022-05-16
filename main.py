import PySimpleGUI

from ui import *
from core import *
from imggen import *

from sys import exc_info
from os import path as ospath

import pandas as pd

csvFileName = 'data\data.csv'
headerFileName = 'variables.txt'
msgFileName = 'data\msg.txt'
settingsFileName = 'data\settings.txt'

doneButtonText = 'Done'
styleButtonText = 'Style'
sliderTextKey = 'Slider'
setButtonTextKey = 'Set'
previewWindowText = 'Preview'
previewCloseKey = 'ClosePreview'
dataButtonText = 'Data'

valuesDic = ''
hueOffset = 0

log = open('data\log.txt', 'r+')
exceptionText = ''
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
    Run()
    # PrintFonts()
    InitUi(settingsFileName)
    window = MainWindow(categories, header, descriptions, doneButtonText, styleButtonText, dataButtonText)
    while True:
        event, valuesDic = window.read()
        if event == styleButtonText:
            styleWindow = StyleWindow(styleButtonText, sliderTextKey, previewWindowText, setButtonTextKey)
            while True:
                styleEvent, styleValuesDic = styleWindow.read()
                if styleEvent == sliderTextKey:
                    hueOffset = styleValuesDic[sliderTextKey]
                elif styleEvent == previewWindowText:
                    previewWindow = PreviewWindow(previewWindowText, previewCloseKey, hueOffset)
                    while True:
                        previewEvent, previewValuesDic = previewWindow.read()
                        if previewEvent == previewCloseKey or previewEvent == sg.WIN_CLOSED:
                            previewWindow.close()
                            break
                elif styleEvent == setButtonTextKey or styleEvent == sg.WIN_CLOSED:
                    if styleEvent == setButtonTextKey:
                        SaveSettingsFile(hueOffset, settingsFileName)
                    styleWindow.close()
                    break
        elif event == dataButtonText:
            textArg = "Sample Text"
            imgArg = "assets\data\sample.png"
            dataWindow = DataWindow(dataButtonText, textArg, imgArg)
            while True:
                dataEvent, dataValuesDic = dataWindow.read()
                if dataEvent == PySimpleGUI.WIN_CLOSED:
                    dataWindow.close()
                    break
        elif event == doneButtonText or event == sg.WIN_CLOSED:
            if event == doneButtonText:
                SaveData(data, valuesDic, csvFileName)

                message = GetPopUpMessage(frequencies, habitMessages, header, data, msgFileName)
                SaveMessageFile(msgFileName, message)

                PopUp(message)
            break
    window.close()
except Exception as e:
    e_type, e_obj, e_tb = exc_info()
    e_filename = ospath.split(e_tb.tb_frame.f_code.co_filename)[1]
    exceptionText = f'{e_obj} at line {e_tb.tb_lineno} of {e_filename}\n'
    LogWrite(log, exceptionText)
finally:
    LogWrite(log, f'***** {date.today()} - {datetime.now().time().replace(microsecond=0)} *****\n{valuesDic}\n\n', exceptionText)
    log.close()


# TODO LIST
# DATA VISUALIZATION
#   get data
#   graph heatmap
#   calendar like
#   colored squares for each header
#   same hue for each category
#   different saturation for each goal

# EDIT DATA
#   methods
#   ui
#   limit to 1 y-day

# HABITS
#   redefine

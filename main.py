
from ui import *
from core import *

from sys import exc_info
from datetime import datetime
from os import path as ospath

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
                SaveData(data, valuesDic, csvFileName)

                message = GetPopUpMessage(frequencies, habitMessages, header, data, msgFileName)
                SaveMessageFile(msgFileName, message)

                PopUp(message)
            break
    window.close()
except Exception as e:
    e_type, e_obj, e_tb = exc_info()
    e_filename = ospath.split(e_tb.tb_frame.f_code.co_filename)[1]
    log.write(f'***** {date.today()} - {datetime.now().time().replace(microsecond=0)} *****\n{valuesDic}\n\n{e_obj}\tat line {e_tb.tb_lineno} of {e_filename}\n\n')
finally:
    log.close()


# TODO LIST
# -----------
# POP UP
#   style based on frequency difference
#   priority for message? maybe just cycle

# UI
#   HSV color decomp for styles
#   popup for styles maybe

# HABITS
#   redefine

# DATA VISUALIZATION
#   have a button launch it
#   calendar like
#   colored squares for each header
#   same hue for each category

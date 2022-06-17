from ui import *
from core import *
from imggen import *

from sys import exc_info
from os import path as ospath

csvFileName = 'data\data.csv'
headerFileName = 'variables.txt'
msgFileName = 'data\msg.txt'
settingsFileName = 'data\settings.txt'
logFileName = 'data\log.txt'
exportImageFileName = 'image.png'

doneButtonText = 'Done'
styleButtonText = 'Style'
sliderTextKey = 'Slider'
setButtonTextKey = 'Set'
previewWindowText = 'Preview'
previewCloseKey = 'ClosePreview'
dataButtonText = 'Data'
exportButtonText = 'Export'

valuesDic = {}
hueOffset = 0

CreateFileIfDoesntExist(logFileName)
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
        data = ReadCsv(csvFileName)
    variables = list(data.columns)
    variables.pop(0)

    VerifyHeaderAndData(header, variables, csvFileName, data)
    data = CreateEntry(data)
    # GenerateImage(categories, header, frequencies, CleanDF(data))
    # PrintFonts()
    settings = ReadSettings(settingsFileName)
    InitUi(settings.hueOffset)
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
                        settings.hueOffset = hueOffset
                        SaveSettingsFile(settings, settingsFileName)
                    styleWindow.close()
                    break
        elif event == dataButtonText:
            img = GenerateImage(categories, header, frequencies, settings.dataDays, CleanDF(data))
            dataWindow = DataWindow(dataButtonText, exportButtonText, ImageBytesToBase64(img))
            while True:
                dataEvent, dataValuesDic = dataWindow.read()
                if dataEvent == exportButtonText:
                    img.save(exportImageFileName)
                if dataEvent == sg.WIN_CLOSED or dataEvent == exportButtonText:
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
    LogWrite(log, f"\n{e_obj} at line {e_tb.tb_lineno} of {e_filename}\n\n")
finally:
    finallyString = f"***** {date.today()} - {datetime.now().time().replace(microsecond=0)} *****\n"
    if any(valuesDic.values()):
        LogWrite(log, f"{finallyString}{valuesDic}\n\n")
    else:
        LogWrite(log, f"{finallyString}")
    log.close()

# TODO LIST
# HABITS
#   redefine when living alone

# EDIT DATA
#   methods
#   ui
#   limit to y-day

#   FUTURE
#   compile code
#   have an indicator on the side of each row based on frequencies:
#       all good
#       improving, but still bad
#       declining, but still good
#       all bad
#   remove unnecessary imports (from x import *)
#   ui for variables, very nani
#   improve style's ui
#   have some sort of readme?

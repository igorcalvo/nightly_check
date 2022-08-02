from ui import *
from core import *
from imggen import *

from sys import exc_info

dataFolder = 'data'
csvFileName = f'{dataFolder}\data.csv'
msgFileName = f'{dataFolder}\msg.txt'
settingsFileName = f'{dataFolder}\settings.txt'
logFileName = f'{dataFolder}\log.txt'
headerFileName = 'variables.csv'

doneButtonText = 'Done'
styleButtonText = 'Style'
sliderTextKey = 'Slider'
setButtonTextKey = 'Set'
previewWindowText = 'Preview'
previewCloseKey = 'ClosePreview'
dataButtonText = 'Data'
exportButtonText = 'Export'
exportImageFileNameKey = 'ExportFileName'

valuesDic = {}
hueOffset = 0

CreteFolderIfDoesntExist(dataFolder)
CreateFileIfDoesntExist(logFileName)
log = open(logFileName, 'r+')
try:
    if not exists(headerFileName):
        raise Exception(f"No header file found, create the file {headerFileName}")
    variablesFile = ReadCsv(headerFileName)
    conditions, fractions, habitMessages, descriptions, header, categories = GetData(variablesFile)

    if not exists(csvFileName):
        cols = [item for item in FlattenList(header)]
        cols.insert(0, dateHeader)
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
    window = MainWindow(categories, header, descriptions, doneButtonText, styleButtonText, dataButtonText, len(data) > 1)
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
            img = GenerateImage(categories, header, conditions, settings.dataDays, settings.graphExpectedValue, CleanDF(data))
            dataWindow = DataWindow(dataButtonText, exportImageFileNameKey, exportButtonText, ImageBytesToBase64(img))
            while True:
                dataEvent, dataValuesDic = dataWindow.read()
                if dataEvent == exportButtonText:
                    exportImageFileName = dataValuesDic[exportButtonText]
                    if exportImageFileName:
                        dataWindow[exportImageFileNameKey].update(value=exportImageFileName)
                        img.save(exportImageFileName)
                if dataEvent == sg.WIN_CLOSED or dataEvent == exportButtonText:
                    dataWindow.close()
                    break
        elif event == doneButtonText or event == sg.WIN_CLOSED:
            if event == doneButtonText:
                SaveData(data, valuesDic, csvFileName)

                message = GetPopUpMessage(conditions, fractions, habitMessages, header, data, msgFileName)
                if message and settings.displayMessages:
                    SaveMessageFile(msgFileName, message)
                    PopUp(message)
            break
    window.close()
except Exception as e:
    e_type, e_obj, e_tb = exc_info()
    e_filename = path.split(e_tb.tb_frame.f_code.co_filename)[1]
    LogWrite(log, f"\n{e_obj} at line {e_tb.tb_lineno} of {e_filename}\n\n")
finally:
    finallyString = f"***** {date.today()} - {datetime.now().time().replace(microsecond=0)} *****\n"
    if any(valuesDic.values()):
        LogWrite(log, f"{finallyString}{valuesDic}\n\n")
    else:
        LogWrite(log, f"{finallyString}")
    log.close()
# TODO LIST
    # function to validate variables
    # fix ui
    # fix image header alignment
    # fix image too tall to fit the screen
# notificacao on startup
#   if esqueceu y-terday entry
# feature edit yday
# what if no message in variobles?

# EDIT DATA
#   methods
#   ui
#       display: message from {date}
#       main window without buttons
#   limit to y-day

# TAG FEATURE? LATEST TIME TAG
#   separete file

#   FUTURE
#   have an indicator on the side of each row based on frequencies:
#       all good
#       improving, but still bad
#       declining, but still good
#       all bad
#   ui for variables, very nani
#       if never ran, start this window
#       else have a button to edit it later
#   improve style's ui
#   have some sort of readme?
#   write reddit post
#   (week challenge?!?!?!?!)
#       reward for completing challenge!!
#       or completing streaks(i.e. 30 days working out)
#
#   alerta baseado em tema conta mais:
#       exemplo: nao malhar e comer a mais
#       	 cel no trabalho e nao meditar
#       	 anime fap e jogar
#
#   COMPILED CODE
#   run: python -m PyInstaller --onefile main.py
#   solution to assets problem: https://stackoverflow.com/q/31836104
#   improve code
#       remove unnecessary imports (from x import *)
#       remove commented out code
#   refer to: assets/reference/compiled.PNG
#       assets folder -> check if folder exists and maybe unzip automatically?
#       variables.txt -> handle msg, or create with ui
#       create data folder -> check if folder exists and maybe unzip automatically?
#   icon
#       make icon change color
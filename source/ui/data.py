from io import BytesIO
from PIL import Image
from base64 import b64decode

import PySimpleGUI as sg
from source.constants import COLORS, FONTS, PATHS

PATH = PATHS()
PATH.__init__()

def DataWindow(data_button_text: str, export_button_text: str, scrollable_image: bool, img_base64: str):
    width, height = Image.open(BytesIO(b64decode(img_base64))).size
    layout = [
        [sg.Image(data=img_base64)],
        [
            sg.InputText(key=export_button_text, do_not_clear=False, enable_events=True, visible=False),
            sg.FileSaveAs(
                button_text=export_button_text,
                font=FONTS["btn"],
                initial_folder="%HomeDrive%",
                file_types=(('PNG', '.png'), ('JPG', '.jpg')),
                pad=((width - 50, 5), (5, 5)),
                button_color=(COLORS["exp_bkg"], COLORS["exp_txt"])
            )
        ]
    ]
    return sg.Window(data_button_text, [
        [sg.Column(layout, scrollable=scrollable_image, key='Column')]
    ],
                     return_keyboard_events=True,
                     use_custom_titlebar=True,
                     titlebar_background_color=COLORS["bar_bkg"],
                     titlebar_text_color=COLORS["bar_txt"],
                     titlebar_icon=PATH.data_icon,
                     background_color=COLORS["dat_bkg"],
                     relative_location=(0, -15),
                     ).Finalize()


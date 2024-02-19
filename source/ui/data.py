import PySimpleGUI as sg
from io import BytesIO
from PIL import Image
from base64 import b64decode

from source.constants import COLORS, FONTS, PATHS, TEXTS_AND_KEYS

PATH = PATHS()
PATH.__init__()


def DataWindow(
    scrollable_image: bool,
    img_base64: str,
):
    width, height = Image.open(BytesIO(b64decode(img_base64))).size
    layout = [
        [sg.Image(data=img_base64)],
        [
            sg.InputText(
                key=TEXTS_AND_KEYS.export_button_text,
                do_not_clear=False,
                enable_events=True,
                visible=False,
            ),
            sg.FileSaveAs(
                button_text=TEXTS_AND_KEYS.export_button_text,
                font=FONTS["btn"],
                initial_folder="%HomeDrive%",
                file_types=(("PNG", ".png"), ("JPG", ".jpg")),
                pad=((width - 50, 5), (5, 5)),
                button_color=(COLORS["bar_bkg"], COLORS["bar_txt"]),
            ),
        ],
    ]
    return sg.Window(
        TEXTS_AND_KEYS.data_button_text,
        [[sg.Column(layout, scrollable=scrollable_image, key="Column")]],
        return_keyboard_events=True,
        use_custom_titlebar=True,
        titlebar_background_color=COLORS["bar_bkg"],
        titlebar_text_color=COLORS["bar_txt"],
        titlebar_icon=PATH.data_icon,
        background_color=COLORS["sld_bkg"],
        relative_location=(0, -15),
    ).Finalize()

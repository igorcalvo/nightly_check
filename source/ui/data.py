from base64 import b64decode
from io import BytesIO
from PIL import Image
import PySimpleGUI as sg

from source.constants import COLORS, FONTS, TEXTS_AND_KEYS
from source.core.theme import THEME_PROPS
from source.ui.utils import get_min_win_size, get_paths

ICON_PATHS = get_paths()


def DataWindow(
    scrollable_image: bool,
    img_base64: str,
) -> sg.Window:
    width, height = Image.open(BytesIO(b64decode(img_base64))).size
    layout = [
        [sg.Image(data=img_base64)],
        [
            sg.InputText(
                key=TEXTS_AND_KEYS.export_button_text,
                do_not_clear=False,
                enable_events=True,
                visible=False,
                background_color=COLORS[THEME_PROPS.INPUT],
                text_color=COLORS[THEME_PROPS.TEXT_INPUT],
            ),
            sg.FileSaveAs(
                button_text=TEXTS_AND_KEYS.export_button_text,
                font=FONTS["btn"],
                initial_folder="%HomeDrive%",
                file_types=(("PNG", ".png"), ("JPG", ".jpg")),
                pad=((width - 50, 5), (5, 5)),
                button_color=(
                    COLORS[THEME_PROPS.BUTTON][0],
                    COLORS[THEME_PROPS.BUTTON][1],
                ),
            ),
        ],
    ]
    return sg.Window(
        TEXTS_AND_KEYS.data_button_text,
        [
            [
                sg.Column(
                    layout,
                    scrollable=scrollable_image,
                    key="Column",
                    size=(None, None) if not scrollable_image else get_min_win_size(),
                )
            ]
        ],
        return_keyboard_events=True,
        use_custom_titlebar=True,
        titlebar_background_color=COLORS[THEME_PROPS.BUTTON][0],
        titlebar_text_color=COLORS[THEME_PROPS.BUTTON][1],
        titlebar_icon=ICON_PATHS.data_icon,
        background_color=COLORS[THEME_PROPS.SCROLL],
        relative_location=(0, -15),
        finalize=True,
    )

from PySimpleGUI import LOOK_AND_FEEL_TABLE

from source.constants import COLORS2, THEME_PROPS
from source.utils import safe_value_from_dict

class THEME:
    def __init__(
        self,
        theme: str = "Default"
    ):
        self.ACCENT1 = safe_value_from_dict(THEME_PROPS.ACCENT1, LOOK_AND_FEEL_TABLE[theme])
        self.ACCENT2 = safe_value_from_dict(THEME_PROPS.ACCENT2, LOOK_AND_FEEL_TABLE[theme])
        self.ACCENT3 = safe_value_from_dict(THEME_PROPS.ACCENT3, LOOK_AND_FEEL_TABLE[theme])
        self.BACKGROUND = safe_value_from_dict(THEME_PROPS.BACKGROUND, LOOK_AND_FEEL_TABLE[theme])
        self.BORDER = safe_value_from_dict(THEME_PROPS.BORDER, LOOK_AND_FEEL_TABLE[theme])
        self.BUTTON = safe_value_from_dict(THEME_PROPS.BUTTON, LOOK_AND_FEEL_TABLE[theme])
        self.COLOR_LIST = safe_value_from_dict(THEME_PROPS.COLOR_LIST, LOOK_AND_FEEL_TABLE[theme])
        self.DESCRIPTION = safe_value_from_dict(THEME_PROPS.DESCRIPTION, LOOK_AND_FEEL_TABLE[theme])
        self.INPUT = safe_value_from_dict(THEME_PROPS.INPUT, LOOK_AND_FEEL_TABLE[theme])
        self.PROGRESS = safe_value_from_dict(THEME_PROPS.PROGRESS, LOOK_AND_FEEL_TABLE[theme])
        self.PROGRESS_DEPTH = safe_value_from_dict(THEME_PROPS.PROGRESS_DEPTH, LOOK_AND_FEEL_TABLE[theme])
        self.SCROLL = safe_value_from_dict(THEME_PROPS.SCROLL, LOOK_AND_FEEL_TABLE[theme])
        self.SLIDER_DEPTH = safe_value_from_dict(THEME_PROPS.SLIDER_DEPTH, LOOK_AND_FEEL_TABLE[theme])
        self.TEXT = safe_value_from_dict(THEME_PROPS.TEXT, LOOK_AND_FEEL_TABLE[theme])
        self.TEXT_INPUT = safe_value_from_dict(THEME_PROPS.TEXT_INPUT, LOOK_AND_FEEL_TABLE[theme])

# def get_default_theme() -> THEME:
#     theme = THEME()
#     theme.ACCENT1 = 
#     theme.ACCENT2 = 
#     theme.ACCENT3 = 
#     theme.BACKGROUND = COLORS2.win_bkg
#     theme.BORDER = 1
#     theme.BUTTON = (COLORS2.bar_bkg, COLORS2.bar_txt)
#     theme.COLOR_LIST = 
#     theme.DESCRIPTION = 
#     theme.INPUT = 
#     theme.PROGRESS = ('#000000', '#000000') # useless
#     theme.PROGRESS_DEPTH = 
#     theme.SCROLL = 
#     theme.SLIDER_DEPTH = 
#     theme.TEXT = COLORS2.bar_txt 
#     theme.TEXT_INPUT = 
#     return theme

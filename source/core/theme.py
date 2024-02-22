from PySimpleGUI import LOOK_AND_FEEL_TABLE

from source.utils import safe_value_from_dict


class DEFAULT_COLORS:
    bar_bkg = "#00274f"
    bar_txt = "#b1d8ff"
    win_bkg = "#002f5f"
    cat_txt = "#dbedff"
    sld_bkg = "#004080"


class THEME_PROPS:
    ACCENT1 = "ACCENT1"
    ACCENT2 = "ACCENT2"
    ACCENT3 = "ACCENT3"
    BACKGROUND = "BACKGROUND"
    BORDER = "BORDER"
    BUTTON = "BUTTON"
    COLOR_LIST = "COLOR_LIST"
    DESCRIPTION = "DESCRIPTION"
    INPUT = "INPUT"
    PROGRESS = "PROGRESS"
    PROGRESS_DEPTH = "PROGRESS_DEPTH"
    SCROLL = "SCROLL"
    SLIDER_DEPTH = "SLIDER_DEPTH"
    TEXT = "TEXT"
    TEXT_INPUT = "TEXT_INPUT"


class THEME:
    def __init__(self, theme: str = "Default"):
        self.ACCENT1 = safe_value_from_dict(
            THEME_PROPS.ACCENT1, LOOK_AND_FEEL_TABLE[theme]
        )
        self.ACCENT2 = safe_value_from_dict(
            THEME_PROPS.ACCENT2, LOOK_AND_FEEL_TABLE[theme]
        )
        self.ACCENT3 = safe_value_from_dict(
            THEME_PROPS.ACCENT3, LOOK_AND_FEEL_TABLE[theme]
        )
        self.BACKGROUND = safe_value_from_dict(
            THEME_PROPS.BACKGROUND, LOOK_AND_FEEL_TABLE[theme]
        )
        self.BORDER = safe_value_from_dict(
            THEME_PROPS.BORDER, LOOK_AND_FEEL_TABLE[theme]
        )
        self.BUTTON = safe_value_from_dict(
            THEME_PROPS.BUTTON, LOOK_AND_FEEL_TABLE[theme]
        )
        self.COLOR_LIST = safe_value_from_dict(
            THEME_PROPS.COLOR_LIST, LOOK_AND_FEEL_TABLE[theme]
        )
        self.DESCRIPTION = safe_value_from_dict(
            THEME_PROPS.DESCRIPTION, LOOK_AND_FEEL_TABLE[theme]
        )
        self.INPUT = safe_value_from_dict(THEME_PROPS.INPUT, LOOK_AND_FEEL_TABLE[theme])
        self.PROGRESS = safe_value_from_dict(
            THEME_PROPS.PROGRESS, LOOK_AND_FEEL_TABLE[theme]
        )
        self.PROGRESS_DEPTH = safe_value_from_dict(
            THEME_PROPS.PROGRESS_DEPTH, LOOK_AND_FEEL_TABLE[theme]
        )
        self.SCROLL = safe_value_from_dict(
            THEME_PROPS.SCROLL, LOOK_AND_FEEL_TABLE[theme]
        )
        self.SLIDER_DEPTH = safe_value_from_dict(
            THEME_PROPS.SLIDER_DEPTH, LOOK_AND_FEEL_TABLE[theme]
        )
        self.TEXT = safe_value_from_dict(THEME_PROPS.TEXT, LOOK_AND_FEEL_TABLE[theme])
        self.TEXT_INPUT = safe_value_from_dict(
            THEME_PROPS.TEXT_INPUT, LOOK_AND_FEEL_TABLE[theme]
        )


def get_default_theme() -> THEME:
    theme = THEME()
    theme.ACCENT1 = None
    theme.ACCENT2 = None
    theme.ACCENT3 = None
    theme.BACKGROUND = DEFAULT_COLORS.win_bkg
    theme.BORDER = 1
    theme.BUTTON = (DEFAULT_COLORS.bar_bkg, DEFAULT_COLORS.bar_txt)
    theme.COLOR_LIST = None
    theme.DESCRIPTION = None
    theme.INPUT = DEFAULT_COLORS.sld_bkg  # "ffffff"
    theme.PROGRESS = ("#000000", "#000000")  # useless
    theme.PROGRESS_DEPTH = 0
    theme.SCROLL = DEFAULT_COLORS.sld_bkg  # maybe not?
    theme.SLIDER_DEPTH = 1  # 0
    theme.TEXT = DEFAULT_COLORS.bar_txt
    theme.TEXT_INPUT = "ffffff"  # "000000"
    return theme

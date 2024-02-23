from PySimpleGUI import LOOK_AND_FEEL_TABLE


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
    CATEGORY = "CATEGORY"


class THEME:
    def __init__(
        self,
        ACCENT1: str | None = None,
        ACCENT2: str | None = None,
        ACCENT3: str | None = None,
        BACKGROUND: str = DEFAULT_COLORS.win_bkg,
        BORDER: int = 1,
        BUTTON: tuple[str, str] = (DEFAULT_COLORS.bar_bkg, DEFAULT_COLORS.bar_txt),
        COLOR_LIST: list[str] | None = None,
        DESCRIPTION: list[str] | None = None,
        INPUT: str = DEFAULT_COLORS.sld_bkg,  # "#ffffff"
        PROGRESS: tuple[str, str] = ("#000000", "#000000"),  # useless
        PROGRESS_DEPTH: int = 0,
        SCROLL: str = DEFAULT_COLORS.sld_bkg,  # maybe not?
        SLIDER_DEPTH: int = 1,  # 0
        TEXT: str = DEFAULT_COLORS.bar_txt,
        TEXT_INPUT: str = "#ffffff",  # "#000000"
    ):
        self.ACCENT1 = ACCENT1
        self.ACCENT2 = ACCENT2
        self.ACCENT3 = ACCENT3
        self.BACKGROUND = BACKGROUND
        self.BORDER = BORDER
        self.BUTTON = BUTTON
        self.COLOR_LIST = COLOR_LIST
        self.DESCRIPTION = DESCRIPTION
        self.INPUT = INPUT
        self.PROGRESS = PROGRESS
        self.PROGRESS_DEPTH = PROGRESS_DEPTH
        self.SCROLL = SCROLL
        self.SLIDER_DEPTH = SLIDER_DEPTH
        self.TEXT = TEXT
        self.TEXT_INPUT = TEXT_INPUT


def get_default_theme() -> THEME:
    theme = THEME()
    return theme


def get_theme_from_table(theme_str: str) -> THEME:
    theme = get_default_theme()
    for key in LOOK_AND_FEEL_TABLE[theme_str].keys():
        theme.__dict__[key] = LOOK_AND_FEEL_TABLE[theme_str][key]
    return theme

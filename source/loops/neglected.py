from io import TextIOWrapper
from pandas import DataFrame
from PySimpleGUI import WIN_CLOSED
from source.constants import FILE_NAMES, TEXTS_AND_KEYS
from source.core.data_date import get_yesterday_date
from source.core.data_out import log_write, save_data
from source.core.settings import Settings
from source.ui.main_window import MainWindow, NeglectedPopUp


def Neglected_Loop(
    categories: list[str],
    habits: list[list[str]],
    descriptions: list[list[str]],
    data: DataFrame,
    settings: Settings,
    log: TextIOWrapper,
):
    neglected_window = NeglectedPopUp()
    while True:
        neglected_event, neglected_values_dic = neglected_window.read()  # type: ignore
        if neglected_event == TEXTS_AND_KEYS.neglected_accept_text:
            neglected_data_window = MainWindow(
                categories,
                habits,
                descriptions,
                len(data) >= 1,
                True,
            )
            while True:
                neglected_data_event, neglected_data_values_dict = neglected_data_window.read()  # type: ignore
                if neglected_data_event == TEXTS_AND_KEYS.done_button_text:
                    log_write(
                        log,
                        f"\nsaving data from yesterday\n{neglected_data_values_dict}",
                    )
                    save_data(
                        data,
                        neglected_data_values_dict,
                        FILE_NAMES.csv,
                        get_yesterday_date(
                            settings.new_day_time,
                        ).isoformat(),
                    )
                if (
                    neglected_data_event == WIN_CLOSED
                    or neglected_data_event == TEXTS_AND_KEYS.done_button_text
                ):
                    neglected_window.close()
                    break
        if (
            neglected_event == WIN_CLOSED
            or neglected_event == TEXTS_AND_KEYS.neglected_reject_text
        ):
            neglected_window.close()
            break

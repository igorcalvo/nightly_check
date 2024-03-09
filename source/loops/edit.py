from io import TextIOWrapper
from pandas import DataFrame
from PySimpleGUI import WIN_CLOSED
from source.constants import FILE_NAMES, TEXTS_AND_KEYS
from source.core.data_date import data_from_date_to_list, get_yesterday_date
from source.core.data_out import log_write, save_data
from source.ui.main_window import DatePickerWindow, MainWindow


def Edit_Loop(
    new_day_time: int,
    categories: list[str],
    habits: list[list[str]],
    descriptions: list[list[str]],
    data: DataFrame,
    log: TextIOWrapper,
):
    picked_date = str(get_yesterday_date(new_day_time))
    date_picker_window = DatePickerWindow(picked_date)
    while True:
        date_picker_event, date_picker_dict = date_picker_window.read()  # type: ignore
        if (
            date_picker_event == TEXTS_AND_KEYS.select_date_button_text
            or date_picker_event == WIN_CLOSED
        ):
            if date_picker_event is None and date_picker_dict is None:
                date_picker_window.close()
                break
            picked_date = date_picker_dict[TEXTS_AND_KEYS.select_date_key]
            data_from_date = data_from_date_to_list(data, picked_date, habits)
            edit_data_window = MainWindow(
                categories,
                habits,
                descriptions,
                len(data) > 0,
                True,
                data_from_date,
            )
            while True:
                edit_data_event, edit_data_values_dict = edit_data_window.read()  # type: ignore
                if edit_data_event == TEXTS_AND_KEYS.done_button_text:
                    log_write(
                        log,
                        f"\nsaving data from date '{picked_date}'\n{edit_data_values_dict}",
                    )
                    save_data(data, edit_data_values_dict, FILE_NAMES.csv, picked_date)
                if (
                    edit_data_event == WIN_CLOSED
                    or edit_data_event == TEXTS_AND_KEYS.done_button_text
                ):
                    edit_data_window.close()
                    break
            date_picker_window.close()
            break

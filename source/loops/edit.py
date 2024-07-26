from io import TextIOWrapper
from pandas import DataFrame
from source.constants import FILE_NAMES
from source.core.data_date import data_from_date_to_list, get_yesterday_date
from source.core.data_out import log_write, save_data


def Edit_Loop(
    new_day_time: int,
    habits: list[list[str]],
    data: DataFrame,
    log: TextIOWrapper,
):
    picked_date = str(get_yesterday_date(new_day_time))
    data_from_date = data_from_date_to_list(data, picked_date, habits)
    log_write(
        log,
        f"\nsaving data from date '{picked_date}'\n{edit_data_values_dict}",
    )
    save_data(data, edit_data_values_dict, FILE_NAMES.csv, picked_date)

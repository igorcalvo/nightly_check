from io import TextIOWrapper
from pandas import DataFrame
from source.constants import FILE_NAMES
from source.core.data_date import get_yesterday_date
from source.core.data_out import log_write, save_data
from source.core.settings import Settings


def Neglected_Loop(
    data: DataFrame,
    settings: Settings,
    log: TextIOWrapper,
):
    neglected_window = NeglectedPopUp()
    log_write(
        log,
        f"\nsaving data from yesterday\n{neglected_data_values_dict}",
    )
    save_data(
        data,
        neglected_data_values_dict,
        FILE_NAMES.csv,
        str(get_yesterday_date(settings.new_day_time)),
    )

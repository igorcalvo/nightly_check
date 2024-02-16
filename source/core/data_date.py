from datetime import date, timedelta, datetime
from pandas import DataFrame, concat

from source.constants import wakeup_time, date_header
from source.utils import df_row_from_date, to_lower_underscored


def get_today_date() -> date:
    return (
        date.today() + timedelta(days=-1)
        if datetime.now().hour < wakeup_time
        else date.today()
    )


def get_yesterday_date() -> date:
    return get_today_date() + timedelta(days=-1)


def get_latest_date(data: DataFrame) -> str:
    return data.iloc[-1][date_header]


def check_for_todays_entry(lastDate: str) -> int:
    try:
        # Fixes inputting data after midnight
        current_date = get_today_date()
        delta = current_date - date.fromisoformat(lastDate)
    except:
        raise Exception(
            "check_for_todays_entry: Can't parse the date, it needs to be in the format 'yyyy-mm-dd'. \nDatabase probably got corrupted."
        )
    return delta.days


def create_entry(data: DataFrame) -> DataFrame:
    delta_days = None
    last_date = None
    try:
        last_date = get_latest_date(data)
        delta_days = check_for_todays_entry(data.iloc[-1][date_header])
    except:
        print("create_entry: .csv seems to be empty.")
    finally:
        delta_days = 1 if delta_days is None else delta_days
        # Fixes inputting data after midnight
        current_date = get_today_date()
        last_date = (
            (current_date + timedelta(days=-1)).isoformat()
            if last_date is None
            else last_date
        )

    if delta_days > 0:
        di = dict.fromkeys(data.columns.values, "")
        for day in range(delta_days):
            new_date = date.fromisoformat(last_date)
            di[date_header] = str(new_date + timedelta(days=(day + 1)))
            df_row = DataFrame([di])
            data = concat([data, df_row], ignore_index=True)
    return data


def data_from_date_to_list(data: DataFrame, date: str, header: list):
    row_from_date = df_row_from_date(data, date, date_header)
    result = [
        [row_from_date[to_lower_underscored(h)].values[0] == "True" for h in cat]
        for cat in header
    ]
    return result


def todays_data_or_none(data: DataFrame, header: list) -> list | None:
    today = str(get_today_date())
    if len(data.tail(1)["date"].values) == 0:
        return None
    return (
        data_from_date_to_list(data, today, header)
        if data.tail(1)["date"].values[0] == today
        else None
    )

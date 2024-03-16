from datetime import date, datetime
from io import TextIOWrapper
from os.path import exists, isdir
from os import makedirs
from pandas import DataFrame

from source.constants import (
    already_filled_in_today_message,
    category_habit_separator,
    date_header,
    MESSAGES_HEADERS,
)
from source.core.data_date import create_entry, get_today_date
from source.core.settings import Settings
from source.utils import df_row_from_date, to_lower_underscored


def log_write(log_file: TextIOWrapper, new_lines: str):
    log_file.seek(0)
    content: list[str] = log_file.readlines()
    content.insert(0, new_lines)
    log_file.seek(0)
    log_file.write("".join(content))


def create_folder_if_doesnt_exist(folder_name: str):
    if not isdir(folder_name):
        makedirs(folder_name)


def create_file_if_doesnt_exist(file_name: str):
    if not exists(file_name):
        with open(file_name, "w") as file:
            file.write("")
            file.close()


def write_csv(file_name: str, data: DataFrame):
    cols = ",".join([col for col in data.columns])
    content = ""
    for index, row in data.iterrows():
        row_data = [
            str(item).replace("True", "1").replace("False", "0") for item in list(row)
        ]
        content += (
            f"\n{row_data}".replace("[", "")
            .replace("]", "")
            .replace("'", "")
            .replace(" ", "")
        )
    with open(file_name, "w") as data_file:
        data_file.seek(0)
        data_file.write(f"{cols}")
        data_file.write(f"{content}")
        data_file.close()


def backup_data(csv_file_name: str, data: DataFrame):
    date_time_str = f"{date.today()}-{datetime.now().hour}:{datetime.now().minute}"
    file_name = csv_file_name.replace(".csv", "_" + date_time_str + ".csv")
    if exists(file_name):
        raise Exception(
            f"File {file_name} already exists. Please move it before proceeding"
        )
    write_csv(file_name, data)


def save_data(data: DataFrame, checkbox_dict: dict, csv_file_name: str, date: str = ""):
    offset = 0
    if date != "":
        if date not in data[date_header].values:
            raise Exception(f"date '{date}' could not be found on the data.")
        row_from_date = df_row_from_date(data, date, date_header)
        row_index = list(row_from_date.index)[0]
        last_index = list(data.index)[-1]
        offset = row_index - last_index - 1
    else:
        offset = -1

    for key in checkbox_dict.keys():
        data.iloc[offset, data.columns.get_loc(to_lower_underscored(key))] = (
            checkbox_dict[key]
        )
    write_csv(csv_file_name, data)
    return data


def save_message_file(
    messages_file_name: str,
    messages: DataFrame,
    todays_message: str,
    view_data_reminder_displayed: bool,
    new_day_time: int
):
    if todays_message not in ("", None, already_filled_in_today_message):
        today = get_today_date(new_day_time)
        messages = create_entry(today, messages)

        ([cat, hab], msg) = (
            todays_message.split("\n")[0].split(category_habit_separator),
            todays_message.split("\n")[1],
        )

        messages.loc[messages.index[-1], MESSAGES_HEADERS.category] = cat
        messages.loc[messages.index[-1], MESSAGES_HEADERS.habit] = hab
        messages.loc[messages.index[-1], MESSAGES_HEADERS.message] = msg.replace(
            '""', ""
        )
        messages.loc[messages.index[-1], MESSAGES_HEADERS.data_reminder] = (
            view_data_reminder_displayed
        )

        messages.to_csv(messages_file_name, index=False)


def save_settings_file(settings_file_name: str, settings: Settings):
    with open(settings_file_name, "w") as s:
        s.write(settings.to_json())
        s.close()

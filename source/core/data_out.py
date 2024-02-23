from pandas import DataFrame
from datetime import date
from os.path import exists, isdir
from os import makedirs

from source.constants import date_header, already_filled_in_today_message
from source.utils import df_row_from_date, to_lower_underscored, flatten_list
from source.core.data_date import get_today_date
from source.core.settings import Settings


def log_write(log_file, new_lines: str):
    log_file.seek(0)
    content: list = log_file.readlines()
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
    file_name = csv_file_name.replace(".csv", "_" + str(date.today()) + ".csv")
    if exists(file_name):
        raise Exception(f"File {file_name} already exists.")
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
    new_day_time: int, msg_file_name: str, header_list: list, todays_message: str
):
    if todays_message == already_filled_in_today_message:
        return

    today = get_today_date(new_day_time)
    header, message = todays_message.split("\n")
    longest_header = max(flatten_list(header_list), key=len)
    spacing = "\t" * (
        len(longest_header) // 4 - len(header) // 4 + (0 if len(header) >= 4 else 1)
    )
    spacing += "" if len(spacing) > 0 else "\t"
    data = f"\n{today}\t{header}{spacing}{message}"
    if not exists(msg_file_name):
        data = data.replace("\n", "")
    with open(msg_file_name, "a") as f:
        f.write(data)
        f.close()


def save_settings_file(settings: Settings, settings_file_name: str):
    with open(settings_file_name, "w") as s:
        s.write(settings.to_json())
        s.close()

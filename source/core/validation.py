from pandas import DataFrame

from source.constants import date_header
from source.utils import to_lower_underscored, replace_commas_for_double_spaces
from source.core.data_date import get_yesterday_date
from source.core.data_out import backup_data


def verify_header_and_data(
    header: list,
    data_variables: list,
    csv_file_name: str,
    data: DataFrame,
    disabled_headers: list,
):
    flat_header = [to_lower_underscored(item) for sublist in header for item in sublist]
    if (
        len([item for item in data_variables if item not in flat_header]) > 0
        or len([item for item in flat_header if item not in data_variables]) > 0
    ):
        for h in data_variables:
            if h not in flat_header and h not in disabled_headers:
                backup_data(csv_file_name, data)
                print("header " + h + " was removed")
                data.drop(h, inplace=True, axis=1)
        for h in flat_header:
            if h not in data_variables:
                backup_data(csv_file_name, data)
                print("header " + h + " was added")
                data[h] = [None for item in range(data.shape[0])]
                # maybe None is not the right value, it should be empty string


def verify_variables(variables_file_name):
    try:
        with open(variables_file_name, "r") as file:
            lines = file.readlines()
            file.close()
        header = lines[0].replace("\n", "").split(",")
        content = [
            replace_commas_for_double_spaces(string_line).replace("\n", "").split(",")
            for string_line in lines[1:]
        ]
        for idx, line in enumerate(content):
            if len(line) != len(header):
                raise Exception(
                    f"verify_variables - Length of line {idx} and header is different from {len(header)}\n{line}"
                )
            if line[0] == "" or line[1] == "":
                raise Exception(
                    f"verify_variables - Cannot have empty value for line {idx} at the first two columns\n{line}"
                )
        df = DataFrame(content, columns=header)
    except Exception as e:
        raise e


def no_data_from_yesterday(new_day_time: int, data: DataFrame):
    yesterday = get_yesterday_date(new_day_time).isoformat()
    last_column_row = data.loc[data[date_header] == yesterday]
    if data.shape[0] <= 1:
        return False

    # { date, "", true, false }
    if len(set(last_column_row.values[0])) <= 2:
        return True
    return False


def rid_message_file_of_blank_lines(msg_file_name: str):
    with open(msg_file_name, "r") as file:
        content = file.readlines()
        file.close()
    with open(msg_file_name, "w") as file:
        content = [
            line for line in content if len(line.replace("\n", "").replace(" ", "")) > 0
        ]
        file.seek(0)
        file.writelines(content)
        file.close()

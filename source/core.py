from datetime import date, timedelta, datetime
from os.path import exists, getsize, isdir
from os import makedirs, path
from random import choice

from .utils import *
from .constants import wakeup_time, date_header, already_filled_in_today_message, SETTINGS_KEYS

from pandas import concat
import json

#region .csv and data
def read_csv(file_name: str, data_file_name: str):
    with open(file_name, 'r') as file:
        lines = file.readlines()
        file.close()
    header = lines[0].replace('\n', '').split(',')
    if file_name == data_file_name:
        content = [stringLine.replace('\n', '').replace(',1', ',True').replace(',0', ',False').split(',') for stringLine in lines[1:]]
    else:
        content = [replace_commas_for_double_spaces(stringLine).replace('\n', '').split(',') for stringLine in lines[1:]]
        content = [[replace_double_spaces_for_commas(string) for string in habit_row] for habit_row in content]
    df = DataFrame(content, columns=header)
    return df

def group_by_category(dataframe: DataFrame, column: str) -> list:
    category_column = "category"
    capitalized_columns = ["header"]
    categories = remove_duplicates(dataframe[category_column])
    result = []
    for category in categories:
        result.append([to_capitalized(x) if column in capitalized_columns else x for x in list(dataframe.loc[dataframe[category_column] == category][column])])
    return result

def get_data(variables_file):
    fractions = group_by_category(variables_file, "frequency")
    conditions = group_by_category(variables_file, "condition")
    habit_messages = group_by_category(variables_file, "message")
    descriptions = group_by_category(variables_file, "tooltip")
    header = group_by_category(variables_file, "header")
    categories = remove_duplicates(flatten_list(group_by_category(variables_file, "category")))
    return conditions, fractions, habit_messages, descriptions, header, categories

def write_csv(file_name: str, data: DataFrame):
    cols = ','.join([col for col in data.columns])
    content = ''
    for index, row in data.iterrows():
        row_data = [str(item).replace('True', '1').replace('False', '0') for item in list(row)]
        content += f'\n{row_data}'.replace("[", "").replace("]", "").replace("'", "").replace(" ", "")
    with open(file_name, 'w') as data_file:
        data_file.seek(0)
        data_file.write(f'{cols}')
        data_file.write(f'{content}')
        data_file.close()

def check_for_todays_entry(lastDate: str) -> int:
    try:
        # Fixes inputting data after midnight
        current_date = date.today() + timedelta(days=-1) if datetime.now().hour < wakeup_time else date.today()
        delta = current_date - date.fromisoformat(lastDate)
    except:
        raise Exception("check_for_todays_entry: Can't parse the date, it needs to be in the format 'yyyy-mm-dd'. \nDatabase probably got corrupted.")
    return delta.days

def get_latest_date(data: DataFrame) -> str:
    return data.iloc[-1][date_header]

def get_current_date() -> datetime.date:
    return date.today() + timedelta(days=-1) if datetime.now().hour < wakeup_time else date.today()

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
        current_date = get_current_date()
        last_date = (current_date + timedelta(days=-1)).isoformat() if last_date is None else last_date

    if delta_days > 0:
        di = dict.fromkeys(data.columns.values, '')
        for day in range(delta_days):
            new_date = date.fromisoformat(last_date)
            di[date_header] = str(new_date + timedelta(days=(day + 1)))
            df_row = DataFrame([di])
            data = concat([data, df_row], ignore_index=True)
    return data

def backup_data(csv_file_name: str, data: DataFrame):
    file_name = csv_file_name.replace('.csv', '_' + str(date.today()) + '.csv')
    if exists(file_name):
        raise Exception(f"File {file_name} already exists.")
    write_csv(file_name, data)

def save_data(data: DataFrame, checkbox_dict: dict, csv_file_name: str, fill_in_yesterday: bool = False, date: str = ''):
    offset = 0
    if date != '':
        if date not in data[date_header].values:
            raise Exception(f"date '{date}' could not be found on the data.")
        row_from_date = df_row_from_date(data, date, date_header)
        row_index = list(row_from_date.index)[0]
        last_index = list(data.index)[-1]
        offset = row_index - last_index - 1
    else:
        offset = -2 if fill_in_yesterday else -1

    for key in checkbox_dict.keys():
        data.iloc[offset, data.columns.get_loc(to_lower_underscored(key))] = checkbox_dict[key]
    write_csv(csv_file_name, data)
    return data

def data_from_date_to_list(data: DataFrame, date: str, header: list):
    row_from_date = df_row_from_date(data, date, date_header)
    result = [[row_from_date[to_lower_underscored(h)].values[0] == 'True' for h in cat] for cat in header]
    return result

def todays_data_or_none(data: DataFrame, header: list):
    today = str(get_current_date())
    if len(data.tail(1)['date'].values) == 0:
        return None
    return data_from_date_to_list(data, today, header) if data.tail(1)['date'].values[0] == today else None

#endregion

#region .txt
def get_matrix_data_by_header_indexes(other_matrix: list, header_matrix: list, header_value: str) -> str:
    for idx1, sublist in enumerate(header_matrix):
        for idx2, item in enumerate(sublist):
            if item == header_value:
                return other_matrix[idx1][idx2]
    print("get_matrix_data_by_header_indexes: Couldn't find description for: " + header_value)
    return ''

def log_write(log_file, new_lines: str):
    log_file.seek(0)
    content: list = log_file.readlines()
    content.insert(0, new_lines)
    log_file.seek(0)
    log_file.write(''.join(content))

def create_folder_if_doesnt_exist(folder_name: str):
    if not isdir(folder_name):
        makedirs(folder_name)

def create_file_if_doesnt_exist(file_name: str):
    if not exists(file_name):
        with open(file_name, 'w') as file:
            file.write('')
            file.close()
#endregion

#region Verifying
def verify_header_and_data(header: list, data_variables: list, csv_file_name: str, data: DataFrame):
    flat_header = [to_lower_underscored(item) for sublist in header for item in sublist]
    if len([item for item in data_variables if item not in flat_header]) > 0 or len([item for item in flat_header if item not in data_variables]) > 0:
        backup_data(csv_file_name, data)
        for h in data_variables:
            if h not in flat_header:
                print("header " + h + " was removed")
                data.drop(h, inplace=True, axis=1)
        for h in flat_header:
            if h not in data_variables:
                print("header " + h + " was added")
                data[h] = [None for item in range(data.shape[0])]

def verify_variables(variables_file_name):
    try:
        with open(variables_file_name, 'r') as file:
            lines = file.readlines()
            file.close()
        header = lines[0].replace('\n', '').split(',')
        content = [replace_commas_for_double_spaces(string_line).replace('\n', '').split(',') for string_line in lines[1:]]
        for idx, line in enumerate(content):
            if len(line) != len(header):
                raise Exception(f"verify_variables - Length of line {idx} and header is different from {len(header)}\n{line}")
            if line[0] == '' or line[1] == '':
                raise Exception(f"verify_variables - Cannot have empty value for line {idx} at the first two columns\n{line}")
        df = DataFrame(content, columns=header)
    except Exception as e:
        raise e

def no_data_from_yesterday(data: DataFrame):
    yesterday = (date.today() + timedelta(days=-2 if datetime.now().hour < wakeup_time else -1)).isoformat()
    last_column_row = data.loc[data[date_header] == yesterday]
    if data.shape[0] <= 1:
        return False

    # TODO Improve code
    if len([v for v in last_column_row.values[0] if v == '']) > 0:
        return True
    return False
#endregion

#region Habit messages
def calculate_frequency(data_frequency: float, nominal_frequency: float, condition: str) -> bool:
    match condition:
        case '>=':
            return data_frequency < nominal_frequency
        case '>':
            return data_frequency <= nominal_frequency
        case '<=':
            return data_frequency > nominal_frequency
        case '<':
            return data_frequency >= nominal_frequency
        # Skips this message
        case '':
            return False
        case _:
            raise Exception(f"calculate_frequency: Condition {condition} {nominal_frequency} is not defined.")

def parse_frequency(column: str, conditions: list, fractions: list, header: list) -> tuple:
    condition = get_matrix_data_by_header_indexes(conditions, header, column)
    fraction = get_matrix_data_by_header_indexes(fractions, header, column)
    if '/' not in fraction:
        return condition, 0, 1
    return condition, int(fraction.split('/')[0]), int(fraction.split('/')[1])

def check_habit(column: str, conditions: list, fractions: list, header: list, data: DataFrame) -> tuple:
    condition, num, den = parse_frequency(column, conditions, fractions, header)
    nominal = num/den
    trues = [1 if str(x) == 'True' else 0 for x in data.loc[:, to_lower_underscored(column)].tail(den)]
    frequency = sum(trues)/len(trues)
    check_if_failed = calculate_frequency(frequency, nominal, condition)
    return (frequency, nominal, check_if_failed)

def determine_successful_today(data: DataFrame, conditions: list, header: list, habit_messages: list) -> list:
    expectation = [[False if d == '<' else True for d in arr] for arr in conditions]

    reality = [[] for item in range(len(header))]
    for idx1, sublist in enumerate(header):
        for idx2, item in enumerate(sublist):
            reality[idx1].append(get_value_from_df_by_row(to_lower_underscored(header[idx1][idx2]), -1, data))

    mission_accomplished_messages = []
    for idx1, sublist in enumerate(reality):
        for idx2, item in enumerate(sublist):
            if reality[idx1][idx2] == expectation[idx1][idx2]:
                mission_accomplished_messages.append(habit_messages[idx1][idx2])
    return mission_accomplished_messages

def get_popup_message(conditions: list, fractions: list, habit_messages: list, header: list, data: DataFrame, msg_file_name: str, random_messages: bool) -> str | None:
    flat_header = flatten_list(header)
    message_data = [(check_habit(h, conditions, fractions, header, data), h, get_matrix_data_by_header_indexes(habit_messages, header, h)) for h in flat_header]
    message_data.sort(key=lambda m: m[0][1], reverse=True)

    # m[0] = (frequency, nominal, failed: bool)
    # m[1] = header
    # m[2] = nessage
    candidate_messages = set([f"{get_matrix_data_by_header_indexes(header, habit_messages, m[2])}\n{m[2]}" for m in message_data if m[0][2]])

    # No idea why this is here
    empty_messages = set([cm if cm.split('\n')[-1] == '' else None for cm in candidate_messages])
    empty_messages.remove(None)
    candidate_messages.difference_update(candidate_messages.intersection(empty_messages))

    past_messages, last_date = read_past_messages(msg_file_name)
    if last_date == str(get_current_date()):
        return already_filled_in_today_message

    previous_message = past_messages[-1] if past_messages is not None else ''
    if previous_message != '' and len(candidate_messages.intersection({previous_message})) > 0:
        candidate_messages.remove(previous_message)

    success_messages = determine_successful_today(data, conditions, header, habit_messages)
    success_messages = list(set(success_messages))
    if '' in success_messages:
        success_messages.remove('')

    sucesses_to_be_removed = [c for c in candidate_messages for s in success_messages if s in c]
    candidate_messages.difference_update(sucesses_to_be_removed)

    if len(candidate_messages) == 0:
        return None

    if not random_messages:
        candidate_messages = [replace_double_spaces_for_commas(c) for c in candidate_messages]
        for m in message_data:
            if f'{m[-2]}\n{m[-1]}' in candidate_messages:
                return f'{m[-2]}\n{m[-1]}'

    return choice(list(candidate_messages))

def read_past_messages(msg_file_name: str) -> (list | None, str | None):
    if not exists(msg_file_name):
        return None, None
    else:
        rid_message_file_of_blank_lines(msg_file_name)
        with open(msg_file_name, 'r') as f:
            # lines = [l.split('\t')[-1].replace('\n', '') for l in f.readlines()]
            lines = [l.replace('\t\t', '\t').split('\t') for l in f.readlines()]
            f.close()
            return [f"{l[1]}\n{l[2]}" for l in lines], lines[-1][0]

def rid_message_file_of_blank_lines(msg_file_name: str):
    with open(msg_file_name, 'r') as file:
        content = file.readlines()
        file.close()
    with open(msg_file_name, 'w') as file:
        content = [line for line in content if len(line.replace('\n', '').replace(' ', '')) > 0]
        file.seek(0)
        file.writelines(content)
        file.close()

def save_message_file(msg_file_name: str, header_list: list, todays_message: str):
    if todays_message == already_filled_in_today_message:
        return

    today = date.today().isoformat()
    header, message = todays_message.split('\n')
    # longest_header = max(header_list, key=len)
    # spacing = '\t' * (len(longest_header) // 4 - len(header) // 4 + 2)
    longest_header = max(flatten_list(header_list), key=len)
    spacing = '\t' * (len(longest_header) // 4 - len(header) // 4)
    spacing += '' if len(spacing) > 0 else '\t'
    data = f"\n{today}\t{header}{spacing}{message}"
    if not exists(msg_file_name):
        data = data.replace('\n', '')
    with open(msg_file_name, 'a') as f:
        f.write(data)
        f.close()
#endregion

#region Settings
class Settings:
    def __init__(self,
                 hue_offset: float = 0,
                 data_days: int = 21,
                 display_messages: bool = True,
                 graph_expected_value: bool = False,
                 scrollable_image: bool = False,
                 message_duration: int = 5,
                 random_messages: bool = True,
                 weekdays_language: str = "jp"
                 ):
        self.hue_offset = hue_offset
        self.data_days = data_days
        self.display_messages = display_messages
        self.graph_expected_value = graph_expected_value
        self.scrollable_image = scrollable_image
        self.message_duration = message_duration
        self.random_messages = random_messages
        self.weekdays_language = weekdays_language

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    @staticmethod
    def from_dict(dictionary: dict):
        hue_offset = float(dictionary[SETTINGS_KEYS.hue_offset])
        data_days = int(dictionary[SETTINGS_KEYS.data_days])
        display_messages = bool(dictionary[SETTINGS_KEYS.display_messages])
        graph_expected_value = bool(dictionary[SETTINGS_KEYS.graph_expected_value])
        scrollable_image = bool(dictionary[SETTINGS_KEYS.scrollable_image])
        message_duration = int(dictionary[SETTINGS_KEYS.message_duration])
        random_messages = bool(dictionary[SETTINGS_KEYS.random_messages])
        weekdays_language = str(dictionary[SETTINGS_KEYS.weekdays_language])
        return Settings(hue_offset,
                        data_days,
                        display_messages,
                        graph_expected_value,
                        scrollable_image,
                        message_duration,
                        random_messages,
                        weekdays_language
                        )

    @staticmethod
    def from_json(jsonString: str):
        json_dict = json.loads(jsonString)
        return Settings.from_dict(json_dict)

def read_settings(settings_file_name: str) -> Settings:
    settings: Settings = Settings()
    if not exists(settings_file_name) or getsize(settings_file_name) == 0:
        with open(settings_file_name, 'w') as s:
            s.write(settings.to_json())
            s.close()

    with open(settings_file_name, 'r') as s:
        settings_file_content = s.read()
        settingsObj = Settings.from_json(settings_file_content)
        s.close()
    return settingsObj

def save_settings_file(settings: Settings, settings_file_name: str):
    with open(settings_file_name, 'w') as s:
        s.write(settings.to_json())
        s.close()

#endregion

#region  Data Visualization
def get_date_array(data: DataFrame, squares: int) -> list:
    latest_date_iso = get_latest_date(data)
    latest_date_value = datetime.fromisoformat(latest_date_iso)
    result = [(latest_date_value + timedelta(days=-day)).strftime("%Y-%m-%d") for day in range(squares)]
    return result

def get_expeted_value(header: str, headerList: list, conditions: list) -> bool:
    condition = get_matrix_data_by_header_indexes(conditions, headerList, header)
    return False if condition in ['=', '<=', '<'] else True

def get_header_data(data: DataFrame, date_array: list, squares: int, header: str, expected_value: bool = True) -> list:
    column_header = to_lower_underscored(header)
    header_data = data[[date_header, column_header]]
    header_data = header_data.reset_index()

    result = [not expected_value for item in range(squares)]
    for index, date_value in enumerate(date_array):
        try:
            data_value = get_value_from_df_by_value(date_header, date_value, header_data)
            value = data_value[column_header].values[0]
            if value == str(expected_value):
                result[index] = expected_value
        except:
            continue
    result.reverse()
    return result

def get_fail_indexes_list(headerData: list, expectedValue: bool = True) -> list:
    result = []
    for index, item in enumerate(headerData):
        if item != expectedValue:
            result.append(index)
    return result
#endregion

#region HabitsInit
def habit_index_from_event(event: str):
    number = event.split('_')[-1]
    return int(number) - 1

def variables_row(category: str, header: str, tooltip: str, message: str, condition: str, numerator: str, denominator: str):
    empty_conditions = ['', None, '-', '_', ' ']
    valid_conditions = empty_conditions + ['>=', '>', '=', '<', '<=']
    if condition not in valid_conditions:
        raise Exception(f"variables_row: condition '{condition}' not in valid_conditions: '{valid_conditions}'")
    if condition in valid_conditions and numerator in ('', ' ', '0'):
        condition = ''

    result = ''
    slap = ',,' if condition in empty_conditions else f'{replace_commas_for_double_spaces(message)},{condition},{numerator}/{denominator}'
    result += f'{category.lower()},{join_white_spaced_header(header.lower())},{tooltip},{slap}\n'
    return result

def generate_variables(variables_file_name: str, variables_init_values_dict: dict, habits_init_category_key: str,
                       habits_init_habit_key: str, habits_init_question_key: str, habit_count: list,
                       habits_init_message_key: str, habits_init_condition_key: str, habits_init_fraction_num_key: str,
                       habits_init_fraction_den_key: str):
    categories = values_from_keyword(habits_init_category_key, variables_init_values_dict)
    repeated_categories = flatten_list([[categories[idx] for i in range(item)] for idx, item in enumerate(habit_count)])
    habits = values_from_keyword(habits_init_habit_key, variables_init_values_dict)
    questions = values_from_keyword(habits_init_question_key, variables_init_values_dict)
    messages = values_from_keyword(habits_init_message_key, variables_init_values_dict)
    conditions = values_from_keyword(habits_init_condition_key, variables_init_values_dict)
    numerators = values_from_keyword(habits_init_fraction_num_key, variables_init_values_dict)
    denominators = values_from_keyword(habits_init_fraction_den_key, variables_init_values_dict)

    header = 'category,header,tooltip,message,condition,frequency'
    file_content = f'{header}\n'
    for i in range(len(repeated_categories)):
        row = variables_row(repeated_categories[i], habits[i], questions[i], messages[i], conditions[i], numerators[i], denominators[i])
        file_content += row

    with open(variables_file_name, 'w') as v:
        v.write(file_content)
        v.close()
#endregion

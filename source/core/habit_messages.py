from pandas import DataFrame
from random import choice

from source.constants import already_filled_in_today_message, category_habit_separator
from source.utils import (
    to_lower_underscored,
    flatten_list,
    replace_double_spaces_for_commas,
    get_value_from_df_by_row,
)
from source.core.data_in import get_matrix_data_by_header_indexes, get_category
from source.core.data_date import get_latest_date, get_today_date


def calculate_frequency(
    data_frequency: float, nominal_frequency: float, condition: str
) -> bool:
    match condition:
        case ">=":
            return data_frequency < nominal_frequency
        case ">":
            return data_frequency <= nominal_frequency
        case "<=":
            return data_frequency > nominal_frequency
        case "<":
            return data_frequency >= nominal_frequency
        # Skips this message
        case "":
            return False
        case _:
            raise Exception(
                f"calculate_frequency: Condition {condition} {nominal_frequency} is not defined."
            )


def parse_frequency(
    column: str, conditions: list, fractions: list, header: list
) -> tuple:
    condition = get_matrix_data_by_header_indexes(conditions, header, column)
    fraction = get_matrix_data_by_header_indexes(fractions, header, column)
    if "/" not in fraction:
        return condition, 0, 1
    return condition, int(fraction.split("/")[0]), int(fraction.split("/")[1])


def check_habit(
    column: str, conditions: list, fractions: list, header: list, data: DataFrame
) -> tuple:
    condition, num, den = parse_frequency(column, conditions, fractions, header)
    nominal = num / den
    trues = [
        1 if str(x) == "True" else 0
        for x in data.loc[:, to_lower_underscored(column)].tail(den)
    ]
    frequency = sum(trues) / len(trues)
    check_if_failed = calculate_frequency(frequency, nominal, condition)
    return (frequency, nominal, check_if_failed)


def determine_successful_today(
    data: DataFrame, conditions: list, header: list, habit_messages: list
) -> list:
    expectation = [[False if d == "<" else True for d in arr] for arr in conditions]

    reality = [[] for item in range(len(header))]
    for idx1, sublist in enumerate(header):
        for idx2, item in enumerate(sublist):
            reality[idx1].append(
                get_value_from_df_by_row(
                    to_lower_underscored(header[idx1][idx2]), -1, data
                )
            )

    mission_accomplished_messages = []
    for idx1, sublist in enumerate(reality):
        for idx2, item in enumerate(sublist):
            if reality[idx1][idx2] == expectation[idx1][idx2]:
                mission_accomplished_messages.append(habit_messages[idx1][idx2])
    return mission_accomplished_messages


def get_popup_message(
    new_day_time: int,
    conditions: list,
    fractions: list,
    habit_messages: list,
    header: list,
    categories: list,
    data: DataFrame,
    messages: DataFrame,
    random_messages: bool,
) -> str | None:
    todays_date = get_today_date(new_day_time)
    flat_header = flatten_list(header)
    message_data = [
        (
            check_habit(h, conditions, fractions, header, data),
            get_category(h, header, categories),
            h,
            get_matrix_data_by_header_indexes(habit_messages, header, h),
        )
        for h in flat_header
    ]
    message_data.sort(key=lambda m: m[0][1], reverse=True)

    # m[0] = (frequency, nominal, failed: bool)
    # m[1] = category
    # m[2] = habit
    # m[3] = message
    candidate_messages = set(
        [
            f"{m[1].upper()}{category_habit_separator}{get_matrix_data_by_header_indexes(header, habit_messages, m[3])}\n{m[3]}"
            for m in message_data
            if m[0][2]
        ]
    )

    # No idea why this is here
    empty_messages = set(
        [cm if cm.split("\n")[-1] == "" else None for cm in candidate_messages]
    )
    if None in empty_messages:
        empty_messages.remove(None)
    candidate_messages.difference_update(
        candidate_messages.intersection(empty_messages)
    )

    last_date = get_latest_date(messages)
    past_messages = list(messages["message"])
    if last_date == todays_date.isoformat() and messages.iloc[-1]["message"] != "":
        return already_filled_in_today_message

    previous_message = past_messages[-1] if past_messages is not None else ""
    if (
        previous_message != ""
        and len(candidate_messages.intersection({previous_message})) > 0
    ):
        candidate_messages.remove(previous_message)

    success_messages = determine_successful_today(
        data, conditions, header, habit_messages
    )
    success_messages = list(set(success_messages))
    if "" in success_messages:
        success_messages.remove("")

    sucesses_to_be_removed = [
        c for c in candidate_messages for s in success_messages if s in c
    ]
    candidate_messages.difference_update(sucesses_to_be_removed)

    if len(candidate_messages) == 0:
        return None

    if not random_messages:
        candidate_messages = [
            replace_double_spaces_for_commas(c) for c in candidate_messages
        ]
        for m in message_data:
            if f"{m[-2]}\n{m[-1]}" in candidate_messages:
                return f"{m[-2]}\n{m[-1]}"

    todays_message = choice(list(candidate_messages))
    return todays_message

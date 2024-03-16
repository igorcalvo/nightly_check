from datetime import date, timedelta
from pandas import DataFrame
from random import choice

from source.core.data_in import get_category, get_matrix_data_by_header_indexes
from source.core.data_date import get_latest_date, get_today_date
from source.constants import (
    already_filled_in_today_message,
    category_habit_separator,
    MESSAGES_HEADERS,
)
from source.utils import (
    flatten_list,
    get_value_from_df_by_row,
    replace_double_spaces_for_commas,
    to_lower_underscored,
    trim_quotes,
)


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
    column: str,
    conditions: list[list[str]],
    fractions: list[list[str]],
    habits: list[list[str]],
) -> tuple[str, int, int]:
    condition = get_matrix_data_by_header_indexes(conditions, habits, column)
    fraction = get_matrix_data_by_header_indexes(fractions, habits, column)
    if "/" not in fraction:
        return condition, 0, 1
    return condition, int(fraction.split("/")[0]), int(fraction.split("/")[1])


def check_habit(
    column: str, conditions: list, fractions: list, habits: list, data: DataFrame
) -> tuple[float, float, bool]:
    condition, num, den = parse_frequency(column, conditions, fractions, habits)
    nominal = num / den
    trues = [
        1 if str(x) == "True" else 0
        for x in data.loc[:, to_lower_underscored(column)].tail(den)
    ]
    frequency = sum(trues) / len(trues)
    check_if_failed = calculate_frequency(frequency, nominal, condition)
    return (frequency, nominal, check_if_failed)


def determine_successful(
    data: DataFrame,
    conditions: list[list[str]],
    habits: list[list[str]],
    habit_messages: list[list[str]],
    dataframe_row: int = -1,
) -> list[str]:
    expectation = [[False if "<" in d else True for d in arr] for arr in conditions]

    reality = [[] for item in range(len(habits))]
    for idx1, sublist in enumerate(habits):
        for idx2, item in enumerate(sublist):
            reality[idx1].append(
                get_value_from_df_by_row(
                    to_lower_underscored(habits[idx1][idx2]), dataframe_row, data
                )
            )

    mission_accomplished_messages = []
    for idx1, sublist in enumerate(reality):
        for idx2, item in enumerate(sublist):
            if reality[idx1][idx2] == expectation[idx1][idx2]:
                mission_accomplished_messages.append(habit_messages[idx1][idx2])
    return mission_accomplished_messages


def format_habit_popup_message(
    category: str, habit: str, message: str, separator: str
) -> str:
    return f"{category.upper()}{separator}{habit}\n{message}"


def get_popup_message(
    new_day_time: int,
    conditions: list[list[str]],
    fractions: list[list[str]],
    habit_messages: list[list[str]],
    habits: list[list[str]],
    categories: list[str],
    data: DataFrame,
    messages: DataFrame,
    random_messages: bool,
) -> str | None:
    flat_habits = flatten_list(habits)
    message_data = [
        (
            check_habit(h, conditions, fractions, habits, data),
            get_category(h, habits, categories),
            h,
            get_matrix_data_by_header_indexes(habit_messages, habits, h),
        )
        for h in flat_habits
    ]
    message_data.sort(key=lambda m: m[0][1], reverse=True)

    # m[0] = (frequency, nominal, failed: bool)
    # m[1] = category
    # m[2] = habit
    # m[3] = message
    candidate_messages = set(
        [
            format_habit_popup_message(
                m[1],
                get_matrix_data_by_header_indexes(habits, habit_messages, m[3]),
                m[3],
                category_habit_separator,
            )
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

    # Checking for message already shown today
    todays_date = get_today_date(new_day_time)
    last_date = get_latest_date(messages)
    past_messages = list(messages[MESSAGES_HEADERS.message])
    if (last_date == str(todays_date)):
        return already_filled_in_today_message

    # Removing message from yesterday
    previous_message = past_messages[-1] if past_messages is not None else ""
    if (
        previous_message != ""
        and len(candidate_messages.intersection({previous_message})) > 0
    ):
        candidate_messages.remove(previous_message)

    # Successes from today
    success_messages_today = determine_successful(
        data, conditions, habits, habit_messages, -1
    )

    # Successes from yesterday
    success_messages_yesterday = determine_successful(
        data, conditions, habits, habit_messages, -2
    )

    # Removing successes
    success_messages = success_messages_today + success_messages_yesterday
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
            msg = format_habit_popup_message(
                m[1],
                get_matrix_data_by_header_indexes(habits, habit_messages, m[3]),
                m[3],
                category_habit_separator,
            )
            if msg in candidate_messages:
                return trim_quotes(msg)

    todays_message = trim_quotes(choice(list(candidate_messages)))
    return todays_message


def should_show_data_visualization_reminder(
    show_data_vis_reminder: bool,
    data_vis_reminder_days: int,
    new_day_time: int,
    messages: DataFrame,
) -> bool:
    if not show_data_vis_reminder:
        return False

    shown = messages.loc[(messages[MESSAGES_HEADERS.data_reminder] == True)]
    if len(shown.values) == 0:
        return True

    latest = shown.iloc[-1][MESSAGES_HEADERS.date]
    today = str(get_today_date(new_day_time))
    if today >= str(
        date.fromisoformat(latest) + timedelta(days=data_vis_reminder_days)
    ):
        return True

    return False

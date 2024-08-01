from source.models.dtos import EditDTO


def get_variables(
    conditions: list[list[str]],
    fractions: list[list[str]],
    habit_messages: list[list[str]],
    descriptions: list[list[str]],
    habits: list[list[str]],
    categories: list[str],
    disabled_habits: list[str],
) -> str:
    edit = EditDTO.from_lists(
        conditions,
        fractions,
        habit_messages,
        descriptions,
        habits,
        categories,
        disabled_habits,
    )
    return edit.to_json()

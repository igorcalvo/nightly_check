from json import dumps
from source.models.variable import Variable


class EditDTO():
    def __init__(self, categories: list[list[Variable]]):
        self.categories = categories

    def to_json(self):
        return dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    @staticmethod
    def from_lists(
        conditions: list[list[str]],
        fractions: list[list[str]],
        habit_messages: list[list[str]],
        descriptions: list[list[str]],
        habits: list[list[str]],
        categories: list[str],
        disabled_habits: list[str],
        ):
        result = []
        for cat_index, category in enumerate(categories):
            category_content = []
            for habit_index, habit in enumerate(habits[cat_index]):
                variable = Variable(
                    enabled=True if not habit in disabled_habits else False,
                    category=category,
                    name=habit,
                    question=descriptions[cat_index][habit_index],
                    message=habit_messages[cat_index][habit_index],
                    condition=conditions[cat_index][habit_index],
                    frequency=fractions[cat_index][habit_index]
                )
                category_content.append(variable)
            result.append(category_content)
        return EditDTO(result)


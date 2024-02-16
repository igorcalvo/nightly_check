from source.constants import SETTINGS_KEYS
from json import dumps, loads


class Settings:
    def __init__(
        self,
        hue_offset: float = 0,
        data_days: int = 21,
        display_messages: bool = True,
        graph_expected_value: bool = False,
        scrollable_image: bool = False,
        message_duration: int = 5,
        random_messages: bool = True,
        weekdays_language: str = "jp",
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
        return dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    @staticmethod
    def from_dict(dictionary: dict):
        hue_offset = round(float(dictionary[SETTINGS_KEYS.hue_offset]), 4)
        data_days = int(dictionary[SETTINGS_KEYS.data_days])
        display_messages = bool(dictionary[SETTINGS_KEYS.display_messages])
        graph_expected_value = bool(dictionary[SETTINGS_KEYS.graph_expected_value])
        scrollable_image = bool(dictionary[SETTINGS_KEYS.scrollable_image])
        message_duration = int(dictionary[SETTINGS_KEYS.message_duration])
        random_messages = bool(dictionary[SETTINGS_KEYS.random_messages])
        weekdays_language = str(dictionary[SETTINGS_KEYS.weekdays_language])
        return Settings(
            hue_offset,
            data_days,
            display_messages,
            graph_expected_value,
            scrollable_image,
            message_duration,
            random_messages,
            weekdays_language,
        )

    @staticmethod
    def from_json(jsonString: str):
        json_dict = loads(jsonString)
        return Settings.from_dict(json_dict)

from source.constants import SETTINGS_KEYS, SETTINGS_DEFAULT_VALUES
from json import dumps, loads


class Settings:
    def __init__(
        self,
        hue_offset: float = SETTINGS_DEFAULT_VALUES.hue_offset,
        theme: str = SETTINGS_DEFAULT_VALUES.theme,
        data_days: int = SETTINGS_DEFAULT_VALUES.data_days,
        display_messages: bool = SETTINGS_DEFAULT_VALUES.display_messages,
        graph_expected_value: bool = SETTINGS_DEFAULT_VALUES.graph_expected_value,
        scrollable_image: bool = SETTINGS_DEFAULT_VALUES.scrollable_image,
        message_duration: int = SETTINGS_DEFAULT_VALUES.message_duration,
        random_messages: bool = SETTINGS_DEFAULT_VALUES.random_messages,
        weekdays_language: str = SETTINGS_DEFAULT_VALUES.weekdays_language,
        new_day_time: int = SETTINGS_DEFAULT_VALUES.new_day_time,
    ):
        self.hue_offset = hue_offset
        self.theme = theme
        self.data_days = data_days
        self.display_messages = display_messages
        self.graph_expected_value = graph_expected_value
        self.scrollable_image = scrollable_image
        self.message_duration = message_duration
        self.random_messages = random_messages
        self.weekdays_language = weekdays_language
        self.new_day_time = new_day_time

    def to_json(self):
        return dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    @staticmethod
    def from_dict(dictionary: dict):
        hue_offset = round(float(dictionary[SETTINGS_KEYS.hue_offset]), 4)
        theme = str(dictionary[SETTINGS_KEYS.theme])
        data_days = int(dictionary[SETTINGS_KEYS.data_days])
        display_messages = bool(dictionary[SETTINGS_KEYS.display_messages])
        graph_expected_value = bool(dictionary[SETTINGS_KEYS.graph_expected_value])
        scrollable_image = bool(dictionary[SETTINGS_KEYS.scrollable_image])
        message_duration = int(dictionary[SETTINGS_KEYS.message_duration])
        random_messages = bool(dictionary[SETTINGS_KEYS.random_messages])
        weekdays_language = str(dictionary[SETTINGS_KEYS.weekdays_language])
        new_day_time = int(dictionary[SETTINGS_KEYS.new_day_time])
        return Settings(
            hue_offset,
            theme,
            data_days,
            display_messages,
            graph_expected_value,
            scrollable_image,
            message_duration,
            random_messages,
            weekdays_language,
            new_day_time,
        )

    @staticmethod
    def from_json(jsonString: str):
        json_dict = loads(jsonString)
        return Settings.from_dict(json_dict)

from PySimpleGUI import WIN_CLOSED
from source.constants import FILE_NAMES, TEXTS_AND_KEYS
from source.core.data_in import read_csv
from source.core.data_vis import image_bytes_to_base64
from source.core.settings import Settings
from source.image_gen import generate_image
from source.ui.data import DataWindow


def Data_Viz_Loop(
    categories: list[str],
    habits: list[list[str]],
    conditions: list[list[str]],
    settings: Settings,
):
    graph_data = read_csv(FILE_NAMES.csv)
    img = generate_image(
        categories,
        habits,
        conditions,
        settings.data_days,
        settings.graph_expected_value,
        settings.weekdays_language,
        graph_data,
    )
    data_window = DataWindow(settings.scrollable_image, settings.data_days, image_bytes_to_base64(img))
    while True:
        data_event, data_values_dict = data_window.read()  # type: ignore
        if data_event == TEXTS_AND_KEYS.export_button_text:
            export_image_file_name = data_values_dict[TEXTS_AND_KEYS.export_button_text]
            if export_image_file_name:
                img.save(export_image_file_name)
        if data_event == WIN_CLOSED or data_event == TEXTS_AND_KEYS.export_button_text:
            data_window.close()
            break

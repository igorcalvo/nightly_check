from source.constants import FILE_NAMES
from source.core.data_in import read_csv
from source.core.data_vis import image_bytes_to_base64
from source.core.settings import Settings
from source.image_gen import generate_image

def Data_Vis_Loop(
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
        settings.data_vis_dark_theme,
        graph_data,
    )
    img_bytes = image_bytes_to_base64(img)
    img.save(export_image_file_name)

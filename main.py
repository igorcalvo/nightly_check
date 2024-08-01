from flask import Flask

from source.constants import FILE_NAMES, ROUTES
from source.core.data_in import get_data, get_data_dataframe, read_csv
from source.core.validation import verify_header_and_data, verify_variables
from source.services.edit import get_variables

nightly = Flask("RE: Nightly Check")

verify_variables(FILE_NAMES.var)
variables_file = read_csv(FILE_NAMES.var)
(
    conditions,
    fractions,
    habit_messages,
    descriptions,
    habits,
    categories,
    disabled_habits,
) = get_data(variables_file)
data = get_data_dataframe(habits)
variables = list(data.columns)
variables.pop(0)
verify_header_and_data(habits, variables, FILE_NAMES.csv, data, disabled_habits)

@nightly.route("/")
def welcome():
    return "hello world!"
    
@nightly.get(f"/{ROUTES.initial}")
def initial_get():
    return "initial"

@nightly.get(f"/{ROUTES.edit}")
def edit_get():
    return get_variables(
        conditions,
        fractions,
        habit_messages,
        descriptions,
        habits,
        categories,
        disabled_habits,
    )

@nightly.post(f"/{ROUTES.edit}")
def edit_post():
    return "edit post"

@nightly.get(f"/{ROUTES.visual}")
def vis_get():
   return "vis get"

@nightly.get(f"/{ROUTES.settings}")
def settings_get():
    return "settings get"

@nightly.post(f"/{ROUTES.settings}")
def settings_post():
    return "settings post"

@nightly.get(f"/{ROUTES.close}")
def close_get():
   return "close get"

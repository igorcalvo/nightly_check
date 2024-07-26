from flask import Flask
from source.constants import ROUTES

nightly = Flask("RE: Nightly Check")

@nightly.route("/")
def welcome():
    return "hello world!"
    
@nightly.get(f"/{ROUTES.initial}")
def initial_get():
    return "initial"

@nightly.get(f"/{ROUTES.edit}")
def edit_get():
    return "edit get"

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

from flask import Blueprint

app_pages = Blueprint("app_pages", __name__, url_prefix="/")

from web_dynamic.resource.login import *

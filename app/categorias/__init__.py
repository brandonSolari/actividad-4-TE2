from flask import Blueprint

bp = Blueprint("categorias", __name__)

from . import routes

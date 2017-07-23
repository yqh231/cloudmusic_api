from flask import Blueprint

api = Blueprint('api', __name__)

from website.app.api import views
from flask import Blueprint
from flask_restplus import Api

plus = Blueprint('plus', __name__)


@plus.before_request
def before_request():
    pass


api = Api(plus)

from . import user, login

from flask import Blueprint, request, jsonify
from flask.views import MethodView
from .models import User
from .schemas import user_schema, users_schema
from . import db

main = Blueprint('main', __name__)
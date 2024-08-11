from flask_smorest import Blueprint
from flask.views import MethodView
from app.extensions import db
from app.models import User
from app.schemas import UserSchema
from flask_jwt_extended import jwt_required
from flask import abort

blp = Blueprint('users', __name__, url_prefix='/users', description='Operations on users')

@blp.route('/')
class Users(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        # To view all the users
        return User.query.all()

    

@blp.route('/<int:id>')
class User(MethodView):
    @jwt_required(optional= True)
    @blp.response(200, UserSchema)
    def get(self, id):
        # To view the profile of a specific company
        user = User.query.get_or_404(id)
        return user

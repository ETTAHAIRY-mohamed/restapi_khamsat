from flask_smorest import Blueprint
from flask.views import MethodView
from app.extensions import db
from app.models import User
from app.schemas import UserSchema

blp = Blueprint('users', __name__, url_prefix='/users', description='Operations on users')

@blp.route('/')
class Users(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        return User.query.all()

    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, new_data):
        user = User(**new_data)
        db.session.add(user)
        db.session.commit()
        return user

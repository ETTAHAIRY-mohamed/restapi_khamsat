from flask_smorest import Blueprint, abort
from flask.views import MethodView
from app.extensions import db
from app.models import User
from app.schemas import UserSchema, UserLoginSchema, UserRegistrationSchema
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

blp = Blueprint('auth', __name__, url_prefix='/auth', description='Authentication operations')

@blp.route('/register', methods=['POST'])
class RegisterUser(MethodView):
    @blp.arguments(UserRegistrationSchema)
    @blp.response(201, UserSchema)
    def post(self, new_data):
        # Hash the password before saving
        new_data['password'] = generate_password_hash(new_data['password'])
        user = User(**new_data)
        db.session.add(user)
        db.session.commit()
        return user

@blp.route('/login', methods=['POST'])
class LoginUser(MethodView):
    @blp.arguments(UserLoginSchema)
    def post(self, login_data):
        user = User.query.filter_by(username=login_data['username']).first()
        if user and check_password_hash(user.password, login_data['password']):
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}
        else:
            abort(401, message="Invalid credentials")

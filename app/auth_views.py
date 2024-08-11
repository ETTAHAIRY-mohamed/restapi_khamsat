from flask_smorest import Blueprint, abort
from flask.views import MethodView
from app.extensions import db
from app.models import AuthUser, User, Company
from app.schemas import UserSchema, UserLoginSchema, UserRegistrationSchema
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from constants import *

blp = Blueprint('auth', __name__, url_prefix='/auth', description='Authentication operations')
    

@blp.route('/register', methods=['POST'])
class RegisterUser(MethodView):
    @blp.arguments(UserRegistrationSchema)
    @blp.response(201, UserSchema)
    def post(self, new_data):
        user_type = new_data.pop('user_type')
        auth_user = AuthUser(username=new_data['username'], 
                             password=generate_password_hash(new_data['password']), 
                             user_type=user_type)

        if user_type == USER_N:
            user = User(**new_data)
            db.session.add(user)
            auth_user.user = user
        elif user_type == COMPANY_N:
            company = Company(**new_data)
            db.session.add(company)
            auth_user.company = company

        db.session.add(auth_user)
        db.session.commit()
        return auth_user

@blp.route('/login', methods=['POST'])
class LoginUser(MethodView):
    @blp.arguments(UserLoginSchema)
    def post(self, login_data):
        auth_user = AuthUser.query.filter_by(username=login_data['username']).first()
        if auth_user and check_password_hash(auth_user.password, login_data['password']):
            access_token = create_access_token(identity=auth_user.id)
            return {'Authorization': f"Bearer {access_token}"}
        else:
            abort(401, message="Invalid credentials")



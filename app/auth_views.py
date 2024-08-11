from flask_smorest import Blueprint, abort
from flask.views import MethodView
from app.extensions import db
from app.models import AuthUser, User, Company
from app.schemas import UserSchema, UserLoginSchema, UserRegistrationSchema
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity
from .constants import *

blp = Blueprint('auth', __name__, url_prefix='/auth', description='Authentication operations')
    

@blp.route('/register', methods=['POST'])
class RegisterUser(MethodView):
    @blp.arguments(UserRegistrationSchema)
    @blp.response(201, UserRegistrationSchema)
    def post(self, new_data):
        # To create a new user
        user_type = new_data.pop('user_type')
        auth_user = AuthUser(username=new_data['username'], 
                             password=generate_password_hash(new_data['password']), 
                             user_type=user_type)

        if user_type == USER_N:
            user = User()
            user.profile_picture = new_data.get('profile_picture')
            user.name = new_data.get('name')
            user.about = new_data.get('about')
            db.session.add(user)
            auth_user.user = user

        elif user_type == COMPANY_N:
            company = Company()
            company.name = new_data.get('name')
            company.logo = new_data.get('logo')
            company.about = new_data.get('about')
            company.address = new_data.get('address')
            db.session.add(company)
            auth_user.company = company

        db.session.add(auth_user)
        db.session.commit()
        return auth_user

@blp.route('/login', methods=['POST'])
class LoginUser(MethodView):
    @blp.arguments(UserLoginSchema)
    def post(self, login_data):
        # To login
        auth_user = AuthUser.query.filter_by(username=login_data['username']).first()
        if auth_user and check_password_hash(auth_user.password, login_data['password']):
            access_token = create_access_token(identity=auth_user.id)
            return {'Authorization': f"Bearer {access_token}"}
        else:
            abort(401, message="Invalid credentials")


@blp.route('/update_profile', methods=['PUT'])
class UpdateProfile(MethodView):
    @jwt_required(optional= True)
    @blp.arguments(UserRegistrationSchema)
    @blp.response(201, UserSchema)
    def put(self, new_data):
        # To update the user's profile || company's profile
        user_id = get_jwt_identity()
        auth_user = AuthUser.query.get_or_404(user_id)

        if 'password' in new_data:
            auth_user.password = generate_password_hash(new_data['password'])
        
        if 'username' in new_data:
            auth_user.username = new_data['username']

        if auth_user.user_type == USER_N:
            user = auth_user.user
            # Update user profile
            user.name = new_data.get('name', user.name)
            user.profile_picture = new_data.get('profile_picture', user.profile_picture)
            user.about = new_data.get('about', user.about)
            db.session.commit()
            return user
            
        elif auth_user.user_type == COMPANY_N:
            company = auth_user.company
            # Update company profile
            company.name = new_data.get('name', company.name)
            company.logo = new_data.get('logo', company.logo)
            company.about = new_data.get('about', company.about)
            company.address = new_data.get('address', company.address)
            db.session.commit()
            return company

        abort(403, 'User type unknown!')
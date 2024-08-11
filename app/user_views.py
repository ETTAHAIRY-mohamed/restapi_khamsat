from flask_smorest import Blueprint
from flask.views import MethodView
from app.extensions import db
from app.models import User
from app.schemas import UserSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import abort

blp = Blueprint('users', __name__, url_prefix='/users', description='Operations on users')

@blp.route('/')
class Users(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        return User.query.all()

    

@blp.route('/<int:id>')
class UserProfile(MethodView):
    @jwt_required(optional=True)
    @blp.response(200, UserSchema)
    def get(self, id):
        user = User.query.get_or_404(id)
        return user

    @jwt_required()
    @blp.arguments(UserSchema)
    @blp.response(200, UserSchema)
    def put(self, updated_data, id):
        current_user_id = get_jwt_identity()
        user = User.query.get_or_404(id)
        
        # Ensure the user is updating their own profile
        if user.id != current_user_id:
            abort(403, message="Unauthorized to update this profile")
        
        # Update user profile
        user.name = updated_data.get('name', user.name)
        user.username = updated_data.get('username', user.username)
        user.profile_picture = updated_data.get('profile_picture', user.profile_picture)
        user.about = updated_data.get('about', user.about)
        db.session.commit()

        return user


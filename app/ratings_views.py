from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Product, Rating, AuthUser
from app.schemas import RatingSchema
from constants import *
from flask import abort

blp = Blueprint('ratings', __name__, url_prefix='/ratings', description='Operations on product ratings')

@blp.route('/')
class Ratings(MethodView):
    @jwt_required(optional=True)
    @blp.arguments(RatingSchema)
    @blp.response(201, RatingSchema)
    def post(self, new_data):
        auth_user_id = get_jwt_identity()  # Get the ID of the logged-in user
        auth_user = AuthUser.query.get_or_404(auth_user_id)

        if not auth_user.user_type == USER_N:
            abort(403, "You don't have this permission")

        new_data['user_id'] = auth_user.user.id  # Add the user ID to the rating data

        rating = Rating(**new_data)
        db.session.add(rating)
        db.session.commit()
        return rating
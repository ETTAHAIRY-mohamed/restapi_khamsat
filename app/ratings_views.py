from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Product, Rating, AuthUser
from app.schemas import RatingSchema, UpdateRatingSchema
from .constants import *
from flask import abort, jsonify

blp = Blueprint('ratings', __name__, url_prefix='/ratings', description='Operations on product ratings')

@blp.route('/')
class Ratings(MethodView):
    @jwt_required(optional=True)  # Ensure authentication
    @blp.arguments(RatingSchema)
    @blp.response(201, RatingSchema)
    def post(self, new_data):
        auth_user_id = get_jwt_identity()  # Get the ID of the logged-in user
        auth_user = AuthUser.query.get_or_404(auth_user_id)

        if auth_user.user_type != USER_N:
            abort(403, description="You don't have this permission")

        if not auth_user.user:
            abort(403, description="No associated user found for the authenticated account")

        # Check if the user has already rated this product
        existing_rating = Rating.query.filter_by(user_id=auth_user.user.id, product_id=new_data['product_id']).first()
        if existing_rating:
            abort(400, description="You have already rated this product")

        new_data['user_id'] = auth_user.user.id  # Add the user ID to the rating data

        rating = Rating(**new_data)
        db.session.add(rating)
        db.session.commit()
        return rating

@blp.route('/<int:rating_id>')
class RatingResource(MethodView):
    @jwt_required()  # Ensure authentication
    @blp.response(200, RatingSchema)
    def get(self, rating_id):
        # Fetch a specific rating
        rating = Rating.query.get_or_404(rating_id)
        return rating

    @jwt_required()
    @blp.arguments(UpdateRatingSchema)
    @blp.response(200, RatingSchema)
    def put(self, updated_data, rating_id):
        # Update a specific rating
        auth_user_id = get_jwt_identity()
        auth_user = AuthUser.query.get_or_404(auth_user_id)

        rating = Rating.query.get_or_404(rating_id)

        if rating.user_id != auth_user.user.id:
            abort(403, description="You can only update your own ratings")

        for key, value in updated_data.items():
            setattr(rating, key, value)
        
        db.session.commit()
        return rating

    @jwt_required()
    def delete(self, rating_id):
        # Delete a specific rating
        auth_user_id = get_jwt_identity()
        auth_user = AuthUser.query.get_or_404(auth_user_id)

        rating = Rating.query.get_or_404(rating_id)

        if rating.user_id != auth_user.user.id:
            abort(403, description="You can only delete your own ratings")

        db.session.delete(rating)
        db.session.commit()
        return jsonify(message="Rating deleted successfully"), 200

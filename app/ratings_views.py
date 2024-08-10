from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Product, Rating
from app.schemas import RatingSchema

blp = Blueprint('ratings', __name__, url_prefix='/ratings', description='Operations on product ratings')

@blp.route('/')
class Ratings(MethodView):
    @jwt_required(optional=True)
    @blp.arguments(RatingSchema)
    @blp.response(201, RatingSchema)
    def post(self, new_data):
        user_id = get_jwt_identity()  # Get the ID of the logged-in user
        new_data['user_id'] = user_id  # Add the user ID to the rating data

        rating = Rating(**new_data)
        db.session.add(rating)
        db.session.commit()
        return rating
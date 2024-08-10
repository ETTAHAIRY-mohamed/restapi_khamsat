from flask_smorest import Blueprint
from flask.views import MethodView
from app.extensions import db
from app.models import Product
from app.schemas import ProductSchema
from flask_jwt_extended import jwt_required
from flask import request

blp = Blueprint('products', __name__, url_prefix='/products', description='Operations on products')

@blp.route('/')
class Products(MethodView):
    @jwt_required(optional=True)
    @blp.response(200, ProductSchema(many=True))
    def get(self):
        search_query = request.args.get('search')
        # include_ratings = request.args.get('include_ratings', 'false').lower() == 'true'
        
        query = Product.query

        if search_query:
            query = query.filter(Product.name.ilike(f'%{search_query}%'))

        products = query.all()

        # if not include_ratings:
        #     # If ratings are not requested, exclude them from the response
        #     for product in products:
        #         product.ratings = []

        return products

    @blp.arguments(ProductSchema)
    @blp.response(201, ProductSchema)
    def post(self, new_data):
        product = Product(**new_data)
        db.session.add(product)
        db.session.commit()
        return product

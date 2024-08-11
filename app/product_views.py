from flask_smorest import Blueprint
from flask.views import MethodView
from app.extensions import db
from app.models import Product, AuthUser
from app.schemas import ProductSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, abort
from constants import *

blp = Blueprint('products', __name__, url_prefix='/products', description='Operations on products')

@blp.route('/')
class Products(MethodView):
    @jwt_required(optional=True)
    @blp.response(200, ProductSchema(many=True))
    def get(self):
        # To view products + you can filter products by category, min|max price
        search_query = request.args.get('search')
        category_filter = request.args.get('category')
        price_min = request.args.get('price_min', type=float)
        price_max = request.args.get('price_max', type=float)
        
        query = Product.query

        if search_query:
            query = query.filter(Product.name.ilike(f'%{search_query}%'))
        if category_filter:
            query = query.filter(Product.category == category_filter)
        if price_min is not None:
            query = query.filter(Product.price >= price_min)
        if price_max is not None:
            query = query.filter(Product.price <= price_max)

        return query.all()

    @jwt_required(optional=True)
    @blp.arguments(ProductSchema)
    @blp.response(201, ProductSchema)
    def post(self, new_data):
        # To add a product
        user_id = get_jwt_identity()
        auth_user = AuthUser.query.get_or_404(user_id)
        if not auth_user.user_type == COMPANY_N:
            abort(403, description = 'You are not authorized to access this resource.')
        
        new_data['company_id'] = auth_user.company.id

        product = Product(**new_data)
        db.session.add(product)
        db.session.commit()
        return product

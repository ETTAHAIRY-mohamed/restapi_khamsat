from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Product, Company, AuthUser
from flask import abort, jsonify
from app.constants import *

blp = Blueprint('favorites', __name__, url_prefix='/favorites', description='Operations on user favorites')

@blp.route('/products/<int:product_id>')
class FavoriteProduct(MethodView):

    @jwt_required()  # Ensure authentication
    def post(self, product_id):
        auth_user_id = get_jwt_identity()  # Get the ID of the logged-in user
        auth_user = AuthUser.query.get_or_404(auth_user_id)

        if auth_user.user_type != USER_N:
            abort(403, description="You don't have permission to perform this action")
        
        user = auth_user.user
        product = Product.query.get_or_404(product_id)

        if product in user.favorite_products:
            return jsonify(message="Product already in favorites"), 400

        user.favorite_products.append(product)
        db.session.commit()
        return jsonify(message="Product added to favorites"), 200

    @jwt_required()
    def delete(self, product_id):
        auth_user_id = get_jwt_identity()  # Get the ID of the logged-in user
        auth_user = AuthUser.query.get_or_404(auth_user_id)

        if auth_user.user_type != USER_N:
            abort(403, description="You don't have permission to perform this action")
        
        user = auth_user.user
        product = Product.query.get_or_404(product_id)

        if product not in user.favorite_products:
            return jsonify(message="Product not in favorites"), 400

        user.favorite_products.remove(product)
        db.session.commit()
        return jsonify(message="Product removed from favorites"), 200


@blp.route('/companies/<int:company_id>')
class FavoriteCompany(MethodView):
    @jwt_required()  # Ensure authentication
    def post(self, company_id):
        auth_user_id = get_jwt_identity()  # Get the ID of the logged-in user
        auth_user = AuthUser.query.get_or_404(auth_user_id)

        if auth_user.user_type != USER_N:
            abort(403, description="You don't have permission to perform this action")
        
        user = auth_user.user
        company = Company.query.get_or_404(company_id)

        if company in user.favorite_companies:
            return jsonify(message="Company already in favorites"), 400

        user.favorite_companies.append(company)
        db.session.commit()
        return jsonify(message="Company added to favorites"), 200

    @jwt_required()
    def delete(self, company_id):
        auth_user_id = get_jwt_identity()  # Get the ID of the logged-in user
        auth_user = AuthUser.query.get_or_404(auth_user_id)

        if auth_user.user_type != USER_N:
            abort(403, description="You don't have permission to perform this action")
        
        user = auth_user.user
        company = Company.query.get_or_404(company_id)

        if company not in user.favorite_companies:
            return jsonify(message="Company not in favorites"), 400

        user.favorite_companies.remove(company)
        db.session.commit()
        return jsonify(message="Company removed from favorites"), 200


@blp.route('/categories/<string:category>')
class FavoriteCategory(MethodView):
    @jwt_required()  # Ensure authentication
    def post(self, category):
        auth_user_id = get_jwt_identity()  # Get the ID of the logged-in user
        auth_user = AuthUser.query.get_or_404(auth_user_id)

        if auth_user.user_type != USER_N:
            abort(403, description="You don't have permission to perform this action")
        
        user = auth_user.user

        if category in user.favorite_categories:
            return jsonify(message="Category already in favorites"), 400

        user.favorite_categories.append(category)
        db.session.commit()
        return jsonify(message="Category added to favorites"), 200

    @jwt_required()
    def delete(self, category):
        auth_user_id = get_jwt_identity()  # Get the ID of the logged-in user
        auth_user = AuthUser.query.get_or_404(auth_user_id)

        if auth_user.user_type != USER_N:
            abort(403, description="You don't have permission to perform this action")
        
        user = auth_user.user

        if category not in user.favorite_categories:
            return jsonify(message="Category not in favorites"), 400

        user.favorite_categories.remove(category)
        db.session.commit()
        return jsonify(message="Category removed from favorites"), 200


@blp.route('/view', methods=['GET'])
class ViewFavorites(MethodView):
    @jwt_required()  # Ensure authentication
    def get(self):
        auth_user_id = get_jwt_identity()  # Get the ID of the logged-in user
        auth_user = AuthUser.query.get_or_404(auth_user_id)

        if auth_user.user_type != USER_N:
            abort(403, description="You don't have permission to perform this action")
        
        user = auth_user.user

        favorite_products = [product.id for product in user.favorite_products]
        favorite_companies = [company.id for company in user.favorite_companies]
        favorite_categories = user.favorite_categories

        return jsonify({
            'favorite_products': favorite_products,
            'favorite_companies': favorite_companies,
            'favorite_categories': favorite_categories
        })

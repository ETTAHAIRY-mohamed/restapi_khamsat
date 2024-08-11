from flask_smorest import Blueprint
from flask.views import MethodView
from app.extensions import db
from app.models import Company, AuthUser
from app.schemas import CompanySchema
from flask import request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from constants import *

blp = Blueprint('companies', __name__, url_prefix='/companies', description='Operations on companies')

@blp.route('/')
class Companies(MethodView):
    @jwt_required(optional=True)
    @blp.response(200, CompanySchema(many=True))
    def get(self):
        # Get query parameters for search
        search_query = request.args.get('search')
        query = Company.query
        # Apply search filtering
        if search_query:
            query = query.filter(Company.name.ilike(f'%{search_query}%'))

        return query.all()


@blp.route('/<int:id>')
class CompanyProfile(MethodView):
    @jwt_required(optional= True)
    @blp.response(200, CompanySchema)
    def get(self, id):
        # To view the profile of a company
        company = Company.query.get_or_404(id)
        return company

    
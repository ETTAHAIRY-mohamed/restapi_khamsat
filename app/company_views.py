from flask_smorest import Blueprint
from flask.views import MethodView
from app.extensions import db
from app.models import Company
from app.schemas import CompanySchema
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

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

    @blp.arguments(CompanySchema)
    @blp.response(201, CompanySchema)
    def post(self, new_data):
        company = Company(**new_data)
        db.session.add(company)
        db.session.commit()
        return company



@blp.route('/<int:id>')
class CompanyProfile(MethodView):
    @jwt_required()
    @blp.response(200, CompanySchema)
    def get(self, id):
        company = Company.query.get_or_404(id)
        return company

    @jwt_required()
    @blp.arguments(CompanySchema)
    @blp.response(200, CompanySchema)
    def put(self, updated_data, id):
        # Ensure the user has permission to update the company profile
        # For example, you might check if the user is an admin or associated with the company

        company = Company.query.get_or_404(id)
        
        # Update company profile
        company.name = updated_data.get('name', company.name)
        company.username = updated_data.get('username', company.username)
        company.logo = updated_data.get('logo', company.logo)
        company.about = updated_data.get('about', company.about)
        company.address = updated_data.get('address', company.address)
        db.session.commit()

        return company

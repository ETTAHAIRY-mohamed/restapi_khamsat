from flask_smorest import Blueprint
from flask.views import MethodView
from app.extensions import db
from app.models import Company
from app.schemas import CompanySchema
from flask import request
from flask_jwt_extended import jwt_required

blp = Blueprint('companies', __name__, url_prefix='/companies', description='Operations on companies')

@blp.route('/')
class Companies(MethodView):
    @jwt_required()
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

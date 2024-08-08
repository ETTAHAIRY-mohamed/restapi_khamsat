from flask_smorest import Blueprint
from flask.views import MethodView
from app.extensions import db
from app.models import Company
from app.schemas import CompanySchema

blp = Blueprint('companies', __name__, url_prefix='/companies', description='Operations on companies')

@blp.route('/')
class Companies(MethodView):
    @blp.response(200, CompanySchema(many=True))
    def get(self):
        return Company.query.all()

    @blp.arguments(CompanySchema)
    @blp.response(201, CompanySchema)
    def post(self, new_data):
        company = Company(**new_data)
        db.session.add(company)
        db.session.commit()
        return company

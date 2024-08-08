from flask_smorest import Blueprint
from flask.views import MethodView
from app.extensions import db
from app.models import Product
from app.schemas import ProductSchema

blp = Blueprint('products', __name__, url_prefix='/products', description='Operations on products')

@blp.route('/')
class Products(MethodView):
    @blp.response(200, ProductSchema(many=True))
    def get(self):
        return Product.query.all()

    @blp.arguments(ProductSchema)
    @blp.response(201, ProductSchema)
    def post(self, new_data):
        product = Product(**new_data)
        db.session.add(product)
        db.session.commit()
        return product

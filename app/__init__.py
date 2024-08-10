from flask import Flask
from flask import Flask
from app.extensions import db, migrate, jwt, api
from app.company_views import blp as CompanyBlueprint
from app.product_views import blp as ProductBlueprint
from app.user_views import blp as UserBlueprint
from app.auth_views import blp as AuthBlueprint
from app.ratings_views import blp as RatingsBlueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    api.init_app(app)

    api.register_blueprint(CompanyBlueprint)
    api.register_blueprint(ProductBlueprint)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(AuthBlueprint)
    api.register_blueprint(RatingsBlueprint)

    with app.app_context():
        db.create_all()

    return app


# db = SQLAlchemy()
# ma = Marshmallow()

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object('config.Config')

#     db.init_app(app)
#     ma.init_app(app)

#     # Enregistrement des blueprints
#     from .views import main as main_blueprint
#     app.register_blueprint(main_blueprint)

#     return app

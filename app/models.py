from app.extensions import db
from datetime import datetime
from .constants import *

user_favorite_products = db.Table('user_favorite_products',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)
user_favorite_companies = db.Table('user_favorite_companies',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('company_id', db.Integer, db.ForeignKey('company.id'), primary_key=True)
)



class AuthUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    user_type = db.Column(db.Integer, db.CheckConstraint(f'user_type IN ({USER_N}, {COMPANY_N})'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=True)

    def __repr__(self):
        return f'<AuthUser {self.username} ({self.user_type})>'



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    profile_picture = db.Column(db.String(256), nullable=True)
    about = db.Column(db.String(256), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Many-to-many relationship with Product
    favorite_products = db.relationship('Product', secondary=user_favorite_products, lazy='subquery',
                                        backref=db.backref('favorited_by_users', lazy=True))
    
    # Many-to-many relationship with company
    favorite_companies = db.relationship('Company', secondary=user_favorite_companies, lazy='subquery',
                                        backref=db.backref('favorited_by_users', lazy=True))
    favorite_categories = db.Column(db.JSON, nullable=True, default=[])

    auth_user = db.relationship('AuthUser', backref='user', uselist=False)

    
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    logo = db.Column(db.String(256), nullable=True)
    about = db.Column(db.String(256), nullable=True)
    address = db.Column(db.String(256), nullable=True)
    products = db.relationship('Product', backref='company', lazy=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    auth_user = db.relationship('AuthUser', backref='company', uselist=False)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    category = db.Column(db.String(128), nullable=False)
    main_image = db.Column(db.String(256), nullable=False)
    additional_images = db.Column(db.JSON, nullable=True)
    price = db.Column(db.Float, nullable=True)
    
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(256), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('User', backref=db.backref('ratings', lazy=True))
    product = db.relationship('Product', backref=db.backref('ratings', lazy=True))

    def __repr__(self):
        return f'<Rating {self.rating} by User {self.user_id} on Product {self.product_id}>'
    
class ProductClick(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    clicked_at = db.Column(db.DateTime, default=datetime.utcnow)

class CategoryClick(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_name = db.Column(db.String(80), nullable=False)
    clicked_at = db.Column(db.DateTime, default=datetime.utcnow)
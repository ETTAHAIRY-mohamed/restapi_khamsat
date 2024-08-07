from app.extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    username = db.Column(db.String(80), nullable=False, unique=True)
    # email = db.Column(db.String(120), unique=True, nullable=False)
    profile_picture = db.Column(db.String(256), nullable=True)
    about = db.Column(db.String(256), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<User {self.username}>'
    
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    username = db.Column(db.String(128), nullable=False, unique=True)
    logo = db.Column(db.String(256), nullable=True)
    about = db.Column(db.String(256), nullable=True)
    address = db.Column(db.String(256), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    products = db.relationship('Product', backref='company', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    category = db.Column(db.String(128), nullable=False)
    main_image = db.Column(db.String(256), nullable=False)
    additional_images = db.Column(db.JSON, nullable=True)
    
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
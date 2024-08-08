# from . import ma
# from .models import User

# class UserSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = User
#         load_instance = True

# user_schema = UserSchema()
# users_schema = UserSchema(many=True)
from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    username = fields.Str(required=True)
    profile_picture = fields.Str()
    about = fields.Str()
    created_at = fields.DateTime(dump_only=True)

class UserRegistrationSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)  # Load only means it won't be included in the serialized output
    profile_picture = fields.Str()
    about = fields.Str()
    created_at = fields.DateTime(dump_only=True)

class UserLoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class CompanySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    username = fields.Str(required=True)
    logo = fields.Str()
    about = fields.Str()
    address = fields.Str()
    created_at = fields.DateTime(dump_only=True)


class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    main_image = fields.Str(required=True)
    additional_images = fields.List(fields.Str())
    company_id = fields.Int(required=True)

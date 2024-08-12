from marshmallow import Schema, fields, validate
from .constants import *

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    username = fields.Str(required=True)
    profile_picture = fields.Str()
    about = fields.Str()
    created_at = fields.DateTime(dump_only=True)

class UserRegistrationSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)  # Load only means it won't be included in the serialized output
    user_type = fields.Int(required=True, validate=validate.OneOf([USER_N, COMPANY_N]))

    # Filelds for user
    profile_picture = fields.Str()

    # Filelds for company
    logo = fields.Str()
    address = fields.Str()

    # Commun fileds
    name = fields.Str(required= True)
    about = fields.Str()
    created_at = fields.DateTime(dump_only=True)

class UserUpdateProfileSchema(Schema):
    username = fields.Str()
    password = fields.Str(load_only=True)  # Load only means it won't be included in the serialized output

    # Filelds for user
    profile_picture = fields.Str()

    # Filelds for company
    logo = fields.Str()
    address = fields.Str()

    # Commun fileds
    name = fields.Str()
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

class RatingSchema(Schema):
    id = fields.Int(dump_only=True)
    rating = fields.Int(required=True)
    comment = fields.Str()
    product_id = fields.Int(required=True)
    user_id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

class UpdateRatingSchema(Schema):
    id = fields.Int(dump_only=True)
    rating = fields.Int()
    comment = fields.Str()
    product_id = fields.Int(dump_only = True)
    user_id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    main_image = fields.Str(required=True)
    additional_images = fields.List(fields.Str())
    ratings = fields.List(fields.Nested(RatingSchema), dump_only=True)
    price = fields.Float(required=True)  # Added price field

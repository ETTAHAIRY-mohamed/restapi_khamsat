from flask import Blueprint, request, jsonify
from flask.views import MethodView
from .models import User
from .schemas import user_schema, users_schema
from . import db

main = Blueprint('main', __name__)

class UserAPI(MethodView):
    def get(self, user_id=None):
        if user_id is None:
            # Return a list of users
            users = User.query.all()
            return users_schema.jsonify(users)
        else:
            # Return a single user
            user = User.query.get(user_id)
            if not user:
                return jsonify({'message': 'User not found'}), 404
            return user_schema.jsonify(user)

    def post(self):
        username = request.json['username']
        email = request.json['email']
        new_user = User(username=username, email=email)
        db.session.add(new_user)
        db.session.commit()
        return user_schema.jsonify(new_user), 201

    def put(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        user.username = request.json.get('username', user.username)
        user.email = request.json.get('email', user.email)
        db.session.commit()
        return user_schema.jsonify(user)

    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted'}), 204

# Create URL routes
user_view = UserAPI.as_view('user_api')
main.add_url_rule('/users', defaults={'user_id': None}, view_func=user_view, methods=['GET'])
main.add_url_rule('/users', view_func=user_view, methods=['POST'])
main.add_url_rule('/users/<int:user_id>', view_func=user_view, methods=['GET', 'PUT', 'DELETE'])

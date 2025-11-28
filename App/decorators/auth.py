from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from App.models import User, Staff

def login_required(required_class):
    def wrapper(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            verify_jwt_in_request()
            identity = get_jwt_identity()
            user = User.query.filter_by(id=identity).first()
            
            if not user:
                return jsonify({"error": "User not found"}), 404

            if not isinstance(user, required_class):
                return jsonify({"error": "Forbidden: invalid role"}), 403

            return fn(*args, **kwargs)
        return decorated
    return wrapper

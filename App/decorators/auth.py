from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity

from App.models import User

def login_required(required_class):
    def wrapper(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            identity = get_jwt_identity()
            user = User.query.filter_by(username=identity).first()

            if not user:
                return jsonify({"error": "User not found"}), 404

            if not isinstance(user, required_class):
                return jsonify({"error": "Forbidden: invalid role"}), 403

            return fn(*args, **kwargs)
        return decorated
    return wrapper

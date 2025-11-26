import os
from functools import wraps
from flask import Flask, render_template, jsonify
from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

from flask_jwt_extended import jwt_required, get_jwt_identity

from App.database import init_db
from App.config import load_config

from App.controllers import (
    setup_jwt,
    add_auth_context
)

from App.models import Employer, Student, Staff, User   # <-- IMPORTANT
from App.views import views


def login_required(required_class):

    def wrapper(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            identity = get_jwt_identity()
            # identity is their username (from login())
            # We find the actual user object
            user = User.query.filter_by(username=identity).first()

            if not user:
                return jsonify({"error": "User not found"}), 404

            # Role check: class type comparison
            if not isinstance(user, required_class):
                return jsonify({"error": "Forbidden: invalid role"}), 403

            return fn(*args, **kwargs)
        return decorated

    return wrapper


def add_views(app):
    for view in views:
        app.register_blueprint(view)


def create_app(overrides={}):
    app = Flask(__name__, static_url_path='/static')
    load_config(app, overrides)
    CORS(app)

    add_auth_context(app)

    photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)

    add_views(app)
    init_db(app)

    jwt = setup_jwt(app)

    @jwt.invalid_token_loader
    @jwt.unauthorized_loader
    def custom_unauthorized_response(error):
        return render_template('401.html', error=error), 401

    app.app_context().push()
    return app


__all__ = ["login_required", "create_app"]

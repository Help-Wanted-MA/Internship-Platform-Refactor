from App.controllers.position import get_all_positions, get_position
from flask import Blueprint, jsonify, request
from App.main import login_required
from flask_jwt_extended import jwt_required, current_user

position_views = Blueprint('position_views', __name__)

# View ONE position
@position_views.route('/positions/<int:position_id>', methods=['GET'])
def view_position(position_id):
    return jsonify(get_position(position_id)), 200

# View ALL positions
@position_views.route('/positions', methods=['GET'])
def view_all_positions():
    return jsonify(get_all_positions()), 200

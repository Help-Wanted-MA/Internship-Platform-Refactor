from flask import Blueprint, jsonify, request
from App.exceptions.handlers import register_error_handlers
from App.controllers import (
    get_all_positions,
    get_position
)

position_views = Blueprint('position_views', __name__)
register_error_handlers(position_views)

# View ONE position
@position_views.route('/positions/<int:position_id>', methods=['GET'])
def view_position(position_id):
    return jsonify(get_position(position_id)), 200

# View ALL positions
@position_views.route('/positions', methods=['GET'])
def view_all_positions():
    return jsonify(get_all_positions()), 200

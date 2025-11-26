from App.models.student import Student
from flask import Blueprint, jsonify, request
from App.decorators.auth import login_required
from App.exceptions.handlers import register_error_handlers
from App.controllers import (
    view_shortlisted_positions,
    view_employer_response
)

student_views = Blueprint('student_views', __name__)
register_error_handlers(student_views)

# View shortlisted positions
@student_views.route('/students/<int:student_id>/applications', methods=['GET'])
@login_required(Student)
def get_shortlisted(student_id):
    state = request.args.get("state")

    if state != "Shortlisted":
        return jsonify({"error": "Invalid state parameter"}), 400
    
    applications = view_shortlisted_positions(student_id)
    return jsonify([a.toJSON() for a in applications]), 200

# View employer response
@student_views.route('/students/<int:student_id>/applications/<int:position_id>', methods=['GET'])
@login_required(Student)
def student_get_employer_response(student_id, position_id):
    response = view_employer_response(student_id, position_id)

    # Wrap the response in a JSON structure
    return jsonify({
        "studentId": student_id,
        "positionId": position_id,
        "status": response
        }), 200
    
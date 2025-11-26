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
def student_shortlisted(student_id):
    state = request.args.get("state")
    if state == "Shortlisted":
        return jsonify(view_shortlisted_positions(student_id)), 200
    return jsonify({"error": "Invalid request"}), 400

# View employer response
@student_views.route('/students/<int:student_id>/applications/<int:application_id>', methods=['GET'])
@login_required(Student)
def student_employer_response(student_id, application_id):
    result = view_employer_response(student_id, application_id)
    return jsonify(result), 200

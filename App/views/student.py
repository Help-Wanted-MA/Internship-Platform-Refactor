from flask_jwt_extended import get_jwt_identity
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
@student_views.route('/students/applications', methods=['GET'])
@login_required(Student)
def get_shortlisted():
    student_id = get_jwt_identity()
    applications = view_shortlisted_positions(student_id)
    return jsonify([application.get_json() for application in applications]), 200

# View employer response
@student_views.route('/students/applications/<int:position_id>', methods=['GET'])
@login_required(Student)
def student_get_employer_response(position_id):
    student_id = get_jwt_identity()
    response = view_employer_response(student_id, position_id)

    return jsonify(response), 200
    
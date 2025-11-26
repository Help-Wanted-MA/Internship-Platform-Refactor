from App.exceptions.handlers import register_error_handlers
from App.models.employer import Employer
from flask import Blueprint, jsonify, request
from App.decorators.auth import login_required
from App.controllers import (
    create_position,
    manage_position_status,
    decide_shortlist,
    get_student
)

employer_views = Blueprint('employer_views', __name__)
register_error_handlers(employer_views)

# Create Internship Position
@employer_views.route('/employers/<int:employer_id>/positions', methods=['POST'])
@login_required(Employer)
def employer_create_position(employer_id):
    data = request.json
    pos = create_position(
        employerId=employer_id,
        title=data["title"],
        requirements=data["requirements"],
        description=data["description"],
        availableSlots=data["availableSlots"]
    )
    return jsonify(pos.toJSON()), 201

# Accept/Reject student from shortlist
@employer_views.route('/employers/<int:employer_id>/applications/<int:application_id>/decision', methods=['PUT'])
@login_required(Employer)
def employer_decide_shortlist(employer_id, application_id):
    data = request.json
    result = decide_shortlist(
        positionId=data["positionId"],
        studentId=data["studentId"],
        decision=data["decision"]
    )
    return jsonify(result.toJSON()), 200

# Open/close position
@employer_views.route('/employers/<int:employer_id>/positions/<int:position_id>/status', methods=['PUT'])
@login_required(Employer)
def employer_status_change(employer_id, position_id):
    data = request.json
    result = manage_position_status(
        employerId=employer_id,
        positionId=position_id,
        status=data["status"]
    )
    return jsonify(result.toJSON()), 200

# Employer view student
@employer_views.route('/employers/<int:employer_id>/students/<int:student_id>', methods=['GET'])
@login_required(Employer)
def employer_view_student(employer_id, student_id):
    student = get_student(student_id)
    return jsonify(student.toJSON()), 200

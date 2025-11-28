from flask_jwt_extended import get_jwt_identity
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
@employer_views.route('/employers/positions', methods=['POST'])
@login_required(Employer)
def employer_create_position():
    employer_id = get_jwt_identity()
    data = request.json
    pos = create_position(
        employerId=employer_id,
        title=data["title"],
        requirements=data["requirements"],
        description=data["description"],
        availableSlots=data["availableSlots"]
    )
    return jsonify({"success": True, "result": pos.get_json()}), 201

# Accept/Reject student from shortlist
@employer_views.route('/employers/positions/<int:position_id>/decision', methods=['PATCH'])
@login_required(Employer)
def employer_decide_shortlist(position_id):
    employer_id = get_jwt_identity()
    data = request.json
    result = decide_shortlist(
        employerId=employer_id,
        positionId=position_id,
        studentId=data["studentId"],
        accept=data["accept"],
        message=data["message"]
    )
    return jsonify({"success": True, "result": result.get_json()}), 200

# Open/close position
@employer_views.route('/employers/positions/<int:position_id>/status', methods=['PATCH'])
@login_required(Employer)
def employer_status_change(position_id):
    employer_id = get_jwt_identity()
    data = request.json
    result = manage_position_status(
        employerId=employer_id,
        positionId=position_id,
        status=data["status"]
    )
    return jsonify({"success": True, "result": result.get_json()}), 200

# Employer view student
@employer_views.route('/employers/students/<int:student_id>', methods=['GET'])
@login_required(Employer)
def employer_view_student(student_id):
    student = get_student(student_id)
    return jsonify(student.get_json()), 200

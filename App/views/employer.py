from flask_jwt_extended import get_jwt_identity
from App.exceptions.handlers import register_error_handlers
from App.models.employer import Employer
from flask import Blueprint, jsonify, request
from App.decorators.auth import login_required
from App.controllers import (
    create_position,
    manage_position_status,
    decide_shortlist,
    get_student,
    view_positions,
    view_position_shortlist
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

# View employer's positions
@employer_views.route('/employers/positions', methods=['GET'])
@login_required(Employer)
def employer_view_positions():
    employer_id = get_jwt_identity()
    positions = view_positions(employer_id)
    return jsonify([position.get_json() for position in positions]), 200

# View shortlist for a position
@employer_views.route('/employers/positions/<int:position_id>', methods=['GET'])
@login_required(Employer)
def employer_view_shortlist(position_id):
    employer_id = get_jwt_identity()
    students = view_position_shortlist(employer_id, position_id)
    return jsonify([student.get_json() for student in students]), 200

# Accept/Reject student from shortlist
@employer_views.route('/employers/positions/<int:position_id>/decision', methods=['PATCH'])
@login_required(Employer)
def employer_decide_shortlist(position_id):
    employer_id = get_jwt_identity()
    data = request.json
    application = decide_shortlist(
        employerId=employer_id,
        positionId=position_id,
        studentId=data["studentId"],
        action=data["action"],
        message=data["message"]
    )
    
    result = {
        "action": data["action"],
        "success": True,
        "ApplicationID": application.id,
        "Student": application.student.username,
        "Position": application.position.title,
        "Employer": application.employer.username,
        "Company": application.employer.company,
        "State": application.state.value
    }
    return jsonify(result), 200

# Open/close position
@employer_views.route('/employers/positions/<int:position_id>/status', methods=['PATCH'])
@login_required(Employer)
def employer_status_change(position_id):
    employer_id = get_jwt_identity()
    data = request.json
    result = manage_position_status(
        employerId=employer_id,
        positionId=position_id,
        action=data["action"]
    )
    
    return jsonify({
        "action": data["action"],
        "success": True, 
        "positionData": result.get_json()
    }), 200

# Employer view student
@employer_views.route('/employers/students/<int:student_id>', methods=['GET'])
@login_required(Employer)
def employer_view_student(student_id):
    student = get_student(student_id)
    return jsonify(student.get_json()), 200

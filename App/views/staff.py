from App.exceptions.handlers import register_error_handlers
from App.models.staff import Staff
from flask import Blueprint, jsonify, request
from App.decorators.auth import login_required
from flask_jwt_extended import get_jwt_identity
from App.controllers import (
    get_all_students,
    get_student,
    shortlist_student,
    get_all_positions
)

staff_views = Blueprint('staff_views', __name__)
register_error_handlers(staff_views)

# View all students
@staff_views.route('/staff/students', methods=['GET'])
@login_required(Staff)
def staff_get_students():
    students = get_all_students()
    return jsonify([student.get_json() for student in students]), 200

# View student
@staff_views.route('/staff/students/<int:student_id>', methods=['GET'])
@login_required(Staff)
def staff_view_student(student_id):
    return jsonify(get_student(student_id).get_json()), 200

# Shortlist student
@staff_views.route('/staff/positions/<int:position_id>/shortlist/<int:student_id>', methods=['PATCH'])
@login_required(Staff)
def staff_shortlist(position_id, student_id):
    staff_id = get_jwt_identity()
    application = shortlist_student(position_id, student_id, staff_id)
    result = {
        "success": True,
        "ApplicationID": application.id,
        "Position": application.position.title,
        "Company": application.position.employer.company,
        "Student": application.student.username,
        "Status": application.state.value,
    }
    return jsonify(result), 200

# View all positions
@staff_views.route('/staff/positions', methods=['GET'])
@login_required(Staff)
def staff_get_positions():
    positions = get_all_positions()
    result = []
    for position in positions:
        json = position.get_json()
        json["company"] = position.employer.company if position.employer else None
        result.append(json)

    return jsonify(result), 200       
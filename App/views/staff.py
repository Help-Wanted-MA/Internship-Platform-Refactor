from App.exceptions.handlers import register_error_handlers
from App.models.staff import Staff
from flask import Blueprint, jsonify, request
from App.decorators.auth import login_required
from App.controllers import (
    get_all_students,
    get_student,
    shortlist_student
)

staff_views = Blueprint('staff_views', __name__)
register_error_handlers(staff_views)

# View all students
@staff_views.route('/staff/students', methods=['GET'])
@login_required(Staff)
def staff_get_students():
    return jsonify(get_all_students()), 200

# View student
@staff_views.route('/staff/students/<int:student_id>', methods=['GET'])
@login_required(Staff)
def staff_view_student(student_id):
    return jsonify(get_student(student_id)), 200

# Shortlist student
@staff_views.route('/staff/applications/<int:application_id>/shortlist', methods=['PUT'])
@login_required(Staff)
def staff_shortlist(application_id):
    data = request.json
    studentId = data["studentId"]
    positionId = data["positionId"]
    result = shortlist_student(studentId, positionId)
    return jsonify(result), 200

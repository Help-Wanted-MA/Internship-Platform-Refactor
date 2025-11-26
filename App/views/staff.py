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
    students = get_all_students()
    return jsonify([s.toJSON() for s in students]), 200

# View student
@staff_views.route('/staff/students/<int:student_id>', methods=['GET'])
@login_required(Staff)
def staff_view_student(student_id):
    return jsonify(get_student(student_id).toJSON()), 200

# Shortlist student
@staff_views.route('/staff/positions/<int:position_id>/shortlist/<int:student_id>', methods=['PUT'])
@login_required(Staff)
def staff_shortlist(position_id, student_id):
    result = shortlist_student(student_id, position_id)
    return jsonify(result.toJSON()), 200

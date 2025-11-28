from App.exceptions.handlers import register_error_handlers
from App.models.staff import Staff
from flask import Blueprint, jsonify, request
from App.decorators.auth import login_required
from flask_jwt_extended import get_jwt_identity
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
    print(f'positionID: {position_id}, studentID: {student_id}')
    staff_id = get_jwt_identity()
    result = shortlist_student(position_id, student_id, staff_id)
    return jsonify({'success': True, "result": result.get_json()}), 200
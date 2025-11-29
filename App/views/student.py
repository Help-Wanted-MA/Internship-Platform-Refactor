from flask_jwt_extended import get_jwt_identity
from App.models.student import Student
from flask import Blueprint, jsonify, request
from App.decorators.auth import login_required
from App.exceptions.handlers import register_error_handlers
from App.controllers import (
    view_shortlisted_positions,
    view_employer_response,
    reject_offer
)

student_views = Blueprint('student_views', __name__)
register_error_handlers(student_views)

# View shortlisted positions
@student_views.route('/students/applications', methods=['GET'])
@login_required(Student)
def get_shortlisted():
    student_id = get_jwt_identity()
    shortlistedPositions = view_shortlisted_positions(student_id)
    
    result = []
    for application in shortlistedPositions:
        position = application.position
        employer = position.employer
        result.append({
            "positionID": position.id,
            "applicationID": application.id,
            "Company": employer.company, 
            "Position": position.title, 
            "Status": application.state.value
        })
        
    return jsonify(result), 200

# View employer response
@student_views.route('/students/applications/<int:position_id>', methods=['GET'])
@login_required(Student)
def student_get_employer_response(position_id):
    student_id = get_jwt_identity()
    application = view_employer_response(student_id, position_id)

    position = application.position
    employer = position.employer
    result = {
        "ApplicationID": application.id,
        "Company": employer.company if employer else None,
        "Employer": employer.username if employer else None,
        "Position": position.title,
        "Status": application.state.value,
        "Employer Response": application.employerResponse
    }
    
    return jsonify(result), 200
    
# Reject offer
@student_views.route('/students/applications/<int:position_id>', methods=['PATCH'])
@login_required(Student)
def student_reject_offer(position_id):
    student_id = get_jwt_identity()
    application = reject_offer(student_id, position_id)
    
    result = {
        "success": True,
        "applicationData": application.get_json()
    }
    
    return jsonify(result), 200
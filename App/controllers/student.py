from App.models import Position, Student, Application
from App.exceptions.exceptions import NotFoundError
from App.states.state_enums import ApplicationStatus

def view_employer_response(studentId, positionId):
    student = Student.query.get(studentId)
    if student is None:
        raise NotFoundError(f'Student with id: {studentId} not found')
    
    position = Position.query.get(positionId)
    if position is None:
        raise NotFoundError(f'Position with id: {positionId} not found')

    application = Application.query.filter_by(studentId=studentId, positionId=positionId).first()
    if application is None:
        raise NotFoundError(f'Application for studentID: {studentId} not found for positionID: {positionId}')
    
    return application.state.value

def view_shortlisted_positions(studentId):
    student = Student.query.get(studentId)
    if student is None:
        raise NotFoundError(f'Student with id: {studentId} not found')
    
    shortlistedApplications = Application.query.filter_by(studentId=studentId, state=ApplicationStatus.SHORTLISTED).all()
    return shortlistedApplications

def get_all_students():
    return Student.query.all()

def get_student(studentId):
    student = Student.query.get(studentId)
    if student is None:
        raise NotFoundError(f'Student with id: {studentId} not found')
    
    return student

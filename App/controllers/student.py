from App.models import Position, Student, Application
from App.exceptions.exceptions import InternalError, NotFoundError
from App.states.state_enums import ApplicationStatus
from App.database import db

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
    
    return application.employerResponse

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

def create_student(username, password, email, degree, resume, gpa):
    try:
        student = Student(username, password, email, degree, resume, gpa)
        db.session.add(student)
        
        positions = Position.query.all()
        for position in positions:
            application = Application(position.id, student.id)
            db.session.add(application)
            
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        raise InternalError(f"Unable to create student: {e}")

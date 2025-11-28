from App.exceptions.exceptions import *
from App.models import Position, Employer, Application, Student
from App.database import db
from sqlalchemy.exc import SQLAlchemyError
from App.states.state_enums import ApplicationStatus, TransitionContext

def create_position(employerId, title, requirements, description, availableSlots):
    employer = Employer.query.get(employerId)

    if employer is None:
        raise NotFoundError(f'Employer with id: {employerId} not found')
    newPosition = Position(employerId=employer.id, title=title, requirements=requirements, description=description, availableSlots=availableSlots)
    db.session.add(newPosition)
    students = Student.query.all()
    for student in students:
        application = Application(newPosition.id, student.id)
        db.session.add(application)
    
    try:
        db.session.commit()
        return newPosition
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e
    
def decide_shortlist(employerId, positionId, studentId, accept, message=None):
    position = Position.query.filter_by(id=positionId, employerId=employerId)
    if position is None:
        raise NotFoundError(f'Position with ID: {positionId} not found for employer with ID: {employerId}')
    
    application = Application.query.filter_by(positionId=positionId, studentId=studentId).first()

    if application is None:
        raise NotFoundError(f'Application for position with ID: {positionId} for StudentID: {studentId}:  not found')
    
    if application.state != ApplicationStatus.SHORTLISTED:
        raise ValidationError(f'Student is not Shortlisted for this position')

    transitionContext = TransitionContext(employerId, message)
    if accept:
        application.accept(transitionContext)
    else:
        application.deny(transitionContext)

    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e
    
    return application

def manage_position_status(employerId, positionId, status):
    position = Position.query.filter_by(id=positionId, employerId=employerId).first()
    status = status.lower()

    if position is None:
        raise NotFoundError(f'Position {positionId} for Employer {employerId}: not found')
    
    if status == "open":
        position.open()
    elif status == "close" or status == "closed":
        position.closed()
    else:
        raise ValidationError(f"Status '{status}' does not exist. Please Enter 'open' or 'closed'")

    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e
    
    return position

def get_all_employers():
    return Employer.query.all()

def get_employer(employerId):
    employer = Employer.query.get(employerId)

    if employer is None:
        raise NotFoundError(f'Employer with id: {employerId} not found')
    
    return employer

def create_employer(username, password, email, company):
    try:
        newuser = Employer(username, password, email, company)
        db.session.add(newuser)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False

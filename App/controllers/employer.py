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
    
def decide_shortlist(employerId, positionId, studentId, action, message=None):
    action = action.lower()
    position = Position.query.filter_by(id=positionId, employerId=employerId).first()
    if position is None:
        raise NotFoundError(f'Position with ID: {positionId} not found for employer with ID: {employerId}')
    
    application = Application.query.filter_by(positionId=positionId, studentId=studentId).first()

    if application is None:
        raise NotFoundError(f'Application for position with ID: {positionId} for StudentID: {studentId}:  not found')
    
    if application.state != ApplicationStatus.SHORTLISTED:
        raise ValidationError(f'Student is not Shortlisted for this position')

    transitionContext = TransitionContext(employerId, message)
    if action == "accept":
        application.accept(transitionContext)
        
        position = Position.query.get(positionId)
        position.availableSlots = position.availableSlots - 1
    elif action == "reject":
        application.deny(transitionContext)
    else:
        raise ValidationError(f"Action '{action}' does not exist. Please Enter `accept` or `reject`")

    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e
    
    return application

def manage_position_status(employerId, positionId, action):
    position = Position.query.filter_by(id=positionId, employerId=employerId).first()
    action = action.lower()

    if position is None:
        raise NotFoundError(f'Position {positionId} does not exist or does not belong to Employer {employerId}')
    
    if action == "open":
        position.open()
    elif action == "close":
        position.closed()
    else:
        raise ValidationError(f"Action '{action}' does not exist. Please Enter `open` or `closed`")

    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e
    
    return position

def view_positions(employerId):
    positions = Position.query.filter_by(employerId=employerId).all()
    return positions

def view_position_shortlist(employerId, positionId):
    position = Position.query.get(positionId)
    if position is None:
        raise NotFoundError(f'Position {positionId} does not exist or does not belong to Employer {employerId}')
    
    if position.employerId != int(employerId):
        raise ValidationError(f'Position does not belong this employer: {employerId}')
    
    shortlistedApplications = Application.query.filter(
        Application.positionId == positionId,
        Application.state != ApplicationStatus.APPLIED
    ).all()
    
    return [application.student for application in shortlistedApplications]
    
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

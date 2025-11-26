from App.exceptions.exceptions import *
from App.models import Position, Employer, Application
from App.database import db
from sqlalchemy.exc import SQLAlchemyError

def create_position(employerId, title, requirements, description, availableSlots):
    employer = Employer.query.filter_by(user_id=employerId).first()

    if employer is None:
        raise NotFoundError(f'Employer with id: {employerId} not found')
    
    newPosition = Position(employerId=employer.id, title=title, requirements=requirements, description=description, availableSlots=availableSlots)
    db.session.add(newPosition)

    try:
        db.session.commit()
        return newPosition
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e
    
def decide_shortlist(positionId, studentId, decision):
    shortList = Application.query.get(positionId=positionId, studentId=studentId)

    if shortList is None:
        raise NotFoundError(f'ShortList at Position {positionId} for Student {studentId}:  not found')
    
    if decision:
        shortList.accept()
    else:
        shortList.deny()

    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e
    
    return shortList

def manage_position_status(employerId, positionId, status):
    position = Position.query.get(id=positionId, employerId=employerId)
    status = status.lower()

    if position is None:
        raise NotFoundError(f'Position {positionId} for Employer {employerId}: not found')
    
    if status == "open":
        position.open()
    elif status == "close" or status == "closed":
        position.closed()
    else:
        raise ValidationError(f'Status "{status}" does not exist. Please Enter "open" or "closed"')

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

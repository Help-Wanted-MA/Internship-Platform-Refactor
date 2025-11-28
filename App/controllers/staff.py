from App.exceptions.exceptions import *
from App.models import Application, Staff
from App.database import db
from sqlalchemy.exc import SQLAlchemyError
from App.states.state_enums import ApplicationStatus, TransitionContext
    
def shortlist_student(positionId, studentId, staff_id):
    application = Application.query.filter_by(positionId=positionId, studentId=studentId).first()
    
    if application is None:
        raise NotFoundError(f'Application at Position {positionId} for Student {studentId}:  not found')
    
    transitionContext = TransitionContext(staff_id)
    if application.state == ApplicationStatus.APPLIED:
        application.accept(transitionContext)
    else:
        raise ValidationError(f'Student is not Applied for this position. Current state: {application.state}')

    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e

    return application

def get_all_staff():
    return Staff.query.all()

def get_staff(staffId):
    staff = Staff.query.get(staffId)

    if staff is None:
        raise NotFoundError(f'Staff with id: {staffId} not found')
    
    return staff

def create_staff(username, password, email):
    try:
        newuser = Staff(username, password, email)
        db.session.add(newuser)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False
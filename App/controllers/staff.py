from App.exceptions.exceptions import *
from App.models import Application, Staff
from App.database import db
from sqlalchemy.exc import SQLAlchemyError
from App.states.state_enums import ApplicationStatus
    
def shortlist_student(studentId, positionId):
    application = Application.query.get(positionId=positionId, studentId=studentId)

    if application is None:
        raise NotFoundError(f'Application at Position {positionId} for Student {studentId}:  not found')
    
    if application.get_state() == ApplicationStatus.APPLIED:
        application.accept()
    else:
        raise ValidationError(f'Student is not Applied for this position')

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
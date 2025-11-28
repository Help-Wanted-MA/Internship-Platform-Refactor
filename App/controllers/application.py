from App.exceptions.exceptions import NotFoundError
from App.models import Application
from App.database import db

def create_application(positionId, studentId):
    try:
        application = Application(positionId, studentId)
        db.session.add(application)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False
    
def get_application(applicationId):
    application = Application.query.get(applicationId)
    if application is None:
        raise NotFoundError(f'application with id: {applicationId} not found')
    
    return application

def get_all_applications():
    return Application.query.all()
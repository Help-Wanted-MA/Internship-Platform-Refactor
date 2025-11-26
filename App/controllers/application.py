from App.exceptions.exceptions import NotFoundError
from App.models import Application

def get_application(applicationId):
    application = Application.query.get(applicationId)
    if application is None:
        raise NotFoundError(f'application with id: {applicationId} not found')
    
    return application

def get_all_applications():
    return Application.query.all()
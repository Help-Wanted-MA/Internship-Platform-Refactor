from App.database import db
from App.states.state_enums import ApplicationStatus
from App.states.enum_state_map import get_state_object
from sqlalchemy import Enum

class Application(db.Model):
    __tablename__ = 'application'
    id = db.Column(db.Integer, primary_key=True)
    positionId = db.Column(db.Integer, db.ForeignKey('position.id'), nullable=False)
    studentId = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    staffId = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=True)
    state = db.Column(Enum(ApplicationStatus, native_enum=False), nullable=False, default=ApplicationStatus.APPLIED)

    def __init__(self, positionId, studentId, staffId):
        self.positionId = positionId
        self.studentId = studentId
        self.staffId = staffId

    def get_state(self):
        return get_state_object(self)
    
    def accept(self):
        return self.get_state().accept()
    
    def deny(self):
        return self.get_state().deny()
    
    def toJSON(self):
        return {
            "id": self.id,
            "positionId": self.positionId,
            "studentId": self.studentId,
            "staffId": self.staffId,
            "state": self.state.value
        }
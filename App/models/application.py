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
    employerId = db.Column(db.Integer, db.ForeignKey('employer.id'), nullable=True)
    employerResponse = db.Column(db.String(256), nullable=True)
    state = db.Column(Enum(ApplicationStatus, native_enum=False), nullable=False, default=ApplicationStatus.APPLIED)
    position = db.relationship("Position", backref="applications", lazy=True)
    student = db.relationship("Student", backref="applications", lazy=True)
    staff = db.relationship("Staff", backref="shortlistedApplications", lazy=True)
    employer = db.relationship("Employer", backref="decidedApplications", lazy=True)
    
    def __init__(self, positionId, studentId):
        self.positionId = positionId
        self.studentId = studentId
        self.state = ApplicationStatus.APPLIED

    def get_state(self):
        return get_state_object(self)
    
    def accept(self, transitionContext):
        return self.get_state().accept(transitionContext)
    
    def deny(self, transitionContext):
        return self.get_state().deny(transitionContext)
    
    def get_json(self):
        return {
            "id": self.id,
            "positionId": self.positionId,
            "studentId": self.studentId,
            "staffId": self.staffId,
            "state": self.state.value,
            "employerId": self.employerId,
            "employerResponse": self.employerResponse
        }
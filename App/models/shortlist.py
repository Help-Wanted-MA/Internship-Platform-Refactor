from App.database import db
from App.models.user import User
from sqlalchemy import Enum
import enum  

class PositionStatus(enum.Enum):
    accepted = "accepted"
    rejected = "rejected"
    pending = "pending"

class Shortlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('Student.id'), nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey('Position.id'))
    staff_id = db.Column(db.Integer, db.ForeignKey('Staff.id'), nullable=False)
    status = db.Column(Enum(PositionStatus, native_enum=False), nullable=False, default=PositionStatus.pending)
    student = db.relationship('Student', backref=db.backref('shortlists', lazy=True))
    position = db.relationship('Position', backref=db.backref('shortlists', lazy=True))
    staff = db.relationship('Staff', backref=db.backref('shortlists', lazy=True))

    def __init__(self, student_id, position_id, staff_id):
        self.student_id = student_id
        self.position_id = position_id
        self.status = "pending"
        self.staff_id = staff_id
        
    def update_status(self, status):
        self.status = PositionStatus(status)
        db.session.commit()
        return self.status

    def student_shortlist(self, student_id):
        return db.session.query(Shortlist).filter_by(student_id=student_id).all()

    def position_shortlist(self, position_id):
        return db.session.query(Shortlist).filter_by(position_id=position_id).all()
        
    def toJSON(self):
        return{
            "id": self.id,
            "student_id": self.student_id,
            "position_id": self.position_id,
            "staff_id": self.staff_id,
            "status": self.status
        }
      
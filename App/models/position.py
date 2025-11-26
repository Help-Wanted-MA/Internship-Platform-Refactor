from App.database import db
from sqlalchemy import Enum
import enum

class PositionStatus(enum.Enum):
    open = "open"
    closed = "closed"

class Position(db.Model):
    __tablename__ = 'position'
    id = db.Column(db.Integer, primary_key=True)
    employerId = db.Column(db.Integer, db.ForeignKey('employer.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    requirements = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    availableSlots = db.Column(db.Integer, nullable=False)
    status = db.Column(Enum(PositionStatus, native_enum=False), nullable=False, default=PositionStatus.open)

    employer = db.relationship("Employer", back_populates="createdPositions")

    def __init__(self, employerId, title, requirements, description, availableSlots):
        self.employerId = employerId
        self.title = title
        self.requirements = requirements
        self.description = description
        self.availableSlots = availableSlots
        self.status = PositionStatus.open

    def open(self):
        self.status = PositionStatus.open
    
    def closed(self):
        self.status = PositionStatus.closed

    def toJSON(self):
        return {
            "id": self.id,
            "employerId": self.employerId,
            "title": self.title,
            "requirements": self.requirements,
            "description": self.description,
            "availableSlots": self.availableSlots,
            "status": self.status.value
        }
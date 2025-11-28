from App.database import db
from App.models.user import User
from datetime import date

class Student(User):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    degree = db.Column(db.String(30), nullable=False)
    resume = db.Column(db.JSON, nullable=False)
    gpa = db.Column(db.Float, nullable=False)
    dob = db.Column(db.Date, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }

    def __init__(self, username, password, email, degree, resume, gpa, dob):
        super().__init__(username, password, email)
        self.degree = degree
        self.resume = resume
        self.gpa = gpa
        self.dob = dob

    def get_age(self):
        today = date.today()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
    
    def get_json(self):
        return{
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'degree': self.degree,
            'resume': self.resume,
            'gpa': self.gpa,
            'dob': self.dob.strftime("%d/%m/%Y")
        }
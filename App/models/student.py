from App.database import db
from App.models.user import User

class Student(User):
    __tablename__ = 'student'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    degree = db.Column(db.String(256))
    gpa = db.Column(db.Float)
    resume = db.Column(db.JSON)

    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }

    def __init__(self, username, password, email, degree, resume, gpa):
        super().__init__(username, password, email)
        self.degree = degree
        self.resume = resume
        self.gpa = gpa
    
    def get_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'degree': self.degree,
            'resume': self.resume,
            'gpa': self.gpa,
        }
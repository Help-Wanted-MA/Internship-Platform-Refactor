from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    
    def __init__(self, username, password, email, role):
        self.username = username
        self.set_password(password)
        self.email = email

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

    def setPassword(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def checkPassword(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
        


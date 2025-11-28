from .user import create_user
from .student import create_student
from .staff import create_staff
from .employer import create_employer, create_position
from App.database import db

def initialize():
    db.drop_all()
    db.create_all()
    create_staff('john', 'johnpass', "staff@email.com")
    create_employer('frank', 'frankpass', "employer@email.com", "company1")
    create_position(2, "Combustion Oil Refinery", "2 working eyes, 1 thumb preferable", "We oil the combustion refinery", 2)
    create_position(2, "Aquarium Lifeguard", "x1 Person, Human preferable", "The Aquarium Lifeguard rescues frowning fish", 5)
    create_student('bob', 'bobpass', "student@email.com", "Computer Science", {"Current Job": "Unemployed", "Likes": "Fish"}, 2.1)
    create_user("defaultuser", "userpass", "user@gmail.com")

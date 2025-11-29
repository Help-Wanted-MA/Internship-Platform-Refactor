from .user import *
from .student import *
from .staff import *
from .employer import *
from App.database import db

def initialize():
    db.drop_all()
    db.create_all()

    create_student('Alice', 'alicepass', "alice@student.com", "Computer Science", {"Current Job": "Intern", "Likes": "AI"}, 3.5)  # ID: 1
    create_student('Bob', 'bobpass', "bob@student.com", "Mechanical Engineering", {"Current Job": "Unemployed", "Likes": "Robotics"}, 2.8)  # ID: 2
    create_student('Carol', 'carolpass', "carol@student.com", "Business", {"Current Job": "Part-time Clerk", "Likes": "Marketing"}, 3.1)  # ID: 3
    create_student('Dave', 'davepass', "dave@student.com", "Marine Biology", {"Current Job": "Unemployed", "Likes": "Diving"}, 3.9)  # ID: 4
    create_student('Eve', 'evepass', "eve@student.com", "Computer Science", {"Current Job": "Unemployed", "Likes": "Cybersecurity"}, 3.2)  # ID: 5

    create_staff('John', 'johnpass', "john@staff.com")  # ID: 6
    create_staff('Mary', 'marypass', "mary@staff.com")  # ID: 7

    create_employer('Frank', 'frankpass', "frank@company1.com", "CompanyOne")  # ID: 8
    create_employer('Grace', 'gracepass', "grace@company2.com", "CompanyTwo")  # ID: 9
    create_employer('Jim', 'jimpass', "jim@company3.com", "CompanyThree")  # ID: 10
    
    create_position(8, "Coal Miner", "A functional body", "Mine coal for the local village", 2)  # ID: 1
    create_position(9, "Aquarium Lifeguard", "Diving experience", "Rescue drowning fish and ensure the safety of marinefolk", 5)  # ID: 2
    create_position(10, "Junior Software Engineer", "Knowledge of Python and SQL", "Assist in software development projects", 3)  # ID: 3
    create_position(8, "Research Assistant", "Lab experience preferred", "Assist in lab experiments and data collection", 1)  # ID: 4
    create_position(9, "Marketing Intern", "Strong communication skills", "Support marketing campaigns and social media", 2)  # ID: 5

    shortlist_student(positionId=2, studentId=4, staff_id=6)
    shortlist_student(positionId=3, studentId=1, staff_id=7)
    shortlist_student(positionId=4, studentId=1, staff_id=6)
    shortlist_student(positionId=5, studentId=3, staff_id=7)
    shortlist_student(positionId=5, studentId=1, staff_id=6)
    shortlist_student(positionId=3, studentId=2, staff_id=7)
    shortlist_student(positionId=5, studentId=2, staff_id=7)
    
    manage_position_status(8, 1, "close")
    decide_shortlist(9, 2, 4, "accept", "Dave, your experience in diving has earned you a position at our company. We look forward to your response.")
    decide_shortlist(10, 3, 1, "accept", "You passion for AI makes you a suitable candidate to join our team. We looking forward to working with you.")
    decide_shortlist(9, 5, 1, "reject", "After careful consideration, we regret to inform you that you have not been selected for this position.")

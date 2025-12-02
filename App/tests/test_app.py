import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash
import pytest_check as check

from App.main import create_app
from App.database import db, create_db
from App.models import User, Employer, Position, Staff, Student, PositionStatus, Application, ApplicationStatus
from App.states.application_states import Applied
from App.states.state_enums import TransitionContext
from App.controllers import (create_student,  get_student, get_all_students, create_staff, get_staff, get_all_staff, create_employer, get_employer, get_all_employers,
                             login, create_position, get_application, get_all_positions, get_all_applications, shortlist_student, view_position_shortlist,
                             decide_shortlist, manage_position_status, view_positions, view_shortlisted_positions, view_employer_response, reject_offer)

pytest.MAX_DIFF = None
unittest.TestCase.maxDiff = None

LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''

class StudentUnitTests(unittest.TestCase):

    def test_create_student_user(self):
        newStudent = Student("Bob", "bobpass", "bob@mail.com", "Computer Science", {
            "name": "Bob",
            "education": {
                "school": "University of the West Indies",
                "bachelor": "B.Sc. Computer Science (Special)"
                },
                "skills": {
                    "langauges": ["C++", "Java", "Python"],
                    "frameworks": ["REST", "JUnit"]
                }
            }, 3.9)
        
        expected = {
            "name": "Bob",
            "email": "bob@mail.com",
            "role": "student",
            "degree": "Computer Science",
            "resume": {
                "name": "Bob",
                "education": {
                    "school": "University of the West Indies",
                    "bachelor": "B.Sc. Computer Science (Special)"
                },
                "skills": {
                    "langauges": ["C++", "Java", "Python"],
                    "frameworks": ["REST", "JUnit"]
                }
            },
            "gpa": 3.9
        }

        actual = {
            "name": newStudent.username,
            "email": newStudent.email,
            "role": newStudent.role,
            "degree": newStudent.degree,
            "resume": newStudent.resume,
            "gpa": newStudent.gpa
        }

        self.assertDictEqual(actual, expected)

    def test_student_get_json(self):
        newStudent = Student("Bob", "bobpass", "bob@mail.com", "Computer Science", {
            "name": "Bob",
            "education": {
                "school": "University of the West Indies",
                "bachelor": "B.Sc. Computer Science (Special)"
                },
                "skills": {
                    "langauges": ["C++", "Java", "Python"],
                    "frameworks": ["REST", "JUnit"]
                }
            }, 3.9)
        
        expected = {
            "id": None,
            "username": "Bob",
            "email": "bob@mail.com",
            "degree": "Computer Science",
            "resume": {
                "name": "Bob",
                "education": {
                    "school": "University of the West Indies",
                    "bachelor": "B.Sc. Computer Science (Special)"
                },
                "skills": {
                    "langauges": ["C++", "Java", "Python"],
                    "frameworks": ["REST", "JUnit"]
                }
            },
            "gpa": 3.9
        }

        studentJson = newStudent.get_json()

        self.assertDictEqual(studentJson, expected)

    def test_hashed_student_password(self):
        student = Student("Bob", "bobpass", "bob@mail.com", "Computer Science", {
            "name": "Bob",
            "education": {
                "school": "University of the West Indies",
                "bachelor": "B.Sc. Computer Science (Special)"
                },
                "skills": {
                    "langauges": ["C++", "Java", "Python"],
                    "frameworks": ["REST", "JUnit"]
                }
            }, 3.9)
        
        assert student.password != "bobpass"

    def test_check_student_password(self):
        student = Student("Bob", "bobpass", "bob@mail.com", "Computer Science", {
            "name": "Bob",
            "education": {
                "school": "University of the West Indies",
                "bachelor": "B.Sc. Computer Science (Special)"
                },
                "skills": {
                    "langauges": ["C++", "Java", "Python"],
                    "frameworks": ["REST", "JUnit"]
                }
            }, 3.9)
        
        assert student.check_password("bobpass")

class EmployerUnitTests(unittest.TestCase):

    def test_create_employer_user(self):
        newEmployer = Employer("Cob", "cobpass", "cob@mail.com", "Cob's Company")
        expected = ["Cob", "cob@mail.com", "employer", "Cob's Company"]
        actual = [newEmployer.username, newEmployer.email, newEmployer.role, newEmployer.company]

        for act, exp in zip(actual, expected):
            check.equal(act, exp)


    def testtest_employer_get_json(self):
        newEmployer = Employer("Cob", "cobpass", "cob@mail.com", "Cob's Company")
        
        expected = {
            "id": None,
            "username": "Cob",
            "email": "cob@mail.com",
            "company": "Cob's Company"
        }

        employerJson = newEmployer.get_json()

        self.assertDictEqual(employerJson, expected)

    def test_hashed_employer_password(self):
        employer = Employer("Cob", "cobpass", "cob@mail.com", "Cob's Company")
        assert employer.password != "cobpass"

    def test_check_employer_password(self):
        employer = Employer("Cob", "cobpass", "cob@mail.com", "Cob's Company")
        assert employer.check_password("cobpass")

class StaffUnitTests(unittest.TestCase):

    def test_create_staff_user(self):
        newStaff = Staff("Dob", "dobpass", "dob@mail.com")
        
        expected = ["Dob", "dob@mail.com", "staff"]
        actual = [newStaff.username, newStaff.email, newStaff.role]

        for act, exp in zip(actual, expected):
            check.equal(act, exp)

    def test_staff_get_json(self):
        newStaff = Staff("Dob", "dobpass", "dob@mail.com")
        
        expected = {
            "id": None,
            "username": "Dob",
            "email": "dob@mail.com"
        }

        staffJson = newStaff.get_json()

        self.assertDictEqual(staffJson, expected)

    def test_hashed_staff_password(self):
        staff = Staff("Dob", "dobpass", "dob@mail.com")
        assert staff.password != "dobpass"

    def test_check_staff_password(self):
        staff = Staff("Dob", "dobpass", "dob@mail.com")
        assert staff.check_password("dobpass")

class PositionUnitTests(unittest.TestCase):

    def test_create_position(self):
        newPosition = Position(1, "NBA Player", "Must be at least 6 feet tall", "Play for NBA", 11)

        expected = [1, "NBA Player", "Must be at least 6 feet tall", "Play for NBA", 11, "open"]
        actual = [newPosition.employerId, newPosition.title, newPosition.requirements, newPosition.description, newPosition.availableSlots, newPosition.status.value]

        for act, exp in zip(actual, expected):
            check.equal(act, exp)

    def test_close_position(self):
        newPosition = Position(1, "NBA Player", "Must be at least 6 feet tall", "Play for NBA", 11)
        newPosition.closed()
        assert newPosition.status.value == "closed"

    def test_open_position(self):
        newPosition = Position(1, "NBA Player", "Must be at least 6 feet tall", "Play for NBA", 11)
        newPosition.status = PositionStatus.closed
        newPosition.open()
        assert newPosition.status.value == "open"

    def test_position_get_json(self):
        position = Position(1, "NBA Player", "Must be at least 6 feet tall", "Play for NBA", 11)

        expected = {
            "id": None,
            "employerId": 1,
            "title": "NBA Player",
            "requirements": "Must be at least 6 feet tall",
            "description": "Play for NBA",
            "availableSlots": 11,
            "status": "open"
        }

        positionJson = position.get_json()

        self.assertDictEqual(positionJson, expected)

class ApplicationUnitTests(unittest.TestCase):

    def test_create_application(self):
        newApplication = Application(1, 1)

        expected = [1, 1, "APPLIED"]
        actual = [newApplication.positionId, newApplication.studentId, newApplication.state.value]

        for act, exp in zip(actual, expected):
            check.equal(act, exp)

    def test_get_application_state(self):
        newApplication = Application(1, 1)
        stateObj = newApplication.get_state()
        assert isinstance(stateObj, Applied)

    def test_shortlisting_application(self):
        application = Application(1, 1)
        resultString = application.accept(TransitionContext(1))

        expected = ["Shortlisted student application!", "SHORTLISTED", 1]
        actual = [resultString, application.state.value, application.staffId]

        for act, exp in zip(actual, expected):
            check.equal(act, exp)

    def test_accepting_application(self):
        application = Application(1, 1)
        application.state = ApplicationStatus.SHORTLISTED
        resultString = application.accept(TransitionContext(1, "Good Application"))

        expected = ["Employer accepted application!", "ACCEPTED", 1, "Good Application"]
        actual = [resultString, application.state.value, application.employerId, application.employerResponse]

        for act, exp in zip(actual, expected):
            check.equal(act, exp)

    def test_accepting_accepted_Application(self):
        application = Application(1, 1)
        application.state = ApplicationStatus.ACCEPTED
        resultString = application.accept(TransitionContext)

        expected = ["Application already accepted.", "ACCEPTED"]
        actual = [resultString, application.state.value]

        for act, exp in zip(actual, expected):
            check.equal(act, exp)

    def test_accepting_rejected_Application(self):
        application = Application(1, 1)
        application.state = ApplicationStatus.REJECTED
        resultString = application.accept(TransitionContext)

        expected = ["Application is rejected. No further action.", "REJECTED"]
        actual = [resultString, application.state.value]

        for act, exp in zip(actual, expected):
            check.equal(act, exp)

    def test_deny_applied_application(self):
        application = Application(1, 1)
        resultString = application.deny(TransitionContext(1))

        expected = ["Application rejected.", "REJECTED", 1]
        actual = [resultString, application.state.value, application.staffId]

        for act, exp in zip(actual, expected):
            check.equal(act, exp)

    def test_deny_shortlisted_application(self):
        application = Application(1, 1)
        application.state = ApplicationStatus.SHORTLISTED
        resultString = application.deny(TransitionContext(1, "Bad Application"))

        expected = ["Employer rejected application.", "Bad Application", 1, "REJECTED"]
        actual = [resultString, application.employerResponse, application.employerId, application.state.value]

        for act, exp in zip(actual, expected):
            check.equal(act, exp)

    def test_deny_accepted_application(self):
        application = Application(1, 1)
        application.state = ApplicationStatus.ACCEPTED
        resultString = application.deny(TransitionContext)

        expected = ["Student rejected offer.", "REJECTED"]
        actual = [resultString, application.state.value]

        for act, exp in zip(actual, expected):
            check.equal(act, exp)

    def test_deny_rejected_application(self):
        application = Application(1, 1)
        application.state = ApplicationStatus.REJECTED
        resultString = application.deny(TransitionContext)

        expected = ["Application already rejected.", "REJECTED"]
        actual = [resultString, application.state.value]

        for act, exp in zip(actual, expected):
            check.equal(act, exp)

    def test_application_get_json(self):
        application = Application(1, 1)

        expected = {
            "id": None,
            "positionId": 1,
            "studentId": 1,
            "staffId": None,
            "state": "APPLIED",
            "employerId": None,
            "employerResponse": None
        }

        applicationJson = application.get_json()

        self.assertDictEqual(applicationJson, expected)

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


class UserCreationIntegrationTests(unittest.TestCase):

    def test_A_create_student_no_positions(self):
        assert create_student("Bob", "bobpass", "bob@mail.com", "Computer Science", {
            "name": "Bob",
            "education": {
                "school": "University of the West Indies",
                "bachelor": "B.Sc. Computer Science (Special)"
                },
                "skills": {
                    "langauges": ["C++", "Java", "Python"],
                    "frameworks": ["REST", "JUnit"]
                }
            }, 3.9)
        
        newStudent = get_student(1)

        expected = {
            "id": 1,
            "name": "Bob",
            "email": "bob@mail.com",
            "degree": "Computer Science",
            "resume": {
                "name": "Bob",
                "education": {
                    "school": "University of the West Indies",
                    "bachelor": "B.Sc. Computer Science (Special)"
                },
                "skills": {
                    "langauges": ["C++", "Java", "Python"],
                    "frameworks": ["REST", "JUnit"]
                }
            },
            "gpa": 3.9
        }

        actual = {
            "id": newStudent.id,
            "name": newStudent.username,
            "email": newStudent.email,
            "degree": newStudent.degree,
            "resume": newStudent.resume,
            "gpa": newStudent.gpa
        }

        self.assertDictEqual(actual, expected)

    def test_B_student_login(self):
        assert login("Bob", "bobpass") != None
        
    def test_C_get_all_student(self):
        students = get_all_students()
        assert students[0].id == 1
        
    def test_D_create_employer(self):
        assert create_employer("Cob", "cobpass", "cob@mail.com", "Cob's Company")

        newEmployer = get_employer(2)

        expected = [2, "Cob", "cob@mail.com", "Cob's Company"]
        actual = [newEmployer.id, newEmployer.username, newEmployer.email, newEmployer.company]

        for act, exp in zip(actual, expected):
            check.equal(act, exp)
        
    def test_E_employer_login(self):
        login("Cob", "cobpass")

    def test_F_get_all_employer(self):
        employers = get_all_employers()
        assert employers[0].id == 2

    def test_G_create_staff(self):
        assert create_staff("Dob", "dobpass", "dob@mail.com")

        newStaff = get_staff(3)

        expected = [3, "Dob", "dob@mail.com"]
        actual = [newStaff.id, newStaff.username, newStaff.email]

        for act, exp in zip(actual, expected):
            check.equal(act, exp)
        
    def test_H_staff_login(self):
        login("Dob", "dobpass")

    def test_I_get_all_staff(self):
        staff = get_all_staff()
        assert staff[0].id == 3

class ApplicationIntegrationTests(unittest.TestCase):

    def test_A_create_position(self):
        newPosition = create_position(2, "NBA Player", "Must be at least 6 feet tall", "Play for NBA", 11)

        expected = [1, 2, "NBA Player", "Must be at least 6 feet tall", "Play for NBA", 11, "open"]
        actual = [newPosition.id, newPosition.employerId, newPosition.title, newPosition.requirements, newPosition.description, newPosition.availableSlots, newPosition.status.value]

        for act, exp in zip(actual, expected):
            check.equal(act, exp)

        newApplication = get_application(1)

        expected = [1, 1, 1, "APPLIED"]
        actual = [newApplication.id, newApplication.positionId, newApplication.studentId, newApplication.state.value]

        for act, exp in zip(actual, expected):
            check.equal(act, exp)

    def test_B_create_student_positions(self):
        assert create_student("Fob", "fobpass", "fob@mail.com", "Basketball Playing", {
            "name": "Fob",
            "education": {
                "school": "University of the West Indies",
                "bachelor": "B.Sc. Play Bball"
                },
                "skills": {
                    "position": ["All"]
                }
            }, 5)
        
        newStudent = get_student(4)
        newApplication = get_application(2)

        expected = {
            "id": 4,
            "name": "Fob",
            "email": "fob@mail.com",
            "degree": "Basketball Playing",
            "resume": {
                "name": "Fob",
                "education": {
                    "school": "University of the West Indies",
                    "bachelor": "B.Sc. Play Bball"
                },
                "skills": {
                    "position": ["All"]
                }
            },
            "gpa": 5
        }

        actual = {
            "id": newStudent.id,
            "name": newStudent.username,
            "email": newStudent.email,
            "degree": newStudent.degree,
            "resume": newStudent.resume,
            "gpa": newStudent.gpa
        }

        self.assertDictEqual(actual, expected)

        expected = [2, 1, 4, "APPLIED"]
        actual = [newApplication.id, newApplication.positionId, newApplication.studentId, newApplication.state.value]

        for act, exp in zip(actual, expected):
            check.equal(act, exp)

    def test_C_get_all_positions(self):
        positions = get_all_positions()
        assert positions[0].id == 1

    def test_D_get_all_applications(self):
        applications = get_all_applications()
        
        for i, app in enumerate(applications):
            check.equal(app.id, i+1)

    def test_E_shortlist_application(self):
        application = shortlist_student(1, 1, 3)
        assert application.state.value == "SHORTLISTED"
        shortlist_student(1, 4, 3)

    def test_F_view_position_shortlist(self):
        positionShortlist = view_position_shortlist(2, 1)
        check.equal(positionShortlist[0].id, 1)
        check.equal(positionShortlist[1].id, 4)

    def test_G_decide_shortlist(self):
        rejectedApplcation = decide_shortlist(2, 1, 1, "reject", "Bad Application")
        acceptedApplcation = decide_shortlist(2, 1, 4, "accept", "Good Application")


        expected = [1, 2,  "REJECTED", "Bad Application"]
        actual = [rejectedApplcation.id, rejectedApplcation.employerId, rejectedApplcation.state.value, rejectedApplcation.employerResponse]

        for act, exp in zip(actual, expected):
            check.equal(act, exp)

        expected = [2, 2,  "ACCEPTED", "Good Application"]
        actual = [acceptedApplcation.id, acceptedApplcation.employerId, acceptedApplcation.state.value, acceptedApplcation.employerResponse]

        for act, exp in zip(actual, expected):
            check.equal(act, exp)

        position = get_all_positions()
        check.equal(position[0].availableSlots, 10)

    def test_H_manage_position_status(self):
        position = manage_position_status(2, 1, "close")
        check.equal(position.status.value, "closed")

    def test_I_view_positions(self):
        positions = view_positions(2)
        check.equal(positions[0].id, 1)

    def test_J_view_shortlisted_positions(self):
        shortlistedPositions = view_shortlisted_positions(4)
        check.equal(shortlistedPositions[0].id, 2)

    def test_K_view_employer_response(self):
        application = view_employer_response(1, 1)
        check.equal(application.employerResponse, "Bad Application")

    def test_L_test_reject_offer(self):
        application = reject_offer(4, 1)
        check.equal(application.state.value, "REJECTED")
        
        position = get_all_positions()
        check.equal(position[0].availableSlots, 11)
import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash
import pytest_check as check

from App.main import create_app
from App.database import db, create_db
from App.models import User, Employer, Position, Staff, Student, PositionStatus, Application, ApplicationStatus
from App.states.application_states import Applied
from App.states.state_enums import TransitionContext
""" from App.controllers import () """

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
        assert "closed" == newPosition.status.value

    def test_open_position(self):
        newPosition = Position(1, "NBA Player", "Must be at least 6 feet tall", "Play for NBA", 11)
        newPosition.status = PositionStatus.closed
        newPosition.open()
        assert "open" == newPosition.status.value

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

""" class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass")
        assert user.username == "bob"

    def test_new_student(self):
            student = Student("john", "johnpass")
            assert student.username == "john"
            assert student.role == "student"

    def test_new_staff(self):
        staff = Staff("jim", "jimpass")
        assert staff.username == "jim"
        assert staff.role == "staff"

    def test_new_employer(self):
        employer = Employer("alice", "alicepass")
        assert employer.username == "alice"
        assert employer.role == "employer"

    def test_new_position(self):
        position = Position("Software Developer", 10, 5) 
        assert position.title == "Software Developer"
        assert position.employer_id == 10
        assert position.status == "open"
        assert position.number_of_positions == 5

    def test_new_shortlist(self):
        shortlist = Shortlist(1,2,3)
        assert shortlist.student_id == 1
        assert shortlist.position_id == 2
        assert shortlist.staff_id == 3
        assert shortlist.status == "pending"

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = User("bob", "bobpass")
        user_json = user.get_json()
        self.assertEqual(user_json["username"], "bob")
        self.assertTrue("id" in user.get_json())
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password)
        user = User("bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.check_password(password) """

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="function")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    
    with app.app_context():
        create_db()
        yield app.test_client()
        db.drop_all()


class UserIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        
        staff = create_user("rick", "bobpass", "staff")
        assert staff.username == "rick" 

        employer = create_user("sam", "sampass", "employer")
        assert employer.username == "sam"

        student = create_user("hannah", "hannahpass", "student")
        assert student.username == "hannah"

   # def test_get_all_users_json(self):
     #   users_json = get_all_users_json()
      #  self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

    # Tests data changes in the database
    #def test_update_user(self):
      #  update_user(1, "ronnie")
      #  user = get_user(1)
       # assert user.username == "ronnie"
        
    def test_open_position(self):
        position_count = 2
        employer = create_user("sally", "sallypass", "employer")
        assert employer is not None
        position = open_position("IT Support", employer.id, position_count)
        positions = get_positions_by_employer(employer.id)
        assert position is not None
        assert position.number_of_positions == position_count
        assert len(positions) > 0
        assert any(p.id == position.id for p in positions)
        
        invalid_position = open_position("Developer",-1,1)
        assert invalid_position is False


    def test_add_to_shortlist(self):
        position_count = 3
        staff = create_user("linda", "lindapass", "staff")
        assert staff is not None
        student = create_user("hank", "hankpass", "student")
        assert student is not None
        employer =  create_user("ken", "kenpass", "employer")
        assert employer is not None
        position = open_position("Database Manager", employer.id, position_count)
        invalid_position = open_position("Developer",-1,1)
        assert invalid_position is False
        added_shortlist = add_student_to_shortlist(student.id, position.id ,staff.id)
        assert position is not None
        assert (added_shortlist)
        shortlists = get_shortlist_by_student(student.id)
        assert any(s.id == added_shortlist.id for s in shortlists)


    def test_decide_shortlist(self):
        position_count = 3
        student = create_user("jack", "jackpass", "student")
        assert student is not None
        staff = create_user ("pat", "patpass", "staff")
        assert staff is not None
        employer =  create_user("frank", "pass", "employer")
        assert employer is not None
        position = open_position("Intern", employer.id, position_count)
        assert position is not None
        stud_shortlist = add_student_to_shortlist(student.id, position.id ,staff.id)
        assert (stud_shortlist)
        decided_shortlist = decide_shortlist(student.id, position.id, "accepted")
        assert (decided_shortlist)
        shortlists = get_shortlist_by_student(student.id)
        assert any(s.status == PositionStatus.accepted for s in shortlists)
        assert position.number_of_positions == (position_count-1)
        assert len(shortlists) > 0
        invalid_decision = decide_shortlist(-1, -1, "accepted")
        assert invalid_decision is False


    def test_student_view_shortlist(self):

        student = create_user("john", "johnpass", "student")
        assert student is not None
        staff = create_user ("tim", "timpass", "staff")
        assert staff is not None
        employer =  create_user("joe", "joepass", "employer")
        assert employer is not None
        position = open_position("Software Intern", employer.id, 4)
        assert position is not None
        shortlist = add_student_to_shortlist(student.id, position.id ,staff.id)
        shortlists = get_shortlist_by_student(student.id)
        assert any(shortlist.id == s.id for s in shortlists)
        assert len(shortlists) > 0

    # Tests data changes in the database
    #def test_update_user(self):
    #    update_user(1, "ronnie")
    #   user = get_user(1)
    #   assert user.username == "ronnie"


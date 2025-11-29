import click, pytest, sys
from flask.cli import with_appcontext, AppGroup
from App.database import db, get_migrate
from App.models import User
from App.main import create_app
from App.controllers import (create_user, get_all_users_json, get_all_users, initialize, get_all_applications,
                             get_application, create_position, decide_shortlist, get_all_employers, get_employer,
                             manage_position_status, get_all_positions, get_position, get_all_students, get_student,
                             view_employer_response, view_shortlisted_positions, create_employer)


# This commands file allow you to create convenient CLI commands for testing controllers
app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')


'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands')


# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
@click.argument("user_type", default="student")
def create_user_command(username, password, user_type):
    result = create_user(username, password, user_type)
    if result:
        print(f'{username} created successfully')
    else:
        print("User creation failed")


@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())


app.cli.add_command(user_cli)


'''
Employer Commands
'''


employer_cli = AppGroup('employer', help='Employer object commands')


@employer_cli.command("create", help="Creates a new employer account")
@click.argument("username")
@click.argument("password")
@click.argument("email")
@click.argument("company")
def employer_create_command(username, password, email, company):
    try:
        result = create_employer(username, password, email, company)
        if result:
            print(f"Employer '{username}' created successfully")
        else:
            print("Employer creation failed")
    except Exception as e:
        print(e)
        print("------------------------------------------------------------------------\n")


@employer_cli.command("list", help="Lists all employers in the database")
def list_employers_command():
    employers = get_all_employers()
    if employers:
        print("========================================================================")
        print(f"{'ID':<5} {'Username':<22} {'Company':<100}")
        print("------------------------------------------------------------------------")
        for emp in employers:
            print(f"{emp.id:<5} {emp.username:<22} {emp.company:<100}")
        print("------------------------------------------------------------------------\n")
    else:
        print("No employers found")


@employer_cli.command("get", help="Gets a specific employer by ID")
@click.argument("employer_id", type=int)
def get_employer_command(employer_id):
    try:
        employer = get_employer(employer_id)
        print("========================================================================")
        print(f"{'ID':<5} {'Username':<22} {'Company':<100}")
        print("------------------------------------------------------------------------")
        print(f"{employer.id:<5} {employer.username:<22} {employer.company:<100}")
        print("------------------------------------------------------------------------\n")
    except Exception as e:
        print(e)
        

@employer_cli.command("create_position", help="Creates a new internship position")
@click.argument("employer_id", type=int)
@click.argument("title")
@click.argument("requirements")
@click.argument("description")
@click.argument("available_slots", type=int)
def employer_create_position_command(employer_id, title, requirements, description, available_slots):

    try:
        position = create_position(employer_id, title, requirements, description, available_slots)
        
        print("  Position created successfully!")
        print(f"  Position ID: {position.id}")
        print(f"  Title: {position.title}")
        print(f"  Requirements: {position.requirements}")
        print(f"  Description: {position.description}")
        print(f"  Available Slots: {position.availableSlots}")
        print(f"  Status: {position.status.value}")
        print("------------------------------------------------------------------------\n")
        
    except Exception as e:
        print(e)
        print("------------------------------------------------------------------------\n")


@employer_cli.command("decide_shortlist", help="Accept or reject a shortlisted student")
@click.argument("employer_id", type=int)
@click.argument("position_id", type=int)
@click.argument("student_id", type=int)
@click.argument("decision")
@click.argument("message", default="")
def employer_decide_shortlist_command(employer_id, position_id, student_id, decision, message):
    
    try:
        decision_lower = decision.lower()
        if decision_lower not in ['accept', 'reject']:
            print(f"Decision must be 'accept' or 'reject', you typed: '{decision}'")
            return
        
        if decision_lower == 'accept':
            accept_bool = True
        else:
            accept_bool = False
        application = decide_shortlist(employer_id, position_id, student_id, accept_bool, message)
        
        print("  Student shortlist decision recorded!")
        print(f"  Position ID: {position_id}")
        print(f"  Student ID: {student_id}")
        print(f"  Decision: {decision_lower.upper()}")
        print(f"  Application Status: {application.state.value}")
        print("------------------------------------------------------------------------\n")
        
    except Exception as e:
        print(e)
        print("------------------------------------------------------------------------\n")


@employer_cli.command("manage_status", help="Open or close an internship position")
@click.argument("employer_id", type=int)
@click.argument("position_id", type=int)
@click.argument("status")
def employer_manage_status_command(employer_id, position_id, status):

    try:
        position = manage_position_status(employer_id, position_id, status)
        
        print("  Position status updated successfully!")
        print(f"  Position ID: {position_id}")
        print(f"  Position Title: {position.title}")
        print(f"  New Status: {position.status.value}")
        print("------------------------------------------------------------------------\n")
        
    except Exception as e:
        print(e)
        print("------------------------------------------------------------------------\n")
        
        
app.cli.add_command(employer_cli)



'''
Student Commands
'''

student_cli = AppGroup('student', help='Student object commands')

@student_cli.command("get", help="Gets a specific student by ID")
@click.argument("student_id", type=int)
def get_student_command(student_id):
    try:
        student = get_student(student_id)
        print(f'Student ID: {student.id} | Username: {student.username} | Degree: {student.degree} | GPA: {student.gpa}')
        print("------------------------------------------------------------------------\n")
    except Exception as e:
        print(e)

@student_cli.command("list", help="Lists all students in the database")
def list_students_command():
    students = get_all_students()
    if students:
        for stu in students:
            print(f'Student ID: {stu.id} | Username: {stu.username} | Degree: {stu.degree} | GPA: {stu.gpa}')
        print("------------------------------------------------------------------------\n")
    else:
        print("No students found")

@student_cli.command("view_response", help="View employer response for a specific application")
@click.argument("student_id", type=int)
@click.argument("position_id", type=int)
def view_employer_response_command(student_id, position_id):
    try:
        response = view_employer_response(student_id, position_id)
        print(f'Employer Response for Student ID {student_id} on Position ID {position_id}:')
        print(f'"{response}"')
        print("------------------------------------------------------------------------\n")
    except Exception as e:
        print(e)
        print("------------------------------------------------------------------------\n")

@student_cli.command("view_shortlisted", help="View all shortlisted positions for a student")
@click.argument("student_id", type=int)
def view_shortlisted_positions_command(student_id):
    try:
        applications = view_shortlisted_positions(student_id)
        if applications:
            print(f'Shortlisted Positions for Student ID {student_id}:')
            for app in applications:
                print(f'Position ID: {app.positionId} | Application Status: {app.state.value}')
            print("------------------------------------------------------------------------\n")
        else:
            print(f'No shortlisted positions found for Student ID {student_id}.')
    except Exception as e:
        print(e)
        print("------------------------------------------------------------------------\n")

app.cli.add_command(student_cli)



'''
Generic Commands
'''


generic_cli = AppGroup('view', help='Generic view commands')


@generic_cli.command("application", help="View details of a specific application")
@click.argument("application_id", type=int)
def view_application_command(application_id):
    
    try:
        application = get_application(application_id)
        
        print("\n========================================================================")
        print("APPLICATION DETAILS")
        print("========================================================================")
        print(f"Application ID: {application.id}")
        print(f"Position ID: {application.positionId}")
        print(f"Student ID: {application.studentId}")
        print(f"Current Status: {application.get_state().value}")
        print("========================================================================\n")
        
    except Exception as e:
        print(e)
        print("------------------------------------------------------------------------\n")


@generic_cli.command("applications", help="View all applications in the system")
def view_all_applications_command():

    try:
        applications = get_all_applications()
        
        if not applications:
            print("\nNo applications found.\n")
            return
        
        print("\n========================================================================")
        print("ALL APPLICATIONS")
        print("========================================================================")
        print(f"{'App ID':<8} {'Position ID':<12} {'Student ID':<12} {'Status':<20}")
        print("------------------------------------------------------------------------")
        
        for app in applications:
            status = app.state.value
            print(f"{app.id:<8} {app.positionId:<12} {app.studentId:<12} {status:<20}")
        
        print("========================================================================")
        
    except Exception as e:
        print(e)
        print("------------------------------------------------------------------------\n")


@generic_cli.command("position", help="View details of a specific internship position")
@click.argument("position_id", type=int)
def view_position_command(position_id):

    try:
        position = get_position(position_id)
        
        print("\n========================================================================")
        print("POSITION DETAILS")
        print("========================================================================")
        print(f"Position ID: {position.id}")
        print(f"Employer ID: {position.employerId}")
        print(f"Title: {position.title}")
        print(f"Requirements: {position.requirements}")
        print(f"Description: {position.description}")
        print(f"Available Slots: {position.availableSlots}")
        print(f"Status: {position.status.value}")
        print("========================================================================\n")
        
    except Exception as e:
        print(e)
        print("------------------------------------------------------------------------\n")


@generic_cli.command("positions", help="View all available internship positions")
def view_all_positions_command():

    try:
        positions = get_all_positions()
        
        if not positions:
            print("\nNo positions found in the system.\n")
            return
        
        print("\n========================================================================")
        print("ALL INTERNSHIP POSITIONS")
        print("========================================================================")
        print(f"{'Pos ID':<8} {'Employer':<10} {'Title':<25} {'Slots':<6} {'Status':<15}")
        print("------------------------------------------------------------------------")
        
        for pos in positions:
            # Literally all this does is truncate the title, adding ... to the end of it, if it's too long.
            title = pos.title[:22] + "..." if len(pos.title) > 25 else pos.title
            print(f"{pos.id:<8} {pos.employerId:<10} {title:<25} {pos.availableSlots:<6} {pos.status.value:<15}")
        
        print("========================================================================")
        
    except Exception as e:
        print(e)
        print("------------------------------------------------------------------------\n")


app.cli.add_command(generic_cli)



'''
Staff Commands
'''
staff_cli = AppGroup('staff', help='Staff object commands')

@staff_cli.command("list", help="Lists all staff in the database")
def list_staff_command():
    staff_members = get_all_staff()
    if staff_members:
        for staff in staff_members:
            print(f'Staff ID: {staff.id} | Username: {staff.username}')
        print("------------------------------------------------------------------------\n")
    else:
        print("No staff found")

@staff_cli.command("get", help="Gets a specific staff member by ID")
@click.argument("staff_id", type=int)
def get_staff_command(staff_id):
    try:
        staff = get_staff(staff_id)
        print(f'Staff ID: {staff.id} | Username: {staff.username}')
        print("------------------------------------------------------------------------\n")
    except Exception as e:
        print(e)

@staff_cli.command("shortlist_student", help="Shortlist a student for a position")
@click.argument("position_id", type=int)
@click.argument("student_id", type=int)
@click.argument("staff_id", type=int)
def shortlist_student_command(position_id, student_id, staff_id):
    try:
        application = shortlist_student(position_id, student_id, staff_id)
        print("  Student shortlisted successfully!")
        print(f"  Position ID: {position_id}")
        print(f"  Student ID: {student_id}")
        print(f"  Application Status: {application.state.value}")
        print("------------------------------------------------------------------------\n")
    except Exception as e:
        print(e)
        print("------------------------------------------------------------------------\n")

app.cli.add_command(staff_cli)



'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("run", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "StudentUnitTests or EmployerUnitTests or StaffUnitTests or PositionUnitTests or ApplicationUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserCreationIntegrationTests or ApplicationIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)
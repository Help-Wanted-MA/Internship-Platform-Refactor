import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.controllers.employer import create_position, decide_shortlist, get_all_employers, get_employer, manage_position_status
from App.database import db, get_migrate
from App.models import User
from App.main import create_app
from App.controllers import (create_user, get_all_users_json, get_all_users, initialize)


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

@employer_cli.command("list", help="Lists all employers in the database")
def list_employers_command():
    employers = get_all_employers()
    if employers:
        for emp in employers:
            print(f'Employer ID: {emp.id} | Username: {emp.username}')
        print("------------------------------------------\n")
    else:
        print("No employers found")


@employer_cli.command("get", help="Gets a specific employer by ID")
@click.argument("employer_id", type=int)
def get_employer_command(employer_id):
    try:
        employer = get_employer(employer_id)
        print(f'Employer ID: {employer.id} | Username: {employer.username}')
        print("------------------------------------------\n")
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
        print("------------------------------------------\n")
        
    except Exception as e:
        print(e)
        print("------------------------------------------\n")


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
        print("------------------------------------------\n")
        
    except Exception as e:
        print(e)
        print("------------------------------------------\n")


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
        print("------------------------------------------\n")
        
    except Exception as e:
        print(e)
        print("------------------------------------------\n")


'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)
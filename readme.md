# Flask MVC Template
A template for flask applications structured in the Model View Controller pattern.
1. [Deployed Site](https://internship-platform-np0m.onrender.com/)
2. [Postman Collection](https://documenter.getpostman.com/view/42693601/2sB3dLUC28)

# Internship Platform (Infin1te-Loopers)
An app for staff to shortlist students to internship opportunities.  
* (Employer) create internship position.
* (Staff) Add student to an internship positions shortlist.
* (Employer) accept/reject student from shortlist.
* (Student) view shortlisted positions and employer response.  

# CLI Commands

Creates and initializes the database.
```
flask init
```

## Test Commands

Run both Unit and Integration tests
```
flask test run
```

Run Unit tests
```
flask test run unit
```

Run Integration tests
```
flask test run int
```

## User Commands

Lists all users.
```
flask user list
```

## Employer Commands

Creates a new employer user.
```
flask employer create <username> <password> <email> <company>
```

Prints a table of all employers, showing ID, username, company.
```
flask employer list
```

Retrieves a single employer by ID.
```
flask employer get <employer_id>
```

Creates a new internship position associated with an employer.
```
flask employer create_position <employer_id> <title> <requirements> <description> <available_slots>
```

Allows employers to accept or reject a shortlisted student. The `<decision>` is `accept` or `reject`.
```
flask employer decide_shortlist <employer_id> <position_id> <student_id> <decision> [message]
```

Opens or closes a position. The `<status>` is `open` or `closed`.
```
flask employer manage_status <employer_id> <position_id> <status>
```

## Student Commands

Creates a new student user.
```
flask student create <username> <password> <email> <degree> <resume> <gpa>
```

Lists all students in the system.
```
flask student list
```

Retrieves a single student by ID.
```
flask student get <student_id>
```

Shows the employer’s response message for a specific application.
```
flask student view_response <student_id> <position_id>
```

Lists all positions where the student has been shortlisted, including application status.
```
flask student view_shortlisted <student_id>
```

## Staff Commands

Creates a new staff user.
```
flask staff create <username> <password> <email>
```

Lists all staff accounts.
```
flask staff list
```

Retrieves a single staff by ID.
```
flask staff get <staff_id>
```

Shortlists a student for a position, then prints updated application status.
```
flask staff shortlist_student <position_id> <student_id> <staff_id>
```

## View Commands

Displays details of a specific application by ID.
```
flask view application <application_id>
```

Prints all applications in a table.
```
flask view applications
```

Displays details of a specific internship position by ID.
```
flask view position <position_id>
```

Lists all internship positions in the system in a formatted table
```
flask view positions
```

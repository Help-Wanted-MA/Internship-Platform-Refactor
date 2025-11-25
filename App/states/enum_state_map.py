from App.states.application_states import Applied, Shortlisted, Accepted, Rejected
from App.states.state_enums import ApplicationStatus

def get_state_object(context):
    enum_map = {
        ApplicationStatus.APPLIED: Applied,
        ApplicationStatus.SHORTLISTED: Shortlisted,
        ApplicationStatus.ACCEPTED: Accepted,
        ApplicationStatus.REJECTED: Rejected
    }
    return enum_map[context.state](context)

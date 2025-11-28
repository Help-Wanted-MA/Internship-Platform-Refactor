from enum import Enum

class TransitionContext:
    def __init__(self, actorId=None, message=None):
        self.actorId = actorId
        self.message = message
        
class ApplicationStatus(Enum):
    APPLIED = "APPLIED"
    SHORTLISTED = "SHORTLISTED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
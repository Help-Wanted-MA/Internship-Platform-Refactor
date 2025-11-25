from enum import Enum

class ApplicationStatus(Enum):
    APPLIED = "APPLIED"
    SHORTLISTED = "SHORTLISTED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
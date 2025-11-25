from abc import ABC, abstractmethod
from .state_enums import ApplicationStatus

class ApplicationState(ABC):
    def __init__(self, context):
        self.context = context

    @abstractmethod
    def accept(self):
        pass

    @abstractmethod
    def deny(self):
        pass

class Applied(ApplicationState):
    def accept(self):
        self.context.state = ApplicationStatus.SHORTLISTED
        return "Shortlisted student application!"

    def deny(self):
        self.context.state = ApplicationStatus.REJECTED
        return "Application rejected."

class Shortlisted(ApplicationState):
    def accept(self):
        self.context.state = ApplicationStatus.ACCEPTED
        return "Employer accepted application!"

    def deny(self):
        self.context.state = ApplicationStatus.REJECTED
        return "Employer rejected application."

class Accepted(ApplicationState):
    def accept(self):
        return "Application already accepted."

    def deny(self):
        self.context.state = ApplicationStatus.REJECTED
        return "Student rejected offer."

class Rejected(ApplicationState):
    def accept(self):
        return "Application is rejected. No further action."

    def deny(self):
        return "Application already rejected."

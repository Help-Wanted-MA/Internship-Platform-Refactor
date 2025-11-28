from abc import ABC, abstractmethod
from .state_enums import ApplicationStatus, TransitionContext

class ApplicationState(ABC):
    def __init__(self, context):
        self.context = context

    @abstractmethod
    def accept(self, transitionContext: TransitionContext = None):
        pass

    @abstractmethod
    def deny(self, transitionContext: TransitionContext = None):
        pass

class Applied(ApplicationState):
    def accept(self, transitionContext: TransitionContext = None):
        self.context.state = ApplicationStatus.SHORTLISTED
        self.context.staffId = transitionContext.actorId
        return "Shortlisted student application!"

    # Staff do not necessarily have to explicity reject every student. They would most likely simply leave them in the Applied
    # state in practice. But the option to reject is still there.
    def deny(self, transitionContext: TransitionContext = None):
        self.context.state = ApplicationStatus.REJECTED
        self.context.staffId = transitionContext.actorId
        return "Application rejected."

class Shortlisted(ApplicationState):
    def accept(self, transitionContext: TransitionContext = None):
        self.context.state = ApplicationStatus.ACCEPTED
        self.context.employerId = transitionContext.actorId
        self.context.employerResponse = transitionContext.message
        return "Employer accepted application!"

    def deny(self, transitionContext: TransitionContext = None):
        self.context.state = ApplicationStatus.REJECTED
        self.context.employerId = transitionContext.actorId
        self.context.employerResponse = transitionContext.message
        return "Employer rejected application."

class Accepted(ApplicationState):
    def accept(self, transitionContext: TransitionContext = None):
        return "Application already accepted."

    def deny(self, transitionContext: TransitionContext = None):
        self.context.state = ApplicationStatus.REJECTED
        return "Student rejected offer."

class Rejected(ApplicationState):
    def accept(self, transitionContext: TransitionContext = None):
        return "Application is rejected. No further action."

    def deny(self, transitionContext: TransitionContext = None):
        return "Application already rejected."

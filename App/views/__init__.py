# Import all view Blueprints
from .auth import auth_views
from .employer import employer_views
from .index import index_views
from .position import position_views
from .staff import staff_views
from .student import student_views
from .user import user_views

# Register all Blueprints in a single list
views = [
    auth_views,
    employer_views,
    index_views,
    position_views,
    staff_views,
    student_views,
    user_views
]

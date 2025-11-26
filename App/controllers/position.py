from App.exceptions.exceptions import NotFoundError
from App.models import Position

def get_position(positionId):
    position = Position.query.get(positionId)
    if position is None:
        raise NotFoundError(f'Position with id: {positionId} not found') 
    
def get_all_positions():
    return Position.query.all()
from sqlmodel import Session, select, SQLModel
from app.database import engine
from app.services.rooms.models import Room

from fastapi import APIRouter
from fastapi import HTTPException, status

router = APIRouter()

class RoomUpdate(SQLModel):
    name: str | None = None
    max_occupancy: int | None = None

### ROOM ROUTES ###
### ROOT IS /rooms ###

@router.post('/test')
async def test(room: Room) -> Room:
    room.current_occupancy = 5
    return room

@router.delete('/{room_id}')
async def delete_rooms(room_id: int):
    with Session(engine) as session:
        room = session.scalars(
            select(Room)
            .filter_by(id=room_id)
            .limit(1)
            ).first()
        if room:
            session.delete(room)
            session.commit()
            return {'success': f'Room {room_id} deleted'}
        return {'error': 'Room not found'}, 404

@router.get('')
async def get_rooms():
    with Session(engine) as session:
        rooms = session.scalars(
            select(Room)
            ).all()
        return {'rooms': rooms}

@router.get('/{room_id}')
async def get_room(room_id: int):
    with Session(engine) as session:
        room = session.scalars(
            select(Room)
            .filter_by(id=room_id)
            .limit(1)
            ).first()
        if room:
            return {'room': room}
        return {'error': 'Room not found'}, 404
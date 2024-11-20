from sqlmodel import SQLModel, Session, select, Field
from app.database import engine
from app.services.rooms.models import Room

from fastapi import APIRouter,FastAPI
from fastapi import HTTPException, status

router = APIRouter()

class RoomUpdate(SQLModel):
    name: str | None = None
    max_occupancy: int | None = None

@router.post('/test')
async def test(room: Room) -> Room:
    room.current_occupancy = 5
    return room
# @router.put('/{room_id}')
# async def edit_room(room_id: int, name: str, max_occupancy: int):
#     with Session(engine) as session:
#         room = session.scalars(
#             select(Room)
#             .filter_by(id=room_id)
#             .limit(1)
#             ).first()
#         if room:
#             room.max_occupancy = max_occupancy;
#             room.name = name;
#             return {'room': room}
#         return {'error': 'Room not found'}, 404

@router.put('/{room_id}')
async def edit_room(room_id: int, newroom: RoomUpdate):
    with Session(engine) as session:
        room = session.get(Room, room_id)
        if not room:
            raise HTTPException(status_code=404, detail="Room not found")
        room.sqlmodel_update(newroom)
        session.commit()
        session.refresh(room)
        return room

# @router.put('/{room_id}')
# async def edit_room(room_id: int, max_occupancy: int):
#     with Session(engine) as session:
#         room = session.scalars(
#             select(Room)
#             .filter_by(id=room_id)
#             .limit(1)
#             ).first()
#         if room:
#             room.max_occupancy = max_occupancy;
#             return {'room': room}
#         return {'error': 'Room not found'}, 404

@router.post('')
async def create_room(name: str, max_occupancy: int):
    with Session(engine) as session:
        new_room = Room(name=name, max_occupancy = max_occupancy);
        session.add(new_room)
        session.commit()
        return {'success': f'Room {new_room.id} created'}


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
        room = session.get(Room, room_id)
        if not room:
            raise HTTPException(status_code=404, detail="Room not found")
        return room
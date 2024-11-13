from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import engine
from app.services.rooms.models import Room

from fastapi import APIRouter,FastAPI
from fastapi import HTTPException, status

router = APIRouter()

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
async def edit_room(room_id: int, newroom: Room):
    with Session(engine) as session:
        room = session.scalars(
            select(Room)
            .filter_by(id=room_id)
            .limit(1)
            ).first()
        if room:
            room = newroom
            session.commit()
            return {'room': room}
        return {'error': 'Room not found'}, 404

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
        session.add(new_room);
        session.commit();
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
        room = session.scalars(
            select(Room)
            .filter_by(id=room_id)
            .limit(1)
            ).first()
        if room:
            return {'room': room}
        return {'error': 'Room not found'}, 404
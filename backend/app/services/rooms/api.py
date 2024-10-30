from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import engine
from app.services.rooms.models import Room

from fastapi import APIRouter

router = APIRouter()

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
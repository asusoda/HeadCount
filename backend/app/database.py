from app.models import Base
from app.services.rooms.models import Room
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine("sqlite:///database.db", echo=True)

def init():
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        # Drop all existing Room records
        session.query(Room).delete()
        
        # Create mock Room records
        room1 = Room(name="Room 1", max_occupancy=10)
        room2 = Room(name="Room 2", max_occupancy=20)
        room3 = Room(name="Room 3", max_occupancy=30)
        
        session.add_all([room1, room2, room3])
        session.commit()

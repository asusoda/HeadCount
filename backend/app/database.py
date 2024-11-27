from app.models import Base
from app.services.rooms.models import Room
from app.services.auth.models import User
from sqlmodel import Session, create_engine, select, delete

engine = create_engine("sqlite:///database.db", echo=True)

def init():
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        # Drop all existing Room records
        # TODO: Replace this deprecated method
        session.exec(delete(Room))
        session.exec(delete(User))
        
        # Create mock Room records
        room1 = Room(name="Room 1", max_occupancy=10)
        room2 = Room(name="Room 2", max_occupancy=20)
        room3 = Room(name="Room 3", max_occupancy=30)

        # Create mock User records
        user1 = User(email="user1@example.com", verified_email=True, name="User One", given_name="User", family_name="One", picture="user1.jpg", hd="example.com")
        user2 = User(email="user2@example.com", verified_email=True, name="User Two", given_name="User", family_name="Two", picture="user2.jpg", hd="example.com")
        user3 = User(email="user3@example.com", verified_email=True, name="User Three", given_name="User", family_name="Three", picture="user3.jpg", hd="example.com")

        user1.rooms.extend([room1, room2])
        user2.rooms.extend([room2, room3])
        user3.rooms.extend([room3])

        session.add_all([room1, room2, room3])
        session.add_all([user1, user2, user3])
        session.commit()

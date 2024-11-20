from typing import Optional
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select
from app.models import Base
from app.services.auth.models import User

class RoomUserLink(Base, table=True):
    room_id: int | None = Field(default=None, foreign_key="room.id", primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="roomuser.id", primary_key=True)
    
class RoomUser(Base, table=True):
    id: int | None = Field(default=None, foreign_key="user.id", primary_key=True)
    rooms: list["Room"] = Relationship(back_populates="users", link_model=RoomUserLink)

class Room(Base, table=True):
    # __tablename__ = "room"
    id: int = Field(primary_key=True)
    name: str = Field(index=True)
    max_occupancy: int = Field(default=10)
    current_occupancy: int = Field(default=0)
    
    users: list["RoomUser"] = Relationship(back_populates="rooms", link_model=RoomUserLink)

    def __repr__(self) -> str:
        return (f"Room(id={self.id!r}, name={self.name!r}, "
                f"max_occupancy={self.max_occupancy!r}, current_occupancy={self.current_occupancy!r})")
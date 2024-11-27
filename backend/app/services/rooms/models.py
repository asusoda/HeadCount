from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select
from app.models import Base

class RoomUserLink(Base, table=True):
    user_id: str | None = Field(default=None, foreign_key="user.id", primary_key=True)
    room_id: int | None = Field(default=None, foreign_key="room.id", primary_key=True)

class Room(Base, table=True):
    # __tablename__ = "room"
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    max_occupancy: int = Field(default=10)
    current_occupancy: int = Field(default=0)
    
    users: list["User"] = Relationship(back_populates="rooms", link_model=RoomUserLink)

    def __repr__(self) -> str:
        return (f"Room(id={self.id!r}, name={self.name!r}, "
                f"max_occupancy={self.max_occupancy!r}, current_occupancy={self.current_occupancy!r})")
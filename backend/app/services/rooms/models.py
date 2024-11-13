from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select
from app.models import Base
from app.services.auth.models import User

class Room(Base, table=True):
    __tablename__ = "room"
    id: int = Field(primary_key=True)
    name: str = Field(index=True)
    max_occupancy: int = Field(default=10)
    current_occupancy: int = Field(default=0)

    def __repr__(self) -> str:
        return (f"Room(id={self.id!r}, name={self.name!r}, "
                f"max_occupancy={self.max_occupancy!r}, current_occupancy={self.current_occupancy!r})")
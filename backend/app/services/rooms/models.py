from typing import Optional
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from app.models import Base

class Room(Base):
    __tablename__ = "room"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    max_occupancy: Mapped[int] = mapped_column(Integer)
    current_occupancy: Mapped[Optional[int]] = mapped_column(Integer, default=0)

    def __repr__(self) -> str:
        return (f"Room(id={self.id!r}, name={self.name!r}, "
                f"max_occupancy={self.max_occupancy!r}, current_occupancy={self.current_occupancy!r})")
from sqlalchemy import Column, String, Boolean
from app.models import Base
from sqlmodel import Field

class User(Base):
    __tablename__ = 'users'
    
    id: int = Field(primary_key=True)
    email: str = Field(unique=True, nullable=False)
    verified_email: bool = Field(nullable=False)
    name: str = Field(nullable=False)
    given_name: str = Field(nullable=False)
    family_name: str = Field(nullable=False)
    picture: str = Field()
    hd: str = Field()

    def __repr__(self):
        return f"<User(id='{self.id}', email='{self.email}', verified_email={self.verified_email}, name='{self.name}', given_name='{self.given_name}', family_name='{self.family_name}', picture='{self.picture}', hd='{self.hd}')>"
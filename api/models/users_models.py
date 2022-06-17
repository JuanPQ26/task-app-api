# sqlalchemy
from sqlalchemy import Column, Integer, String, Boolean, Text
from sqlalchemy.orm import relationship
# database
from database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String(30), index=True)
    username = Column(String(30), unique=True, index=True)
    password = Column(Text)
    is_active = Column(Boolean, default=True)

    tasks = relationship("Task", back_populates="owner")

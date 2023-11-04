from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from ..database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    user_words = relationship("UserWord", back_populates="user")
    user_definitions = relationship("UserDefinition", back_populates="user")

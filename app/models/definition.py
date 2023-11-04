from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class Definition(Base):
    __tablename__ = "definitions"

    definition_id = Column(Integer, primary_key=True)
    definition = Column(String, nullable=False)
    word_id = Column(Integer, ForeignKey("words.word_id"), nullable=False)

    word = relationship("Word", back_populates="definitions")
    user_definitions = relationship("UserDefinition", back_populates="definition")

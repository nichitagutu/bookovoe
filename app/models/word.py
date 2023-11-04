from sqlalchemy import Column, String, Integer, Index
from sqlalchemy.orm import relationship
from ..database import Base


class Word(Base):
    __tablename__ = "words"

    word_id = Column(Integer, primary_key=True)
    word = Column(String(255), nullable=False)

    __table_args__ = (Index("idx_word", "word"),)

    definitions = relationship("Definition", back_populates="word")
    user_words = relationship("UserWord", back_populates="word")

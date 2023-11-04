from sqlalchemy import Column, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class UserWord(Base):
    __tablename__ = "user_words"

    user_word_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    word_id = Column(Integer, ForeignKey("words.word_id"), nullable=False)
    active = Column(Boolean, default=True, nullable=False)

    user = relationship("User", back_populates="user_words")
    word = relationship("Word", back_populates="user_words")
    user_word_reviews = relationship("UserWordReview", back_populates="user_word")

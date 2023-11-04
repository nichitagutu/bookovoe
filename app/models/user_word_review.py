from sqlalchemy import Column, Date, Integer, ForeignKey, Float, Index
from sqlalchemy.orm import relationship
from ..database import Base


class UserWordReview(Base):
    __tablename__ = "user_word_reviews"

    review_id = Column(Integer, primary_key=True)
    user_word_id = Column(
        Integer, ForeignKey("user_words.user_word_id"), nullable=False
    )
    review_date = Column(Date, nullable=False)
    ease_factor = Column(Float, default=2.5, nullable=False)
    interval = Column(Integer, default=1, nullable=False)
    repetitions = Column(Integer, default=0, nullable=False)
    previous_interval = Column(Integer)
    review_quality = Column(Integer, default=0, nullable=False)

    user_word = relationship("UserWord", back_populates="user_word_reviews")

    __table_args__ = (
        Index("idx_user_word_review", "user_word_id", "review_date"),
        Index("idx_review_date", "review_date"),
    )

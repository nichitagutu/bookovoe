from typing import List
from sqlalchemy.orm import Session
from .base import CRUDBase
from app.models.word import Word


class CRUDUser(CRUDBase[Word]):
    def get_by_word(self, db: Session, *, word: str) -> Word:
        return db.query(Word).filter(Word.word == word).first()

    def get_multi_by_name(
        self, db: Session, *, word: str, skip: int = 0, limit: int = 100
    ) -> List[Word]:
        return (
            db.query(Word)
            .filter(Word.word == word)
            .offset(skip)
            .limit(limit)
            .all()
        )


word = CRUDUser(Word)

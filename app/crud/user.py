from typing import List
from sqlalchemy.orm import Session
from .base import CRUDBase
from app.models.user import User


class CRUDUser(CRUDBase[User]):
    def get_by_email(self, db: Session, *, email: str) -> User:
        return db.query(User).filter(User.email == email).first()

    def get_multi_by_name(
        self, db: Session, *, username: str, skip: int = 0, limit: int = 100
    ) -> List[User]:
        return (
            db.query(User)
            .filter(User.username == username)
            .offset(skip)
            .limit(limit)
            .all()
        )


user = CRUDUser(User)

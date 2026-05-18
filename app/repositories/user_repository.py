from sqlalchemy.orm import Session

from app.entities.user_entity import (
    UserEntity
)


class UserRepository:

    @staticmethod
    def get_by_username(
        db: Session,
        username: str
    ):

        return (
            db.query(UserEntity)
            .filter(
                UserEntity.username == username
            )
            .first()
        )
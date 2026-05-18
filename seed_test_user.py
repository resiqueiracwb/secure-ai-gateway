from app.database.session import (
    SessionLocal
)

from app.entities.user_entity import (
    UserEntity
)

from app.security.password_handler import (
    get_password_hash
)

db = SessionLocal()

existing_user = (
    db.query(UserEntity)
    .filter(
        UserEntity.username == "renato"
    )
    .first()
)

if not existing_user:

    user = UserEntity(
        username="renato",
        password=get_password_hash(
            "123456"
        ),
        role="admin"
    )

    db.add(user)
    db.commit()

db.close()
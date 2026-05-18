from fastapi import APIRouter

from app.security.jwt_handler import (
    create_access_token
)

from fastapi import (
    APIRouter,
    HTTPException,
    status
)

from app.models.auth_models import (
    LoginRequest
)

from app.security.password_handler import (
    verify_password
)

from app.security.jwt_handler import (
    create_access_token
)

from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.dependencies import (
    get_db
)

from app.repositories.user_repository import (
    UserRepository
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login")
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    user = UserRepository.get_by_username(
        db,
        request.username
    )

    if not user:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    valid_password = verify_password(
        request.password,
        user.password
    )

    if not valid_password:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token = create_access_token(
        data={
            "sub": user.username,
            "role": user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
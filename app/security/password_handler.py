from passlib.context import (
    CryptContext
)

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def verify_password(
    plain_password: str,
    hashed_password: str
):

    print("PLAIN:", plain_password)
    print("HASH:", hashed_password)

    return pwd_context.verify(
        plain_password,
        hashed_password
    )
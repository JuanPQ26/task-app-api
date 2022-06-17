# services
from api.services import users_services
# schemas
from api.schemas.auth_schemas import SigninBase, SignupBase
from api.schemas.users_schemas import UserCreate
# fastapi
from fastapi.exceptions import HTTPException
# sqlalchemy
from sqlalchemy.orm import Session
# utils
from api.utils import encrypt, token


def decode_auth_token(auth_token: str):
    if token is None:
        raise HTTPException(401, "auth token not found")

    decoded = token.decoded_token(auth_token)

    if decoded.get("err"):
        raise HTTPException(401, decoded.get("message"))

    payload = decoded.get("payload", {})

    return payload.get("id", 0)


def signin(db: Session, user: SigninBase):
    user_found = users_services.get_user_by_username(db, user.username)

    if user_found is None:
        raise HTTPException(404, "user not found")

    if not encrypt.validate_password(user.password, user_found.password):
        raise HTTPException(401, "password incorrect")

    user_payload = {
        "id": user_found.id,
        "username": user_found.username,
        "fullname": user_found.fullname
    }

    user_token = token.generate_token(user_payload)

    return user_token


def signup(db: Session, user: SignupBase):
    user_found = users_services.get_user_by_username(db, user.username)

    if user_found:
        raise HTTPException(400, "username already registered")

    new_user = UserCreate(
        username=user.username, password=user.password, fullname=user.fullname)

    user_created = users_services.create_user(db, new_user)

    user_payload = {
        "id": user_created.id,
        "username": user_created.username,
        "fullname": user_created.fullname
    }

    user_token = token.generate_token(user_payload)

    return user_token

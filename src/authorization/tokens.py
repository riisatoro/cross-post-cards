import os
from datetime import datetime, timedelta
from typing import Annotated

import jwt
from fastapi import HTTPException, Header

from database.main import Database
from models.user import UserSignInPayload, UserProfile
from models.token import JWTResponse


SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_ACCESS_EXPIRES_AT = int(os.getenv("JWT_ACCESS_EXPIRES_AT"))
JWT_REFRESH_EXPIRES_AT = int(os.getenv("JWT_REFRESH_EXPIRES_AT"))

ACCESS_AUDIENCE = "user:access"
REFRESH_AUDIENCE = "user:refresh"


def make_jwt_tokens(user: UserSignInPayload) -> JWTResponse:
    created_at = datetime.utcnow()
    access_expired_at = created_at + timedelta(seconds=JWT_ACCESS_EXPIRES_AT)
    refresh_expired_at = created_at + timedelta(seconds=JWT_REFRESH_EXPIRES_AT)

    access = {
        "email": user.email,
        "aud": ACCESS_AUDIENCE,
        "iat": created_at.timestamp(),
        "exp": access_expired_at.timestamp(),
    }
    refresh = {
        "email": user.email,
        "aud": REFRESH_AUDIENCE,
        "iat": created_at.timestamp(),
        "exp": refresh_expired_at.timestamp(),
    }
    return JWTResponse(
        access=jwt.encode(access, SECRET_KEY, algorithm=ALGORITHM),
        refresh=jwt.encode(refresh, SECRET_KEY, algorithm=ALGORITHM),
    )


def verify_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, audience=ACCESS_AUDIENCE, algorithms=[ALGORITHM])
    except (jwt.InvalidAudienceError, jwt.ExpiredSignatureError):
        raise HTTPException(status_code=401, detail="Invalid token")


def verify_refresh_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, audience=REFRESH_AUDIENCE, algorithms=[ALGORITHM])
    except (jwt.InvalidAudienceError, jwt.ExpiredSignatureError):
        raise HTTPException(status_code=401, detail="Invalid token")


def refresh_tokens(refresh_token: str) -> JWTResponse:
    token_payload = verify_refresh_token(refresh_token)
    user_email = token_payload.get("email")
    db_user = Database.get(Database.USER_COLLECTION_NAME, {"email": user_email})
    return make_jwt_tokens(UserSignInPayload(**db_user))


def get_user_from_token(X_ACCESS_TOKEN: Annotated[str, Header()]) -> UserProfile:
    token_payload = verify_access_token(X_ACCESS_TOKEN)
    user_email = token_payload.get("email")
    db_user = Database.get(Database.USER_COLLECTION_NAME, {"email": user_email})
    return UserProfile(**db_user)

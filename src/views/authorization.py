from fastapi import APIRouter, HTTPException

from authorization.tokens import make_jwt_tokens, refresh_tokens
from authorization.passwords import check_password
from database.main import Database
from models.default_status import DefaultStatus
from models.token import JWTResponse, RefreshTokenPayload
from models.user import UserSignInPayload, UserSignUpPayload


router = APIRouter(
    prefix="/auth",
    tags=["authorization"]
)


@router.post("/signup")
async def signup(user: UserSignUpPayload) -> DefaultStatus:
    Database.create_user(user)
    return DefaultStatus()


@router.post("/signin")
async def signin(user: UserSignInPayload) -> JWTResponse:
    db_user = Database.get(Database.USER_COLLECTION_NAME, {"email": user.email})
    if not db_user or not check_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return make_jwt_tokens(user)


@router.post("/refresh")
async def refresh(refresh_token: RefreshTokenPayload) -> JWTResponse:
    return refresh_tokens(refresh_token.refresh)

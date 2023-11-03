from fastapi import APIRouter, Depends

from authorization.tokens import get_user_from_token
from database.main import Database
from models.user import UserProfile, UserPatchProfilePayload


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/me")
async def read_user_me(
        user: UserProfile = Depends(get_user_from_token),
) -> UserProfile:
    return user


@router.get("/{user_id}")
async def read_user(
        username: str,
        user: UserProfile = Depends(get_user_from_token),
) -> UserProfile:
    user = Database.get(Database.USER_COLLECTION_NAME, {"username": username})
    return UserProfile(**user)


@router.patch("/me")
async def update_user_me(
        patch_user: UserPatchProfilePayload,
        user: UserProfile = Depends(get_user_from_token),
) -> UserProfile:
    Database.update(
        Database.USER_COLLECTION_NAME,
        {"email": user.email},
        patch_user.model_dump(exclude_none=True)
    )
    db_user = Database.get(Database.USER_COLLECTION_NAME, {"email": user.email})
    return UserProfile(**db_user)

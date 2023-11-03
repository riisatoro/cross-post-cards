from models.base import Base


class UserSignUpPayload(Base):
    email: str
    password: str
    username: str


class UserSignInPayload(Base):
    email: str
    password: str


class UserPatchProfilePayload(Base):
    first_name: str | None = None
    last_name: str | None = None

    country: str | None = None
    city: str | None = None
    address: str | None = None
    phone: str | None = None
    zip_code: int | None = None

    longitude: float | None = None
    latitude: float | None = None


class UserProfile(Base):
    email: str
    username: str
    first_name: str | None = None
    last_name: str | None = None

    country: str | None = None
    city: str | None = None
    address: str | None = None
    phone: str | None = None
    zip_code: int | None = None

    longitude: float | None = None
    latitude: float | None = None
from models.base import Base


class AccessTokenPayload(Base):
    access: str


class RefreshTokenPayload(Base):
    refresh: str


class JWTResponse(AccessTokenPayload, RefreshTokenPayload):
    ...

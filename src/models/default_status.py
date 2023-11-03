from models.base import Base


class DefaultStatus(Base):
    status: str = "ok"

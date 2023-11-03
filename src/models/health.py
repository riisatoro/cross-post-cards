from models.base import Base


class HealthCheckResponse(Base):
    api_status: str = "ok"
    db_status: str = "ok"

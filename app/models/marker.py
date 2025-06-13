from uuid import uuid4

from sqlalchemy import UUID, Column, DateTime, Float, String, func
from sqlalchemy.orm import relationship

from app.database import Base


class Marker(Base):
    __tablename__ = "markers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    title = Column(String(255))
    description = Column(String(255))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    address = Column(String(255))
    image_url = Column(String(255))
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user = relationship("User", back_populates="markers")

    """
      createdAt   DateTime @default(now())
      updatedAt   DateTime @updatedAt
    """

    def __repr__(self) -> str:
        return f"{self.title}({self.latitude}, {self.longitude})"

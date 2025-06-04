import datetime
import uuid
from sqlalchemy import LargeBinary
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base

class User(Base):
    __tablename__ = "users"

    id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username:Mapped[str] = mapped_column(unique=True, nullable=True)
    password:Mapped[str]
    email:Mapped[str] = mapped_column(unique=True)
    date_created:Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)
    # saved_posts:Mapped[]
    bio:Mapped[str] = mapped_column(nullable=True)
    profile_pic:Mapped[bytes] = mapped_column(LargeBinary, nullable=True)

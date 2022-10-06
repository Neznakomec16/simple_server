from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from sqlalchemy_utils import EmailType

from main.db.models.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    email = Column(EmailType, unique=True, nullable=False)
    last_login = Column(DateTime(timezone=True), nullable=True)
    created_dt = Column(DateTime(timezone=True), server_default=func.now())
    disabled = Column(Boolean, default=False, nullable=False)

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.db import Base


class URLBase(Base):
    """Data about URL for shorten."""
    __tablename__ = 'URLs'

    id = Column(Integer, primary_key=True)
    target_url = Column(String)
    short_url_id = Column(String, unique=True)
    short_url = Column(String, default='http://127.0.0.1:8080/api/v1/')
    is_active = Column(Boolean, default=True)
    clicks = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class History(Base):
    """Data about link clicks."""
    __tablename__ = 'History'

    id = Column(Integer, primary_key=True)
    url_id = Column(ForeignKey('URLs.id'), nullable=False)
    client = Column(String)
    click_at = Column(DateTime, default=datetime.utcnow)
    url = relationship('URLBase')

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.db import Base


class URLBase(Base):
    """Data about URL for shorten."""
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True)
    target_url = Column(String)
    short_url_id = Column(String, unique=True)
    is_active = Column(Boolean, default=True)
    clicks = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class History(Base):
    """Data about link clicks."""
    __tablename__ = 'history'

    id = Column(Integer, primary_key=True)
    url_id = Column(ForeignKey('urls.id'), nullable=False)
    client = Column(String)
    click_at = Column(DateTime, default=datetime.utcnow)
    url = relationship('URLBase')

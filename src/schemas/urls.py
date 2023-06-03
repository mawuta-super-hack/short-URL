from datetime import datetime

from pydantic import BaseModel, HttpUrl


class URLCreate(BaseModel):
    """Request schema for url."""
    target_url: str


class URLRead(URLCreate):
    """Response schema for url."""
    short_url_id: str
    is_active: bool
    clicks: int

    class Config:
        orm_mode = True


class URLDelete(URLCreate):
    """Response schema for delete url."""
    is_active: bool

    class Config:
        orm_mode = True


class URLSRead(BaseModel):
    """Schema for url list."""
    short_url_id: str
    short_url: HttpUrl

    class Config:
        orm_mode = True


class URLReadList(BaseModel):
    """Response schema for url list."""
    __root__: list[URLSRead]


class URLCreateList(BaseModel):
    """Request schema for url list."""
    __root__: list[URLCreate]


class HistoryBase(BaseModel):
    """Schema for history."""
    client: str
    click_at: datetime

    class Config:
        orm_mode = True


class HistoryList(BaseModel):
    """Response schema for history."""
    __root__: list[HistoryBase]

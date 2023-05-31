from pydantic import BaseModel, HttpUrl
from typing import List
from datetime import datetime

class URLBase(BaseModel):
    target_url: str


class URL(URLBase):
    short_url_id: str
    short_url: HttpUrl
    is_active: bool
    clicks: int

    class Config:
        orm_mode = True


class URLDel(URLBase):
    is_active: bool

    class Config:
        orm_mode = True


class URLSRead(BaseModel):
    short_url_id: str
    short_url: HttpUrl

    class Config:
        orm_mode = True


class URLSReadList(BaseModel):
    __root__: List[URLSRead]


class URLSCreateList(BaseModel):
    __root__: List[URLBase]


class HistoryBase(BaseModel):
    client: str
    click_at: datetime


class HistoryList(BaseModel):
    __root__: List[HistoryBase]


class URLReadList(URLSReadList):
    pass


class URLCreateList(URLSCreateList):
    pass


class URLRead(URL):
    pass


class URLCreate(URLBase):
    pass


class URLDelete(URLDel):
    pass

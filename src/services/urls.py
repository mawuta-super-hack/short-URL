
from models.urls import History, URLBase
from schemas.urls import URLCreate, URLCreateList

from .base import RepositoryDB


class RepositoryURL(RepositoryDB[URLBase, History, URLCreate, URLCreateList]):
    pass


url_crud = RepositoryURL(URLBase, History)


from models.urls import URLBase, History
from schemas.urls import URLCreate, URLDelete, URLCreateList
from .base import RepositoryDB


class RepositoryURL(RepositoryDB[URLBase, History, URLCreate, URLCreateList]): # URLDelete
    pass


url_crud = RepositoryURL(URLBase, History)

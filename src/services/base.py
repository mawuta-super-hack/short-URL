import secrets
import string
from typing import Generic, List, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import PROJECT_HOST, PROJECT_PORT, SHORT_URL_ID_LENGTH
from db.db import Base

ModelType = TypeVar('ModelType', bound=Base)
ClientModelType = TypeVar('ClientModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
CreatelistSchemaType = TypeVar('CreatelistSchemaType', bound=BaseModel)


class Repository:
    """Basic crud class."""

    def get(self, *args, **kwargs):
        raise NotImplementedError

    def get_multi(self, *args, **kwargs):
        raise NotImplementedError

    def create(self, *args, **kwargs):
        raise NotImplementedError

    def update(self, *args, **kwargs):
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        raise NotImplementedError


class RepositoryDB(
    Repository, Generic[
        ModelType, ClientModelType, CreateSchemaType, CreatelistSchemaType]):
    """CRUD class for URL and History models."""

    def __init__(self, model: Type[ModelType], client: Type[ClientModelType]):
        self._model = model
        self._client_model = client

    def generate_link(self) -> str:
        """Generate short link for URLModel objects."""
        symbols = string.ascii_letters + string.digits
        short_url_id = ''.join(
            secrets.choice(symbols) for i in range(SHORT_URL_ID_LENGTH))

        short_url = (f'http://{PROJECT_HOST}:'
                     f'{PROJECT_PORT}/api/v1/{short_url_id}')
        return short_url_id, short_url

    def update_history(
            self,
            db: AsyncSession,
            url_obj: Optional[ModelType],
            client: str
    ) -> None:
        """Update history for the url."""
        history_obj = self._client_model(client=client, url_id=url_obj.id)
        db.add(history_obj)
        print(client, history_obj)
        db.commit()
        db.refresh(history_obj)

    async def get(
            self,
            db: AsyncSession,
            short_url_id: str,
            client: str
    ) -> Optional[ModelType]:
        """Get url object."""
        statement = select(
            self._model).where(self._model.short_url_id == short_url_id)
        results = await db.execute(statement=statement)
        obj = results.scalar_one_or_none()
        obj.clicks += 1
        self.update_history(db, obj, client)
        await db.commit()
        await db.refresh(obj)
        return obj

    async def get_target(
            self,
            db: AsyncSession,
            short_url_id: str
    ) -> Optional[ModelType]:
        """Get target url."""
        statement = select(
            self._model).where(self._model.short_url_id == short_url_id)
        results = await db.execute(statement=statement)
        return results.scalar_one_or_none()

    async def create(
            self,
            db: AsyncSession,
            *,
            obj_in: CreateSchemaType
    ) -> ModelType:
        """Create url object."""
        short_url_id, short_url = self.generate_link()
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self._model(
            **obj_in_data, short_url_id=short_url_id, short_url=short_url)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(
            self,
            db: AsyncSession,
            short_url_id: str
    ) -> Optional[ModelType]:
        """Delete url object."""
        statement = select(
            self._model).where(self._model.short_url_id == short_url_id)
        obj = await db.execute(statement=statement)
        obj = obj.scalar_one_or_none()
        obj.is_active = False
        await db.commit()
        await db.refresh(obj)
        return obj

    async def db_ping(self, db: AsyncSession) -> str:
        """Get DB connection status."""
        statement = select(self._model)
        result = await db.execute(statement=statement)
        if result:
            status = 'active'
        else:
            status = 'failed'
        message = f'DB connection status: {status}.'
        return message

    async def create_list(
            self,
            db: AsyncSession,
            *,
            obj_in: CreateSchemaType
    ) -> List[ModelType]:
        """Create url objects."""
        objs = []

        obj_in_data = jsonable_encoder(obj_in)
        for obj in obj_in_data:
            short_url_id, short_url = self.generate_link()
            db_obj = self._model(
                target_url=obj['target_url'],
                short_url=short_url,
                short_url_id=short_url_id)
            objs.append(db_obj)

        db.add_all(objs)
        await db.commit()
        for obj in objs:
            await db.refresh(obj)
        return objs

    async def get_status(
            self,
            db: AsyncSession,
            short_url_id: str,
            full_info: bool = False,
            max_result: int = 100,
            offset: int = 0
    ) -> ModelType | str:
        """Get url click history."""
        statement = select(
            self._model).where(self._model.short_url_id == short_url_id)
        results = await db.execute(statement=statement)
        obj = results.scalar_one_or_none()
        print(obj, obj.__dict__)
        if full_info:
            statement = select(
                self._client_model).where(
                self._client_model.url_id == obj.id).offset(
                offset).limit(max_result)
            results = await db.execute(statement=statement)
            return results.scalars().all()
        else:
            message = f'Сlicks count the link - {obj.clicks}.'
            return message

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel
from db.db import Base
from core.config import PROJECT_HOST, PROJECT_PORT
import string
import secrets
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.encoders import jsonable_encoder

ModelType = TypeVar("ModelType", bound=Base)
RequestModelType = TypeVar("RequestModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
CreatelistSchemaType = TypeVar("CreatelistSchemaType", bound=BaseModel)


class Repository:

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


class RepositoryDB(Repository, Generic[ModelType, RequestModelType, CreateSchemaType, CreatelistSchemaType]):#, DeleteSchemaType]):

    def __init__(self, model: Type[ModelType], request: Type[RequestModelType]):
        self._model = model
        self._request_model = request

    def generate_link(self):
        symbols = string.ascii_letters + string.digits
        short_url_id = ''.join(secrets.choice(symbols) for i in range(6))

        short_url = (f'http://{PROJECT_HOST}:'
                     f'{PROJECT_PORT}/api/v1/{short_url_id}')
        #print(short_url)
        return short_url_id, short_url
    
    #def update_clicks(self, db: AsyncSession, db_obj):
    ##    print(db_obj.clicks)
    #    db_obj.clicks += 1
    #    print(db_obj.clicks)
    #    db.add(db_obj)
    #    db.commit()
    #    db.refresh(db_obj)
    #    return db_obj

    async def get(self, db: AsyncSession, short_url_id: str) -> Optional[ModelType]:
        statement = select(self._model).where(self._model.short_url_id == short_url_id)
        results = await db.execute(statement=statement)
        obj = results.scalar_one_or_none()
        print(obj)
        obj.clicks += 1
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    async def get_multi(
        self, db: AsyncSession, *, skip=0, limit=100
    ) -> List[ModelType]:
        statement = select(self._model).offset(skip).limit(limit)
        results = await db.execute(statement=statement)
        return results.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        #symbols = string.ascii_letters + string.digits
        #short_url = ''.join(secrets.choice(symbols) for i in range(6))
        short_url_id, short_url = self.generate_link()

        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self._model(**obj_in_data, short_url_id=short_url_id, short_url=short_url)
        print(db_obj)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, short_url_id: str) -> Optional[ModelType]:
        statement = select(self._model).where(self._model.short_url_id == short_url_id)
        obj = await db.execute(statement=statement)
        obj = obj.scalar_one_or_none()
        obj.is_active = False
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    async def db_ping(self, db: AsyncSession):
        statement = select(self._model)
        result = await db.execute(statement=statement)
        if result:
            status = 'active'
        else:
            status = 'failed'
        message = f'DB connection status: {status}.'
        return message

    async def create_list(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        objs = []

        obj_in_data = jsonable_encoder(obj_in)
        for obj in obj_in_data:
            #symbols = string.ascii_letters + string.digits
            short_url_id, short_url = self.generate_link()
            db_obj = self._model(target_url=obj['target_url'], short_url=short_url, short_url_id=short_url_id)
            objs.append(db_obj)

        db.add_all(objs)
        await db.commit()
        for obj in objs:
            await db.refresh(obj)
        return objs

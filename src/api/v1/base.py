from fastapi import APIRouter
from typing import Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status,  Request
from db.db import get_session
from schemas.urls import URL, URLBase, URLRead, URLCreate, URLDelete, URLReadList, URLCreateList, HistoryList
from models.urls import URLBase
from services.urls import url_crud
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=URLRead)
async def create_url(*, db: AsyncSession = Depends(get_session), url_in: URLCreate) -> Any:
    url = await url_crud.create(db=db, obj_in=url_in)
    return url

@router.get('/{short_url_id}')#, response_model=URLRead)
async def read_url(*, db: AsyncSession = Depends(get_session), short_url_id: str):
    url = await url_crud.get(db=db, short_url_id=short_url_id)
    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found.")
    elif not url.is_active:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail="URL delete.")
    return RedirectResponse(url=url.target_url)

@router.get('/{short_url_id}/target', status_code=status.HTTP_307_TEMPORARY_REDIRECT)#, response_model=URLRead)
async def read_url(*, db: AsyncSession = Depends(get_session), short_url_id: str):
    url = await url_crud.get(db=db, short_url_id=short_url_id)
    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found.")
    elif not url.is_active:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail="URL delete.")
    return url.target_url

@router.get('/{short_url_id}/status')#, response_model=HistoryList)
async def read_url_status(
    *, db: AsyncSession = Depends(get_session), request: Request,
    full_info: Optional[bool] = None,
    max_result: Optional[int] = None,
    offset: Optional[int] = None
):
    pass
    #message = await url_crud.db_ping(db)
    #return request.client, request.state
    #return await url_crud.get_multi(db=db)

@router.get('/ping')
async def read_db_status(db: AsyncSession = Depends(get_session)):
    message = await url_crud.db_ping(db)
    return message

@router.delete('/{short_url_id}', status_code=status.HTTP_200_OK, response_model=URLDelete) # /<shorten-url-id>
async def delete_url(*, db: AsyncSession = Depends(get_session), short_url_id: str) -> Any:
    url = await url_crud.delete(db=db, short_url_id=short_url_id)
    return url

@router.post('/shorten', status_code=status.HTTP_201_CREATED, response_model=URLReadList)
async def url_list(*, db: AsyncSession = Depends(get_session), urls_in: URLCreateList):
    url_list = await url_crud.create_list(db=db, obj_in=urls_in)
    return url_list

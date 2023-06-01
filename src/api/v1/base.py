from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from schemas.urls import (HistoryList, URLCreate, URLCreateList, URLDelete,
                          URLRead, URLReadList)
from services.urls import url_crud

router = APIRouter()


@router.get('/ping')
async def read_db_status(db: AsyncSession = Depends(get_session)) -> str:
    """Execute a database ping."""
    message = await url_crud.db_ping(db)
    return message


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=URLRead)
async def create_url(
    *,
    db: AsyncSession = Depends(get_session),
    url_in: URLCreate
) -> Any:
    """Create a short url."""
    url = await url_crud.create(db=db, obj_in=url_in)
    return url


@router.get('/{short_url_id}')
async def read_url(
    *,
    db: AsyncSession = Depends(get_session),
    short_url_id: str,
    request: Request
) -> Any:
    """Redirect on target url."""
    client = (f'Сlient {request.client.host}:'
              f'{request.client.port} clicked the link.')
    url = await url_crud.get(db=db, short_url_id=short_url_id, client=client)
    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='URL not found.')
    elif not url.is_active:
        raise HTTPException(
            status_code=status.HTTP_410_GONE, detail='URL delete.')
    return RedirectResponse(url=url.target_url)


@router.get('/{short_url_id}/target',
            status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def read_url(
    *,
    db: AsyncSession = Depends(get_session),
    short_url_id: str
) -> Any:
    """Return target url."""
    url = await url_crud.get_target(db=db, short_url_id=short_url_id)
    if not url.is_active:
        raise HTTPException(
            status_code=status.HTTP_410_GONE, detail='URL delete.')
    return url.target_url


@router.get('/{short_url_id}/status', response_model=HistoryList | str)
async def read_url_status(
    *, db: AsyncSession = Depends(get_session),
    short_url_id: str,
    full_info: Optional[bool] = None,
    max_result: Optional[int] = None,
    offset: Optional[int] = None
) -> Any:
    """Get url status."""
    status = await url_crud.get_status(
        db=db, short_url_id=short_url_id, full_info=full_info,
        max_result=max_result, offset=offset)
    return status


@router.delete('/{short_url_id}', status_code=status.HTTP_200_OK,
               response_model=URLDelete)
async def delete_url(
    *,
    db: AsyncSession = Depends(get_session),
    short_url_id: str
) -> Any:
    """Delete the url."""
    url = await url_crud.delete(db=db, short_url_id=short_url_id)
    return url


@router.post('/shorten', status_code=status.HTTP_201_CREATED,
             response_model=URLReadList)
async def url_list(
    *,
    db: AsyncSession = Depends(get_session),
    urls_in: URLCreateList
) -> Any:
    """Create list url."""
    url_list = await url_crud.create_list(db=db, obj_in=urls_in)
    return url_list

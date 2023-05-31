from fastapi import FastAPI
import uvicorn
from fastapi.responses import ORJSONResponse
from core import config
from api.v1 import base

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse
)

app.include_router(base.router, prefix='/api/v1')

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=config.PROJECT_HOST,
        port=config.PROJECT_PORT
    )
# uvicorn main:app --host 127.0.0.1 --port 8080 --reload

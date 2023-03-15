import logging

import uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis

from api.v1 import genres_router, movies_router, persons_router
from core import LOGGING, PROJECT_NAME, ElasticConfig, RedisConfig
from db import elastic, redis

app = FastAPI(
    title=PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    description='Information about movies, genres, and people involved in creating the film work',
    version='1.0.0',
)


@app.on_event('startup')
async def startup():
    redis.redis = await Redis(host=RedisConfig().redis_host, port=RedisConfig().redis_port)
    elastic.es = AsyncElasticsearch(
        hosts=[f'https://{ElasticConfig().elastic_host}:{ElasticConfig().elastic_port}'], verify_certs=False
    )


@app.on_event('shutdown')
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()


app.include_router(movies_router)
app.include_router(genres_router)
app.include_router(persons_router)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )

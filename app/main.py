from typing import List

from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

from routers import routers

app = FastAPI(title="Tortoise ORM FastAPI example")

for router in routers:
    app.include_router(router)

register_tortoise(
    app,
    db_url="mysql://root:root@db:3306/ikapi",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

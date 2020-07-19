from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from models import Users
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

app = FastAPI(title="Tortoise ORM FastAPI example")


class Status(BaseModel):
    message: str

register_tortoise(
    app,
    db_url="mysql://root:root@db:3306/ikapi",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

from fastapi import FastAPI, Depends
from db import config
from routers import elevator
from typing import Annotated


# Initializing database
config.Base.metadata.create_all(bind=config.engine)

app = FastAPI()
app.include_router(elevator.router)


@app.get("/")
async def root() -> str:
    return "Hello World!"

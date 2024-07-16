from fastapi import FastAPI

from db import config

# Initializing database
config.Base.metadata.create_all(bind=config.engine)

app = FastAPI()


@app.get("/")
async def root() -> str:
    return "Hello World!"

from fastapi import FastAPI
from db import config
from routers import elevator, demand, dataset


# Initializing database
config.Base.metadata.create_all(bind=config.engine)

app = FastAPI()
app.include_router(elevator.router)
app.include_router(demand.router)
app.include_router(dataset.router)

@app.get("/")
async def root() -> str:
    return "Hello World!"

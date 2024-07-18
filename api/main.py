from fastapi import FastAPI
from routers import elevator, demand, dataset

from db import config

# Initializing database
config.Base.metadata.create_all(bind=config.engine)

# Creating API and adding the routters
app = FastAPI()
app.include_router(elevator.router)
app.include_router(demand.router)
app.include_router(dataset.router)

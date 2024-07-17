from fastapi import APIRouter, Response, status, Depends, Path
from fastapi.responses import JSONResponse
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from db import crud
from dependencies import get_db
from typing import Annotated
from contracts.utils import WeekDayToNumerical

ROUTER_PATH = "/dataset"

router = APIRouter()


@router.get(ROUTER_PATH+"/generate/{id}")
async def generate_dataset_from_elevator_id(id: Annotated[int, Path(gt=0)], response: Response, db: Session = Depends(get_db)):
    elevator = crud.get_elevator(db, id)

    if elevator == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"ID {id} not found."

    demands = elevator.demands

    if len(demands) == 0:
        response.status_code = status.HTTP_403_FORBIDDEN
        return f"The elevator with Id {id} does not have demands to generate a dataset"

    temp_data = []
    for demand in demands:
        temp_data.append([
            (demand.timestamp.hour*3600) +
            (demand.timestamp.minute*60) + demand.timestamp.second,
            WeekDayToNumerical[demand.week_day],
            demand.source,
            demand.destination if demand.source != demand.destination else 0])

    return JSONResponse(pd.DataFrame(temp_data, columns=[
        "time", "weekday", "floor", "class"], dtype=np.int32).to_dict(orient="index"))


@router.get(ROUTER_PATH)
async def root():
    return "Hello World!"

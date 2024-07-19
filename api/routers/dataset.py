import pandas as pd
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Response, status, Depends, Path

from db import crud
from dependencies import get_db
from contracts.utils import WeekDayToNumerical

ROUTER_PATH = "/dataset"

router = APIRouter()

# Getting a dataset from a elevator_id
@router.get(ROUTER_PATH + "/generate/{elevator_id}")
async def generate_dataset_from_elevator_id(elevator_id: Annotated[int, Path(gt=0)],
                                            response: Response,
                                            db: Session = Depends(get_db)):
    elevator = crud.get_elevator(db, elevator_id)

    # Checking if the provided elevator exists
    if elevator == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"Elevator with ID {elevator_id} not found."}

    demands = elevator.demands

    # Checking if the elevator does have demands
    if len(demands) == 0:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"message": 
                f"The elevator with ID {elevator_id} does not have demands to generate a dataset"}

    '''
    To generate a dataset from the data that we save in our DB, I considered the following:
    - The year and the day of a demand will not contribute to the classification;
    - De timestamp of the demand can be converted into a single value by converting the time
      into hours and then normalized to values between 0.0 and 1.0;
    - The week day is a super meaningful information;
    - The destination floor should be used as the class for each entry in the dataframe;
    - The classes would be in the format: 
      [0 = don't move (resting), 1 = go to the 1st floor, 2 = go to the 2nd floor, ...]

    Dataset features:
    hour (normalized, [0,1])
    weekday (normalized, [0, 1])
    source_floor (normalized [0, 1])

    Class:
    destination_floor  
    
    ALL FEATURES (hour, week_day, source_floor) SHOULD BE NORMALIZED TO [0.0, 1.0]
    '''

    # Generating dataset
    data = []
    for demand in demands:
        data.append([
            ((demand.timestamp.hour) +
            (demand.timestamp.minute/60) + demand.timestamp.second/3600)/24.0, # Converting timestamp to hours and normalizing
            WeekDayToNumerical[demand.week_day]/len(WeekDayToNumerical.keys()), # Week Day "normalized"
            demand.source/elevator.n_floors, # "Normalized" source_floor
            demand.destination if demand.source != demand.destination else 0])# Checking if the elevator was resting 

    df = pd.DataFrame(data, columns=["hours", "weekday", "source_floor", "class"])

    # Creating the dataframe and exporting it into a JSON file
    return JSONResponse(df.to_dict(orient="index"))

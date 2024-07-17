from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Response, status, Depends, Path
from contracts import demand
from db import crud
from dependencies import get_db

ROUTER_PATH = "/demand"

router = APIRouter()


# Retrieve demand info by Id
@router.get(ROUTER_PATH+"/get/{id}")
async def get_demand(id: Annotated[int, Path(gt=0)], response: Response, db: Session = Depends(get_db)):
    demand_item = crud.get_demand(db, id)

    # Checking if the item was actually found
    if demand_item == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"ID {id} not found."

    return demand_item


# Create demand
@router.post(ROUTER_PATH+"/create")
async def create_demand(body: demand.DemandCreate, response: Response, db: Session = Depends(get_db)):
    elevator_item = crud.get_elevator(db, body.elevator_id)

    if elevator_item == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Elevator with ID {body.elevator_id} was not found."
    
    # Checking if source floor is invalid 0 < source <= db_elevator_item.n_floors
    if body.source > elevator_item.n_floors or body.source <= 0:
        response.status_code = status.HTTP_403_FORBIDDEN
        return f"Source floor invalid."

    # Checking if destination floor is invalid 0 < destination <= db_elevator_item.n_floors
    if body.destination > elevator_item.n_floors or body.destination <= 0:
        response.status_code = status.HTTP_403_FORBIDDEN
        return f"Destination floor invalid."

    demand_item = crud.create_demand(db, body)

    return demand_item


# Edit demand by Id
@router.put(ROUTER_PATH+"/edit/{id}")
async def edit_demand(id: Annotated[int, Path(gt=0)], body: demand.DemandCreate, response: Response, db: Session = Depends(get_db)):
    elevator_item = crud.get_elevator(db, body.elevator_id)
    
    # If the elevator does not exists, return None
    if elevator_item == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Elevator with ID {body.elevator_id} was not found."
    
    # Checking if source floor is invalid 0 < source <= db_elevator_item.n_floors
    if body.source > elevator_item.n_floors or body.source <= 0:
        response.status_code = status.HTTP_403_FORBIDDEN
        return f"Source floor invalid."

    # Checking if destination floor is invalid 0 < destination <= db_elevator_item.n_floors
    if body.destination > elevator_item.n_floors or body.destination <= 0:
        response.status_code = status.HTTP_403_FORBIDDEN
        return f"Destination floor invalid."
    
    r_affected, demand_item = crud.update_demand(db, id, body)

    if r_affected == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"No matches found for ID: {id}"

    return demand_item


# Delete demand by Id
@router.delete(ROUTER_PATH+"/delete/{id}")
async def delete_demand(id: Annotated[int, Path(gt=0)], response: Response, db: Session = Depends(get_db)):
    deleted_item = crud.remove_demand(db, id)

    if not deleted_item:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"No matches found for ID: {id}."

    return f"Demand with Id {id} removed."

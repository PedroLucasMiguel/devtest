from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Response, status, Depends, Path

from db import crud
from contracts import demand
from dependencies import get_db

ROUTER_PATH = "/demand"

router = APIRouter()


# Retrieve demand
@router.get(ROUTER_PATH + "/get/{id}")
async def get_demand(id: Annotated[int, Path(gt=0)], 
                     response: Response, 
                     db: Session = Depends(get_db)):
    demand_item = crud.get_demand(db, id)

    # Checking if the item was actually found
    if demand_item == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"Demand with ID {id} not found."}

    return demand_item


# Create demand
@router.post(ROUTER_PATH + "/create")
async def create_demand(body: demand.DemandCreate, 
                        response: Response, 
                        db: Session = Depends(get_db)):
    elevator_item = crud.get_elevator(db, body.elevator_id)

    # Checking if the provided elevator_id corresponds to a elevator in the DB
    if elevator_item == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"Elevator with ID {body.elevator_id} not found."}
    
    # Checking if source floor is invalid 0 < source <= db_elevator_item.n_floors
    if body.source > elevator_item.n_floors or body.source <= 0:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"messsage": f"Source floor should be between 1 and {elevator_item.n_floors}."}

    # Checking if destination floor is invalid 0 < destination <= db_elevator_item.n_floors
    if body.destination > elevator_item.n_floors or body.destination <= 0:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"messsage": f"Destination floor should be between 1 and {elevator_item.n_floors}."}

    demand_item = crud.create_demand(db, body)

    return demand_item


# Edit demand by Id
@router.put(ROUTER_PATH + "/edit/{id}")
async def edit_demand(id: Annotated[int, Path(gt=0)], 
                      body: demand.DemandCreate, 
                      response: Response, 
                      db: Session = Depends(get_db)):
    elevator_item = crud.get_elevator(db, body.elevator_id)
    
    # Checking if the provided elevator_id corresponds to a elevator in the DB
    if elevator_item == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"Elevator with ID {body.elevator_id} not found."}
    
    # Checking if source floor is invalid 0 < source <= db_elevator_item.n_floors
    if body.source > elevator_item.n_floors or body.source <= 0:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"messsage": f"Source floor should be between 1 and {elevator_item.n_floors}."}

    # Checking if destination floor is invalid 0 < destination <= db_elevator_item.n_floors
    if body.destination > elevator_item.n_floors or body.destination <= 0:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"messsage": f"Destination floor should be between 1 and {elevator_item.n_floors}."}
    
    r_affected, demand_item = crud.update_demand(db, id, body)

    # Check if the demand was edited
    if r_affected == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"messsage": f"Demand with ID {id} not found."}

    return demand_item


# Delete demand by Id
@router.delete(ROUTER_PATH + "/delete/{id}")
async def delete_demand(id: Annotated[int, Path(gt=0)],
                        response: Response,
                        db: Session = Depends(get_db)):
    deleted_item = crud.remove_demand(db, id)

    # Checking if demand was deleted
    if not deleted_item:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"messsage": f"Demand with ID {id} not found."}

    return {"messsage": f"Demand with ID {id} removed."}

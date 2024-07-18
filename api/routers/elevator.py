from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Response, status, Path

from db import crud
from contracts import elevator
from dependencies import get_db

ROUTER_PATH = "/elevator"

router = APIRouter()


# GET: Retrieve elevator info by Id
@router.get(ROUTER_PATH + "/get/{id}")
async def get_elevator(id: Annotated[int, Path(gt=0)], 
                       response: Response, 
                       db: Session = Depends(get_db)):
    elevator_item = crud.get_elevator(db, id)

    # Checking if the item was actually found
    if elevator_item == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"Elevator with ID {id} not found."}

    return elevator_item


# POST: Create elevator
@router.post(ROUTER_PATH + "/create")
async def create_elevator(body: elevator.ElevatorCreate, 
                          response: Response, 
                          db: Session = Depends(get_db)):
    # Checking the number of floors, if <= 0 don't create
    if body.n_floors <= 0:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"message": "n_floors must be >= 1."}
    
    # Checking if the name is not empty
    if body.name == "":
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"message": "Elevator name must not be empty."}

    elevator_item = crud.create_elevator(db, body)
    return elevator_item


# Edit elevator by Id
@router.put(ROUTER_PATH + "/edit/{id}")
async def edit_elevator(id: Annotated[int, Path(gt=0)], 
                        body: elevator.ElevatorCreate, 
                        response: Response, 
                        db: Session = Depends(get_db)):
    # Checking the number of floors
    if body.n_floors <= 0:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"message": "n_floors must be >= 1"}

    r_affected, elevator = crud.update_elevator(db, id, body)

    # Checking if the object was actually modified
    if r_affected == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"Elevator with ID {id} not found."}

    return elevator


# Delete elevator by Id
@router.delete(ROUTER_PATH + "/delete/{id}")
async def delete_elevator(id: Annotated[int, Path(gt=0)], 
                          response: Response, 
                          db: Session = Depends(get_db)):
    deleted = crud.remove_elevator(db, id)

    # Checking if the item was wactually deleted
    if not deleted:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"Elevator with ID {id} not found."}

    return {"message": f"Elevator with Id {id} removed."}


# Retrieve all demand from a elevator
@router.get(ROUTER_PATH + "/{id}/demands")
async def get_demands_from_elevator(id: Annotated[int, Path(gt=0)], 
                                    response: Response, 
                                    db: Session = Depends(get_db)):
    item = crud.get_elevator(db, id)

    # Checking if the item was actually found
    if item == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"Elevator with  ID {id} not found."}
    
    return item.demands

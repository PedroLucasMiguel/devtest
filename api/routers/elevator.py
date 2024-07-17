from fastapi import APIRouter, Depends, Response, status, Path
from contracts import elevator
from sqlalchemy.orm import Session
from db import crud
from dependencies import get_db
from typing import Annotated

ROUTER_PATH = "/elevator"

router = APIRouter()


# Retrieve elevator info by Id
@router.get(ROUTER_PATH+"/get/{id}")
async def get_elevator(id: Annotated[int, Path(gt=0)], response: Response, db: Session = Depends(get_db)):
    item = crud.get_elevator(db, id)

    # Checking if the item was actually found
    if item == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"ID {id} not found."

    return item


# Create elevator
@router.post(ROUTER_PATH+"/create")
async def create_elevator(body: elevator.ElevatorCreate, response: Response, db: Session = Depends(get_db)):

    # Checking the number of floors
    if body.n_floors <= 0:
        response.status_code = status.HTTP_403_FORBIDDEN
        return "n_floors must be >= 1."

    item = crud.create_elevator(db, body)
    return item


# Edit elevator by Id
@router.put(ROUTER_PATH+"/edit/{id}")
async def edit_elevator(id: int, body: elevator.ElevatorCreate, response: Response, db: Session = Depends(get_db)):

    # Checking the number of floors
    if body.n_floors <= 0:
        response.status_code = status.HTTP_403_FORBIDDEN
        return "n_floors must be >= 1"

    r_affected = crud.update_elevator(db, id, body)

    # Checking if the object was actually modified
    if r_affected == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"No matches found for ID: {id}"

    return f"{r_affected} rows affected."


# Delete elevator by Id
@router.delete(ROUTER_PATH+"/delete")
async def delete_elevator(id: int, response: Response, db: Session = Depends(get_db)):
    r_affected = crud.remove_elevator(db, id)

    # Checking if
    if r_affected == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"No matches found for ID: {id}."

    return f"{r_affected} rows affected."

# Retrieve all demand from a elevator
@router.get(ROUTER_PATH+"/{id}/demands")
async def get_demands_from_elevator(id: int, response: Response, db: Session = Depends(get_db)):
    item = crud.get_elevator(db, id)

    # Checking if the item was actually found
    if item == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"ID {id} not found."
    
    return item.demands

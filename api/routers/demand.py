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
    item = crud.get_demand(db, id)

    # Checking if the item was actually found
    if item == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"ID {id} not found."

    return item


# Create demand
@router.post(ROUTER_PATH+"/create")
async def create_demand(body: demand.DemandCreate, response: Response, db: Session = Depends(get_db)):
    item = crud.create_demand(db, body)

    if item == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Elevator with ID {body.elevator_id} was not found."

    return item


# Edit demand by Id
@router.put(ROUTER_PATH+"/edit/{id}")
async def edit_demand(id: Annotated[int, Path(gt=0)], body: demand.DemandCreate, response: Response, db: Session = Depends(get_db)):
    r_affected = crud.update_demand(db, id, body)

    if r_affected == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"No matches found for ID: {id}."

    return f"{r_affected} rows affected."


# Delete demand by Id
@router.delete(ROUTER_PATH+"/delete")
async def delete_demand(id: Annotated[int, Path(gt=0)], response: Response, db: Session = Depends(get_db)):
    deleted = crud.remove_demand(db, id)

    if not deleted:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"No matches found for ID: {id}."

    return f"Demand with Id {id} removed."

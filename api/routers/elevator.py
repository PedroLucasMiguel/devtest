from fastapi import APIRouter, Depends, Response, status
from contracts import elevator
from sqlalchemy.orm import Session
from db import crud
from dependencies import get_db

router = APIRouter()


# Retrieve elevator info by Id
@router.get("/elevator/get/{id}")
async def get_elevator(id: int, response: Response, db: Session = Depends(get_db)):
    item = crud.get_elevator(db, id)

    if item == None:
        response.status_code = status.HTTP_404_NOT_FOUND

    return item if item != None else f"ID {id} not found"


# Create elevator
@router.post("/elevator/create")
async def create_elevator(body: elevator.ElevatorCreate, db: Session = Depends(get_db)):
    item = crud.create_elevator(db, body)
    return item


# Edit elevator by Id
@router.put("/elevator/edit/{id}")
async def edit_elevator(id: int, body: elevator.ElevatorCreate, response: Response, db: Session = Depends(get_db)):
    i = crud.update_elevator(db, id, body)

    if i == 0:
        response.status_code = status.HTTP_404_NOT_FOUND

    return f"{i} rows affected" if i != 0 else f"No matches found for ID: {id}"


# Delete elevator by Id
@router.delete("/elevator/delete")
async def delete_elevator(id: int, response: Response, db: Session = Depends(get_db)):
    i = crud.remove_elevator(db, id)

    if i == 0:
        response.status_code = status.HTTP_404_NOT_FOUND

    return f"{i} rows affected" if i != 0 else f"No matches found for ID: {id}"

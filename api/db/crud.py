from sqlalchemy.orm import Session, Query
from typing import Tuple
from . import models
from contracts import demand, elevator


# Elevator CRUD
def get_elevator(db: Session, elevator_id: int) -> models.Elevator | None:
    return db.query(models.Elevator).filter(models.Elevator.id == elevator_id).first()


def create_elevator(db: Session, elevator: elevator.ElevatorCreate) -> models.Elevator:
    db_item = models.Elevator(**elevator.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_elevator(db: Session, elevator_id: int, updated_elevator: elevator.ElevatorCreate) -> Tuple[int, models.Elevator]:
    elevator = db.query(models.Elevator).filter(
        models.Elevator.id == elevator_id)
    r_affected = elevator.update(updated_elevator.model_dump())

    if r_affected > 0:
        db.commit()

    return (r_affected, elevator.first())


def remove_elevator(db: Session, elevator_id: int) -> bool:
    elevator = db.query(models.Elevator).filter(
        models.Elevator.id == elevator_id).first()

    if (elevator == None):
        return False

    db.delete(elevator)
    db.commit()
    return True


# Demands CRUD
def get_demand(db: Session, demand_id: int) -> models.Demand:
    return db.query(models.Demand).filter(models.Demand.id == demand_id).first()


def create_demand(db: Session, demand: demand.DemandCreate) -> models.Demand | None:

    db_elevator_item = db.query(models.Elevator).filter(
        models.Elevator.id == demand.elevator_id).first()

    db_item = models.Demand(**demand.model_dump(exclude={"elevator_id"}))
    db_elevator_item.demands.append(db_item)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_demand(db: Session, demand_id: int, updated_demand: demand.DemandCreate) -> Tuple[int, models.Elevator]:
    demand = db.query(models.Demand).filter(models.Demand.id == demand_id)
    r_affected = demand.update(updated_demand.model_dump())

    if r_affected > 0:
        db.commit()

    return (r_affected, demand.first())


def remove_demand(db: Session, demand_id: int) -> bool:
    demand = db.query(models.Demand).filter(
        models.Demand.id == demand_id).first()

    if (demand == None):
        return False

    db.delete(demand)
    db.commit()
    return True

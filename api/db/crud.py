from sqlalchemy.orm import Session

from . import models
from ..contracts import demand, elevator

# Elevator CRUD
def get_elevator(db: Session, elevator_id: int) -> models.Elevator:
    return db.query(models.Elevator).filter(models.Elevator.id == elevator_id).first()


def create_elevator(db: Session, elevator: elevator.ElevatorCreate) -> models.Elevator:
    db_item = models.Elevator(**elevator.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh()
    return db_item


def update_elevator(db: Session, elevator_id: int, updated_elevator: elevator.ElevatorCreate) -> None:
    db.query(models.Elevator).filter(models.Elevator.id ==
                                     elevator_id).update(**updated_elevator.model_dump())
    db.commit()
    db.refresh()


def remove_elevator(db: Session, elevator_id: int) -> None:
    db.query(models.Elevator).filter(
        models.Elevator.id == elevator_id).delete()
    db.commit()
    db.refresh()


# Demands CRUD
def get_demand(db: Session, demand_id: int) -> models.Demand:
    return db.query(models.Demand).filter(models.Demand.id == demand_id).first()


def create_demand(db: Session, demand: demand.DemandCreate, elevator_id: int) -> models.Demand:
    db_item = models.Demand(**demand.model_dump(), elevator_id=elevator_id)
    db.add(db_item)
    db.commit()
    db.refresh()
    return db_item


def update_demand(db: Session, demand_id: int, updated_demand: demand.DemandCreate) -> None:
    db.query(models.Elevator).filter(models.Elevator.id ==
                                     demand_id).update(**updated_demand.model_dump())
    db.commit()
    db.refresh()


def remove_demand(db: Session, demand_id: int) -> None:
    db.query(models.Demand).filter(models.Demand.id == demand_id).delete()
    db.commit()
    db.refresh()

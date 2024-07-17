from sqlalchemy.orm import Session

from . import models
from contracts import demand, elevator

# Elevator CRUD


def get_elevator(db: Session, elevator_id: int) -> models.Elevator:
    return db.query(models.Elevator).filter(models.Elevator.id == elevator_id).first()


def create_elevator(db: Session, elevator: elevator.ElevatorCreate) -> models.Elevator:
    db_item = models.Elevator(**elevator.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_elevator(db: Session, elevator_id: int, updated_elevator: elevator.ElevatorCreate) -> int:
    r_affected = db.query(models.Elevator).filter(models.Elevator.id ==
                                                  elevator_id).update(updated_elevator.model_dump())
    if r_affected > 0:
        db.commit()

    return r_affected


def remove_elevator(db: Session, elevator_id: int) -> None:
    r_affected = db.query(models.Elevator).filter(
        models.Elevator.id == elevator_id).delete()
    if (r_affected > 0):
        db.commit()
    return r_affected


# Demands CRUD
def get_demand(db: Session, demand_id: int) -> models.Demand:
    return db.query(models.Demand).filter(models.Demand.id == demand_id).first()


def create_demand(db: Session, demand: demand.DemandCreate) -> models.Demand | None:

    db_elevator_item = db.query(models.Elevator).filter(
        models.Elevator.id == demand.elevator_id).first()

    # If not items where found, return none
    if db_elevator_item == None:
        return None
    
    # Checking if source floor is invalid 0 < source <= db_elevator_item.n_floors
    if demand.source > db_elevator_item.n_floors or demand.source <= 0:
        return None
    
    # Checking if destination floor is invalid 0 < destination <= db_elevator_item.n_floors
    if demand.destination > db_elevator_item.n_floors or demand.destination <= 0:
        return None

    db_item = models.Demand(**demand.model_dump(exclude={"elevator_id"}))
    db_elevator_item.demands.append(db_item)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_demand(db: Session, demand_id: int, updated_demand: demand.DemandCreate) -> None:
    db.query(models.Elevator).filter(models.Elevator.id ==
                                     demand_id).update(**updated_demand.model_dump())
    db.commit()


def remove_demand(db: Session, demand_id: int) -> int:
    r_affected = db.query(models.Demand).filter(
        models.Demand.id == demand_id).delete()
    if (r_affected > 0):
        db.commit()
    return r_affected

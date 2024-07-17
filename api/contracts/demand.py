from pydantic import BaseModel
from pydantic.types import datetime
from .utils import WeekDay

# Base class for a demand
class DemandBase(BaseModel):
    timestamp: datetime
    weekday: WeekDay
    source: int
    destination: int
    elevator_id: int


# Abstraction from the base class to make the creation process easier
class DemandCreate(DemandBase):
    pass


# Abstraction from the base class in order to make easier searches
class Demand(DemandBase):
    id: int

    class Config:
        from_attributes = True

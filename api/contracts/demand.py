from datetime import datetime
from pydantic import BaseModel
from .utils import WeekDay

# Base class for a demand
class DemandBase(BaseModel):
    # We must ask for a timestamp from the "elevator" in order to avoid delays
    # with the API, wich could make the data useless.
    timestamp: datetime 
    week_day: WeekDay
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

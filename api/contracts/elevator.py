from pydantic import BaseModel


# Base class for a elevator
class ElevatorBase(BaseModel):
    name: str
    n_floors: int

# Abstraction from the base class to make the creation process easier
class ElevatorCreate(ElevatorBase):
    pass

# Abstraction from the base class in order to make easier searches
class Elevator(ElevatorBase):
    id: int

    class Config:
        from_attributes = True

from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List

from .config import Base


# Table that will store all demands from the elevator
class Demand(Base):
    __tablename__ = "Demands"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime]
    week_day: Mapped[str]
    source: Mapped[int]
    destination: Mapped[int]

    # One to one with elevators
    elevator_id: Mapped[int] = mapped_column(
        ForeignKey("Elevators.id", ondelete="CASCADE"))


# Table that will store elevators
class Elevator(Base):
    __tablename__ = "Elevators"
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    section: Mapped[str]
    n_floors: Mapped[int]

    # One to many with demands
    demands: Mapped[List["Demand"]] = relationship(backref="Elevators", cascade="all, delete")

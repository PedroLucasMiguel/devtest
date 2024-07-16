from sqlalchemy import Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List

from .config import Base


# Table that will store all demands from the elevator
class Demand(Base):
    __tablename__ = "Demands"
    id: Mapped[Integer] = mapped_column(primary_key=True, autoincrement=True)
    timestamp: Mapped[DateTime]
    week_day: Mapped[String]
    source: Mapped[Integer]
    destination: Mapped[Integer]

    # One to one with elevators
    elevator_id: Mapped[Integer] = mapped_column(
        ForeignKey("Elevators.id", ondelete="CASCADE"))


class Elevator(Base):
    __tablename__ = "Elevators"
    id: Mapped[Integer] = mapped_column(autoincrement=True, primary_key=True)
    section: Mapped[String]
    n_floors: Mapped[Integer]

    # One to many with demands
    demands: Mapped[List["Demand"]] = relationship(backref="Elevators")

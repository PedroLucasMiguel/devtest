from enum import Enum


class WeekDay(str, Enum):
    sun = "Sunday"
    mon = "Monday"
    tues = "Tuesday"
    wed = "Wednesday"
    thurs = "Thursday"
    fri = "Friday"
    sat = "Saturday"

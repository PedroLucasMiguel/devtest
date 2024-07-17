from enum import Enum


class WeekDay(str, Enum):
    sun = "Sunday"
    mon = "Monday"
    tues = "Tuesday"
    wed = "Wednesday"
    thurs = "Thursday"
    fri = "Friday"
    sat = "Saturday"


WeekDayToNumerical = {
    "Sunday": 0,
    "Monday": 1,
    "Tuesday": 2,
    "Wednesday": 3,
    "Thursday": 4,
    "Friday": 5,
    "Saturday": 6
}

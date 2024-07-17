'''
06:00 am - 07:00 pm
intervals = 30 seconds

65% - Called
35% - rest
'''

from datetime import datetime, timedelta
import numpy as np
import requests
from typing import Any
import json

API_URL = "http://127.0.0.1:8000"
WEEK_DAYS = ["Sunday", "Monday", "Tuesday",
             "Wednesday", "Thursday", "Friday", "Saturday"]


def setup_simulation_enviroment(n_floors: int) -> int | Any:

    create_elevator_response = requests.post(
        API_URL+"/elevator/create", data=json.dumps({"section": "simulation", "n_floors": n_floors}))

    if create_elevator_response.status_code != 200:
        return create_elevator_response.json()

    return create_elevator_response.json()['id']


def add_demand(timestamp: datetime, week_day: str, source_floor: int, destination_floor: int, elevator_id: int) -> str | None:

    create_demand_response = requests.post(
        API_URL+"/demand/create", data=json.dumps({
            "timestamp": str(timestamp),
            "week_day": week_day,
            "source": source_floor,
            "destination": destination_floor,
            "elevator_id": elevator_id
        }))

    if create_demand_response.status_code != 200:
        return create_demand_response.json()

    return None


def main():

    n_floors = 12
    elevator = setup_simulation_enviroment(n_floors)

    if type(elevator) != int:
        print(f"Error! API request failed.\n{elevator}")
        return

    hour = "06"
    minutes = "00"
    stop_hour = 19
    minutes_increment = 2
    call_prob = 0.65
    rest_prob = 0.35

    prev_floor = 2

    for week_day in WEEK_DAYS:
        start_time = datetime.fromisoformat(f"2024-07-17 {hour}:{minutes}:00.000")

        while start_time.hour != stop_hour:
            start_time += timedelta(minutes=minutes_increment)
            action = np.random.choice(["Move", "Rest"], 1, p=[call_prob, rest_prob])

            if action == "Move":
                floors = list(range(1, n_floors+1))
                floors.remove(prev_floor)
                destination_floor = int(np.random.choice(floors))
                response = add_demand(start_time, week_day,
                                    prev_floor, destination_floor, elevator)
                prev_floor = destination_floor

            else:
                response = add_demand(start_time, week_day,
                                    prev_floor, prev_floor, elevator)

            if type(response) == str:
                print(f"Error! API request failed.\n{response}")
                return
        
        print(f"Finished simulation for {week_day}")
    

if __name__ == "__main__":
    main()

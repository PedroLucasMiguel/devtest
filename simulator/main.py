
import json
import requests
import numpy as np
from typing import Any, Tuple
from datetime import datetime, timedelta

WEEK_DAYS = ["Sunday", "Monday", "Tuesday",
             "Wednesday", "Thursday", "Friday", "Saturday"]

# Configuration:
# Change the values to alter the result of the simulation

API_URL = "http://127.0.0.1:8000" # API URL
N_FLOORS = 12 # N° of floors for the mock elevator
START_HOUR = "06" # Hour to start the simulation, must be in 00 format
START_MINUTES = "00" # Minutes to start the simulation, must be in 00 format
STOP_HOUR = 19 # Hour to stop the simulation, must be in between 0 <= STOP_HOUR <= 24
MINUTES_INCREMENT = 30 # Minute increment for each iteration
CALL_PROB = 0.65 # Probability of the elevator to be called
REST_PROB = 0.35 # Probability of the elevator to stay in the same spot


# Initialize the simulation enviroment by creating a test elevator
def setup_simulation_enviroment() -> int | Any:
    create_elevator_response = requests.post(
        f"{API_URL}/elevator/create",
        data=json.dumps({"name": "simulation", 
                         "n_floors": N_FLOORS}))

    # Check if the elevator was created, if not, return the error
    if create_elevator_response.status_code != 200:
        return create_elevator_response.json()

    return create_elevator_response.json()['id']

# Creating a demand
def add_demand(timestamp: datetime, 
               week_day: str, 
               source_floor: int, 
               destination_floor: int, 
               elevator_id: int) -> str | None:
    # Making the requst
    create_demand_response = requests.post(
        API_URL+"/demand/create", data=json.dumps({
            "timestamp": str(timestamp),
            "week_day": week_day,
            "source": source_floor,
            "destination": destination_floor,
            "elevator_id": elevator_id
        }))

    # If it fails returns the JSON
    if create_demand_response.status_code != 200:
        return create_demand_response.json()

    return None


# Getting the dataset
def retrieve_dataset_json(elevator_id: int) -> Tuple[bool, requests.Response]:
    dt_json = requests.get(f"{API_URL}/dataset/generate/{elevator_id}")

    # If it fails returns false and the JSON
    if dt_json.status_code != 200:
        return (False, dt_json)
    
    return (True, dt_json)


def main():
    elevator = setup_simulation_enviroment()

    if type(elevator) != int:
        print(f"Error! API request failed.\n{elevator}")
        return

    prev_floor = 1

    # This simulation will run from START_HOUR to STOP_HOUR with the minutes stepping by MINUTES_INCREMENT
    for week_day in WEEK_DAYS:
        start_time = datetime.fromisoformat(
            f"2024-07-17 {START_HOUR}:{START_MINUTES}:00.000")

        while start_time.hour != STOP_HOUR:
            # Incrementing the time
            start_time += timedelta(minutes=MINUTES_INCREMENT)

            # Randomly choose if the elevator will be called or will rest by the defined probabilities
            action = np.random.choice(["Move", "Rest"], 1, 
                                      p=[CALL_PROB,  REST_PROB])

            if action == "Move":
                # Moving the elevator by adding a demand with a random floor
                floors = list(range(1, N_FLOORS+1))
                floors.remove(prev_floor)
                destination_floor = int(np.random.choice(floors))
                response = add_demand(start_time, week_day,
                                      prev_floor, destination_floor, elevator)
                prev_floor = destination_floor

            else:
                # Elevator is resting in this floor
                response = add_demand(start_time, week_day,
                                      prev_floor, prev_floor, elevator)

            # Checking if the request was successfull
            if type(response) == str:
                print(f"Error! API request failed.\n{response}")
                return

        print(f"Finished simulation for {week_day}")
    
    # Saving the dataset into a JSON file
    with open("dt.json", "w") as f:
        response = retrieve_dataset_json(elevator)
        if not response[0]:
            print(f"Error! API request failed.\n{response[1].text}")
            return
        json.dump(response[1].json(), f)

    print("Dataset generated successfully!")


if __name__ == "__main__":
    main()

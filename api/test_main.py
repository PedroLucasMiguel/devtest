from fastapi.testclient import TestClient
from main import app
from dependencies import get_db
from routers.elevator import ROUTER_PATH as ELEVATOR_PATH
from routers.demand import ROUTER_PATH as DEMAND_PATH
from routers.dataset import ROUTER_PATH as DATASET_PATH
import pytest
from datetime import datetime

WEEK_DAYS = ["Sunday", "Monday", "Tuesday",
             "Wednesday", "Thursday", "Friday", "Saturday"]


class TestSequence:
    shared_data = {"elevator_data": None, "demand_data": None}
    client = TestClient(app)

    # Creating a valid user
    def test_create_valid_elevator(self):
        elevator_data = {"name": "testentry", "n_floors": 12}
        response = self.client.post(
            f"{ELEVATOR_PATH}/create/", json=elevator_data)
        assert response.status_code == 200

        response_json = response.json()
        self.shared_data["elevator_data"] = response_json.copy()
        del response_json["id"]

        assert response_json == elevator_data

    # Creating a invalid user by defining a n_floors <= 0

    def test_create_invalid_elevator(self):
        response = self.client.post(f"{ELEVATOR_PATH}/create/",
                                    json={"name": "testentry", "n_floors": -1})
        assert response.status_code == 403

    # Getting the test_elevator and checking if it is the same as we
    # previously created

    def test_get_elevator(self):
        response = self.client.get(
            f"{ELEVATOR_PATH}/get/{self.shared_data["elevator_data"]["id"]}")
        assert response.status_code == 200
        assert response.json() == self.shared_data["elevator_data"]

    # Testing editing the elevator

    def test_edit_elevator(self):
        edited_elevator = self.shared_data["elevator_data"]
        edited_elevator["n_floors"] = 24

        response = self.client.put(f"{ELEVATOR_PATH}/edit/{self.shared_data["elevator_data"]["id"]}",
                                   json=edited_elevator)

        assert response.status_code == 200
        assert response.json() == edited_elevator

    # Testing edit elevator to a invalid entry

    def test_edit_invalid_elevator(self):
        edited_elevator = self.shared_data["elevator_data"]
        edited_elevator["n_floors"] = -12

        response = self.client.put(f"{ELEVATOR_PATH}/edit/{self.shared_data["elevator_data"]["id"]}",
                                   json=edited_elevator)

        assert response.status_code == 403

    # Testing adding an demand
    def test_add_demands(self):

        for weekday in WEEK_DAYS:
            demand_data = {
                "timestamp": str(datetime.now()).replace(" ", "T"),
                "week_day": weekday,
                "source": 1,
                "destination": 1,
                "elevator_id": self.shared_data["elevator_data"]["id"]}

            response = self.client.post(
                f"{DEMAND_PATH}/create", json=demand_data)
            assert response.status_code == 200

            response_json = response.json()

            if weekday == "Sunday":
                self.shared_data["demand_data"] = response_json.copy()

            del response_json["id"]

            assert response_json == demand_data


    # Testing editing a demand:
    def test_edit_demand(self):

        new_demand = self.shared_data["demand_data"].copy()
        new_demand["source"] = 2
        new_demand["destination"] = 2
        new_demand["week_day"] = WEEK_DAYS[1]
        
        new_demand_id = new_demand["id"]

        del new_demand["id"]

        response = self.client.put(
            f"{DEMAND_PATH}/edit/{new_demand_id}", json=new_demand)
        
        assert response.status_code == 200
        new_demand["id"] = new_demand_id
        assert new_demand == response.json()


    # Test invalid demand edit
    def test_edit_invalid_demands(self):

        new_demand = self.shared_data["demand_data"].copy()
        new_demand["source"] = -1
    
        new_demand_id = new_demand["id"]
        del new_demand["id"]

        response = self.client.put(
            f"{DEMAND_PATH}/edit/{new_demand_id}", json=new_demand)
        
        assert response.status_code == 403
        
        new_demand["source"] = 2
        new_demand["destination"] = -1

        response = self.client.put(
            f"{DEMAND_PATH}/edit/{new_demand_id}", json=new_demand)

        assert response.status_code == 403

        new_demand["destination"] = 2
        new_demand["elevator_id"] = -1

        response = self.client.put(
            f"{DEMAND_PATH}/edit/{new_demand_id}", json=new_demand)

        assert response.status_code == 404
    
    # Testing to remove the demand
    def test_remove_demand(self):

        response = self.client.delete(
            f"{DEMAND_PATH}/delete/{self.shared_data["demand_data"]["id"]}")
        
        assert response.status_code == 200

        response = self.client.get(f"{DEMAND_PATH}/get/{self.shared_data["demand_data"]["id"]}")

        assert response.status_code == 404


    # Testing remove invalid demand
    def test_remove_invalid_demand(self):
        response = self.client.delete(f"{DEMAND_PATH}/delete/{self.shared_data["demand_data"]["id"]}")

        assert response.status_code == 404


    # Testing to generate the dataset
    def test_generate_dataset(self):
        response = self.client.get(f"{DATASET_PATH}/generate/{self.shared_data["elevator_data"]["id"]}")

        assert response.status_code == 200

    # Testing to generate a dataset from invalid elevators
    def test_generate_dataset_from_invalid_elevators(self):
        
        # Generating a extra elevator
        elevator_data = {"name": "testentry2", "n_floors": 12}
        response = self.client.post(
            f"{ELEVATOR_PATH}/create/", json=elevator_data)
        
        assert response.status_code == 200

        response_json = response.json()

        response = self.client.get(f"{DATASET_PATH}/generate/{response_json["id"]}")

        assert response.status_code == 403

        response = self.client.delete(
            f"{ELEVATOR_PATH}/delete/{response_json["id"]}")
        
        assert response.status_code == 200

        response = self.client.get(f"{DATASET_PATH}/generate/{response_json["id"]}")

        assert response.status_code == 404


    # Testing to remove a elevator
    def test_remove_elevator(self):
        response = self.client.delete(f"{ELEVATOR_PATH}/delete/{self.shared_data["elevator_data"]["id"]}")

        assert response.status_code == 200

        response = self.client.get(f"{ELEVATOR_PATH}/get/{self.shared_data["elevator_data"]["id"]}")

        assert response.status_code == 404

    
    # Testing to remove a invalid elevator
    def test_remove_invalid_elevator(self):
        response = self.client.delete(f"{ELEVATOR_PATH}/delete/{self.shared_data["elevator_data"]["id"]}")

        assert response.status_code == 404
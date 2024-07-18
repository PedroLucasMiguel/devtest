from datetime import datetime
from fastapi.testclient import TestClient

from main import app
from routers.elevator import ROUTER_PATH as ELEVATOR_PATH
from routers.demand import ROUTER_PATH as DEMAND_PATH
from routers.dataset import ROUTER_PATH as DATASET_PATH

# Week days used in some areas of the code
WEEK_DAYS = ["Sunday", "Monday", "Tuesday",
             "Wednesday", "Thursday", "Friday", "Saturday"]


# This test suite contains a series of test that are meant to be executed sequentially
class TestSequence:

    # shared_data will store the mock data that we will create during tests
    shared_data = {"elevator_data": None, "demand_data": None}

    # Test client from FastAPI
    client = TestClient(app)


    # Creating a valid user
    def test_create_valid_elevator(self):
        # Creating the mock data end sending to the API
        elevator_data = {"name": "testentry", "n_floors": 12}
        response = self.client.post(
            f"{ELEVATOR_PATH}/create/", json=elevator_data)
        assert response.status_code == 200 # User created successfully

        # Storing the user dade to be used in other tests
        response_json = response.json()
        self.shared_data["elevator_data"] = response_json.copy()
        
        # Checking if the user was created correctly
        del response_json["id"] # We delete the just to make the assertion pass, as we do not saved the ID previously
        assert response_json == elevator_data


    # Creating a invalid user by defining a n_floors <= 0
    def test_create_invalid_elevator(self):
        response = self.client.post(f"{ELEVATOR_PATH}/create/",
                                    json={"name": "testentry", "n_floors": -1})
        assert response.status_code == 403 # Elevator should not n_floors <= 0

        response = self.client.post(f"{ELEVATOR_PATH}/create/",
                                    json={"name": "", "n_floors": -1})
        assert response.status_code == 403 # Elevator should not have empty name


    # Testing if we can recover the exact same elevator through or get request
    def test_get_elevator(self):
        response = self.client.get(
            f"{ELEVATOR_PATH}/get/{self.shared_data["elevator_data"]["id"]}")
        assert response.status_code == 200 # Elevator retrieved successfully
        assert response.json() == self.shared_data["elevator_data"] # Checking if it is what we were expecting


    # Testing editing the elevator
    def test_edit_elevator(self):
        # Modifing some data on a auxiliary variable
        edited_elevator = self.shared_data["elevator_data"]
        edited_elevator["n_floors"] = 24

        response = self.client.put(f"{ELEVATOR_PATH}/edit/{self.shared_data["elevator_data"]["id"]}",
                                   json=edited_elevator)

        assert response.status_code == 200 # Elevator edited successfully
        assert response.json() == edited_elevator # The edited elevator is the exact same as we created


    # Testing edit elevator to a invalid values
    def test_edit_invalid_elevator(self):
        # Modifing some data on a auxiliary variable
        edited_elevator = self.shared_data["elevator_data"]
        edited_elevator["n_floors"] = -12

        response = self.client.put(
            f"{ELEVATOR_PATH}/edit/{self.shared_data["elevator_data"]["id"]}", json=edited_elevator)

        assert response.status_code == 403 # The edit request failed because of n_floors value being negative


    # Testing adding an demand
    def test_add_demands(self):
        # For this test, we are going to create a demand for each day of the week
        for weekday in WEEK_DAYS:
            demand_data = {
                "timestamp": str(datetime.now()).replace(" ", "T"), # Fixing datetime format
                "week_day": weekday,
                "source": 1,
                "destination": 1,
                "elevator_id": self.shared_data["elevator_data"]["id"]}

            response = self.client.post(
                f"{DEMAND_PATH}/create", json=demand_data)
            
            assert response.status_code == 200 # The demand on this iteration was created successfully

            response_json = response.json()

            # Saving the first demand to test more cases later
            if weekday == "Sunday":
                self.shared_data["demand_data"] = response_json.copy()

            # Checking if the created data is what we were expecting
            del response_json["id"]
            assert response_json == demand_data


    # Testing editing a demand:
    def test_edit_demand(self):
        # Copying the demand that we saved previously and editing it
        new_demand = self.shared_data["demand_data"].copy()
        new_demand["source"] = 2
        new_demand["destination"] = 2
        new_demand["week_day"] = WEEK_DAYS[1]

        new_demand_id = new_demand["id"]

        del new_demand["id"]

        response = self.client.put(
            f"{DEMAND_PATH}/edit/{new_demand_id}", json=new_demand)

        assert response.status_code == 200 # The demand was created successful

        new_demand["id"] = new_demand_id
        assert new_demand == response.json() # The recieved data is the same


    # Test invalid demand edit
    def test_edit_invalid_demands(self):
        # Copying the demand that we saved previously and editing it with invalid data
        new_demand = self.shared_data["demand_data"].copy()
        new_demand["source"] = -1 # Invalid source floor

        new_demand_id = new_demand["id"]
        del new_demand["id"]

        response = self.client.put(
            f"{DEMAND_PATH}/edit/{new_demand_id}", json=new_demand)

        assert response.status_code == 403 # Demand must not be edited

        new_demand["source"] = 2
        new_demand["destination"] = -1 # Invalid destination floor

        response = self.client.put(
            f"{DEMAND_PATH}/edit/{new_demand_id}", json=new_demand)

        assert response.status_code == 403 # Demand must not be edited

        new_demand["destination"] = 2
        new_demand["elevator_id"] = -1 # Invalid elevator_id

        response = self.client.put(
            f"{DEMAND_PATH}/edit/{new_demand_id}", json=new_demand)

        assert response.status_code == 404 # Demand must not be edited


    # Testing to remove the demand
    def test_remove_demand(self):
        # Removing the demand that we saved previously
        response = self.client.delete(
            f"{DEMAND_PATH}/delete/{self.shared_data["demand_data"]["id"]}")

        assert response.status_code == 200 # Demand removed successful

        # Checking if the data was REALLY removed
        response = self.client.get(
            f"{DEMAND_PATH}/get/{self.shared_data["demand_data"]["id"]}")

        assert response.status_code == 404 # Demand should not be found in the DB


    # Testing remove invalid demand
    def test_remove_invalid_demand(self):
        # Trying to remove the demand that we previously removed
        response = self.client.delete(
            f"{DEMAND_PATH}/delete/{self.shared_data["demand_data"]["id"]}")

        assert response.status_code == 404 # Demand not found


    # Testing to generate the dataset
    def test_generate_dataset(self):
        # Generating a dataset from the elevator that we saved previously
        response = self.client.get(
            f"{DATASET_PATH}/generate/{self.shared_data["elevator_data"]["id"]}")

        assert response.status_code == 200 # Dataset saved successfuly


    # Testing to generate a dataset from invalid elevators
    def test_generate_dataset_from_invalid_elevators(self):

        # Generating a extra elevator with no demands
        elevator_data = {"name": "testentry2", "n_floors": 12}
        response = self.client.post(
            f"{ELEVATOR_PATH}/create/", json=elevator_data)

        assert response.status_code == 200 # Checking if it was created

        response_json = response.json()

        # Trying to generate a dataset from a elavator without demands
        response = self.client.get(
            f"{DATASET_PATH}/generate/{response_json["id"]}")

        assert response.status_code == 403 # Dataset not generated

        # Deleting the extra elevator
        response = self.client.delete(
            f"{ELEVATOR_PATH}/delete/{response_json["id"]}")
        
        assert response.status_code == 200

        # Trying to generate a dataset from the deleted elevator
        response = self.client.get(
            f"{DATASET_PATH}/generate/{response_json["id"]}")

        assert response.status_code == 404 # Elevator not found


    # Testing to remove a elevator
    def test_remove_elevator(self):
        # Removing the elevator that we saved previously
        response = self.client.delete(
            f"{ELEVATOR_PATH}/delete/{self.shared_data["elevator_data"]["id"]}")

        assert response.status_code == 200 # Elevator removed successfuly

        # Trying to get the removed elevator
        response = self.client.get(
            f"{ELEVATOR_PATH}/get/{self.shared_data["elevator_data"]["id"]}")

        assert response.status_code == 404 # Elevator not found


    # Testing to remove a invalid elevator
    def test_remove_invalid_elevator(self):
        # Trying to remove a non existing elevator
        response = self.client.delete(
            f"{ELEVATOR_PATH}/delete/{self.shared_data["elevator_data"]["id"]}")

        assert response.status_code == 404 # Elevator not found

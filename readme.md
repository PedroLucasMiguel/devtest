# Dev Test - Solution by Pedro Lucas Miguel

Hello everyone! This is my solution to the Dev Test.

## How to execute

### To run the API:
```bash
# Create a python "venv" by following: https://docs.python.org/pt-br/dev/library/venv.html
# Next execute the following commands:
pip install -r requirements.txt
cd api
fastapi run main.py
```
You can access the docs of the api by the link provided in your terminal.

### To run the tests on the API:
```bash
# On the "api" folder execute:
pytest test_main.py
```

### To run the simulator:
```bash
# On the "simulator" folder execute:
python main.py

# The simulation parameters must be setted manually in the simulator/main.py file
```
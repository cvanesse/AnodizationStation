# The config file holds all of the station-specific variables like cell parameters, etc.
CELL_PARAMETERS = []

CELL_PARAMETERS.append({
    "running_pin": 7,
    "bus_pins": [11, 15],
    "button_pin": 19,
    "log_file": "tlog.csv",
    "cycle_file": "4ST.cycle",
    "cycle_params": ["0.5", "0.5", "0.5", "0.5", "S", "A", "B", "C"]
})

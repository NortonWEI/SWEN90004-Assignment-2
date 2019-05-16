import json
from pathlib import Path

# Author: Dafu Ai

# Constants which provides default values for dynamic parameters
MAX_JAILED_TERM = ('max_jailed_term', 30)               # Maximum possible jailed term.
GOVERNMENT_LEGITIMACY = ('government_legitimacy', 0.5)  # Government legitimacy.
MOVEMENT = ('movement', True)
FRAME_INTERVAL = ('frame_interval', 0.01)
REBELLION_THRESHOLD = ('rebellion_threshold', 0.5)

# Include all parameters here
DYNAMIC_PARAMETERS = [
    MAX_JAILED_TERM,
    GOVERNMENT_LEGITIMACY,
    MOVEMENT,
    FRAME_INTERVAL,
    REBELLION_THRESHOLD
]


class DynamicParamReader:
    """Reader for dynamic parameters"""
    def __init__(self, file_path) -> None:
        self.file_path = file_path

        # Write out default values if config file not found
        if not Path(file_path).exists():
            params = {}
            for p in DYNAMIC_PARAMETERS:
                # Write key p[0] <-> value p[1]
                params[p[0]] = p[1]

            with open(file_path, 'w') as outfile:
                json.dump(params, outfile)

    def read_params(self) -> dict:
        """Read and return the params dict from the file path"""
        with open(self.file_path, 'r') as file:
            params = json.load(file)
            return params

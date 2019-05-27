import json
from pathlib import Path

# Author: Dafu ai

# Constants for static parameters (they wont change at run time)
K: float = 2.3                      # Factor for determining arrest probability.
THRESHOLD: float = 0.1              # By how much must G > N to make someone rebel?
MAP_HEIGHT: int = 40                # Width of the patch map (i.e. the number of patches in x direction).
MAP_WIDTH: int = 40                 # Width of the patch map (i.e. the number of patches in x direction).
INITIAL_COP_DENSITY: float = 0.05   # Percentage of cops (in the total number of patches in the map).
INITIAL_AGENT_DENSITY: float = 0.7  # Percentage of agents (in the total number of patches in the map).
VISION: float = 7.0                 # Defines the radius of neighbourhood for any patch.
MAX_FRAMES = 1000                   # The number of frames to be ticked for the simulator
FILE_PATH = 'dynamic_params.json'   # Path of the file that stores the parameters


def total_patches() -> int:
    """Total number of patches."""
    return MAP_HEIGHT * MAP_WIDTH


def total_cops() -> int:
    """Total number of cops."""
    return int(total_patches() * INITIAL_COP_DENSITY)


def total_agents() -> int:
    """Total number of agents."""
    return int(total_patches() * INITIAL_AGENT_DENSITY)

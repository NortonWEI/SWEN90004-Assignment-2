"""
This file defines all constants which are to be set before program runs.

Author: Dafu Ai
"""

K: float = 0.1                      # Factor for determining arrest probability.
THRESHOLD: float = 0.4              # By how much must G > N to make someone rebel?
MAP_HEIGHT: int = 10                # Width of the patch map (i.e. the number of patches in x direction).
MAP_WIDTH: int = 10                 # Width of the patch map (i.e. the number of patches in x direction).
INITIAL_COP_DENSITY: float = 0.04   # Percentage of cops (in the total number of patches in the map).
INITIAL_AGENT_DENSITY: float = 0.7  # Percentage of agents (in the total number of patches in the map).
VISION: float = 7.0                 # Defines the radius of neighbourhood for any patch.
MAX_JAILED_TERM: int = 30           # Maximum possible jailed term.
GOVERNMENT_LEGITIMACY: float = 0.1  # Government legitimacy.


def total_patches() -> int:
    """Total number of patches."""
    return MAP_HEIGHT * MAP_WIDTH


def total_cops() -> int:
    """Total number of cops."""
    return int(total_patches() * INITIAL_COP_DENSITY)


def total_agents() -> int:
    """Total number of agents."""
    return int(total_patches() * INITIAL_AGENT_DENSITY)

import random
from math import exp, floor

from models import Turtle, World, Cop
from params import GOVERNMENT_LEGITIMACY, K, THRESHOLD

# Author: Dafu Ai


class Agent(Turtle):
    """
    Simulates an Agent object.
    """
    jail_term: int              # Remaining time length for jailing
    active: bool                # Indicates whether the turtle is open rebelling
    risk_aversion: float        # The degree of reluctance to take risks
    perceived_hardship: float   # Perceived hardship of rebelling

    def __init__(self, world: World) -> None:
        """ Initialise the agent """
        super().__init__(world)
        self.jail_term = 0
        self.active = False
        self.risk_aversion = random.uniform(0, 1)
        self.perceived_hardship = random.uniform(0, 1)

    def update(self) -> None:
        """Determines whether to open rebel."""
        super().update()

        # Only determine behaviour if it is not jailed
        if not self.is_jailed():
            self.determine_behaviour()

    def is_jailed(self) -> bool:
        """Determine whether this agent is currently jailed."""
        return self.jail_term > 0

    def get_grievance(self) -> float:
        """Calculate and return the grievance of the agent."""
        return self.perceived_hardship * (1 - GOVERNMENT_LEGITIMACY)

    def get_estimated_arrest_probability(self) -> float:
        """Calculate and return the estimated arrest probability of the agent (based on the formula)."""
        patch_map = self.world.patch_map

        # c = number of neighbour cops
        c = len(patch_map.filter_neighbour_turtles(self.patch, lambda t: isinstance(t, Cop)))

        # a = 1 + number of neighbour turtles which are active
        a = 1 + len(patch_map.filter_neighbour_turtles(
            self.patch,
            lambda t: isinstance(t, Agent) and t.active
        ))

        return 1 - exp(-K * floor(c/a))

    def determine_behaviour(self) -> None:
        """Determine the behaviour of this agent by flagging its activeness."""
        self.active = (self.get_grievance() - self.risk_aversion * self.get_estimated_arrest_probability()) > THRESHOLD

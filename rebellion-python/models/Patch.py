from math import sqrt
from typing import List, Any

from models import Turtle, Cop, Agent
from params import VISION

# Author: Dafu Ai


class Patch:
    """
    Simulates a Patch (of a map).
    """
    x: int                  # x coordinate of this patch.
    y: int                  # y coordinate of this patch.
    turtles: List[Turtle]   # All turtles in the patch.

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.turtles = []

    def add_turtle(self, turtle: Turtle) -> None:
        """Add a turtle."""
        self.turtles.append(turtle)

    def remove_turtle(self, turtle: Turtle) -> None:
        """Remove a turtle."""
        self.turtles.remove(turtle)

    def is_occupied(self) -> bool:
        """Determine whether this patch is currently occupied."""
        for turtle in self.turtles:
            if isinstance(turtle, Cop):
                return True

            if isinstance(turtle, Agent) and turtle.is_jailed():
                return True

        return False

    def is_neighbour_with(self, patch: 'Patch') -> bool:
        """Determine whether the specified patch is a neighbour to this patch."""
        x_diff = patch.x - self.x
        y_diff = patch.y - self.y

        return sqrt(pow(x_diff, x_diff) + pow(y_diff, y_diff)) <= VISION

from random import shuffle
from typing import List

from models import PatchMap, Cop, Agent, Turtle
from params import total_cops, total_agents

# Author: Dafu Ai


class World:
    """
    Simulates a world of agents, cops and patches.
    """
    patch_map: PatchMap     # The patch map managing all patches
    turtles: List[Turtle]   # All turtles.

    def __init__(self) -> None:
        """Create all components."""
        self.patch_map = PatchMap()
        self.turtles = []

        for i in range(0, total_cops()):
            self.turtles.append(Cop(self))

        for i in range(0, total_agents()):
            self.turtles.append(Agent(self))

    def update(self) -> None:
        """Let all components perform update."""
        self.patch_map.update()

        # Shuffle all turtles so they perform action in a random sequence
        shuffle(self.turtles)

        for turtle in self.turtles:
            turtle.update()

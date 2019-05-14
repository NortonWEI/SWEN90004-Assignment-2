import random

from models import Turtle, World, Agent
from params import MAX_JAILED_TERM

# Author: Dafu Ai


class Cop(Turtle):
    """
    Simulates a Cop.
    """
    def __init__(self, world: World) -> None:
        super().__init__(world)

    def update(self) -> None:
        """Perform relevant action as a Cop."""
        super().update()
        self.enforce()

    def can_move(self) -> bool:
        """Cops can always move if parent class allows movement."""
        return super().can_move()

    def enforce(self) -> None:
        """Find and arrest a random active agent in the neighbourhood."""

        # Find all active agents in the neighbourhood
        agents = self.world.patch_map.filter_neighbour_turtles(
            self.patch,
            lambda t: isinstance(t, Agent) and t.active
        )

        # Don't continue if there is no matched agent
        if len(agents) == 0:
            return

        # Move to the patch of the (about-to-be) jailed agent
        suspect = random.choice(agents)
        self.move_to_patch(suspect.patch)

        # Arrest suspect
        suspect.active = False
        suspect.jail_term = random.randint(1, MAX_JAILED_TERM)




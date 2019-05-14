import random
from typing import Callable, Optional

from models import Patch, Turtle
from params import MAP_HEIGHT, MAP_WIDTH

# Author: Dafu Ai


class PatchMap:
    """
    Simulate a map of patches, which also provides a number of utility functions
    """
    def __init__(self) -> None:
        """Create the required number of patches."""
        self.patches = []

        for y in range(0, MAP_HEIGHT):
            for x in range(0, MAP_WIDTH):
                self.patches.append(Patch(x, y))

    def get_neighbours(self, patch: Patch) -> [Patch]:
        """Ignore the patch to be compared."""
        return filter(lambda p: p != patch and p.is_neighbour_with(patch), self.patches)

    def get_random_unoccupied_patch(self) -> Patch:
        """Get an random, unoccupied patch."""
        return random.choice(filter(lambda p: not p.is_occupied(), self.patches))

    def filter_neighbour_turtles(self, patch: Patch, turtle_filter: Optional[[Turtle], bool]):
        """Get the filtered list of neighbour turtle based on the filter function."""
        neighbour_patches = self.get_neighbours(patch)
        all_turtles = []

        # For each neighbour patch, find all matching turtles and add to the final list
        for patch in neighbour_patches:
            turtles = filter(turtle_filter, patch.turtles)
            all_turtles += turtles
            
        return all_turtles

    def update(self):
        pass


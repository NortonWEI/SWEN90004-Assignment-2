from models import World, Patch

# Author: Dafu Ai


class Turtle:
    """
    Simulates a turtle object, in which the behaviours are shared by both Cop and Turtle.
    """
    world: World    # The world this turtle is in.
    patch: Patch    # The patch this turtle is currently at.

    def __init__(self, world: World) -> None:
        """Place itself to a patch."""
        self.world = world
        self.patch = None
        self.move()

    def can_move(self) -> bool:
        """Determines whether this turtle can move."""
        return True

    def move_to_patch(self, new_patch: Patch) -> None:
        """Move to a specified patch."""

        if self.patch is not None:
            self.patch.remove_turtle(self)

        new_patch.add_turtle(self)
        self.patch = new_patch

    def move(self) -> None:
        """Move to a random, unoccupied patch."""
        if not self.can_move():
            return

        new_patch = self.world.patch_map.get_random_unoccupied_patch()
        self.move_to_patch(new_patch)

    def update(self) -> None:
        """Update the current state by moving to another place"""
        self.move()

import csv
from math import sqrt, exp, floor
from random import shuffle, choice, uniform, randint
from typing import List, Optional, Union, Callable

from dynamic_params import DynamicParamReader, DYNAMIC_PARAMETERS, MAX_JAILED_TERM, GOVERNMENT_LEGITIMACY, MOVEMENT
from static_params import total_cops, total_agents, VISION, MAP_WIDTH, MAP_HEIGHT, K, THRESHOLD


# Author: Dafu Ai
# Please note, all models are interdependent so they are under the same file.


class World:
    """
    Simulates a world of agents, cops and patches.
    """
    patch_map: 'PatchMap'               # The patch map managing all patches
    turtles: List                       # All turtles
    params_reader: DynamicParamReader   # Reader for dynamic parameters
    output_filename: str                # Output file path

    def __init__(self, dynamic_params_reader: DynamicParamReader, output_filename: str) -> None:
        """Create all components."""
        self.params_reader = dynamic_params_reader
        self.output_filename = output_filename
        self.patch_map = PatchMap(self)
        self.turtles = []

        for i in range(0, total_cops()):
            self.turtles.append(Cop(self))

        for i in range(0, total_agents()):
            self.turtles.append(Agent(self))

        # Write header row for output csv
        with open(output_filename, 'w') as output_file:
            csv_writer = csv.writer(output_file)
            header_columns = ['frame', 'quiet', 'jailed', 'active']

            for p in DYNAMIC_PARAMETERS:
                header_columns.append(p[0])

            csv_writer.writerow(header_columns)

    def update(self, frame: int) -> None:
        """Let all components perform update."""
        self.patch_map.update()

        # Shuffle all turtles so they perform action in a random sequence
        shuffle(self.turtles)

        for turtle in self.turtles:
            turtle.update()

        # First filter out non-agent turtles
        agents: List[Agent] = list(filter(lambda t: isinstance(t, Agent), self.turtles))

        # Get stats for each agent status
        quiet = list(filter(lambda t: t.is_quiet(), agents))
        jailed = list(filter(lambda t: t.is_jailed(), agents))
        active = list(filter(lambda t: t.active, agents))

        # Append current state to the output csv
        with open(self.output_filename, 'a') as output_file:
            csv_writer = csv.writer(output_file)
            columns = [frame, len(quiet), len(jailed), len(active)]

            params = self.params_reader.read_params()

            for p in DYNAMIC_PARAMETERS:
                columns.append(params[p[0]])

            csv_writer.writerow(columns)

    def get_dynamic_param(self, key):
        """Get the value of dynamic parameters"""
        return self.params_reader.read_params()[key]


class Turtle:
    """
    Simulates a turtle object, in which the behaviours are shared by both Cop and Turtle.
    """
    world: World    # The world this turtle is in.
    patch: 'Patch'    # The patch this turtle is currently at.

    def __init__(self, world: World) -> None:
        """Place itself to a patch."""
        self.world = world
        self.patch = None
        self.move(True)

    def can_move(self) -> bool:
        """Determines whether this turtle can move."""
        return self.world.get_dynamic_param(MOVEMENT[0]) is True

    def move_to_patch(self, new_patch: 'Patch') -> None:
        """Move to a specified patch."""

        if self.patch is not None:
            self.patch.remove_turtle(self)

        new_patch.add_turtle(self)
        self.patch = new_patch

    def move(self, first_time: bool = False) -> None:
        """Move to a random, unoccupied patch if it can move or they need to have an initial location)."""
        if not self.can_move() and not first_time:
            return

        new_patch = self.world.patch_map.get_random_unoccupied_patch(self.patch)

        # Only move to the new patch if there is one available
        if new_patch is not None:
            self.move_to_patch(new_patch)

    def update(self) -> None:
        """Update the current state by moving to another place"""
        self.move()


class Cop(Turtle):
    """
    Simulates a Cop.
    """
    def update(self) -> None:
        """Perform relevant action as a Cop."""
        super().update()

        if self.patch is not None:
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
        suspect = choice(agents)
        self.move_to_patch(suspect.patch)

        # Arrest suspect
        suspect.active = False
        suspect.jail_term = randint(1, self.world.get_dynamic_param(MAX_JAILED_TERM[0]))


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
        self.risk_aversion = uniform(0, 1)
        self.perceived_hardship = uniform(0, 1)

    def update(self) -> None:
        """Determines whether to open rebel."""
        super().update()

        # Only determine behaviour if it is not jailed
        if self.patch is not None and not self.is_jailed():
            self.determine_behaviour()

    def can_move(self) -> bool:
        """ If it is jailed it cannot move """
        return super().can_move() and not self.is_jailed()

    def is_jailed(self) -> bool:
        """Determine whether this agent is currently jailed."""
        return self.jail_term > 0

    def is_quiet(self) -> bool:
        """Determine whether this patch is quiet (i.e. inactive & not jailed)."""
        return (not self.active) and (not self.is_jailed())

    def get_grievance(self) -> float:
        """Calculate and return the grievance of the agent."""
        return self.perceived_hardship * (1 - self.world.get_dynamic_param(GOVERNMENT_LEGITIMACY[0]))

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


class Patch:
    """
    Simulates a Patch (of a map).
    """
    x: int                  # x coordinate of this patch.
    y: int                  # y coordinate of this patch.
    turtles: List   # All turtles in the patch.

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

        return sqrt(x_diff*x_diff + y_diff*y_diff) <= VISION


class PatchMap:
    """
    Simulate a map of patches, which also provides a number of utility functions
    """
    patches: List[Patch]  # All patches stored
    world: World  # The world this map is in

    def __init__(self, world: World) -> None:
        """Create the required number of patches."""
        self.patches = []
        self.world = world

        for y in range(0, MAP_HEIGHT):
            for x in range(0, MAP_WIDTH):
                self.patches.append(Patch(x, y))

    def get_neighbours(self, patch: Patch) -> [Patch]:
        """Ignore the patch to be compared."""
        return list(filter(lambda p: p != patch and p.is_neighbour_with(patch), self.patches))

    def get_random_unoccupied_patch(self , patch: Patch = None) -> Union[Patch, None]:
        """
        Get an random, unoccupied patch.
        It will be a neighbour patch if the current patch is specified.
        If there is no patch available, return None.
        """

        patches = self.get_neighbours(patch) if patch is not None else self.patches
        unoccupied_patches = list(filter(lambda p: not p.is_occupied(), patches))

        if len(unoccupied_patches) == 0:
            return None

        return choice(unoccupied_patches)

    def filter_neighbour_turtles(
            self,
            patch: Patch,
            turtle_filter: Optional[Callable[[Union[Cop, Agent]], bool]]
    ):
        """Get the filtered list of neighbour turtle based on the filter function."""
        neighbour_patches = self.get_neighbours(patch)
        all_turtles = []

        # For each neighbour patch, find all matching turtles and add to the final list
        for patch in neighbour_patches:
            turtles = list(filter(turtle_filter, patch.turtles))
            all_turtles += turtles

        return all_turtles

    def update(self):
        # Dont do anything for now
        pass

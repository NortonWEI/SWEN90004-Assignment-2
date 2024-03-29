import csv
from math import sqrt, exp, floor
from random import shuffle, choice, uniform, randint
from typing import List, Optional, Union, Callable

from dynamic_params import DynamicParamReader, DYNAMIC_PARAMETERS, MAX_JAILED_TERM, \
    GOVERNMENT_LEGITIMACY, MOVEMENT, REBELLION_THRESHOLD
from static_params import total_cops, total_agents, VISION, MAP_WIDTH, MAP_HEIGHT, K, \
    THRESHOLD, MIN_DANGEROUS_PERCEIVED_HARDSHIP


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
            header_columns = ['frame', 'quiet', 'jailed', 'active', 'killed', 'is_reported']

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

        #Extension : Indicates the number of quiet agent who survived
        quiet_alive = list(filter(lambda t: t.alive, quiet))

        #Extension : Indicates the number of quiet agent who were killed by dangerous rebel agent
        killed = list(filter(lambda t: not t.alive, agents))

        # Extension : If the ratio of active rebels with total agents (exclude jailed)
        # exceeds the rebellion threshold,
        # it would be reported as true. This state is used as a reference for the Government
        # and Cops that critical rebellion situation occurs
        # No changing behaviour on the model
        is_reported = False
        if len(active)/(len(active) + len(quiet_alive)) > \
                self.get_dynamic_param(REBELLION_THRESHOLD[0]):
            is_reported = True 

        # Append current state to the output csv
        with open(self.output_filename, 'a') as output_file:
            csv_writer = csv.writer(output_file)
            columns = [frame, len(quiet_alive), len(jailed), len(active),
                       len(killed), str(is_reported)]

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
        """Determines whether this turtle can move. By default it can always move."""
        return True

    def move_to_patch(self, new_patch: 'Patch') -> None:
        """Move to a specified patch."""

        if self.patch is not None:
            self.patch.remove_turtle(self)

        new_patch.add_turtle(self)
        self.patch = new_patch

    def move(self, first_time: bool = False) -> None:
        """Move to a random, unoccupied patch if it can move
        or they need to have an initial location)."""
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
        agents = PatchMap.filter_neighbour_turtles(
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

        # Extension : If the suspect is dangerous, the suspect will be jailed
        # in the whole simulation by assigning -1
        if suspect.is_dangerous_rebel():
            suspect.jail_term = -1
        else:
            if self.world.get_dynamic_param(MAX_JAILED_TERM[0]) == 0:
                suspect.jail_term = 0
            else:
                suspect.jail_term = randint(1, self.world.get_dynamic_param(MAX_JAILED_TERM[0]))


class Agent(Turtle):
    """
    Simulates an Agent object.
    """
    jail_term: int              # Remaining time length for jailing
    active: bool                # Indicates whether the turtle is open rebelling
    risk_aversion: float        # The degree of reluctance to take risks
    perceived_hardship: float   # Perceived hardship of rebelling
    alive: bool                 # Indicates whether the agent is alive
                                # or killed by the active-rebelling agent

    def __init__(self, world: World) -> None:
        """ Initialise the agent """
        super().__init__(world)
        self.jail_term = 0
        self.active = False
        self.risk_aversion = uniform(0, 1)
        self.perceived_hardship = uniform(0, 1)
        self.alive = True

    def update(self) -> None:
        """Determines whether to open rebel."""

        # Extension : only living agent could perform the actions
        if self.alive:
            super().update()

            # Only determine behaviour if it is not jailed
            if self.patch is not None and not self.is_jailed():
                self.determine_behaviour()
                # Extension : dangerous rebel agents could kill 1 quiet agent in the neighbourhood
                self.do_dismiss_agent()

            # Reduce jail term
            self.decrement_jail_term()

    def can_move(self) -> bool:
        """ If it is jailed or movement is manually disabled it cannot move """
        return super().can_move() and not self.is_jailed() and \
               self.world.get_dynamic_param(MOVEMENT[0]) is True

    def is_jailed(self) -> bool:
        """Determine whether this agent is currently jailed."""
        return hasattr(self, 'jail_term') and (self.jail_term > 0 or self.jail_term == -1)

    def is_quiet(self) -> bool:
        """Determine whether this patch is quiet (i.e. inactive & not jailed)."""
        return (not self.active) and (not self.is_jailed())

    def get_grievance(self) -> float:
        """Calculate and return the grievance of the agent."""

        # Extension : The perceive hardship of an agent could also
        # be affected by the other active agents'
        # perceived hardship in the neighbourhood as the active agent tend
        # to have bad influence to the other agents.
        # The updated grievance is updated by using the average value of the other active agents' 
        # perceived hardship in the neighbourhood

        average_perceived_hardship = 0
        surrounding_active_agents = self.world.patch_map.filter_neighbour_turtles(
                self.patch,
                lambda t: isinstance(t, Agent) and t.active
        )

        # Extension : Calculate the average of agents' perceived hardship in the neighbourhood
        total_perceived_hardships = 0
        total_active_agents = len(surrounding_active_agents)
       
        if total_active_agents > 0 :
            for agent in surrounding_active_agents:
                total_perceived_hardships += agent.perceived_hardship

            average_perceived_hardship = total_perceived_hardships / total_active_agents 
            return ((self.perceived_hardship + average_perceived_hardship)/2) * \
                   (1 - self.world.get_dynamic_param(GOVERNMENT_LEGITIMACY[0]))
       
        else:
            return self.perceived_hardship * \
                   (1 - self.world.get_dynamic_param(GOVERNMENT_LEGITIMACY[0]))

    def get_estimated_arrest_probability(self) -> float:
        """Calculate and return the estimated arrest probability of the agent
        (based on the formula)."""

        # c = number of neighbour cops
        c = len(PatchMap.filter_neighbour_turtles(self.patch, lambda t: isinstance(t, Cop)))

        # a = 1 + number of neighbour turtles which are active
        a = 1 + len(PatchMap.filter_neighbour_turtles(
            self.patch,
            lambda t: isinstance(t, Agent) and t.active
        ))

        return 1 - exp(-K * floor(c/a))

    def determine_behaviour(self) -> None:
        """Determine the behaviour of this agent by flagging its activeness."""
        self.active = (self.get_grievance() - self.risk_aversion *
                       self.get_estimated_arrest_probability()) > THRESHOLD

    def decrement_jail_term(self) -> None:
        """ Decrement the jail term by 1 if it is positive """
        if self.jail_term > 0:
            self.jail_term -= 1

    def is_dangerous_rebel(self) -> bool:
        return self.perceived_hardship > MIN_DANGEROUS_PERCEIVED_HARDSHIP

    def do_dismiss_agent(self) -> None:
        if self.active and self.is_dangerous_rebel():
            # Find all quiet agents in the neighbourhood
            agents = self.world.patch_map.filter_neighbour_turtles(
                 self.patch,
                lambda t: isinstance(t, Agent) and not t.active
            )
            # Don't continue if there is no matched agent
            if len(agents) == 0:
                return

            # Kill a quiet agent
            suspect = choice(agents)
            suspect.alive = False


class Patch:
    """
    Simulates a Patch (of a map).
    """
    x: int                              # x coordinate of this patch.
    y: int                              # y coordinate of this patch.
    turtles: List                       # All turtles in the patch.
    neighbour_patches: List['Patch']    # All neighbour patches within the vision.

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.turtles = []
        self.neighbour_patches = []

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

            # Jailed turtle considered as unoccupied
            if isinstance(turtle, Agent) and turtle.is_jailed():
                return False

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

        # Pre-calculate all neighbour patches
        for curr_patch in self.patches:
            for patch in self.patches:
                if patch == curr_patch:
                    continue
                if patch.is_neighbour_with(curr_patch):
                    curr_patch.neighbour_patches.append(patch)

    @staticmethod
    def get_neighbours(patch: Patch) -> [Patch]:
        """Ignore the patch to be compared."""
        return patch.neighbour_patches

    def get_random_unoccupied_patch(self, patch: Patch = None) -> Union[Patch, None]:
        """
        Get an random, unoccupied patch.
        It will be a neighbour patch if the current patch is specified.
        If there is no patch available, return None.
        """

        patches = PatchMap.get_neighbours(patch) if patch is not None else self.patches
        unoccupied_patches = list(filter(lambda p: not p.is_occupied(), patches))

        if len(unoccupied_patches) == 0:
            return None

        return choice(unoccupied_patches)

    @staticmethod
    def filter_neighbour_turtles(
        patch: Patch,
        turtle_filter: Optional[Callable[[Union[Cop, Agent]], bool]]
    ):
        """Get the filtered list of neighbour turtle based on the filter function."""
        neighbour_patches = PatchMap.get_neighbours(patch)
        all_turtles = []

        # For each neighbour patch, find all matching turtles and add to the final list
        for patch in neighbour_patches:
            turtles = list(filter(turtle_filter, patch.turtles))
            all_turtles += turtles

        return all_turtles

    def update(self):
        # Dont do anything for now
        pass

from time import sleep
from models import World

# Author: Dafu Ai


def main():
    """The entry point for simulation."""
    tick = 0
    world = World()

    while True:
        print("Frame #" + str(tick))
        world.update()

        sleep(1)
        tick += 1

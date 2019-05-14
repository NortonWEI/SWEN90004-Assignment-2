from time import sleep
from models import World

# Author: Dafu Ai
from static_params import MAX_FRAMES


def main():
    """The entry point for simulation."""
    frame = 1
    world = World(dynamic_params_filename='dynamic_params.json', output_filename='out.csv')

    while frame <= MAX_FRAMES:
        print("Frame #" + str(frame))
        world.update(frame)

        sleep(1)
        frame += 1


if __name__ == '__main__':
    main()

from time import sleep

from dynamic_params import DynamicParamReader, FRAME_INTERVAL
from models import World
from static_params import MAX_FRAMES

# Author: Dafu Ai


def main():
    """The entry point for simulation."""
    frame = 1

    # Read dynamic parameters from the specified file
    dynamic_params_filename = 'dynamic_params.json'
    param_reader = DynamicParamReader(dynamic_params_filename)

    # Initialise the world
    world = World(dynamic_params_reader=param_reader, output_filename='out.csv')

    while frame <= MAX_FRAMES:
        print("Frame #" + str(frame))
        world.update(frame)

        # Speed will depend on the frame interval, which can be set dynamically
        sleep(param_reader.read_params()[FRAME_INTERVAL[0]])
        frame += 1


if __name__ == '__main__':
    main()

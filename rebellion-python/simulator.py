from time import sleep

from dynamic_params import DynamicParamReader, FRAME_INTERVAL
from models import World

# Author: Dafu Ai
from static_params import MAX_FRAMES


def main():
    """The entry point for simulation."""
    frame = 1
    dynamic_params_filename = 'dynamic_params.json'
    param_reader = DynamicParamReader(dynamic_params_filename)

    world = World(dynamic_params_reader=param_reader, output_filename='out.csv')

    while frame <= MAX_FRAMES:
        print("Frame #" + str(frame))
        world.update(frame)

        sleep(param_reader.read_params()[FRAME_INTERVAL[0]])
        frame += 1


if __name__ == '__main__':
    main()

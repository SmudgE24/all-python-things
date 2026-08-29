import random

def grass_interaction(day, time, world):
    """
    Function to handle interactions with grass in the game.
    This function can be expanded to include various interactions such as grazing, harvesting, or other actions.
    """
    dirt_blocks = []

    for (x, y, z), block in world.items():

        if block == "dirt":
            dirt_blocks.append((x, y, z))

    grass_blocks = []

    for (x, y, z), block in world.items():

        if block == "grass":
            grass_blocks.append((x, y, z))
        
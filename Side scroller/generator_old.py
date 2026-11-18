import random
import os

# ==========================================
# SETTINGS - CHANGE THESE TO CUSTOMISE LEVEL
# ==========================================

LEVEL_LENGTH = 400       # Horizontal length of the level
HEIGHT_PER_ROUTE = 25    # Height of each individual cave
ROUTE_COUNT = 5          # Number of stacked cave routes

WIDTH = LEVEL_LENGTH
HEIGHT = HEIGHT_PER_ROUTE * ROUTE_COUNT

AIR = '.'
BLOCK = 'B'
LAVA = 'L'
ENEMY = 'N'
COIN = 'C'
CHEST = 'H'
START = 'S'
END = 'E'
VINE = 'P'


def generate_level_file(filename="random_level.txt"):

    # 1. Start with a solid rock matrix
    grid = [[BLOCK for _ in range(WIDTH)] for _ in range(HEIGHT)]

    # ==========================================
    # 2. GENERATE THE THREE INDIVIDUAL CAVE ROUTES
    # ==========================================

    for route in range(ROUTE_COUNT):

        # Calculate the vertical position of this route
        offset = route * HEIGHT_PER_ROUTE

        # Playable area within this route
        playable_top = offset + 5
        playable_bottom = offset + 14
        floor_y = offset + 18
        foundation_y = offset + 19

        # 3. Carve the main cavern
        for x in range(WIDTH):
            for y in range(playable_top, floor_y):
                grid[y][x] = AIR

            # Solid foundation
            grid[foundation_y][x] = BLOCK

        # 4. Generate lava pools
        pool_counter = 0
        in_pool = False

        for x in range(15, WIDTH - 15):

            if not in_pool:
                if random.random() < 0.45:
                    in_pool = True
                    pool_counter = random.randint(4, 9)

            if in_pool and pool_counter > 0:

                for y_lava in range(offset + 15, foundation_y):
                    grid[y_lava][x] = LAVA

                pool_counter -= 1

            else:
                in_pool = False

                for y_block in range(offset + 15, foundation_y):
                    grid[y_block][x] = BLOCK

        # 5. Generate hanging stalactites
        for x in range(12, WIDTH - 12):

            if random.random() < 0.15:

                stalactite_length = random.randint(1, 3)

                for l in range(stalactite_length):

                    y = playable_top + l

                    if y < playable_bottom:
                        grid[y][x] = BLOCK

        # 6. Generate hanging vines inside the caves
        for x in range(15, WIDTH - 15):

            if random.random() < 0.12:

                start_y = playable_top

                while (
                    start_y < offset + 11
                    and grid[start_y][x] == BLOCK
                ):
                    start_y += 1

                if grid[start_y][x] == AIR:

                    vine_length = random.randint(3, 5)

                    for v in range(vine_length):

                        current_y = start_y + v

                        if (
                            current_y < floor_y
                            and grid[current_y][x] == AIR
                        ):
                            grid[current_y][x] = VINE


        # 7. Generate jumping platforms

        # Seven possible heights for platforms
        platform_heights = []

        for y in range(offset + 9, offset + 16):
            platform_heights.append(y)

        last_platform_x = 12
        last_platform_y = offset + 13

        # Start with a larger gap between platforms
        next_platform_gap = random.randint(5, 7)

        for x in range(12, WIDTH - 12):

            # Leave more space between platforms
            force_spawn = (x - last_platform_x) >= next_platform_gap

            # Only allow heights that can reasonably be reached
            possible_heights = []

            for y in platform_heights:

                if abs(y - last_platform_y) <= 2:
                    possible_heights.append(y)

            # Try to spawn a platform
            for y in possible_heights:

                if (
                    grid[y][x] == AIR
                    and grid[y + 1][x] == AIR
                    and grid[y - 1][x] == AIR
                    and grid[y - 2][x] == AIR
                ):

                    if (
                        grid[y][x] != VINE
                        and grid[y - 1][x] != VINE
                    ):

                        if random.random() < 0.10 or force_spawn:

                            # Wider platforms give the player
                            # more room to land
                            width_span = random.randint(3, 5)

                            platform_placed = False

                            for w in range(width_span):

                                if x + w >= WIDTH - 12:
                                    break

                                if (
                                    grid[y][x + w] in [AIR, VINE]
                                    and grid[y - 1][x + w] in [AIR, VINE]
                                    and grid[y - 2][x + w] in [AIR, VINE]
                                ):

                                    grid[y][x + w] = BLOCK
                                    platform_placed = True

                                else:
                                    break

                            # Only update the position if
                            # we actually created a platform
                            if platform_placed:

                                last_platform_x = x + width_span
                                last_platform_y = y

                                # Vary the distance to the
                                # next platform
                                next_platform_gap = random.randint(5, 7)

                                break


        # 8. Generate enemies, coins and chests
        for y in range(playable_top, playable_bottom + 1):

            for x in range(12, WIDTH - 12):

                if (
                    grid[y + 1][x] == BLOCK
                    and grid[y][x] == AIR
                ):

                    if (
                        grid[y - 1][x] == AIR
                        and grid[y - 2][x] == AIR
                    ):

                        spawn_roll = random.random()

                        respective_probabilities = [0.04, 0.08, 0.02]# Coin, Enemy, Chest
                        real_probabilities = []
                        no = 0
                        for p in respective_probabilities:
                            no += p
                            real_probabilities.append(no)
                        if spawn_roll < real_probabilities[2]: 
                            grid[y][x] = CHEST

                        if spawn_roll < real_probabilities[1]:
                            grid[y][x] = ENEMY
                        
                        if spawn_roll < real_probabilities[0]:
                            grid[y][x] = COIN

        # 9. Create the left entrance runway
        # Each route connects to the shared entrance shaft
        for x in range(12):

            for y in range(playable_top, floor_y):
                grid[y][x] = AIR

            grid[floor_y][x] = BLOCK
            grid[foundation_y][x] = BLOCK

        # 10. Create the right runway
        # Each route has its own exit at the very end
        for x in range(WIDTH - 12, WIDTH):

            for y in range(playable_top, floor_y):
                grid[y][x] = AIR

            grid[floor_y][x] = BLOCK
            grid[foundation_y][x] = BLOCK

        # 11. Place an exit at the far-right end of each route
        grid[offset + 17][WIDTH - 1] = END

    # ==========================================
    # 12. CREATE ONE SHARED STARTING AREA
    # ==========================================

    # One starting point, in the first route
    grid[17][1] = START

    # ==========================================
    # 13. CONNECT ALL THREE ROUTES WITH VINES
    # ==========================================

    # Create a vertical shaft through the rock separating
    # the routes, allowing the player to choose a route.
    #
    # The shaft runs through the left entrance area.
    # It is separate from the main cave tunnels.

    shaft_x = 6

    for y in range(5, HEIGHT - 1):

        # Leave the starting tile alone
        if grid[y][shaft_x] != START:
            grid[y][shaft_x] = VINE
            grid[y][shaft_x - 1] = AIR
            grid[y][shaft_x + 1] = AIR

    # Ensure the entrance areas are open on every route
    for route in range(ROUTE_COUNT):

        offset = route * HEIGHT_PER_ROUTE

        for x in range(12):

            for y in range(offset + 5, offset + 18):
                if grid[y][x] != START:
                    grid[y][x] = AIR

    # Restore the vertical vines after clearing the entrances
    for y in range(5, HEIGHT - 1):

        if grid[y][shaft_x] != START:
            grid[y][shaft_x] = VINE

    # Restore the single starting point
    grid[35][0] = START
    grid[17][1] = AIR

    # ==========================================
    # 14. SAVE THE LEVEL
    # ==========================================

    # Make sure the output directory exists
    os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)

    with open(filename, "w") as file:

        for row in grid:
            file.write("".join(row) + "\n")

    print("Level generated successfully!")
    print(f"Length: {WIDTH} tiles")
    print(f"Height: {HEIGHT} tiles")
    print(f"Routes: {ROUTE_COUNT}")
    print(f"Starting points: 1")
    print(f"Exits: {ROUTE_COUNT}")
    print(f"Saved to: {filename}")
    print("Total tiles:", WIDTH * HEIGHT)


# ==========================================
# RUN THE GENERATOR
# ==========================================

def run(place):
    SCRIPT_DIR = (
        os.path.dirname(os.path.abspath(__file__))
        if os.path.dirname(os.path.abspath(__file__))
        else "."
    )

    OUTPUT_PATH = os.path.join(
        SCRIPT_DIR,
        "assets",
        "levels",
        f"{place}.txt"
    )

    generate_level_file(OUTPUT_PATH)

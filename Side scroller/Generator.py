"""
Steppefall level generator (zone based).

Main.py keeps calling:   Generator.run("level12", 12)
The second argument is the LEVEL NUMBER (Main already passes levelNo + 1),
and the generator works out the zone, size and difficulty from it.

Nothing runs on import any more. To test it on its own:
    python Generator.py            (writes a few samples to ./generated_test/)
"""
import os
import random
import re

# ==========================================
# TILES
# ==========================================
AIR = '.'
BLOCK = 'B'
LAVA = 'L'
WATER = 'W'
ENEMY = 'N'
COIN = 'C'
CHEST = 'H'
START = 'S'
END = 'E'
VINE = 'P'
SULFUR = 'M'
LAVA_DRIPPER = 'D'

# ==========================================
# SETTINGS - CHANGE THESE TO CUSTOMISE LEVELS
# ==========================================
ZONE_SIZE = 40            # levels per zone; the last level of a zone is the boss level
HEIGHT_PER_ROUTE = 25     # height of one cave route (keep at 25, the layout relies on it)
ROUTES_MIN = 5            # number of stacked routes, chosen randomly per level
ROUTES_MAX = 7
REWARD_MIN = 2            # how many routes end in treasure instead of an exit
REWARD_MAX = 4            # (there is always at least one exit route)
ENTRANCE_LEN = 12         # length of the flat runway at each end of a route
SHAFT_X = 6               # the vine shaft on the left that links all routes
POOL_MAX = 20             # longest lava/water pit, reached at the hardest difficulty
VINE_SPACING = 30         # a big climbing vine roughly every this many tiles

# One entry per zone. Levels past the last zone reuse the last entry.
#   water       : share of pools that are water instead of lava
#   sulfur      : (min, max) sulfur deposits per route
#   enemy       : base chance that a free floor tile holds an enemy spawn
ZONES = [
    {"name": "Ember Caves",   "water": 0.00, "sulfur": (1, 2), "enemy": 0.06},
    {"name": "Drowned Halls", "water": 0.50, "sulfur": (1, 2), "enemy": 0.07},
    {"name": "Sulfur Depths", "water": 0.15, "sulfur": (3, 5), "enemy": 0.08},
    {"name": "Khan's Road",   "water": 0.25, "sulfur": (2, 4), "enemy": 0.09},
    {"name": "Khan's Tomb",   "water": 0.10, "sulfur": (3, 5), "enemy": 0.10},
]


def zone_info(level_number):
    """Returns (zone_index, zone_dict, progress 0..1 inside the zone)."""
    level_number = max(1, int(level_number))
    zone_index = min((level_number - 1) // ZONE_SIZE, len(ZONES) - 1)
    in_zone = (level_number - 1) % ZONE_SIZE
    progress = in_zone / max(1, ZONE_SIZE - 1)
    return zone_index, ZONES[zone_index], progress


# ==========================================
# ROUTE BUILDING
# ==========================================

def carve_route(grid, route, width, rng, zone, diff, is_reward):
    offset = route * HEIGHT_PER_ROUTE
    top = offset + 5            # first air row
    playable_bottom = offset + 14
    floor_y = offset + 18
    foundation_y = offset + 19

    # 1. carve the cavern
    for x in range(width):
        for y in range(top, floor_y):
            grid[y][x] = AIR
        grid[foundation_y][x] = BLOCK

    # 2. liquid pits. The cave floor is never a free walk: solid stretches
    #    are short and a pit follows each one. Pits get longer with difficulty.
    d_frac = min(1.0, max(0.0, (diff - 1) / 42.0))
    max_len = int(round(8 + d_frac * (POOL_MAX - 8)))      # 8 .. POOL_MAX
    min_len = 6 + int(d_frac * 4)                          # 6 .. 10
    hop_max = 3 + int(round(d_frac))                       # biggest jump between footholds
    solid_lo = max(2, 5 - int(d_frac * 3))                 # solid stretch between pits
    solid_hi = max(4, 9 - int(d_frac * 4))
    x = 12
    end = width - 12
    first = True
    while x < end:
        solid = rng.randint(solid_lo, solid_hi)
        if first:
            solid = max(solid, 6)                          # breathing room after the entrance
            first = False
        solid = min(solid, end - x)
        for dx in range(solid):
            for y in range(offset + 15, foundation_y):
                grid[y][x + dx] = BLOCK
        x += solid
        length = min(rng.randint(min_len, max_len), end - x - 3)
        if length < 3:
            break
        liquid = WATER if rng.random() < zone["water"] else LAVA
        for dx in range(length):
            for y in range(offset + 15, foundation_y):
                grid[y][x + dx] = liquid
        # stepping islands: footholds floating over the liquid, never more
        # than hop_max tiles apart, so the pit is a parkour run, not a walk
        pos = 0
        while length - pos > hop_max:
            gap = rng.randint(2, hop_max)
            width_i = min(rng.randint(1, 2), length - (pos + gap))
            for dx in range(width_i):
                grid[offset + 15][x + pos + gap + dx] = BLOCK
            pos += gap + width_i
        x += length
    for xx in range(width):                                # fill any leftover floor
        if grid[offset + 15][xx] == AIR:
            for y in range(offset + 15, foundation_y):
                grid[y][xx] = BLOCK

    # 3. stalactites
    for x in range(12, width - 12):
        if rng.random() < 0.08 + diff * 0.003:
            length = rng.randint(1, min(5, 2 + int(diff // 10)))
            for l in range(length):
                y = top + l
                if y < playable_bottom:
                    grid[y][x] = BLOCK

    # 4. hanging vines
    for x in range(15, width - 15):
        if rng.random() < 0.10:
            start_y = top
            while start_y < offset + 11 and grid[start_y][x] == BLOCK:
                start_y += 1
            if grid[start_y][x] == AIR:
                for v in range(rng.randint(3, 5)):
                    cy = start_y + v
                    if cy < floor_y and grid[cy][x] == AIR:
                        grid[cy][x] = VINE

    # 5. jumping platforms
    last_platform_x = 12
    last_platform_y = offset + 13
    next_gap = rng.randint(5, 7)
    heights = list(range(offset + 9, offset + 16))
    for x in range(12, width - 12):
        force = (x - last_platform_x) >= next_gap
        for y in heights:
            if abs(y - last_platform_y) > 2:
                continue
            if (grid[y][x] == AIR and grid[y + 1][x] == AIR
                    and grid[y - 1][x] == AIR and grid[y - 2][x] == AIR):
                if rng.random() < 0.10 or force:
                    span = rng.randint(max(2, 3 - int(diff // 15)), 5)
                    placed = False
                    for w in range(span):
                        if x + w >= width - 12:
                            break
                        if (grid[y][x + w] in (AIR, VINE)
                                and grid[y - 1][x + w] in (AIR, VINE)
                                and grid[y - 2][x + w] in (AIR, VINE)):
                            grid[y][x + w] = BLOCK
                            placed = True
                        else:
                            break
                    if placed:
                        last_platform_x = x + span
                        last_platform_y = y
                        next_gap = rng.randint(5 + int(diff // 10), 7 + int(diff // 6))
                        break

    # 5b. big climbing vines from the ceiling down to the route floor, so a
    #     player who falls off the platforms can climb back up
    vx = 12 + rng.randint(12, 22)
    while vx < width - 14:
        col = None
        for off in range(0, 10):
            for c in (vx + off, vx - off):
                if 14 <= c < width - 14 and grid[offset + 15][c] == BLOCK and grid[offset + 16][c] == BLOCK:
                    col = c
                    break
            if col is not None:
                break
        if col is None:
            vx += 5
            continue
        for y in range(top, offset + 15):                  # rows 5..14 of the route
            grid[y][col] = VINE
        vx = col + VINE_SPACING + rng.randint(-4, 4)

    # 6. enemies, coins and (a few) chests along the route
    enemy_chance = zone["enemy"] + diff * 0.002 + (0.03 if is_reward else 0.0)
    coin_chance = 0.04
    chest_chance = 0.010
    for y in range(top, playable_bottom + 1):
        for x in range(12, width - 12):
            if (grid[y + 1][x] == BLOCK and grid[y][x] == AIR
                    and grid[y - 1][x] == AIR and grid[y - 2][x] == AIR):
                roll = rng.random()
                if roll < enemy_chance:
                    grid[y][x] = ENEMY
                elif roll < enemy_chance + coin_chance:
                    grid[y][x] = COIN
                elif roll < enemy_chance + coin_chance + chest_chance:
                    grid[y][x] = CHEST

    # 7. entrance and end runways (flat, 3 tiles below the cave floor)
    for x in list(range(ENTRANCE_LEN)) + list(range(width - ENTRANCE_LEN, width)):
        for y in range(top, floor_y):
            grid[y][x] = AIR
        grid[floor_y][x] = BLOCK
        grid[foundation_y][x] = BLOCK

    # 8. sulfur deposits
    candidates = []
    for sy in range(top, floor_y):
        for sx in range(ENTRANCE_LEN + 1, width - ENTRANCE_LEN - 1):
            if grid[sy][sx] == AIR and grid[sy + 1][sx] == BLOCK:
                near_lava = False
                for nx in range(max(0, sx - 3), min(width, sx + 4)):
                    for ny in range(offset + 15, offset + 19):
                        if grid[ny][nx] == LAVA:
                            near_lava = True
                            break
                    if near_lava:
                        break
                candidates.append((sx, sy, near_lava))
    rng.shuffle(candidates)
    candidates.sort(key=lambda c: c[2], reverse=True)
    wanted = rng.randint(*zone["sulfur"])
    placed = 0
    for sx, sy, _ in candidates:
        if placed >= wanted:
            break
        if any(grid[cy][cx] == SULFUR
               for cx in range(max(0, sx - 5), min(width, sx + 6))
               for cy in range(max(0, sy - 1), min(len(grid), sy + 2))):
            continue
        grid[sy][sx] = SULFUR
        placed += 1

    # 9. lava drippers in the ceiling
    ceiling_y = top - 1
    dx = rng.randint(15, 25)
    while dx < width - 15:
        if grid[ceiling_y][dx] == BLOCK and grid[ceiling_y + 1][dx] == AIR:
            grid[ceiling_y][dx] = LAVA_DRIPPER
        dx += rng.randint(12, 22)


def place_exit(grid, route, width):
    grid[route * HEIGHT_PER_ROUTE + 17][width - 1] = END


def place_reward(grid, route, width, kind, rng):
    """Treasure room on the end runway: chests, coins, or both."""
    stand = route * HEIGHT_PER_ROUTE + 17
    if kind == "chests":
        chest_count = rng.randint(2, 3)
    elif kind == "both":
        chest_count = rng.randint(1, 2)
    else:
        chest_count = 0

    chest_xs = [width - 3 - 3 * i for i in range(chest_count)]
    for cx in chest_xs:
        grid[stand][cx] = CHEST

    if kind in ("coins", "both"):
        for x in range(width - 11, width - 1):
            if grid[stand][x] == AIR:
                grid[stand][x] = COIN
        for x in range(width - 10, width - 2, 2):       # a little arc above
            if grid[stand - 2][x] == AIR:
                grid[stand - 2][x] = COIN
    elif kind == "chests":
        for x in range(width - 11, width - 1, 3):       # a few coins as a trail
            if grid[stand][x] == AIR:
                grid[stand][x] = COIN


# ==========================================
# WHOLE LEVEL
# ==========================================

def build_level(level_number, seed=None):
    """Returns (grid, info). grid is a list of lists of one-character tiles."""
    rng = random.Random(seed)
    zone_index, zone, progress = zone_info(level_number)
    diff = 1 + zone_index * 8 + progress * 10           # roughly 1 .. 43

    width = 100 + int(30 * progress) + 5 * zone_index   # 100 .. 150ish tiles
    n_routes = rng.randint(ROUTES_MIN, ROUTES_MAX)
    height = HEIGHT_PER_ROUTE * n_routes

    grid = [[BLOCK for _ in range(width)] for _ in range(height)]

    reward_count = rng.randint(REWARD_MIN, min(REWARD_MAX, n_routes - 1))
    reward_routes = sorted(rng.sample(range(n_routes), reward_count))
    reward_kind = {r: rng.choice(["chests", "coins", "both"]) for r in reward_routes}

    for route in range(n_routes):
        is_reward = route in reward_kind
        carve_route(grid, route, width, rng, zone, diff, is_reward)
        if is_reward:
            place_reward(grid, route, width, reward_kind[route], rng)
        else:
            place_exit(grid, route, width)

    # shared vine shaft linking every route
    for y in range(5, height - 1):
        grid[y][SHAFT_X - 1] = AIR
        grid[y][SHAFT_X + 1] = AIR
        grid[y][SHAFT_X] = VINE
    for route in range(n_routes):        # keep the entrances open
        offset = route * HEIGHT_PER_ROUTE
        for x in range(ENTRANCE_LEN):
            for y in range(offset + 5, offset + 18):
                if x not in (SHAFT_X - 1, SHAFT_X, SHAFT_X + 1):
                    grid[y][x] = AIR
    for y in range(5, height - 1):
        grid[y][SHAFT_X] = VINE

    # one start point, top route
    grid[17][1] = START

    info = {
        "level": level_number,
        "zone": zone["name"],
        "width": width,
        "height": height,
        "routes": n_routes,
        "exit_routes": [r for r in range(n_routes) if r not in reward_kind],
        "reward_routes": reward_kind,
    }
    return grid, info


def generate_level_file(filename, level_number, seed=None):
    grid, info = build_level(level_number, seed)
    os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)
    with open(filename, "w") as file:
        for row in grid:
            file.write("".join(row) + "\n")
    print(f"Level {info['level']} ({info['zone']}): {info['width']}x{info['height']}, "
          f"{info['routes']} routes, exits on {info['exit_routes']}, "
          f"treasure on {info['reward_routes']}")
    return info


def run(place, difficulty=1, force=False):
    """Called by Main.py as Generator.run('level12', 12).
    'difficulty' is the level number. Boss levels (every ZONE_SIZE) are
    hand-made, so an existing file for one is never overwritten."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "assets", "levels", f"{place}.txt")

    match = re.search(r"(\d+)$", str(place))
    level_number = int(match.group(1)) if match else int(difficulty)

    if level_number % ZONE_SIZE == 0 and os.path.exists(output_path) and not force:
        print(f"{place} is a boss level and already exists, leaving it alone.")
        return None
    return generate_level_file(output_path, level_number)


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    for n in (2, 15, 41, 85, 199):
        generate_level_file(os.path.join(here, "generated_test", f"level{n}.txt"), n, seed=n)

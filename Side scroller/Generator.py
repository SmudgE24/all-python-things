import random
import os

WIDTH = 400
HEIGHT = 20  # Matches your 20-row game world format

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
    # 1. Start with a solid subterranean rock matrix
    grid = [[BLOCK for _ in range(WIDTH)] for _ in range(HEIGHT)]
    
    # 2. Hard-carve a permanent, unbreakable player air zone (Rows 5 to 14)
    for x in range(WIDTH):
        for y in range(5, 15):
            grid[y][x] = AIR
        # Permanent solid bedrock foundation row at the absolute bottom
        grid[HEIGHT - 1][x] = BLOCK

    # 3. Create high-capacity lava pools embedded inside the floor columns (Rows 15 to 18)
    pool_counter = 0
    in_pool = False
    
    for x in range(15, WIDTH - 15):
        if not in_pool:
            if random.random() < 0.45:
                in_pool = True
                pool_counter = random.randint(4, 9)
                
        if in_pool and pool_counter > 0:
            # Place lava strictly inside rows 15 through 18 beneath the track line
            for y_lava in range(15, HEIGHT - 1):
                grid[y_lava][x] = LAVA
            pool_counter -= 1
        else:
            in_pool = False
            # Solid safety platform dividers to contain the fluid simulation pools
            for y_block in range(15, HEIGHT - 1):
                grid[y_block][x] = BLOCK

    # 4. Generate hanging stalactites from the upper cavern ceiling
    for x in range(12, WIDTH - 12):
        if random.random() < 0.15:
            stalactite_length = random.randint(1, 3)
            for l in range(stalactite_length):
                grid[5 + l][x] = BLOCK

    # 5. Generate Climbable Vines ('P') hanging cleanly down from the rock ceiling
    for x in range(15, WIDTH - 15):
        if random.random() < 0.12:
            start_y = 5
            while start_y < 11 and grid[start_y][x] == BLOCK:
                start_y += 1
            
            if grid[start_y][x] == AIR:
                vine_length = random.randint(3, 5)
                for v in range(vine_length):
                    current_y = start_y + v
                    if current_y < 15 and grid[current_y][x] == AIR:
                        grid[current_y][x] = VINE

    # 6. Generate mid-air jumping platforms with strict height controls
    # Max horizontal gap: 4 blocks | Max vertical jump: 3 blocks (2 rows of air between)
    last_platform_x = 12
    last_platform_y = 13  # Baseline platform height anchor matching player jump physics
    
    for x in range(12, WIDTH - 12):
        force_spawn = (x - last_platform_x) >= 4
        
        # Strict vertical clamping bounds so player can comfortably jump up
        min_y = max(11, last_platform_y - 2)  
        max_y = min(14, last_platform_y + 2) 
        
        for y in range(min_y, max_y + 1):
            if grid[y][x] == AIR and grid[y+1][x] == AIR and grid[y-1][x] == AIR:
                if grid[y][x] != VINE and grid[y-1][x] != VINE:
                    if random.random() < 0.14 or force_spawn:
                        if grid[y-1][x] == AIR and grid[y-2][x] == AIR:
                            width_span = random.randint(2, 4)
                            for w in range(width_span):
                                if x + w < WIDTH - 12 and grid[y][x+w] in [AIR, VINE]:
                                    if grid[y-1][x+w] in [AIR, VINE] and grid[y-2][x+w] in [AIR, VINE]:
                                        grid[y][x+w] = BLOCK
                            last_platform_x = x + width_span
                            last_platform_y = y  # Save height anchor
                            break

    # 7. Populate collectibles and enemies safely on top of structures
    for y in range(5, 14):
        for x in range(12, WIDTH - 12):
            if grid[y + 1][x] == BLOCK and grid[y][x] == AIR:
                if grid[y - 1][x] == AIR and grid[y - 2][x] == AIR:
                    spawn_roll = random.random()
                    if spawn_roll < 0.04:
                        grid[y][x] = COIN
                    elif spawn_roll < 0.06:
                        grid[y][x] = ENEMY
                    elif spawn_roll < 0.08:
                        grid[y][x] = CHEST

    # 8. Establish clean runways at the boundaries matching your exact layout formatting
    # Left Runway
    for x in range(12):
        for y in range(5, 19):
            grid[y][x] = AIR
        grid[18][x] = BLOCK  # Clean walking floor baseline for S
        grid[19][x] = BLOCK  # Solid foundation bottom
    grid[17][1] = START

    # Right Runway
    for x in range(WIDTH - 12, WIDTH):
        for y in range(5, 19):
            grid[y][x] = AIR
        grid[18][x] = BLOCK  # Clean walking floor baseline for E
        grid[19][x] = BLOCK
    grid[17][WIDTH - 4] = END

    # 9. Save map matrix output directly to destination file
    with open(filename, "w") as file:
        for row in grid:
            file.write("".join(row) + "\n")
            
    print(f"Success! Perfect 20-row passable cavern level saved to '{filename}'")

# Execute matching file paths safely
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__)) if os.path.dirname(os.path.abspath(__file__)) else "."
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "assets", "levels", "level1.txt")
generate_level_file(OUTPUT_PATH)

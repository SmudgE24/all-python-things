
import pygame

TILE = 40
SRC = 32
FRAMES = 8
TICKS_PER_FRAME = 5

SURFACE_EDGE = 16
CAP_TOP = 10
CAP_H = 16

# Precalculate possible lava heights
LAVA_HEIGHTS = [0] + [
    max(1, round(amount * TILE / 7))
    for amount in range(1, 8)
]

# Animation storage
_body = []
_cap = []


def load(path="assets/images/lava_spritesheet.png"):

    if _body:
        return

    sheet = pygame.image.load(path).convert_alpha()

    for frame in range(FRAMES):

        cap = sheet.subsurface(
            (frame * SRC, 0, SRC, SRC)
        )

        body = sheet.subsurface(
            (frame * SRC, SRC, SRC, SRC)
        )

        cap = pygame.transform.scale(cap, (TILE, TILE))
        body = pygame.transform.scale(body, (TILE, TILE))

        cap = cap.subsurface(
            (0, CAP_TOP, TILE, CAP_H)
        ).copy()

        _cap.append(cap)
        _body.append(body)


def get_frame(ticks):
    return (ticks // TICKS_PER_FRAME) % FRAMES


def draw_lava(surface, px, py, amount, lava_above, frame):

    h = TILE if lava_above else LAVA_HEIGHTS[amount]

    top = py + TILE - h

    body_top = top if lava_above or h <= 8 else top + 8
    body_h = py + TILE - body_top

    if body_h > 0:

        surface.blit(
            _body[frame],
            (px, body_top),
            (0, TILE - body_h, TILE, body_h)
        )

    if not lava_above:

        cap_y = top - (SURFACE_EDGE - CAP_TOP)

        clip = max(
            0,
            min(CAP_H, py + TILE - cap_y)
        )

        if clip > 0:
            surface.blit(
                _cap[frame],
                (px, cap_y),
                (0, 0, TILE, clip)
            )

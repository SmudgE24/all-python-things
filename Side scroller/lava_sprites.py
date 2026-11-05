import os
import pygame

TILE = 40          # game tile size in pixels
SRC = 32           # sprite size in the sheet
FRAMES = 8
TICKS_PER_FRAME = 5   # game runs at 40 fps -> 8 animation fps
SURFACE_EDGE = 16     # y of the lava edge inside a scaled surface tile (13/32 * 40)
CAP_TOP = 10          # first row of the surface tile used as the cap
CAP_H = 16            # rows used for the cap

_body = []
_cap = []


def load(path="assets/images/lava_spritesheet.png"):
    """Call once after pygame.display.set_mode()."""
    if _body:
        return
    sheet = pygame.image.load(path).convert_alpha()
    for f in range(FRAMES):
        for row, store in ((0, _cap), (1, _body)):
            tile = sheet.subsurface((f * SRC, row * SRC, SRC, SRC))
            tile = pygame.transform.scale(tile, (TILE, TILE))
            if row == 0:
                tile = tile.subsurface((0, CAP_TOP, TILE, CAP_H)).copy()
            store.append(tile)


def draw_lava(surface, px, py, amount, lava_above, ticks):
    """Draw one lava cell with its top-left corner at (px, py).
    amount is 1..7 (the number after 'L'), lava_above is True if the cell
    above also holds lava, so no surface edge is drawn."""
    f = (ticks // TICKS_PER_FRAME) % FRAMES
    h = TILE if lava_above else max(1, round(amount * TILE / 7))
    top = py + TILE - h
    body = _body[f]
    if lava_above or h <= 8:
        body_top = top
    else:
        body_top = top + 8
    body_h = py + TILE - body_top
    if body_h > 0:
        surface.blit(body, (px, body_top), (0, TILE - body_h, TILE, body_h))
    if not lava_above:
        cap = _cap[f]
        cap_y = top - (SURFACE_EDGE - CAP_TOP)
        clip = max(0, min(CAP_H, py + TILE - cap_y))
        surface.blit(cap, (px, cap_y), (0, 0, TILE, clip))

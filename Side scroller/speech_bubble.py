import pygame

SCALE = 2           # the bubble sprites are tiny pixel art, so draw them chunky
PAD = 8             # space between the bubble edge and the text
GAP = 4             # space between the tail tip and the top of the head

_cache = {}


def wrap_text(font, text, max_width):
    lines = []
    for paragraph in str(text).split("\\n"):
        line = ""
        for word in paragraph.split(" "):
            test = word if not line else line + " " + word
            if font.size(test)[0] <= max_width or not line:
                line = test
            else:
                lines.append(line)
                line = word
        lines.append(line)
    return lines


def _nine_slice(image, w, h):
    """Stretch the 24x24 bubble sprite (8px corners) to w x h."""
    key = (id(image), w, h)
    if key in _cache:
        return _cache[key]
    c = 8
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    xs = [(0, c, 0, c), (c, 8, c, w - 2 * c), (24 - c, c, w - c, c)]
    ys = [(0, c, 0, c), (c, 8, c, h - 2 * c), (24 - c, c, h - c, c)]
    for sx, sw, dx, dw in xs:
        for sy, sh, dy, dh in ys:
            if dw <= 0 or dh <= 0:
                continue
            piece = image.subsurface((sx, sy, sw, sh))
            surf.blit(pygame.transform.scale(piece, (dw, dh)), (dx, dy))
    _cache[key] = surf
    return surf


def draw_speech_bubble(surface, image_manager, font, text, head_x, head_top_y, max_width=220, color=(36, 20, 14)):
    """Draw `text` in a speech bubble whose tail points down at (head_x, head_top_y).
    head_x / head_top_y are screen coordinates: the centre of the top of the head."""
    bubble_img = image_manager.load("speech bubble")
    tail_img = image_manager.load("speech bubble tail")
    lines = wrap_text(font, text, max_width)
    line_h = font.get_linesize()
    text_w = max(font.size(line)[0] for line in lines)
    w = max(text_w + PAD * 2, 24 * SCALE)
    h = len(lines) * line_h + PAD * 2

    tail_w, tail_h = tail_img.get_width() * SCALE, tail_img.get_height() * SCALE
    x = head_x - w // 2
    x = max(4, min(x, surface.get_width() - w - 4))          # keep the bubble on screen
    y = head_top_y - GAP - tail_h - h + SCALE                 # +SCALE: the tail overlaps the bottom edge

    surface.blit(_nine_slice(bubble_img, w, h), (x, y))
    tail_x = max(x + 8, min(head_x - tail_w // 2, x + w - tail_w - 8))
    surface.blit(pygame.transform.scale(tail_img, (tail_w, tail_h)), (tail_x, y + h - SCALE))
    for i, line in enumerate(lines):
        surface.blit(font.render(line, True, color), (x + PAD, y + PAD + i * line_h))

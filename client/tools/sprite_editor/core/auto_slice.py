import pygame


def detect_slices(surface: pygame.Surface, rect):

    if isinstance(rect, tuple):
        rect = pygame.Rect(rect)

    width, height = surface.get_size()

    visited = set()
    slices = []

    for y in range(rect.top, rect.bottom):
        for x in range(rect.left, rect.right):

            if (x, y) in visited:
                continue

            if x < 0 or y < 0 or x >= width or y >= height:
                continue

            color = surface.get_at((x, y))

            if color.a == 0:
                continue

            stack = [(x, y)]

            min_x = x
            max_x = x
            min_y = y
            max_y = y

            while stack:

                px, py = stack.pop()

                if (px, py) in visited:
                    continue

                if px < rect.left or px >= rect.right:
                    continue

                if py < rect.top or py >= rect.bottom:
                    continue

                if px < 0 or py < 0 or px >= width or py >= height:
                    continue

                visited.add((px, py))

                color = surface.get_at((px, py))

                if color.a == 0:
                    continue

                min_x = min(min_x, px)
                max_x = max(max_x, px)

                min_y = min(min_y, py)
                max_y = max(max_y, py)

                stack.append((px + 1, py))
                stack.append((px - 1, py))
                stack.append((px, py + 1))
                stack.append((px, py - 1))

            w = max_x - min_x + 1
            h = max_y - min_y + 1

            # filtro de ruído
            if w * h < 64:
                continue

            slices.append(pygame.Rect(min_x, min_y, w, h))

    slices.sort(key=lambda r: (r.y, r.x))

    return slices
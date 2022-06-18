import pygame
import math
import time

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 300

SCREEN_SIZE_FACTOR = 1 / 300

MIN_RELATIVE_WIDTH = 0.0001
MAX_RELATIVE_WIDTH = 10

AMOUNT_STABILITY_CHECKS = 75

COLORS = [(255, 255, 255), (0, 255, 255), (255, 255, 0), (0, 0, 255)]

AMOUNT_FPS = 5

def get_stability(x, y):
    c = x + y * 1j

    z = 0 + 0j
    for i in range(AMOUNT_STABILITY_CHECKS):
        z = z * z + c
        if math.hypot(z.real - c.real, z.imag - c.imag) > 2:
            return i / AMOUNT_STABILITY_CHECKS

    return 1

def stability_to_color(stability):
    for i in range(len(COLORS)):
        slice_start = (len(COLORS) - i - 1) / len(COLORS)
        if stability >= slice_start:
            if i == 0:
                darkness = (stability - slice_start) * len(COLORS)
            else:
                darkness = (stability - slice_start) * len(COLORS) * 0.6
            color = COLORS[i]
            return tuple(map(lambda a: int(a * (1 - darkness)), color))
    assert 0

def draw_mandelbrot_set_in_range(screen, start_x, start_y, width, height):
    for y in range(SCREEN_HEIGHT):
        for x in range(SCREEN_WIDTH):
            # The higher the number the more stable
            stability = get_stability(start_x + x * SCREEN_SIZE_FACTOR * width, start_y + y * SCREEN_SIZE_FACTOR * height)
            color = stability_to_color(stability)
            screen.set_at((x, y), "#%.2x%.2x%.2x" % color)
    # Update screen
    pygame.display.flip()

def main():
    pygame.init()

    # sets screen and screen background color
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Mandelbrot simulation")
    running = True

    start_x = -2
    start_y = -2
    width = 4
    height = 4

    # Tells whether we are dragging the surface
    dragging = False
    # Stores the original screen when dragging a surface
    drag_screen_copy = None

    need_redraw = False

    draw_mandelbrot_set_in_range(screen, start_x, start_y, width, height)

    time_last_draw = time.time()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
            elif event.type == pygame.MOUSEWHEEL: # Zoom in
                mouse_x, mouse_y = pygame.mouse.get_pos()
                new_width = width * 1.5 ** -event.y
                new_height = height * 1.5 ** -event.y
                if MIN_RELATIVE_WIDTH < new_width < MAX_RELATIVE_WIDTH:
                    width = new_width
                    height = new_height
                    need_redraw = True
            elif event.type == pygame.MOUSEBUTTONUP: # End move
                if event.button == 1: # Right click
                    mouse_x, mouse_y = event.pos
                    dragging = False
                    start_x += (drag_start_x - mouse_x) * SCREEN_SIZE_FACTOR * width
                    start_y += (drag_start_y - mouse_y) * SCREEN_SIZE_FACTOR * height
                    need_redraw = True
                    drag_screen_copy = None # Deallocate the screen copy
            elif event.type == pygame.MOUSEBUTTONDOWN: # Start move
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    if not dragging:
                        dragging = True
                        drag_start_x = mouse_x
                        drag_start_y = mouse_y
                        drag_screen_copy = screen.copy()
        if dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            screen.fill(COLORS[-1])
            screen.blit(drag_screen_copy, (mouse_x - drag_start_x, mouse_y - drag_start_y))
            pygame.display.flip()

        if time.time() - time_last_draw > 1 / AMOUNT_FPS:
            if need_redraw:
                # Redraw
                screen.fill((0, 0, 0))
                pygame.display.flip()
                draw_mandelbrot_set_in_range(screen, start_x, start_y, width, height)
                # After drawing we don't need to draw anymore
                need_redraw = False
            time_last_draw = time.time()

if __name__ == "__main__":
    main()

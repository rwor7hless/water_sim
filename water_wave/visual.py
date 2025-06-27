import pygame
import sys
import numpy as np
from .core import WaveSimulation
from .config import WIDTH, HEIGHT, SCALE, MIN_DISPLAY, COLOR_RANGE

class WaveApp:
    """
    Класс для визуализации и управления симуляцией волн с помощью pygame.
    """
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Волновое взаимодействие")
        self.clock = pygame.time.Clock()
        self.sim = WaveSimulation()
        self.rain_mode = False

    def draw_wave(self):
        t = (self.sim.current - MIN_DISPLAY) / COLOR_RANGE
        t = np.clip(t, 0, 1)
        r = 0 * (1 - t) + 12 * t
        g = 17 * (1 - t) + 204 * t
        b = 51 * (1 - t) + 255 * t
        depth = np.exp(-0.9 * np.abs(self.sim.current))
        depth = np.clip(depth, 0, 1)
        r = (r * depth).astype(np.uint8)
        g = (g * depth).astype(np.uint8)
        b = (b * depth).astype(np.uint8)
        colors = np.stack([r, g, b], axis=-1)
        surf = pygame.surfarray.make_surface(colors)
        surf = pygame.transform.scale(surf, (WIDTH, HEIGHT))
        self.screen.blit(surf, (1, 1))

    def run(self):
        running = True
        while running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = e.pos
                    if e.button == 1:
                        self.sim.disturb(mx, my, negative=False)
                    elif e.button == 3:
                        self.sim.disturb(mx, my, negative=True)
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_SPACE:
                        self.sim.current.fill(0)
                        self.sim.previous.fill(0)
                    elif e.key == pygame.K_s:
                        self.rain_mode = True
                elif e.type == pygame.KEYUP:
                    if e.key == pygame.K_s:
                        self.rain_mode = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LSHIFT]:
                mx, my = pygame.mouse.get_pos()
                self.sim.disturb(mx, my, negative=False)
            elif keys[pygame.K_LCTRL]:
                mx, my = pygame.mouse.get_pos()
                self.sim.disturb(mx, my, negative=True)

            if self.rain_mode:
                self.sim.simulate_rain(count=1)
            self.sim.update()
            self.draw_wave()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
        sys.exit() 
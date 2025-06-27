import numpy as np
from .config import WIDTH, HEIGHT, SCALE, DAMPING, WAVE_SPEED, MAX_AMPLITUDE

cols, rows = WIDTH // SCALE, HEIGHT // SCALE

class WaveSimulation:
    """
    Класс для моделирования двумерных волн на сетке.
    """
    def __init__(self):
        self.cols = cols
        self.rows = rows
        self.current = np.zeros((self.cols, self.rows), np.float32)
        self.previous = np.zeros_like(self.current)
        self.next_state = np.zeros_like(self.current)

    def update(self):
        wave_term = (
            WAVE_SPEED
            * (
                self.current[:-2, 1:-1]
                + self.current[2:, 1:-1]
                + self.current[1:-1, :-2]
                + self.current[1:-1, 2:]
            )
            - 4 * WAVE_SPEED * self.current[1:-1, 1:-1]
        )
        interaction_term = np.abs(self.current[1:-1, 1:-1]) * wave_term * 0.1
        self.next_state[1:-1, 1:-1] = DAMPING * (
            2 * self.current[1:-1, 1:-1] - self.previous[1:-1, 1:-1] + wave_term - interaction_term
        )
        np.clip(self.next_state, -MAX_AMPLITUDE, MAX_AMPLITUDE, out=self.next_state)
        self.next_state[0, :] *= 0.8
        self.next_state[-1, :] *= 0.8
        self.next_state[:, 0] *= 0.8
        self.next_state[:, -1] *= 0.8
        self.previous, self.current, self.next_state = self.current, self.next_state, self.previous

    def disturb(self, x: int, y: int, negative: bool = False):
        gx, gy = int(x // SCALE), int(y // SCALE)
        sign = -1 if negative else 1
        if 1 <= gx < self.cols - 1 and 1 <= gy < self.rows - 1:
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    dist = np.sqrt(dx * dx + dy * dy)
                    if dist <= 2.5:
                        factor = np.exp(-dist)
                        self.current[gx + dx, gy + dy] += sign * factor * 0.5
            np.clip(self.current, -MAX_AMPLITUDE, MAX_AMPLITUDE, out=self.current)

    def simulate_rain(self, count: int = 10):
        import random
        for _ in range(count):
            gx = random.randint(2, self.cols - 3)
            gy = random.randint(2, self.rows - 3)
            self.disturb(gx * SCALE, gy * SCALE, negative=random.random() < 0.5) 
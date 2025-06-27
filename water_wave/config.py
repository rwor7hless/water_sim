"""
Конфигурация и параметры симуляции волн
"""

WIDTH: int = 1000
HEIGHT: int = 1000
SCALE: int = 5
DAMPING: float = 0.99
FORCE: float = 100.0
WAVE_SPEED: float = 0.3

MIN_DISPLAY: float = -3.0
MAX_DISPLAY: float = 3.0
COLOR_RANGE: float = MAX_DISPLAY - MIN_DISPLAY
MAX_AMPLITUDE: float = 5.0 
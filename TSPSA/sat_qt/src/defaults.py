from dataclasses import dataclass


@dataclass
class Defaults:

    DEFAULT_ITERATIONS_AMOUNT: int = 5000
    MAX_ITERATIONS: int = 100000
    MIN_ITERATIONS: int = 1

    DEFAULT_AMOUNT_OF_POINTS: int = 50
    MIN_AMOUNT_OF_POINTS: int = 3
    MAX_AMOUNT_OF_POINTS: int = 1000

    DEFAULT_INTERVAL_RIGHT_BOUND: float = -1000.0
    DEFAULT_INTERVAL_LEFT_BOUND: float = 1000.0
    MAX_INTERVAL_VALUE = 100000.0
    MIN_INTERVAL_VALUE = -100000.0

    TSP_ANIMATION_DELAY: float = 0.1
    MIN_TSP_ANIMATION_DELAY: float = 0.0
    MAX_TSP_ANIMATION_DELAY: float = 10.0

    COLORS: tuple = (
        'blue',
        'red',
        'green',
        'cyan',
        'magenta',
        'yellow',
        'black',
        'white'
    )

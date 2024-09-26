import math
from scipy import stats
import matplotlib.pyplot as plt

from .Stopwatch import Stopwatch


def probability_of_not_losing(n: int, cost: int) -> float: ...


if __name__ == "__main__":
    max_games = 100_000
    # |max_games|Elapsed Time|
    # |---|---|
    # |100_000|10 seconds|

    with Stopwatch() as sw:
        ...

    print(f"Elapsed: {sw.elapsed_time()}")
    input("Press Enter to close the plot...")

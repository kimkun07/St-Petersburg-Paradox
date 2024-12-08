import math
from decimal import Decimal, getcontext
import matplotlib.pyplot as plt

from .Stopwatch import Stopwatch


def probability_of_not_losing(n: int, cost: int) -> float:
    total_cost = n * cost

    # 1. Pre-caculate X_i ~ St
    X_i: dict[int, Decimal] = {2: Decimal(1) / Decimal(2)}
    winning = 4
    while winning < total_cost:
        X_i[winning] = Decimal(1) / Decimal(winning)
        winning *= 2
    X_i[total_cost] = Decimal(1) / Decimal(winning // 2)

    # 2. Iterate every trial to find Pr(X >= winning)
    X: list[Decimal] = [Decimal(0) for _ in range(total_cost + 1)]

    # First trial: use X_i
    for winning, pr in X_i.items():
        X[winning] = pr

    for _ in range(1, n):
        next_X = [Decimal(0) for _ in range(total_cost + 1)]
        for winning_prev in range(1, total_cost + 1):
            for winning, pr in X_i.items():
                winning_next = min(winning_prev + winning, total_cost)
                next_X[winning_next] = next_X[winning_next] + X[winning_prev] * pr
        X = next_X

    return float(X[total_cost])


def simulate(x_data: list[int], cost: int) -> list[float]:
    """Given x_data, return probability_data for plot

    Args:
        x_data: List of `n`s to simulate
        exponent: _description_
        cost: _description_

    Returns:
        _description_
    """
    # Simulate games
    probabilities: list[float] = []
    for game in x_data:
        probabilities.append(probability_of_not_losing(n=game, cost=cost))

    return probabilities


def show(title: str):
    plt.xlabel("Number of Games")
    plt.ylabel("Probability")
    plt.title(title)
    plt.legend()
    plt.xscale("log")
    plt.ylim(0, 1)
    plt.grid(True)
    plt.show(block=False)
    plt.pause(1)  # too short interval may cause blank plot window


def plot_different_costs(simulate_max_games: int) -> None:
    plt.figure()

    x_data = list(range(1, simulate_max_games, 100))
    for cost in [10]:
        y_data = simulate(x_data=x_data, cost=cost)
        plt.plot(x_data, y_data, marker="o", label=f"Cost={cost}")

    show(f"St. Petersburg Game")


def main():
    # Set Precision for Decimal
    getcontext().prec = 50

    max_games = 10_000
    # |max_games|Elapsed Time|
    # |---|---|
    # |100_000|10 seconds|

    with Stopwatch() as sw:
        plot_different_costs(max_games)

    print(f"Elapsed: {sw.elapsed_time()}")
    input("Press Enter to close the plot...")

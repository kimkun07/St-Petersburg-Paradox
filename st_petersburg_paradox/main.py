import math
from scipy import stats
import matplotlib.pyplot as plt

from .Stopwatch import Stopwatch


def probability_of_not_losing(n: int, p: float, payoff: float, cost: int) -> float:
    """Play a game `n` times with probability `p` of winning $`payoff`.
    Would you play the game with $`cost`?

    Args:
        n (int): Number of games to play.
        p (float): Probability of winning.
        payoff (int): Payoff if player wins.
        cost (int): Cost to play the game.

    Returns:
        float: Probability of not losing money.
    """

    total_cost = n * cost
    games_to_win = math.ceil(total_cost / payoff)

    # X ~ Bin(n=game, p=prob_win)
    # P(X >= games_to_win) = 1 - P(X < games_to_win)
    prob: float = 1 - stats.binom.cdf(games_to_win - 1, n, p)
    return prob


def simulate(x_data: list[int], exponent: int, cost: int) -> list[float]:
    # E[X] = p * payoff = 10
    p, payoff = (1 / 2) ** exponent, 10 * 2**exponent

    # Simulate games
    probabilities: list[float] = []
    for game in x_data:
        probabilities.append(
            probability_of_not_losing(n=game, p=p, payoff=payoff, cost=cost)
        )

    return probabilities


def plot_different_costs(exponent: int, simulate_max_games: int) -> None:
    x_data = list(range(1, simulate_max_games))
    for cost in [9, 10, 11]:
        y_data = simulate(x_data=x_data, exponent=exponent, cost=cost)
        plt.plot(x_data, y_data, marker="o", label=f"Cost: {cost}")

    plt.xlabel("Number of Games")
    plt.ylabel("Probability")
    plt.title(f"p: 1/2^{exponent}")
    plt.legend()
    plt.xscale("log")
    plt.ylim(0, 1)
    plt.grid(True)
    plt.show()


def plot_different_exponents(cost: int, simulate_max_games: int) -> None:
    x_data = list(range(1, simulate_max_games))
    for exponent in [2, 10, 20]:
        y_data = simulate(x_data=x_data, exponent=exponent, cost=cost)
        plt.plot(x_data, y_data, marker="o", label=f"p=1/2^{exponent}")

    plt.xlabel("Number of Games")
    plt.ylabel("Probability")
    plt.title(f"Cost: {cost}")
    plt.legend()
    plt.xscale("log")
    plt.ylim(0, 1)
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    max_games = 100_000
    # |max_games|Elapsed Time|
    # |---|---|
    # |100_000|7 seconds|
    with Stopwatch() as sw:
        plot_different_costs(exponent=2, simulate_max_games=max_games)
        plot_different_costs(exponent=10, simulate_max_games=max_games)
        plot_different_costs(exponent=20, simulate_max_games=max_games)

        plot_different_exponents(cost=9, simulate_max_games=max_games)
        plot_different_exponents(cost=10, simulate_max_games=max_games)
        plot_different_exponents(cost=11, simulate_max_games=max_games)

    print(f"Elapsed: {sw.elapsed_time()}")

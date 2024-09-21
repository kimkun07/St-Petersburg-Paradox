import math
from scipy import stats
import matplotlib.pyplot as plt


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


if __name__ == "__main__":
    # Simulate games
    games = [1, 10, 100, 1000, 10_000, 100_000]
    costs = [9, 10, 11]
    probabilities: dict[int, list[float]] = {cost: [] for cost in costs}

    for game in games:
        for cost in costs:
            probabilities[cost].append(
                probability_of_not_losing(n=game, p=1 / 4, payoff=40, cost=cost)
            )

    for cost in costs:
        plt.plot(games, probabilities[cost], marker="o", label=f"Cost: {cost}")

    plt.xlabel("Number of Games")
    plt.ylabel("Probability")
    plt.title("Probability vs Number of Games for Different Costs")
    plt.legend()
    plt.xscale("log")
    plt.grid(True)
    # plt.show()

    plt.savefig("p=0.25.png")

from __future__ import annotations
import math
from scipy import stats
from st_petersburg_paradox.game import Game


class SimpleGame(Game):
    payoff: int
    probability: float

    def __init__(self, payoff: int, probability: float):
        """_summary_

        Args:
            payoff: _description_
            probability: _description_
        """
        self.payoff = payoff
        self.probability = probability

    @staticmethod
    def from_expected_value(expected_value: int, exponent: int) -> SimpleGame:
        # E[X] = payoff * pr
        return SimpleGame(
            payoff=expected_value * (2**exponent), probability=(1 / 2) ** exponent
        )

    def __str__(self) -> str:
        return f"SimpleGame(payoff={self.payoff}, probability={self.probability})"

    def prob_profit_after_n_games(self, n_games: int, participation_cost: int):
        """_summary_

        Args:
            n_games: _description_
            participation_cost: _description_

        Returns:
            _description_
        """

        total_cost = n_games * participation_cost
        # Player should win `games_to_win` times for profit
        games_to_win = math.ceil(total_cost / self.payoff)

        # X ~ Bin(n=n_games, p=probability)
        # P(X >= games_to_win) = 1 - P(X < games_to_win)
        prob: float = 1 - stats.binom.cdf(games_to_win - 1, n_games, self.probability)
        return prob

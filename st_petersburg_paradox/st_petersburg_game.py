from decimal import Decimal
from st_petersburg_paradox.game import Game


class StPetersburgGame(Game):
    def __init__(self):
        pass

    def prob_profit_after_n_games(self, n_games: int, participation_cost: int) -> float:
        """
        n_games에 따른 profit probability를 계산한다

        Args:
            n_games (int): 게임 횟수
            participation_cost (int): 한 게임 참여 비용

        Returns:
            float: profit probability
        """
        total_cost = n_games * participation_cost

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

        for _ in range(1, n_games):
            next_X = [Decimal(0) for _ in range(total_cost + 1)]
            for winning_prev in range(1, total_cost + 1):
                for winning, pr in X_i.items():
                    winning_next = min(winning_prev + winning, total_cost)
                    next_X[winning_next] = next_X[winning_next] + X[winning_prev] * pr
            X = next_X

        return float(X[total_cost])

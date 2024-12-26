import decimal
from functools import reduce
from decimal import Decimal
from tqdm import tqdm
from st_petersburg_paradox.game import Game


class StPetersburgGame(Game):
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

        # NOTE: We divide all index by 2
        assert total_cost % 2 == 0
        end_index = total_cost // 2

        # 1. Pre-caculate X_i ~ St
        X_i: dict[int, Decimal] = {2 // 2: Decimal(1) / Decimal(2)}
        winning = 4
        while winning < total_cost:
            X_i[winning // 2] = Decimal(1) / Decimal(winning)
            winning *= 2
        X_i[end_index] = Decimal(1) / Decimal(winning // 2)

        # 2. Iterate every trial to find Pr(X >= winning)
        X: list[Decimal] = [Decimal(0) for _ in range(end_index + 1)]

        # First trial: use X_i
        for winning, pr in X_i.items():
            X[winning] = pr

        for _ in range(1, n_games):
            next_X = [Decimal(0) for _ in range(end_index + 1)]
            for winning_prev in range(1, end_index + 1):
                for winning, pr in X_i.items():
                    winning_next = min(winning_prev + winning, end_index)
                    next_X[winning_next] = next_X[winning_next] + X[winning_prev] * pr
            X = next_X

        return float(X[total_cost // 2])

    def batch_prob_profit_after_n_games(
        self, n_games: list[int], participation_cost: list[int]
    ) -> list[list[float]]:
        """_summary_

        Args:
            n_games: sorted list
            participation_cost: _description_

        Returns:
            result[cost][n_games] = profit probability
        """
        total_cost = max(n_games) * max(participation_cost)

        assert n_games == sorted(n_games)

        # NOTE: We divide all index by 2
        assert total_cost % 2 == 0
        end_index = total_cost // 2

        # Allocate all memories first
        print(f"Decimal precision set to: {decimal.getcontext().prec}")
        print("Try allocating memories... OutOfMemory might happen")
        S = [Decimal(0) for _ in range(end_index + 1)]
        next_S = [Decimal(0) for _ in range(end_index + 1)]
        result: list[list[float]] = [
            [0.0 for _ in range(len(n_games))] for _ in range(len(participation_cost))
        ]
        print("Allocating Finished")

        # 1. Pre-caculate X_i ~ St
        X_i: dict[int, Decimal] = {2 // 2: Decimal(1) / Decimal(2)}
        winning = 4
        while winning < total_cost:
            X_i[winning // 2] = Decimal(1) / Decimal(winning)
            winning *= 2
        X_i[end_index] = Decimal(1) / Decimal(winning // 2)

        # 2. Iterate every game to find Pr(X >= winning)
        # First game: use X_i
        for winning, pr in X_i.items():
            S[winning] = pr

        assert n_games[0] > 1
        current_n_index = 0

        for t in tqdm(range(2, max(n_games) + 1)):
            next_S = [Decimal(0) for _ in range(end_index + 1)]
            for winning_prev in range(1, end_index + 1):
                for winning, pr in X_i.items():
                    winning_next = min(winning_prev + winning, end_index)
                    next_S[winning_next] = next_S[winning_next] + S[winning_prev] * pr
            S = next_S

            # Get answer for prob_profit_after_n_games(t, cost)
            if t == n_games[current_n_index]:
                for cost_index, cost in enumerate(participation_cost):
                    local_total_cost = t * cost
                    # sums S[local_total_cost // 2] + ...
                    result[cost_index][current_n_index] = float(
                        reduce(
                            lambda u, v: u + v, S[local_total_cost // 2 :], Decimal(0)
                        )
                    )
                current_n_index = min(current_n_index + 1, len(n_games) - 1)

        return result

    def _show_profit_distribution(self, n_games: int = 5, participation_cost: int = 6):
        total_cost = n_games * participation_cost

        S = [Decimal(0) for _ in range(total_cost + 1)]
        next_S = [Decimal(0) for _ in range(total_cost + 1)]

        # 1. Pre-caculate X_i ~ St
        X_i: dict[int, Decimal] = {2: Decimal(1) / Decimal(2)}
        winning = 4
        while winning < total_cost:
            X_i[winning] = Decimal(1) / Decimal(winning)
            winning *= 2
        X_i[total_cost] = Decimal(1) / Decimal(winning // 2)

        from matplotlib import pyplot as plt

        plt.bar(list(X_i.keys()), [float(pr) for pr in X_i.values()])
        plt.xlabel("Winning")
        plt.xlim(left=2, right=total_cost)
        plt.ylabel("Probability")
        plt.ylim((0, 1))
        plt.title("Winning distribution of single trial")
        plt.show()

        # 2. Iterate every game to find Pr(X >= winning)
        # First game: use X_i
        for winning, pr in X_i.items():
            S[winning] = pr

        plt.subplot(n_games, 1, 1)
        plt.title("Distribution of S_i after i-th trial")
        plt.xlabel("Total Winning")
        plt.ylabel("Probability")
        plt.xlim(left=2, right=total_cost)
        plt.ylim((0, 1))
        plt.bar(range(total_cost + 1), [float(pr) for pr in S])

        for t in range(2, n_games + 1):
            next_S = [Decimal(0) for _ in range(total_cost + 1)]
            for winning_prev in range(1, total_cost + 1):
                for winning, pr in X_i.items():
                    winning_next = min(winning_prev + winning, total_cost)
                    next_S[winning_next] = next_S[winning_next] + S[winning_prev] * pr
            S = next_S

            # Plot histogram of S
            plt.subplot(n_games, 1, t)
            plt.xlabel("Total Winning")
            plt.ylabel("Probability")
            plt.xlim(left=2, right=total_cost)
            plt.ylim((0, 1))
            plt.bar(range(total_cost + 1), [float(pr) for pr in S])

        plt.show()

import pickle
import os
from decimal import Decimal
from st_petersburg_paradox.game import Game


# NOTE: layout of cache
# X_i:   0  A  A  0  ...  A  0  A  A
# S[1]:  A
# S[2]:  A
#
# S[n]:  A  A  A  A  ...  A  x  x  x


class StPetersburgGame(Game):
    def __init__(self):
        self.cache_file = "st_petersburg_cache.pkl"
        self.cache: list[list[Decimal]] = self.load_cache()

    def load_cache(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, "rb") as f:
                return pickle.load(f)
        return []

    def save_cache(self):
        with open(self.cache_file, "wb") as f:
            pickle.dump(self.cache, f)

    @property
    def cache_n(self) -> int:
        return len(self.cache) - 1

    @property
    def cache_X_i(self) -> list[Decimal]:
        return self.cache[0] if self.cache_n >= 0 else []

    def cache_read_S(self, n: int) -> list[Decimal]:
        return self.cache[n] if self.cache_n >= n else []

    def cache_update_S(self, n: int, S: list[Decimal]):
        # NOTE: Assume len(S) > self.cache_read_S(n)
        if n > self.cache_n:
            #  We Assume cache[n-1] is there
            self.cache.append([])
        self.cache[n] = S.copy()

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
        X_i: dict[int, Decimal] = {}
        if len(self.cache_X_i) >= (end_index + 1):
            cache_X_i = self.cache_X_i.copy()
            for i in range(end_index + 1, len(self.cache_X_i)):
                cache_X_i[end_index] += self.cache_X_i[i]
            X_i.update(enumerate(cache_X_i[: end_index + 1]))
        else:
            # Let's caculate from start
            X_i: dict[int, Decimal] = {2 // 2: Decimal(1) / Decimal(2)}
            winning = 4
            while winning < total_cost:
                X_i[winning // 2] = Decimal(1) / Decimal(winning)
                winning *= 2
            X_i[end_index] = Decimal(1) / Decimal(winning // 2)

            # Update cache_X_i
            if self.cache_n < 0:
                self.cache.append([])
            self.cache[0] = [X_i.get(i, Decimal(0)) for i in range(0, end_index + 1)]

        # 2. Iterate every trial to find Pr(X >= winning)
        S: list[Decimal] = [Decimal(0) for _ in range(end_index + 1)]

        # First trial: use X_i
        for winning, pr in X_i.items():
            S[winning] = pr
        self.cache_update_S(1, S)

        for t in range(2, n_games + 1):
            # cached_S_t = self.cache_read_S(t)
            if False:
                ...
            else:
                next_X = [Decimal(0) for _ in range(end_index + 1)]
                for winning_prev in range(1, end_index + 1):
                    for winning, pr in X_i.items():
                        winning_next = min(winning_prev + winning, end_index)
                        next_X[winning_next] = (
                            next_X[winning_next] + S[winning_prev] * pr
                        )
                S = next_X

            # self.cache_update_S(t, S)

        result = float(S[total_cost // 2])
        return result

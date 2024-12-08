import abc


class Game(abc.ABC):
    @abc.abstractmethod
    def prob_profit_after_n_games(
        self, n_games: int, participation_cost: int
    ) -> float: ...

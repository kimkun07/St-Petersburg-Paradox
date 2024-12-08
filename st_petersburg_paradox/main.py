from typing import Callable
from matplotlib import pyplot as plt
from st_petersburg_paradox.game import Game
from st_petersburg_paradox.simple_game import SimpleGame

from st_petersburg_paradox.utils_input import input_int_with_commas
from st_petersburg_paradox.utils_plt import show_plot
from st_petersburg_paradox.utils_pyinquirer import prompt_input, prompt_list


class DataGenerator:
    n_games_list: list[int]  # 그래프의 x축

    def __init__(self, max_n_games: int = 100_000, scale: int = 2):
        """확률 데이터를 생성하기 위한 Helper

        Args:
            max_n_games (int): 한 게임을 반복 시행할 횟수
            scale (int): 게임 횟수를 생성할 때 사용할 스케일 팩터
        """
        self.n_games_list = self.generate_n_games_list(max_n_games, scale)

    @staticmethod
    def generate_n_games_list(max_n_games: int, scale: int = 2) -> list[int]:
        """
        주어진 스케일 팩터를 사용하여 게임 횟수 목록을 생성합니다.

        Args:
            max_n_games (int): 게임의 최대 횟수.
            scale (int): 게임 횟수를 생성할 때 사용할 스케일 팩터.

        Returns:
            list[int]: 게임 횟수 목록.
        """
        n_games_list: list[int] = []
        n_games = 1
        while n_games <= max_n_games:
            n_games_list.append(n_games)
            n_games *= scale
        return n_games_list

    def generate_prob_list(self, game: Game, participation_cost: int) -> list[float]:
        """n_games에 따른 pr of profit 계산

        point[i] = (n_games[i], pr[i]) 가 될 것이다

        Args:
            participation_cost (int): 한 게임에 참여 비용 (n_games 반복 시행하므로, 전체로는 n_games * participation_cost만큼 지불)
        """
        return [
            game.prob_profit_after_n_games(n_games, participation_cost)
            for n_games in self.n_games_list
        ]


class ExperimentAssistant:
    SIMPLE_GAME = "SimpleGame"
    ST_GAME = "St Petersburg Game"
    COST_EXP = "Same probability, different costs"
    PR_EXP = "Same cost, different probability"

    @classmethod
    def choose_experiment(cls):
        game_choice = prompt_list(
            message="Select the game type:", choices=[cls.SIMPLE_GAME, cls.ST_GAME]
        )

        if game_choice == cls.SIMPLE_GAME:
            experiment_choice = prompt_list(
                message="Experiment for: ",
                choices=[cls.COST_EXP, cls.PR_EXP],
            )

            if experiment_choice == cls.COST_EXP:
                launch = cls.simple_game_cost_exp()
                return launch
            else:
                launch = cls.simple_game_exponent_exp()
                return launch
        else:
            game = StPetersburgGame()

    @classmethod
    def simple_game_cost_exp(cls) -> Callable[[int], None]:
        expected_value = int(prompt_input("Set expected value to: ", default="10"))
        cost_str = prompt_input(
            "Cost experiments delimitered by space: ", default="9 10 11"
        )
        participation_cost_list = list(map(int, cost_str.split()))
        exponent = int(
            prompt_input(
                "Set exponent to (probability will be 1/2^exponent): ",
                default="4",
            )
        )

        game = SimpleGame.from_expected_value(expected_value, exponent=exponent)

        def launch(max_n_games: int):
            dg = DataGenerator(max_n_games=max_n_games)

            return Experiment.experiment_for_different_cost(
                dg, game, participation_cost_list
            )

        return launch

    @classmethod
    def simple_game_exponent_exp(cls) -> Callable[[int], None]:
        expected_value = int(prompt_input("Set expected value to: ", default="10"))
        participation_cost = int(
            prompt_input("Set participation cost to: ", default="10")
        )
        cost_str = prompt_input(
            "Exponent experiments delimitered by space: ", default="4 10 16"
        )
        exponent_list = list(map(int, cost_str.split()))

        def launch(max_n_games: int):
            dg = DataGenerator(max_n_games=max_n_games)

            return Experiment.experiment_for_different_exponent(
                dg, exponent_list, expected_value, participation_cost
            )

        return launch


class Experiment:
    @staticmethod
    def experiment_for_different_cost(
        dg: DataGenerator, game: Game, participation_cost_list: list[int]
    ):
        for cost in participation_cost_list:
            prob_list = dg.generate_prob_list(game, cost)
            plt.plot(dg.n_games_list, prob_list, marker="o", label=f"Cost={cost}")

    @staticmethod
    def experiment_for_different_exponent(
        dg: DataGenerator,
        exponent_list: list[int],
        expected_value: int = 10,
        participation_cost: int = 10,
    ):
        # SimpleGame 만 해당된다.
        for exponent in exponent_list:
            game = SimpleGame.from_expected_value(expected_value, exponent=exponent)
            prob_list = dg.generate_prob_list(
                game, participation_cost=participation_cost
            )
            plt.plot(dg.n_games_list, prob_list, marker="o", label=f"Pr=1/2^{exponent}")


if __name__ == "__main__":
    max_n_games = input_int_with_commas("Enter max_n_games: ", default=1_000_000)
    max_n_games = int(prompt_input("Selected max_n_games: ", str(max_n_games)))

    plt.figure()
    start_experiment: Callable[[int], None] = ExperimentAssistant.choose_experiment()
    start_experiment(max_n_games)
    show_plot("Game Experiment")

    input("Press Enter to close the plot...")

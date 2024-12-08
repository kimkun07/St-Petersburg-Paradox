from matplotlib import pyplot as plt


def show_plot(title: str, pop_one_figure: bool = False):
    """Util for pyplot"""
    plt.xlabel("n_games")
    plt.ylabel("Pr of profit")
    plt.title(title)
    plt.legend()
    plt.xscale("log")
    plt.ylim(0, 1)
    plt.grid(True)

    if pop_one_figure:
        # Show one figure, and continue to calculate
        plt.show(block=False)
        plt.pause(1)  # too short interval may cause blank plot window
    else:
        plt.show()

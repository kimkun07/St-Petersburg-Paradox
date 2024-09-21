from scipy import stats


def st_petersburg_paradox(n: int) -> float:
    # Generate n random samples of the game
    samples = stats.geom.rvs(size=n, p=0.5)
    # Calculate the payoff for each sample
    payoffs = 2**samples
    # Calculate the expected payoff
    expected_payoff = payoffs.mean()
    return expected_payoff


if __name__ == "__main__":
    n = 100000
    expected_payoff = st_petersburg_paradox(n)
    print(f"Expected payoff for {n} samples: {expected_payoff}")

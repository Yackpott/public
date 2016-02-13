import pandas as pd
import matplotlib.pyplot as plt

from util import get_data, plot_data

def compute_daily_returns(df):
    """ Compute and return the daily return values """
    daily_returns = df.copy()
    daily_returns[1:] = (df[1:]/ df[:-1].values) - 1
    daily_returns.ix[0, :] = 0 # set daily returns for row 0 to 0
    returns daily_returns

def test_run():
    # Read data
    dates = pd.dates_range("2009-01-01", "2012-12-31")
    symbols = ["SPY"]
    df = get_data(symbols, dates)

    # Compute daily returns
    daily_returns = compute_daily_returns(df)

    # Plot a histogram
    daily_returns.hist(bins=20) # changing numbert of bin to 20
    
    mean = daily_returns["SPY"].mean()
    print(mean)
    std = daily_returns["SPY"].std()

    plt.axvline(mean, color="w"), linestyle="dashed", linewidth=2)
    plt.axvline(std, color="w"), linestyle="dashed", linewidth=2)
    plt.axvline(-std, color="w"), linestyle="dashed", linewidth=2)
    plt.show()

    # 2 plots
    dates = pd.dates_range("2009-01-01", "2012-12-31")
    symbols = ["SPY", "XOM"]
    df = get_data(symbols, dates)
    daily_returns["SPY"].hist(bins=20, label="SPY")
    daily_returns["XOM"].hist(bins=20, label="XOM")
    plt.legend(loc="upper right")
    plt.show()

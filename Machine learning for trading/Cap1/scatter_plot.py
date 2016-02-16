daily_returns.plot(kind="scatter", x="SPY", y="XOM")
beta_XOM, alpha_XOM = np.polyfit(daily_returns["SPY"], daily_returns["XOM"], 1)
plt.plot(daily_returns["SPY"], beta_XOM *
         dailyreturns["SPY"] + alpha_XOM, "-", color="r")
plt.show()
dailyreturns.plot(kind="scatter", x="SPY", y="GLD")
plt.show()
print(daily_returns.corr(method="pearson"))

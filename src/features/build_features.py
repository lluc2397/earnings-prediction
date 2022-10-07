import pandas as pd
import numpy as np
from pathlib import Path


ROOT_DIR = Path().resolve(strict=True)
DATA_DIR = f"{ROOT_DIR}/data"
RESCALE_VALUE = 100000000


def main():
    pd.options.mode.chained_assignment = None

    columns_to_skip = ["Name", "Stock Price"]
    df = pd.read_csv(
        f"{DATA_DIR}/interim/null_filled.csv",
        index_col=0,
        usecols=lambda x: x not in columns_to_skip,
    )
    df = df.sort_values(by=["Ticker", "Fiscal Year"], ascending=True)
    df = df.fillna(0)

    df.loc[df["Ticker"] == df["Ticker"].shift(periods=1), "capex"] = (
        df["Property, Plant & Equipment, Net"].shift(periods=1)
        - df["Property, Plant & Equipment, Net"]
        + df["Depreciation & Amortization"]
    )

    fcf = (
        df["Net Cash from Operating Activities"]
        - df["Net Cash from Financing Activities"]
    )
    df["fcf"] = fcf
    owners_earnings = (
        df["Net Income"]
        + df["Depreciation & Amortization"]
        + df["Change in Working Capital"]
        + df["Net Cash from Financing Activities"]
    )
    df["owners_earnings"] = owners_earnings

    df["roa"] = df["Net Income"] / df["Total Assets"]
    df["roe"] = df["Net Income"] / df["Total Equity"]
    df["roc"] = df["Operating Income (Loss)"] / df["Total Assets"]

    df["current_ratio"] = df["Total Current Assets"] / df["Total Current Liabilities"]
    df["quick_ratio"] = (
        df["Accounts & Notes Receivable"]
        + df["Cash, Cash Equivalents & Short Term Investments"]
    ) / df["Total Current Liabilities"]

    df["gross_margin"] = df["Gross Profit"] / df["Revenue"]
    df["net_income_margin"] = df["Net Income"] / df["Revenue"]
    df["owners_earnings_to_net_income"] = owners_earnings / df["Net Income"]
    df["rd_to_net_income"] = df["Research & Development"] / df["Net Income"]
    df["capex_to_net_income"] = df["capex"] / df["Net Income"]
    df["fcf_margin"] = fcf / df["Revenue"]

    df["net_income_growth_rate"] = df["Net Income"].pct_change()
    df["revenue_growth_rate"] = df["Net Income"].pct_change()
    df["capex_growth_rate"] = df["Net Income"].pct_change()

    resumed_df = df[
        [
            "Ticker",
            "Fiscal Year",
            "Revenue",
            "Cost of Revenue",
            "Net Income",
            "fcf",
            "owners_earnings",
            "roa",
            "roe",
            "roc",
            "current_ratio",
            "quick_ratio",
            "gross_margin",
            "net_income_margin",
            "fcf_margin",
            "owners_earnings_to_net_income",
            "rd_to_net_income",
            "capex_to_net_income",
            "net_income_growth_rate",
        ]
    ]

    resumed_df["Revenue"] = resumed_df["Revenue"] / RESCALE_VALUE
    resumed_df["Cost of Revenue"] = resumed_df["Cost of Revenue"] / RESCALE_VALUE
    resumed_df["Net Income"] = resumed_df["Net Income"] / RESCALE_VALUE
    resumed_df["fcf"] = resumed_df["fcf"] / RESCALE_VALUE
    resumed_df["owners_earnings"] = resumed_df["owners_earnings"] / RESCALE_VALUE

    resumed_df = resumed_df.round(2)
    resumed_df_dropped = resumed_df.dropna()
    resumed_df.replace([np.inf, -np.inf, np.nan], 0, inplace=True)
    resumed_df.to_csv(f"{DATA_DIR}/interim/new_features.csv")
    resumed_df_dropped.to_csv(f"{DATA_DIR}/interim/new_features_drops.csv")


if __name__ == "__main__":

    main()

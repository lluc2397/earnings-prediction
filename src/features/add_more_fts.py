import pandas as pd
import numpy as np

from ..constants import DATA_DIR, RESCALE_VALUE


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

    df["roce"] = (
        df["Operating Income (Loss)"] / df["Total Assets"]
        - df["Total Current Liabilities"]
    ) * 100
    df["rota"] = (df["Net Income"] / df["Property, Plant & Equipment, Net"]) * 100

    df["invested_capital"] = (
        df["Property, Plant & Equipment, Net"]
        + df["Total Current Assets"]
        - df["Total Current Liabilities"]
        - df["Cash, Cash Equivalents & Short Term Investments"]
    )
    df["roic"] = (
        (df["Net Income"] - df["Dividends Paid"]) / df["invested_capital"]
    ) * 100

    # df["current_ratio"] = df["Total Current Assets"] / df["Total Current Liabilities"]
    # df["quick_ratio"] = (
    #     df["Accounts & Notes Receivable"]
    #     + df["Cash, Cash Equivalents & Short Term Investments"]
    # ) / df["Total Current Liabilities"]

    df["gross_margin"] = df["Gross Profit"] / df["Revenue"]
    df["net_income_margin"] = df["Net Income"] / df["Revenue"]
    df["owners_earnings_to_net_income"] = owners_earnings / df["Net Income"]
    df["rd_to_net_income"] = df["Research & Development"] / df["Net Income"]
    df["capex_to_net_income"] = df["capex"] / df["Net Income"]
    df["fcf_margin"] = fcf / df["Revenue"]

    df["net_income_growth_rate"] = df["Net Income"].pct_change()
    df["revenue_growth_rate"] = df["Revenue"].pct_change()
    df["capex_growth_rate"] = df["capex"].pct_change()

    for field in [
        "Revenue",
        "Cost of Revenue",
        "Gross Profit",
        "Operating Expenses",
        "Selling, General & Administrative",
        "Research & Development",
        "Depreciation & Amortization",
        "Operating Income (Loss)",
        "Non-Operating Income (Loss)",
        "Interest Expense, Net",
        "Pretax Income (Loss), Adj.",
        "Abnormal Gains (Losses)",
        "Pretax Income (Loss)",
        "Income Tax (Expense) Benefit, Net",
        "Income (Loss) from Continuing Operations",
        "Net Extraordinary Gains (Losses)",
        "Net Income",
        "Net Income (Common)",
        "Cash, Cash Equivalents & Short Term Investments",
        "Accounts & Notes Receivable",
        "Inventories",
        "Total Current Assets",
        "Property, Plant & Equipment, Net",
        "Long Term Investments & Receivables",
        "Other Long Term Assets",
        "Total Noncurrent Assets",
        "Total Assets",
        "Payables & Accruals",
        "Short Term Debt",
        "Total Current Liabilities",
        "Long Term Debt",
        "Total Noncurrent Liabilities",
        "Total Liabilities",
        "Share Capital & Additional Paid-In Capital",
        "Treasury Stock",
        "Retained Earnings",
        "Total Equity",
        "Total Liabilities & Equity",
        "Net Income/Starting Line",
        "Depreciation & Amortization.1",
        "Non-Cash Items",
        "Change in Working Capital",
        "Change in Accounts Receivable",
        "Change in Inventories",
        "Change in Accounts Payable",
        "Change in Other",
        "Net Cash from Operating Activities",
        "Change in Fixed Assets & Intangibles",
        "Net Change in Long Term Investment",
        "Net Cash from Acquisitions & Divestitures",
        "Net Cash from Investing Activities",
        "Dividends Paid",
        "Cash from (Repayment of) Debt",
        "Cash from (Repurchase of) Equity",
        "Net Cash from Financing Activities",
        "Net Change in Cash",
        "invested_capital",
        "capex",
    ]:
        df[field] = df[field] / RESCALE_VALUE
    df = df.round(2)
    df.replace([np.inf, -np.inf, np.nan], 0, inplace=True)
    df.to_csv(f"{DATA_DIR}/interim/more_fts.csv")


if __name__ == "__main__":

    main()

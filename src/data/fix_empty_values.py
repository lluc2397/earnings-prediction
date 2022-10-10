import pandas as pd

from ..constants import DATA_DIR


def full_empty():
    df = pd.read_excel(f"{DATA_DIR}/raw/compsectorprice.xlsx", index_col=0)
    df["Sector"] = df["Sector"].fillna("Unknown")
    df = df.fillna(0)
    df.to_csv(f"{DATA_DIR}/interim/null_filled.csv")

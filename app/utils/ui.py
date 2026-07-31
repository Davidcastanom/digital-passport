import pandas as pd

def style_keys(df: pd.DataFrame, pk_cols: set, fk_cols: set) -> pd.DataFrame:
    if df.empty:
        return df
    rename = {}
    for col in df.columns:
        if col in pk_cols:
            rename[col] = f"\U0001f511 {col}"
        elif col in fk_cols:
            rename[col] = f"\U0001f517 {col}"
    return df.rename(columns=rename)

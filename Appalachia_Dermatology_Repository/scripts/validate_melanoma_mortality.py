"""Validate melanoma mortality association from the frozen county-level workbook.

This checks the published Pearson r and reports complete-case sample sizes.
The 99th percentile is computed over all counties' dermatologist densities;
if the original figure used a different percentile reference population,
confirm that choice before treating the figure as independently reproduced.
"""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import pearsonr

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "Appalachia_Master_Analysis_Dataset.xlsx"

def main():
    df = pd.read_excel(SOURCE, sheet_name="County_Level_Data")
    for col in ("derms_per_100k", "melanoma_mortality"):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    threshold = df["derms_per_100k"].quantile(0.99)
    complete = df.dropna(subset=["derms_per_100k", "melanoma_mortality"])
    filtered = complete.loc[complete["derms_per_100k"] <= threshold]
    print(f"Counties in workbook: {len(df)}")
    print(f"Mortality observed: {df['melanoma_mortality'].notna().sum()}")
    print(f"Complete cases: {len(complete)}")
    print(f"99th percentile density cutoff (all counties): {threshold:.8f}")
    print(f"Filtered complete cases: {len(filtered)}")
    if len(filtered) < 3:
        raise ValueError("Insufficient complete cases")
    r, p = pearsonr(filtered["derms_per_100k"], filtered["melanoma_mortality"])
    print(f"Filtered Pearson r={r:.6f}; p={p:.9g}")
    print("Published reference: r approximately -0.24, p < 0.001")
    if not (np.isclose(r, -0.237, atol=0.01) and p < 0.001):
        raise AssertionError("Mortality correlation does not match the reported reference")
    print("PASS: mortality correlation within documented tolerance")

if __name__ == "__main__":
    main()

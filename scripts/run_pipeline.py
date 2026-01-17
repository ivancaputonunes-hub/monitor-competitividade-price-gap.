"""
Run the pricing competitiveness pipeline using the package code.

Inputs (expected):
- data/raw/own_prices.csv
- data/raw/competitor_prices.csv

Outputs:
- data/processed/monitor_competitividade.parquet
- outputs/monitor_competitividade.csv

Run:
    python3 scripts/run_pipeline.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from price_gap_monitor.pipeline import build_monitor


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def main() -> None:
    root = _project_root()

    own_path = root / "data" / "raw" / "own_prices.csv"
    comp_path = root / "data" / "raw" / "competitor_prices.csv"

    processed_path = root / "data" / "processed" / "monitor_competitividade.parquet"
    output_csv = root / "outputs" / "monitor_competitividade.csv"

    processed_path.parent.mkdir(parents=True, exist_ok=True)
    output_csv.parent.mkdir(parents=True, exist_ok=True)

    df = build_monitor(own_path=own_path, competitor_path=comp_path)

    df.to_parquet(processed_path, index=False)
    df.to_csv(output_csv, index=False)

    print(f"✅ Wrote: {processed_path}")
    print(f"✅ Wrote: {output_csv}")
    print(f"Rows: {len(df):,} | Cols: {len(df.columns)}")


if __name__ == "__main__":
    main()
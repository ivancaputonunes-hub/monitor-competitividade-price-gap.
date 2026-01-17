"""
Generate anonymized sample datasets for the pricing competitiveness monitor.

Outputs:
- data/raw/own_prices.csv
- data/raw/competitor_prices.csv

Run:
    python3 scripts/generate_sample_data.py
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class SampleConfig:
    """Configuration for sample data generation."""

    seed: int = 42
    n_days: int = 14
    n_stores: int = 8
    n_skus: int = 30
    competitors: tuple[str, ...] = ("Conc_A", "Conc_B", "Conc_C")


def _project_root() -> Path:
    """Return project root assuming this file lives under scripts/."""
    return Path(__file__).resolve().parents[1]


def main(cfg: SampleConfig = SampleConfig()) -> None:
    """Generate sample CSV files under data/raw."""
    rng = np.random.default_rng(cfg.seed)

    root = _project_root()
    raw_dir = root / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    end = date.today()
    start = end - timedelta(days=cfg.n_days - 1)
    dates = [start + timedelta(days=i) for i in range(cfg.n_days)]

    stores = [f"S{str(i).zfill(3)}" for i in range(1, cfg.n_stores + 1)]
    skus = [f"SKU{str(i).zfill(4)}" for i in range(1, cfg.n_skus + 1)]

    # Simple metadata
    clusters = ["A", "B"]
    categories = ["Bebidas", "Snacks", "Higiene"]
    brands = ["Marca_X", "Marca_Y", "Marca_Z"]

    # Own prices
    own_rows: list[dict] = []
    for d in dates:
        for store in stores:
            for sku in skus:
                base = rng.uniform(3.0, 30.0)
                own_price = round(base * rng.uniform(0.95, 1.05), 2)
                own_rows.append(
                    {
                        "date": d.isoformat(),
                        "store_id": store,
                        "sku_id": sku,
                        "own_price": own_price,
                        "cluster": rng.choice(clusters),
                        "category": rng.choice(categories),
                        "brand": rng.choice(brands),
                    }
                )

    own_df = pd.DataFrame(own_rows)

    # Competitor prices (multiple observations per sku/store/day)
    comp_rows: list[dict] = []
    for d in dates:
        for store in stores:
            for sku in skus:
                # Market reference around own price but with noise
                own_price = float(
                    own_df.loc[
                        (own_df["date"] == d.isoformat())
                        & (own_df["store_id"] == store)
                        & (own_df["sku_id"] == sku),
                        "own_price",
                    ].iloc[0]
                )
                market_ref = own_price * rng.uniform(0.92, 1.08)

                for c in cfg.competitors:
                    comp_price = round(market_ref * rng.uniform(0.95, 1.05), 2)
                    comp_rows.append(
                        {
                            "date": d.isoformat(),
                            "store_id": store,
                            "sku_id": sku,
                            "competitor": c,
                            "comp_price": comp_price,
                        }
                    )

    comp_df = pd.DataFrame(comp_rows)

    own_path = raw_dir / "own_prices.csv"
    comp_path = raw_dir / "competitor_prices.csv"

    own_df.to_csv(own_path, index=False)
    comp_df.to_csv(comp_path, index=False)

    print(f"✅ Wrote: {own_path}")
    print(f"✅ Wrote: {comp_path}")
    print(f"Own rows: {len(own_df):,} | Competitor rows: {len(comp_df):,}")


if __name__ == "__main__":
    main()
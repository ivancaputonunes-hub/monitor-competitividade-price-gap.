from __future__ import annotations

from pathlib import Path

import pandas as pd

from price_gap_monitor.pipeline import build_monitor


def test_build_monitor_generates_expected_columns(tmp_path: Path) -> None:
    """
    Teste mínimo do pipeline:
    - cria dois CSVs pequenos (own e competitor)
    - roda build_monitor
    - valida colunas essenciais e quantidade de linhas
    """
    own_path = tmp_path / "own_prices.csv"
    comp_path = tmp_path / "competitor_prices.csv"

    own = pd.DataFrame(
        [
            {"date": "2026-01-01", "store_id": 1, "sku_id": 10, "own_price": 10.0},
            {"date": "2026-01-01", "store_id": 1, "sku_id": 20, "own_price": 20.0},
        ]
    )
    comp = pd.DataFrame(
        [
            {"date": "2026-01-01", "store_id": 1, "sku_id": 10, "comp_price": 9.0},
            {"date": "2026-01-01", "store_id": 1, "sku_id": 10, "comp_price": 11.0},
            {"date": "2026-01-01", "store_id": 1, "sku_id": 20, "comp_price": 19.0},
            {"date": "2026-01-01", "store_id": 1, "sku_id": 20, "comp_price": 21.0},
        ]
    )

    own.to_csv(own_path, index=False)
    comp.to_csv(comp_path, index=False)

    df = build_monitor(own_path=own_path, competitor_path=comp_path)

    # Deve ter 2 linhas (uma por SKU)
    assert len(df) == 2

    # Colunas mínimas esperadas
    required_cols = {
        "date",
        "store_id",
        "sku_id",
        "own_price",
        "comp_price_mean",
        "gap_abs_vs_mean",
        "gap_pct_vs_mean",
        "risk_label",
    }
    assert required_cols.issubset(set(df.columns))

    # Sanidade: gap do sku 10
    row_10 = df[df["sku_id"] == 10].iloc[0]
    assert row_10["comp_price_mean"] == 10.0
    assert row_10["gap_abs_vs_mean"] == 0.0
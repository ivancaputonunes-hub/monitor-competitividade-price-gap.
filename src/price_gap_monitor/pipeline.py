"""
Pipeline principal do Monitor de Competitividade e Price Gap.

Responsabilidade:
- Ler bases (own_prices e competitor_prices)
- Consolidar concorrência por (date, store_id, sku_id)
- Calcular métricas de competitividade (gap absoluto/percentual + dispersão)
- Classificar risco (labels simples)
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def _read_csv(path: Path) -> pd.DataFrame:
    """Read CSV with basic validation."""
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")
    return pd.read_csv(path)


def _aggregate_competitors(comp: pd.DataFrame) -> pd.DataFrame:
    """
    Aggrega concorrência para uma linha por date/store/sku.

    Retorna colunas:
    - comp_price_mean
    - comp_price_min
    - comp_price_max
    - comp_price_std
    - comp_n_obs
    """
    required = {"date", "store_id", "sku_id", "comp_price"}
    missing = required - set(comp.columns)
    if missing:
        raise ValueError(f"competitor_prices.csv sem colunas: {sorted(missing)}")

    agg = (
        comp.groupby(["date", "store_id", "sku_id"], as_index=False)
        .agg(
            comp_price_mean=("comp_price", "mean"),
            comp_price_min=("comp_price", "min"),
            comp_price_max=("comp_price", "max"),
            comp_price_std=("comp_price", "std"),
            comp_n_obs=("comp_price", "count"),
        )
        .copy()
    )
    # std pode virar NaN quando só tem 1 concorrente → troca por 0
    agg["comp_price_std"] = agg["comp_price_std"].fillna(0.0)
    return agg


def _risk_label(gap_pct_vs_mean: float, high: float = 0.05, low: float = -0.05) -> str:
    """
    Classifica risco com limiares simples.
    - high: acima do mercado (ex.: +5%)
    - low: abaixo do mercado (ex.: -5%)
    """
    if gap_pct_vs_mean >= high:
        return "ALTO_RISCO"
    if gap_pct_vs_mean <= low:
        return "ABAIXO_MERCADO"
    return "ALINHADO"


def build_monitor(own_path: Path, competitor_path: Path) -> pd.DataFrame:
    """
    Constrói a tabela final do monitor.

    Parameters
    ----------
    own_path:
        Caminho para data/raw/own_prices.csv
    competitor_path:
        Caminho para data/raw/competitor_prices.csv

    Returns
    -------
    pd.DataFrame
        Uma linha por (date, store_id, sku_id) com métricas e classificação.
    """
    own = _read_csv(own_path)
    comp = _read_csv(competitor_path)

    # validação mínima
    required_own = {"date", "store_id", "sku_id", "own_price"}
    missing_own = required_own - set(own.columns)
    if missing_own:
        raise ValueError(f"own_prices.csv sem colunas: {sorted(missing_own)}")

    comp_agg = _aggregate_competitors(comp)

    # join
    df = own.merge(comp_agg, on=["date", "store_id", "sku_id"], how="left")

    # métricas
    df["gap_abs_vs_mean"] = df["own_price"] - df["comp_price_mean"]
    df["gap_pct_vs_mean"] = np.where(
        df["comp_price_mean"] > 0,
        df["gap_abs_vs_mean"] / df["comp_price_mean"],
        np.nan,
    )

    # dispersão (simples): amplitude relativa e coef de variação
    df["comp_range"] = df["comp_price_max"] - df["comp_price_min"]
    df["comp_range_pct"] = np.where(
        df["comp_price_mean"] > 0, df["comp_range"] / df["comp_price_mean"], np.nan
    )
    df["comp_cv"] = np.where(
        df["comp_price_mean"] > 0, df["comp_price_std"] / df["comp_price_mean"], np.nan
    )

    # risco
    df["risk_label"] = df["gap_pct_vs_mean"].apply(lambda x: _risk_label(float(x)) if pd.notna(x) else "SEM_DADO")

    # ordenação de colunas (legível)
    preferred = [
        "date",
        "store_id",
        "sku_id",
        "cluster",
        "category",
        "brand",
        "own_price",
        "comp_price_mean",
        "comp_price_min",
        "comp_price_max",
        "comp_n_obs",
        "gap_abs_vs_mean",
        "gap_pct_vs_mean",
        "comp_range_pct",
        "comp_cv",
        "risk_label",
    ]
    cols = [c for c in preferred if c in df.columns] + [c for c in df.columns if c not in preferred]
    return df[cols].copy()
# Monitor de Competitividade e Price Gap

Projeto de **Pricing Analytics** para monitorar preços próprios vs. concorrentes, calcular **price gaps**, dispersões e classificar **risco competitivo**.

Este repositório foi estruturado para rodar localmente com **bases anônimas** (geradas via script) e para ser mantido por outras pessoas.

## O que você encontra aqui

- Pipeline em Python (Pandas) para:
  - consolidar preços próprios + concorrência
  - calcular métricas (gap, competitividade, dispersão)
  - classificar risco (acima/abaixo/alinhado)
  - exportar outputs em CSV e Parquet
- SQL opcional (DuckDB) para consolidação local
- Testes unitários (pytest)
- CI no GitHub Actions

## Pré-requisitos

- Python 3.11+ (recomendado)
- Git

## Setup rápido

```bash
# 1) ambiente virtual
python3 -m venv .venv
source .venv/bin/activate  # mac/linux

# 2) dependências
pip install -r requirements.txt
pip install -e .

# 3) gerar dados anônimos
python scripts/generate_sample_data.py

# 4) rodar pipeline
python scripts/run_pipeline.py
# 📊 Monitor de Competitividade e Price Gap

Sistema analítico para **monitoramento competitivo de preços**, identificação de **price gaps**, **dispersões** e **riscos competitivos**, com foco em decisões de pricing no varejo.

O projeto simula um cenário real de negócio, comparando preços próprios vs. concorrência e gerando métricas acionáveis para apoio à tomada de decisão.

---

## 🎯 Objetivo de Negócio

Apoiar decisões reais de pricing, reduzindo risco competitivo e priorizando ações com impacto financeiro.

Permite responder perguntas como:
- Estou acima ou abaixo do mercado?
- Onde o gap de preço é relevante?
- Quais itens estão em **alto risco competitivo**?
- O mercado está estável ou disperso?

---

## 📐 Arquitetura do Projeto

Arquitetura pensada para separar **orquestração**, **lógica de negócio** e **dados**, seguindo boas práticas de engenharia de dados.
```monitor-competitividade-price-gap/
├── data/
│   ├── raw/            # Dados de entrada (preços próprios e concorrência)
│   └── processed/      # Dados tratados (parquet)
├── outputs/            # Outputs finais (CSV para consumo de negócio)
├── scripts/            # Orquestração do pipeline
│   ├── generate_sample_data.py
│   └── run_pipeline.py
├── src/price_gap_monitor/
│   ├── pipeline.py     # Lógica principal de competitividade e pricing
│   ├── metrics.py      # Cálculo de métricas de gap e dispersão
│   ├── risk.py         # Classificação de risco competitivo
│   └── io.py           # Leitura e escrita de dados
├── tests/              # Testes unitários
├── pyproject.toml      # Configuração do pacote Python
└── README.md
```

**Por que essa arquitetura**
- Separação clara entre **orquestração** e **regras de negócio**
- Projeto instalável como **pacote Python**
- Facilita testes, manutenção e escala
- Padrão usado em ambientes profissionais de dados

---

## 🔄 Fluxo de Dados

1. Dados brutos entram em `data/raw`
2. Pipeline calcula métricas de competitividade e risco
3. Dados tratados são salvos em `data/processed` (parquet)
4. Output final é exportado em `outputs/monitor_competitividade.csv`

---

## ⚙️ Como Executar o Projeto

### 1️⃣ Criar e ativar ambiente virtual
```bash
python3 -m venv .venv
source .venv/bin/activate

```

## 📊 Evidências do Projeto (Outputs Reais)

Esta seção demonstra evidências reais de execução do pipeline e exemplos práticos de uso do output para tomada de decisão em pricing.








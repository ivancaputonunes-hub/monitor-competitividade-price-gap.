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

## Como executar o projeto

Este projeto simula um pipeline de análise de competitividade e price gap com foco em apoiar decisões de pricing e RGM.

### Pré-requisitos

- Python 3.11 ou superior
- Git

### Instalação

Clone o repositório e acesse a pasta do projeto:

```bash
git clone https://github.com/ivancaputonunes-hub/monitor-competitividade-price-gap-py.git
cd monitor-competitividade-price-gap-py

```
### Crie um ambiente virtual:
```bash
python -m venv .venv
```

### Ative o ambiente virtual:
```bash
# macOS / Linux
source .venv/bin/activate

# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
```

### Instale as dependências:

```bash
pip install -r requirements.txt
```

### Caso o projeto esteja configurado como pacote:

```bash
pip install -e .
```

---

### Execução rápida

Para rodar o pipeline principal e gerar os outputs:
```bash
python -m src.pipeline
```

Ao final da execução, os arquivos processados serão gerados nas pastas configuradas de saída (ex.: data/processed e/ou outputs).

### Caso o comando acima não funcione
Dependendo da estrutura, o entrypoint pode variar. Tente um dos comandos abaixo conforme o arquivo existente:
```bash
python src/pipeline.py
python src/main.py
python -m src
```
Se o projeto estiver configurado como CLI, consulte o arquivo pyproject.toml na seção project.scripts para identificar o comando correto.

---

### Testes

Para executar os testes automatizados:
```bash
pytest -q
```

---

## 📊 Exemplos de Outputs e Análises

Esta seção demonstra, na prática, os outputs gerados pelo pipeline e como eles suportam decisões reais de pricing e competitividade.

---

### 🧾 Output final do pipeline (CSV processado)

Arquivo gerado automaticamente pelo pipeline (`monitor_competitividade.csv`), contendo métricas de competitividade por SKU, loja e data.

Principais campos:
- `own_price`
- `comp_price_mean`
- `gap_pct_vs_mean`
- `risk_label`

Este arquivo é a base para análises exploratórias, dashboards e priorização de ações de pricing.

![CSV Output Monitor](assets/screenshots/01_csv_output_monitor.png)

---

### 📈 Distribuição de GAP percentual vs mercado (Pivot)

Análise agregada via tabela dinâmica, classificando SKUs conforme o **GAP percentual vs média da concorrência**:

- **Entre -5% e +5%** → Zona neutra / alinhado ao mercado  
- **Inferior a -5%** → Potencial perda de margem  
- **Superior a +5%** → Alto risco competitivo  

Essa visão permite:
- Identificar rapidamente exposição competitiva
- Priorizar revisões de preço com maior impacto
- Apoiar decisões táticas de pricing por categoria

![Distribuição de GAP Percentual](assets/screenshots/02_pivot_gap_distribution.png)

---







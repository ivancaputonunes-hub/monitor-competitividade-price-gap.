## Decisões de pricing que este monitor habilita

Este projeto foi desenhado para apoiar decisões reais de pricing no varejo, reduzindo risco competitivo e priorizando ações com impacto financeiro.

Ele permite responder perguntas como:
- **Estou acima ou abaixo do mercado?** (por SKU, loja e data)
- **Qual é o gap percentual vs. concorrência?** (comparável entre itens baratos e caros)
- **Quais itens estão em ALTO RISCO competitivo** (ex.: +5% vs média de mercado)
- **O mercado está estável ou disperso?** (via dispersão de preços da concorrência)

### Uso prático no dia a dia
Fluxo simples e efetivo:
1. Filtrar `risk_label = ALTO_RISCO`
2. Ordenar por `gap_pct_vs_mean` (desc)
3. Cruzar com volume e margem (quando disponíveis)
4. Priorizar ajustes de preço com maior impacto potencial

> Observação: o projeto roda com **dados anônimos** por padrão. Dados reais devem ser inseridos apenas em `data/raw/` e nunca versionados.

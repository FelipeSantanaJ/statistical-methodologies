# Statistical Methodologies

[Português](#português) · [English](#english)

Companheiro educativo do meu portfólio de dados
([github.com/FelipeSantanaJ](https://github.com/FelipeSantanaJ)) — explica, em três
níveis de profundidade e em dois idiomas, as metodologias estatísticas realmente
usadas nos projetos desse portfólio.

Companion piece to my data portfolio
([github.com/FelipeSantanaJ](https://github.com/FelipeSantanaJ)) — explains, at three
levels of depth and in two languages, the statistical methodologies actually used
across that portfolio's projects.

---

## Português

### Objetivo

Este repositório não introduz dados ou análises novas. Ele pega as metodologias
estatísticas já aplicadas nos meus projetos — de testes de significância a
decomposições de desigualdade, de desenho de experimentos a modelos de contagem —
e explica cada uma para dois públicos ao mesmo tempo:

- quem não tem formação estatística e quer entender a ideia por trás do método;
- quem trabalha com dados e quer ver o raciocínio, as suposições, a formulação
  matemática e as limitações por trás de cada técnica.

### Três níveis

| Nível | O que é | Público |
|---|---|---|
| **1 — Visão geral** | Um único documento cobrindo todas as 23 metodologias, sem fórmulas | Leigo em estatística |
| **2 — Metodologia por metodologia** | Um documento por método: intuição, exemplo simples, quando usar, cuidados | Alguém com alguma familiaridade com dados |
| **3 — Completo** | Formulação matemática, suposições, hipóteses, interpretação e limitações | Analistas, cientistas de dados, pesquisadores |

- [Nível 1 — Visão geral (PT)](docs/pt/simplificado/visao-geral.md)
- [Nível 1 — Overview (EN)](docs/en/simplified/overview.md)

Cada metodologia tem sua própria página em cada nível e idioma — ver tabela
completa abaixo.

### Metodologias cobertas

Agrupadas pelo tipo de pergunta que respondem no portfólio.

**Desigualdade e decomposição de diferenças entre grupos**

| Metodologia | Nível 2 | Nível 3 |
|---|---|---|
| Teste t de Welch | [PT](docs/pt/metodologias/welch-t-test.md) · [EN](docs/en/methodologies/welch-t-test.md) | [PT](docs/pt/completo/welch-t-test.md) · [EN](docs/en/complete/welch-t-test.md) |
| Decomposição de Oaxaca-Blinder | [PT](docs/pt/metodologias/oaxaca-blinder.md) · [EN](docs/en/methodologies/oaxaca-blinder.md) | [PT](docs/pt/completo/oaxaca-blinder.md) · [EN](docs/en/complete/oaxaca-blinder.md) |
| Decomposição por RIF | [PT](docs/pt/metodologias/rif-decomposition.md) · [EN](docs/en/methodologies/rif-decomposition.md) | [PT](docs/pt/completo/rif-decomposition.md) · [EN](docs/en/complete/rif-decomposition.md) |
| Decomposição de desigualdade (Theil, Gini, quantis) | [PT](docs/pt/metodologias/inequality-decomposition.md) · [EN](docs/en/methodologies/inequality-decomposition.md) | [PT](docs/pt/completo/inequality-decomposition.md) · [EN](docs/en/complete/inequality-decomposition.md) |
| Índice de dissimilaridade de Duncan | [PT](docs/pt/metodologias/duncan-index.md) · [EN](docs/en/methodologies/duncan-index.md) | [PT](docs/pt/completo/duncan-index.md) · [EN](docs/en/complete/duncan-index.md) |

**Séries temporais e inferência causal**

| Metodologia | Nível 2 | Nível 3 |
|---|---|---|
| Teste de quebra estrutural | [PT](docs/pt/metodologias/structural-break.md) · [EN](docs/en/methodologies/structural-break.md) | [PT](docs/pt/completo/structural-break.md) · [EN](docs/en/complete/structural-break.md) |
| Diferenças-em-diferenças | [PT](docs/pt/metodologias/diff-in-diff.md) · [EN](docs/en/methodologies/diff-in-diff.md) | [PT](docs/pt/completo/diff-in-diff.md) · [EN](docs/en/complete/diff-in-diff.md) |
| Transições em painel rotativo | [PT](docs/pt/metodologias/panel-transitions.md) · [EN](docs/en/methodologies/panel-transitions.md) | [PT](docs/pt/completo/panel-transitions.md) · [EN](docs/en/complete/panel-transitions.md) |

**Experimentação (testes A/B)**

| Metodologia | Nível 2 | Nível 3 |
|---|---|---|
| Fundamentos de teste A/B | [PT](docs/pt/metodologias/ab-testing.md) · [EN](docs/en/methodologies/ab-testing.md) | [PT](docs/pt/completo/ab-testing.md) · [EN](docs/en/complete/ab-testing.md) |
| Teste de Sample Ratio Mismatch | [PT](docs/pt/metodologias/srm-test.md) · [EN](docs/en/methodologies/srm-test.md) | [PT](docs/pt/completo/srm-test.md) · [EN](docs/en/complete/srm-test.md) |
| Balanceamento e ajuste por covariáveis | [PT](docs/pt/metodologias/covariate-balance.md) · [EN](docs/en/methodologies/covariate-balance.md) | [PT](docs/pt/completo/covariate-balance.md) · [EN](docs/en/complete/covariate-balance.md) |
| Teste de não-inferioridade | [PT](docs/pt/metodologias/non-inferiority.md) · [EN](docs/en/methodologies/non-inferiority.md) | [PT](docs/pt/completo/non-inferiority.md) · [EN](docs/en/complete/non-inferiority.md) |
| Heterogeneidade de efeito e novidade | [PT](docs/pt/metodologias/heterogeneity-testing.md) · [EN](docs/en/methodologies/heterogeneity-testing.md) | [PT](docs/pt/completo/heterogeneity-testing.md) · [EN](docs/en/complete/heterogeneity-testing.md) |
| Poder estatístico e MDE | [PT](docs/pt/metodologias/power-mde.md) · [EN](docs/en/methodologies/power-mde.md) | [PT](docs/pt/completo/power-mde.md) · [EN](docs/en/complete/power-mde.md) |
| Transbordamento espacial / canibalização | [PT](docs/pt/metodologias/spillover-cannibalization.md) · [EN](docs/en/methodologies/spillover-cannibalization.md) | [PT](docs/pt/completo/spillover-cannibalization.md) · [EN](docs/en/complete/spillover-cannibalization.md) |

**Inferência com poucos clusters**

| Metodologia | Nível 2 | Nível 3 |
|---|---|---|
| Erros-padrão robustos a cluster | [PT](docs/pt/metodologias/cluster-robust-se.md) · [EN](docs/en/methodologies/cluster-robust-se.md) | [PT](docs/pt/completo/cluster-robust-se.md) · [EN](docs/en/complete/cluster-robust-se.md) |
| Inferência por randomização | [PT](docs/pt/metodologias/randomization-inference.md) · [EN](docs/en/methodologies/randomization-inference.md) | [PT](docs/pt/completo/randomization-inference.md) · [EN](docs/en/complete/randomization-inference.md) |
| Bootstrap wild-cluster | [PT](docs/pt/metodologias/wild-cluster-bootstrap.md) · [EN](docs/en/methodologies/wild-cluster-bootstrap.md) | [PT](docs/pt/completo/wild-cluster-bootstrap.md) · [EN](docs/en/complete/wild-cluster-bootstrap.md) |

**Analytics de negócio**

| Metodologia | Nível 2 | Nível 3 |
|---|---|---|
| Decomposição de coorte / retenção | [PT](docs/pt/metodologias/cohort-retention-decomposition.md) · [EN](docs/en/methodologies/cohort-retention-decomposition.md) | [PT](docs/pt/completo/cohort-retention-decomposition.md) · [EN](docs/en/complete/cohort-retention-decomposition.md) |
| Decomposição de crescimento | [PT](docs/pt/metodologias/growth-decomposition.md) · [EN](docs/en/methodologies/growth-decomposition.md) | [PT](docs/pt/completo/growth-decomposition.md) · [EN](docs/en/complete/growth-decomposition.md) |

**Modelos esportivos**

| Metodologia | Nível 2 | Nível 3 |
|---|---|---|
| Regressão de Poisson com efeitos fixos | [PT](docs/pt/metodologias/poisson-regression.md) · [EN](docs/en/methodologies/poisson-regression.md) | [PT](docs/pt/completo/poisson-regression.md) · [EN](docs/en/complete/poisson-regression.md) |
| Tendência por mínimos quadrados ponderados | [PT](docs/pt/metodologias/wls-trend.md) · [EN](docs/en/methodologies/wls-trend.md) | [PT](docs/pt/completo/wls-trend.md) · [EN](docs/en/complete/wls-trend.md) |
| Regressão logística | [PT](docs/pt/metodologias/logistic-regression.md) · [EN](docs/en/methodologies/logistic-regression.md) | [PT](docs/pt/completo/logistic-regression.md) · [EN](docs/en/complete/logistic-regression.md) |

### Estrutura

```
statistical-methodologies/
├── README.md
├── docs/
│   ├── pt/
│   │   ├── simplificado/   # Nível 1 — visão geral única
│   │   ├── metodologias/   # Nível 2 — uma página por método
│   │   └── completo/       # Nível 3 — uma página por método
│   └── en/
│       ├── simplified/
│       ├── methodologies/
│       └── complete/
├── assets/
│   ├── figstyle.py         # estilo compartilhado das figuras
│   └── figures/             # figuras ilustrativas (dados sintéticos)
└── pdf/
    ├── pt/                   # visao-geral, metodologias-nivel2, metodologias-nivel3
    └── en/                   # overview, methodologies-level2, methodologies-level3
```

### Versões em PDF

- [Nível 1 (PT)](pdf/pt/visao-geral.pdf) · [Nível 2 (PT)](pdf/pt/metodologias-nivel2.pdf) · [Nível 3 (PT)](pdf/pt/metodologias-nivel3.pdf)
- [Level 1 (EN)](pdf/en/overview.pdf) · [Level 2 (EN)](pdf/en/methodologies-level2.pdf) · [Level 3 (EN)](pdf/en/methodologies-level3.pdf)

### Sobre os exemplos

Todo exemplo numérico e toda figura usam dados inventados para fins didáticos —
salários, tempos de espera, taxas de conversão hipotéticas. Nenhum número deste
repositório vem dos dados reais do
[Hub-Racial-Brasil](https://github.com/FelipeSantanaJ/Hub-Racial-Brasil) ou dos
demais projetos do portfólio. As páginas de cada metodologia mencionam, em uma
frase, em que tipo de análise real o método foi aplicado — sem reproduzir
resultados específicos, que continuam documentados nos próprios projetos.

---

## English

### Purpose

This repository doesn't introduce new data or analysis. It takes the statistical
methodologies already applied across my projects — from significance testing to
inequality decomposition, from experiment design to count models — and explains
each one for two audiences at once:

- people with no statistics background who want the idea behind the method;
- people who work with data and want the reasoning, assumptions, mathematical
  formulation, and limitations behind each technique.

### Three levels

| Level | What it is | Audience |
|---|---|---|
| **1 — Overview** | One document covering all 23 methodologies, no formulas | Statistics layperson |
| **2 — Methodology by methodology** | One document per method: intuition, simple example, when to use it, caveats | Someone with some data familiarity |
| **3 — Complete** | Mathematical formulation, assumptions, hypotheses, interpretation, limitations | Analysts, data scientists, researchers |

- [Level 1 — Visão geral (PT)](docs/pt/simplificado/visao-geral.md)
- [Level 1 — Overview (EN)](docs/en/simplified/overview.md)

Every methodology has its own page at every level and language — see the full
table above (links work the same for both languages; the file itself is
bilingual by folder, not by content).

### Structure

```
statistical-methodologies/
├── README.md
├── docs/
│   ├── pt/
│   │   ├── simplificado/   # Level 1 — single overview
│   │   ├── metodologias/   # Level 2 — one page per method
│   │   └── completo/       # Level 3 — one page per method
│   └── en/
│       ├── simplified/
│       ├── methodologies/
│       └── complete/
├── assets/
│   ├── figstyle.py         # shared figure style
│   └── figures/             # illustrative figures (synthetic data)
└── pdf/
    ├── pt/                   # visao-geral, metodologias-nivel2, metodologias-nivel3
    └── en/                   # overview, methodologies-level2, methodologies-level3
```

### PDF versions

- [Level 1 (EN)](pdf/en/overview.pdf) · [Level 2 (EN)](pdf/en/methodologies-level2.pdf) · [Level 3 (EN)](pdf/en/methodologies-level3.pdf)
- [Nível 1 (PT)](pdf/pt/visao-geral.pdf) · [Nível 2 (PT)](pdf/pt/metodologias-nivel2.pdf) · [Nível 3 (PT)](pdf/pt/metodologias-nivel3.pdf)

### About the examples

Every numeric example and every figure uses invented data for teaching purposes
— salaries, wait times, hypothetical conversion rates. None of the numbers in
this repository come from the real data behind
[Hub-Racial-Brasil](https://github.com/FelipeSantanaJ/Hub-Racial-Brasil) or the
other portfolio projects. Each methodology page mentions, in one sentence, the
kind of real analysis the method was applied to — without reproducing specific
results, which stay documented in the projects themselves.

---

**Felipe Santana** — [LinkedIn](https://www.linkedin.com/in/j-felipe-santana/) ·
[GitHub](https://github.com/FelipeSantanaJ)

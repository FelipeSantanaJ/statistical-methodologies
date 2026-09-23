# Regressão de Poisson com efeitos fixos

## 1. Que problema isso resolve?

Um analista quer prever quantos gols um time marca em uma partida, em função da força ofensiva do time, da força defensiva do adversário e de jogar em casa ou fora. O problema: número de gols é uma contagem — 0, 1, 2, 3... — e uma regressão linear comum pode prever valores absurdos como "−0,4 gol" ou tratar igualmente o salto de 0 para 1 gol e de 5 para 6 gols, quando na prática esses saltos não têm o mesmo "peso" estatístico.

## 2. Intuição

Contagens de eventos raros e discretos — gols numa partida, número de clientes que entram numa loja por hora, número de falhas de uma máquina por semana — tendem a seguir um padrão característico: nunca são negativas, são inteiras, e a maioria dos valores fica concentrada perto de zero com uma cauda longa à direita (é bem mais comum ver 0, 1 ou 2 gols do que 6 ou 7). Uma distribuição normal (a curva de sino simétrica) não captura nada disso — ela permite valores negativos e é simétrica ao redor da média. A distribuição de Poisson foi desenhada exatamente para esse tipo de dado.

## 3. Explicação simples

A regressão de Poisson modela o número esperado de eventos como uma função exponencial das variáveis explicativas, garantindo que a previsão nunca seja negativa. Em vez de prever o número de gols diretamente, o modelo prevê o **logaritmo** do número esperado de gols como uma combinação linear das variáveis — e depois converte de volta usando a exponencial. Essa escolha (chamada de "forma log-linear") é o que garante que, não importa quais sejam os coeficientes, a previsão final sempre será positiva.

Efeitos fixos por time entram no modelo como um "ajuste individual" para cada equipe — uma forma de dizer "descontando o quanto esse time específico costuma marcar ou sofrer gols, o que sobra do efeito que estou investigando (por exemplo, mandar o jogo em casa)?"

## 4. Exemplo conceitual fácil

Imagine comparar o número médio de clientes que entram em duas lojas por hora: uma no centro (movimento alto) e uma no bairro (movimento baixo). Se você quer isolar o efeito de "ser sexta-feira" no fluxo de clientes, precisa primeiro descontar que a loja do centro já tem um patamar de movimento muito maior que a do bairro — senão qualquer diferença observada pode ser só reflexo de qual loja está sendo olhada, não do dia da semana. O efeito fixo por loja faz exatamente esse desconto, loja por loja, antes de estimar o efeito de "sexta-feira".

## 5. Como funciona, em linhas gerais

1. Para cada observação (uma partida, uma hora, um período), o número esperado de eventos é escrito como $\lambda = e^{(\beta_0 + \beta_1 x_1 + \beta_2 x_2 + \dots)}$ — a soma ponderada das variáveis explicativas, exponenciada.
2. Uma dummy (variável indicadora) é criada para cada unidade que recebe efeito fixo (cada time, por exemplo) — isso permite que cada time tenha seu próprio "nível base" de gols esperados, sem impor que todos os times sejam iguais na ausência das outras variáveis.
3. O modelo é ajustado por máxima verossimilhança, encontrando os coeficientes que tornam os dados observados mais prováveis sob a suposição de que a contagem em cada observação segue uma distribuição de Poisson com média $\lambda$.
4. Cada coeficiente estimado representa o efeito daquela variável na escala logarítmica do número esperado de eventos.

## 6. O que o resultado significa

O coeficiente de uma variável, ao ser exponenciado ($e^{\beta}$), vira um **fator multiplicativo** sobre o número esperado de eventos — não um efeito aditivo. Se o coeficiente de "jogar em casa" é 0,30, então $e^{0,30} \approx 1,35$: jogar em casa multiplica o número esperado de gols por 1,35, ou seja, um aumento de 35%, mantendo tudo o mais constante.

## 7. Como interpretar

Sempre traduza o coeficiente bruto (na escala log) para o fator multiplicativo antes de comunicar o resultado — "o coeficiente foi 0,30" não diz nada a alguém sem estatística, mas "jogar em casa aumenta em 35% o número esperado de gols" é imediatamente interpretável. Fatores multiplicativos maiores que 1 indicam aumento; menores que 1, redução (por exemplo, 0,85 significa uma queda de 15%).

## 8. Quando é útil

Sempre que a variável de resposta é uma contagem de eventos — não uma proporção, não uma média contínua. É o tipo de modelo tipicamente usado em análises esportivas para estimar quantos gols uma equipe deve marcar, combinando a força ofensiva do próprio time, a força defensiva do adversário e o efeito de mandar o jogo em casa, com efeitos fixos por clube isolando as diferenças de nível entre equipes.

## 9. Cuidados importantes

- A Poisson assume que a variância da contagem é igual à média (equidispersão). Quando a variância observada é claramente maior que a média — **sobredispersão** — os erros-padrão calculados pela Poisson pura ficam artificialmente pequenos, inflando a aparente significância estatística. Nesses casos, modelos alternativos (Poisson com erro-padrão robusto, binomial negativa) são mais adequados.
- Efeitos fixos por unidade (time, loja) consomem graus de liberdade — com muitas unidades e poucas observações por unidade, o modelo pode ficar instável.
- O modelo pressupõe independência entre eventos condicional às variáveis incluídas; contextos com forte dependência temporal (uma sequência de vitórias que muda a confiança do time) violam essa suposição.

## 10. Um exemplo pequeno com números

Suponha um modelo simplificado (sem efeitos fixos, para ilustrar a mecânica) em que o número esperado de gols de um time visitante é $\lambda = e^{0,10}\approx 1,11$ e, jogando em casa, $\lambda = e^{0,10+0,30} = e^{0,40}\approx 1,49$. A razão entre os dois, $1,49/1,11\approx 1,35$, confirma que o efeito de jogar em casa multiplica o número esperado de gols por 1,35 — um aumento de 35% — sem que precisemos calcular a diferença simples entre 1,49 e 1,11 (que seria apenas 0,38 gol, uma leitura menos informativa que o fator multiplicativo).

![Distribuição de contagem de gols comparada a uma curva normal](../../../assets/figures/poisson-regression-counts-vs-normal-pt.png)

## 11. Exemplo de código simples

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

# uma linha por partida-time: gols marcados, mando de campo e times envolvidos
df = pd.DataFrame({
    "gols": [1, 2, 0, 3, 1, 2, 0, 1, 2, 1],
    "mandante": [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    "time": ["A", "A", "B", "B", "C", "C", "D", "D", "E", "E"],
})

modelo = smf.glm(
    formula="gols ~ mandante + C(time)",
    data=df,
    family=sm.families.Poisson(),
).fit()

print(modelo.summary())

# fator multiplicativo do efeito de mandar o jogo em casa
coef_mandante = modelo.params["mandante"]
print(f"Fator multiplicativo (jogar em casa): {np.exp(coef_mandante):.2f}")
```

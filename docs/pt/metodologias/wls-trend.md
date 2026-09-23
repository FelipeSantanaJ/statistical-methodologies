# Tendência por mínimos quadrados ponderados (WLS) com classificação por intervalo de confiança

## 1. Que problema isso resolve?

Um analista quer saber, para cada loja de uma rede, se o ticket médio está subindo, caindo ou estável ao longo dos últimos trimestres. O problema é que nem todos os trimestres têm o mesmo número de vendas registradas — um trimestre com 500 transações é uma estimativa muito mais confiável do que um com 20. Uma regressão linear comum trata todos os pontos como igualmente confiáveis, deixando um único trimestre com poucos dados distorcer a tendência estimada tanto quanto um trimestre robusto.

## 2. Intuição

Imagine perguntar a duas pessoas a nota média de um restaurante: uma respondeu com base em 400 avaliações, a outra com base em 3. Intuitivamente, você confia mais na primeira resposta. Mínimos quadrados ponderados (*Weighted Least Squares*, WLS) faz exatamente isso ao ajustar uma linha de tendência: dá mais peso aos pontos baseados em mais observações, e menos peso aos pontos baseados em poucas.

## 3. Explicação simples

O método ajusta uma reta (ou outra tendência simples) aos dados ao longo do tempo, exatamente como uma regressão linear comum — mas em vez de minimizar a soma simples dos erros ao quadrado, minimiza a soma **ponderada** dos erros ao quadrado, usando o número de observações de cada período como peso. Depois de estimar a inclinação da reta, calcula-se um intervalo de confiança para essa inclinação, e a tendência é classificada de forma simples e objetiva:

- Se o intervalo de confiança da inclinação está inteiramente **acima de zero** → tendência de **alta**.
- Se está inteiramente **abaixo de zero** → tendência de **queda**.
- Se o intervalo **inclui o zero** → tendência **estável** (não há evidência estatística suficiente de que a inclinação seja diferente de zero).

## 4. Exemplo conceitual fácil

Duas lojas registram ticket médio ao longo de seis trimestres. A Loja A sobe de forma consistente, trimestre após trimestre, com muitas vendas em cada período — a inclinação estimada é claramente positiva e o intervalo de confiança não chega perto de zero: classificação de "subindo". A Loja B oscila para cima e para baixo sem padrão claro, com poucas vendas em alguns trimestres — a inclinação estimada pode até ser levemente positiva, mas o intervalo de confiança é largo o suficiente para incluir zero: classificação de "estável", mesmo que a reta ajustada não seja perfeitamente horizontal.

## 5. Como funciona, em linhas gerais

1. Para cada unidade (loja, região, categoria), organiza-se a métrica de interesse ao longo do tempo (trimestre, mês) junto com o número de observações que sustentam cada ponto.
2. Ajusta-se uma reta pelo método dos mínimos quadrados ponderados, em que o peso de cada ponto é proporcional ao seu número de observações — pontos com mais dados "puxam" mais a reta na direção deles.
3. Calcula-se o erro-padrão da inclinação estimada, que já incorpora a ponderação.
4. Constrói-se um intervalo de confiança (tipicamente 95%) para a inclinação.
5. Classifica-se a tendência como subindo, caindo ou estável, dependendo da posição do intervalo de confiança em relação a zero.

## 6. O que o resultado significa

A inclinação estimada diz o quanto, em média, a métrica muda por período. O intervalo de confiança diz o quão precisa é essa estimativa — intervalos largos (comuns quando há poucas observações, muita variabilidade, ou poucos períodos de tempo) tornam mais difícil afirmar com confiança que existe uma tendência real, mesmo que a inclinação pontual pareça diferente de zero.

## 7. Como interpretar

"Estável" na classificação não significa necessariamente "sem nenhuma mudança" — significa "não há evidência estatística suficiente, dados o volume e a variabilidade observados, para distinguir a inclinação de zero". Uma loja pode estar genuinamente estável, ou pode simplesmente não ter dados suficientes para detectar uma tendência real que exista mas seja pequena. É importante não confundir as duas situações ao comunicar o resultado.

## 8. Quando é útil

Sempre que se quer classificar a tendência de muitas unidades (lojas, jogadores, regiões, produtos) de forma sistemática e comparável, especialmente quando o número de observações por período varia bastante entre unidades ou ao longo do tempo. É a lógica usada em análises esportivas para classificar se o desempenho de um clube está em ascensão, queda ou estabilidade ao longo de uma temporada, ponderando cada período pelo número de partidas ou eventos observados naquele trecho.

## 9. Cuidados importantes

- A classificação por IC depende do nível de confiança escolhido (95% é comum, mas não universal) — um IC de 90% classifica mais séries como "subindo" ou "caindo" que um IC de 99%, para os mesmos dados.
- Poucos pontos no tempo (por exemplo, só três ou quatro períodos) tornam o intervalo de confiança muito largo, dificultando qualquer classificação diferente de "estável" mesmo quando existe uma tendência real.
- WLS assume uma relação linear com o tempo; tendências não lineares (crescimento que acelera ou desacelera) podem ser mal capturadas por uma única reta.
- O peso pelo número de observações corrige desigualdade de precisão amostral, mas não corrige problemas de qualidade dos dados dentro de cada período (por exemplo, um período com muitas transações mas registradas com erro sistemático).

## 10. Um exemplo pequeno com números

Duas lojas, doze trimestres cada, número de observações variando de 40 a 400 por trimestre. Na Loja A, a inclinação estimada por WLS é de +2,4 (unidades da métrica por trimestre), com intervalo de confiança de 95% entre +1,1 e +3,7 — inteiramente acima de zero, classificada como **subindo**. Na Loja B, a inclinação estimada é de +0,05, com intervalo de confiança entre −1,2 e +1,3 — cruza o zero, classificada como **estável**, mesmo que a inclinação pontual seja tecnicamente positiva.

![Classificação de tendência ponderada para duas lojas](../../../assets/figures/wls-trend-classification-pt.png)

## 11. Exemplo de código simples

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm

df = pd.DataFrame({
    "trimestre": range(12),
    "ticket_medio": [100, 102, 105, 104, 108, 110, 111, 115, 116, 119, 121, 124],
    "n_observacoes": [40, 55, 380, 390, 60, 400, 45, 370, 50, 360, 400, 390],
})

X = sm.add_constant(df["trimestre"])
modelo = sm.WLS(df["ticket_medio"], X, weights=df["n_observacoes"]).fit()

inclinacao = modelo.params["trimestre"]
ic_baixo, ic_alto = modelo.conf_int(alpha=0.05).loc["trimestre"]

if ic_baixo > 0:
    classificacao = "subindo"
elif ic_alto < 0:
    classificacao = "caindo"
else:
    classificacao = "estável"

print(f"Inclinação: {inclinacao:.2f} | IC 95%: [{ic_baixo:.2f}, {ic_alto:.2f}] | Classificação: {classificacao}")
```

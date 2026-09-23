# Regressão logística

## 1. Que problema isso resolve?

Um analista quer prever se algo vai acontecer ou não — um cliente cancela ou não, um time cai ou não, um paciente responde ao tratamento ou não — a partir de uma ou mais variáveis contínuas. O problema: o desfecho é binário (0 ou 1), e uma regressão linear comum, ajustada diretamente a essa variável de 0/1, pode prever valores como −0,3 ou 1,4, que não correspondem a nenhuma probabilidade real.

## 2. Intuição

Uma probabilidade precisa ficar entre 0 e 1, sempre. A regressão logística resolve isso modelando, não a probabilidade diretamente, mas uma transformação dela — o **log da razão de chances** (log-odds) — como uma combinação linear das variáveis explicativas. Essa combinação linear pode assumir qualquer valor, de menos a mais infinito; a transformação de volta (a função logística, em forma de S) comprime esse valor para o intervalo (0, 1), garantindo que a saída do modelo seja sempre uma probabilidade válida.

## 3. Explicação simples

O modelo estima, para cada combinação de variáveis explicativas, a probabilidade do desfecho ser 1. A curva que relaciona a combinação linear das variáveis à probabilidade tem formato de S (sigmoide): perto do meio, pequenas mudanças na variável mudam bastante a probabilidade prevista; nos extremos (perto de 0 ou perto de 1), a mesma mudança tem efeito quase nenhum — a probabilidade já está perto do limite e não pode ultrapassá-lo.

## 4. Exemplo conceitual fácil

Pense em prever se um estudante passa numa prova a partir de quantas horas estudou. Quem estudou 0 horas quase certamente não passa; quem estudou 20 horas quase certamente passa — nos dois extremos, uma hora a mais ou a menos quase não muda a previsão. É na faixa do meio (por exemplo, entre 4 e 8 horas) que uma hora extra de estudo faz mais diferença na probabilidade de aprovação — exatamente a região onde a curva em S é mais inclinada.

## 5. Como funciona, em linhas gerais

1. Para cada observação, o modelo calcula uma combinação linear das variáveis explicativas: $z = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \dots$
2. Essa combinação passa pela função logística, $p = 1/(1+e^{-z})$, que converte qualquer número real numa probabilidade entre 0 e 1.
3. Os coeficientes $\beta$ são estimados por máxima verossimilhança — o conjunto de valores que torna os desfechos observados (quem teve 1, quem teve 0) mais prováveis sob o modelo.
4. Para classificar uma observação nova, compara-se a probabilidade prevista a um limiar (0,5, por padrão) — acima, prevê-se 1; abaixo, prevê-se 0. O limiar pode ser ajustado conforme o custo de cada tipo de erro.

## 6. O que o resultado significa

Cada coeficiente, exponenciado ($e^{\beta}$), vira uma **razão de chances** (odds ratio): quanto a chance do desfecho ser 1 multiplica quando a variável aumenta em uma unidade, mantendo tudo o mais constante. Uma razão de chances de 2,0 significa que a chance dobra; uma de 0,5, que ela cai pela metade. "Chance" aqui é a razão $p/(1-p)$, não a probabilidade $p$ em si — a distinção importa porque razão de chances e probabilidade não mudam na mesma proporção.

## 7. Como interpretar

Traduza sempre o coeficiente bruto (na escala log-odds) para razão de chances antes de comunicar — "o coeficiente foi 0,69" não diz nada por si só, mas "cada ponto a mais na pontuação de satisfação reduz a chance de cancelamento pela metade" ($e^{-0,69}\approx 0,50$) é imediatamente interpretável. Para avaliar a qualidade do modelo como classificador — não só a significância dos coeficientes —, duas métricas usuais são a **AUC** (área sob a curva ROC: a probabilidade de o modelo dar uma pontuação mais alta a uma observação positiva aleatória do que a uma negativa aleatória; 0,5 é aleatório, 1,0 é separação perfeita) e o **Brier score** (erro quadrático médio entre probabilidade prevista e desfecho observado; quanto menor, melhor calibrado).

## 8. Quando é útil

Sempre que o desfecho de interesse é binário e se quer tanto **quantificar o efeito** de cada variável explicativa (via razão de chances) quanto **prever uma probabilidade** para casos novos — não apenas uma classificação 0/1. É o tipo de modelo indicado para transformar um indicador contínuo (ritmo de pontos, pontuação de satisfação, tempo de uso) numa chance real de um desfecho binário acontecer.

## 9. Cuidados importantes

- **Quase-separação**: quando uma variável separa quase perfeitamente as duas classes (por exemplo, todo mundo acima de certo valor tem desfecho 1 e todo mundo abaixo tem 0), o algoritmo de máxima verossimilhança não converge de forma estável — os coeficientes e seus erros-padrão ficam artificialmente grandes. Isso costuma acontecer justamente quando o modelo está funcionando bem, e não invalida a direção do efeito, mas exige cautela ao interpretar o intervalo de confiança.
- **Correlação entre observações**: se várias observações vêm da mesma unidade (o mesmo cliente em meses diferentes, o mesmo time em rodadas diferentes de uma temporada), tratá-las como independentes infla artificialmente a confiança do modelo. Nesses casos, validar com uma divisão que respeite a estrutura de grupo (por exemplo, deixar uma unidade inteira de fora por vez) é mais confiável do que confiar só no ajuste dentro da amostra.
- **Significância não é acurácia**: um coeficiente pode ser estatisticamente significativo (p pequeno) e o modelo, mesmo assim, ter pouco poder de separar as classes (AUC próxima de 0,5) — são perguntas diferentes.

## 10. Um exemplo pequeno com números

Suponha um modelo com uma única variável ($x$ = pontuação de satisfação de 0 a 10) prevendo cancelamento, com coeficiente $\hat\beta = -0,69$ (erro-padrão 0,10) e intercepto $\hat\beta_0 = 3,45$. A razão de chances é $e^{-0,69}\approx 0,50$: cada ponto a mais de satisfação reduz a chance de cancelamento pela metade. O ponto de 50% de probabilidade prevista fica em $x = -\hat\beta_0/\hat\beta = 5,0$ — abaixo disso, o modelo prevê mais chance de cancelar do que de ficar; acima, o contrário.

![Regressão logística: da variável contínua à probabilidade](../../../assets/figures/logistic-regression-sigmoid-pt.png)

![Curva ROC de um classificador ilustrativo](../../../assets/figures/logistic-regression-roc-auc-pt.png)

## 11. Exemplo de código simples

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm

# uma linha por cliente: pontuação de satisfação e se cancelou (1) ou não (0)
df = pd.DataFrame({
    "satisfacao": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "cancelou":   [1, 1, 1, 1, 0, 1, 0, 0, 0, 0],
})

X = sm.add_constant(df["satisfacao"])
modelo = sm.Logit(df["cancelou"], X).fit()
print(modelo.summary())

# razão de chances de cada ponto a mais de satisfação
print(f"Razão de chances: {np.exp(modelo.params['satisfacao']):.2f}")

# probabilidade prevista para um cliente com satisfação = 6
print(modelo.predict([1, 6]))
```

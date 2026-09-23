# Bootstrap wild-cluster

## 1. Que problema isso resolve?

Erros-padrão robustos a cluster funcionam bem quando há muitos clusters,
mas ficam pouco confiáveis quando há poucos — uma dezena ou menos, por
exemplo. Nesse cenário, um teste de hipótese baseado nessa aproximação pode
rejeitar a hipótese nula com muito mais frequência do que deveria, mesmo
quando ela é verdadeira. O bootstrap wild-cluster é uma forma de construir
uma distribuição de referência mais confiável nessa situação, sem depender
da aproximação assintótica que falha com poucos clusters.

## 2. Intuição

Em vez de confiar numa fórmula teórica para o erro-padrão, o método gera
muitas versões alternativas e plausíveis dos dados — mantendo o padrão real
de dependência dentro de cada cluster — e observa como a estatística de
teste varia entre essas versões. Essa variação observada vira a régua para
julgar se o resultado real é incomum.

## 3. Explicação simples

O bootstrap wild-cluster não reamostra linhas de dados individuais, nem
sorteia clusters inteiros com reposição (como faz um bootstrap de cluster
comum). Em vez disso, ele pega os **resíduos** de um modelo já ajustado,
multiplica **todos os resíduos de um mesmo cluster pelo mesmo número
aleatório** (tipicamente +1 ou −1, sorteado cluster por cluster), soma esses
resíduos perturbados de volta a uma previsão sob a hipótese nula, e reajusta
o modelo. Repetindo isso milhares de vezes, obtém-se uma distribuição
inteira de estatísticas de teste "poderia ter sido assim, sob a hipótese
nula".

## 4. Exemplo conceitual fácil

Imagine uma rede de 6 hospitais testando um novo protocolo de triagem, com
apenas 6 clusters (hospitais) no total — poucos demais para confiar num
erro-padrão robusto a cluster convencional. O bootstrap wild-cluster gera
milhares de cenários alternativos em que os desvios (resíduos) observados
em cada hospital são "invertidos" ou "mantidos" em bloco, de forma
aleatória, hospital por hospital — preservando o padrão de que dentro de um
mesmo hospital os desvios tendem a se mover juntos.

## 5. Como funciona, em linhas gerais

1. Ajusta-se o modelo sob a hipótese nula (por exemplo, efeito do
   tratamento igual a zero) e obtêm-se os resíduos desse ajuste restrito.
2. Para cada réplica de bootstrap, sorteia-se um sinal aleatório (+1 ou −1)
   **por cluster** — todas as observações do mesmo cluster recebem o mesmo
   sinal naquela réplica.
3. Multiplicam-se os resíduos de cada cluster pelo sinal sorteado para
   aquele cluster, gerando uma nova variável dependente sintética.
4. Reajusta-se o modelo a essa variável sintética e recalcula-se a
   estatística de teste.
5. Repetindo os passos 2 a 4 muitas vezes (tipicamente 999 ou mais réplicas),
   forma-se a distribuição de referência da estatística de teste sob a
   hipótese nula.

## 6. O que o resultado significa

O valor-p do bootstrap wild-cluster é a fração das réplicas em que a
estatística recalculada é tão extrema quanto, ou mais extrema que, a
estatística observada nos dados reais. Diferente do erro-padrão robusto a
cluster tradicional, essa distribuição de referência é construída
diretamente dos dados, sem depender de uma aproximação normal que só
funciona bem com muitos clusters.

## 7. Como interpretar

Um valor-p baixo no bootstrap wild-cluster é evidência mais confiável, com
poucos clusters, do que um valor-p igualmente baixo vindo de um erro-padrão
robusto a cluster convencional — porque o método não depende da suposição
assintótica que falha justamente nesse cenário.

## 8. Quando é útil

Especialmente indicado quando há poucos clusters (uma faixa comum na
literatura aplicada é abaixo de 30, com atenção redobrada abaixo de 10-15),
e o efeito de interesse vem de um modelo de regressão — com ou sem
variáveis de controle — em vez de uma comparação simples de médias entre
dois grupos (nesse caso mais simples, inferência por randomização também é
uma alternativa direta).

## 9. Cuidados importantes

O método ainda depende de o modelo estar razoavelmente bem especificado —
ele resolve o problema do erro-padrão sob poucos clusters, mas não conserta
um modelo mal especificado. Com clusters extremamente poucos (2 ou 3, por
exemplo), mesmo o bootstrap wild-cluster enfrenta limitações, já que o
número de combinações possíveis de sinais por cluster também fica pequeno.

## 10. Um exemplo pequeno com números

Um modelo de regressão com 6 clusters produz um coeficiente estimado de
tratamento de 4,2, com erro-padrão robusto a cluster convencional de 1,3,
dando t ≈ 3,2 — aparentemente significativo pela referência t assintótica
usual. Rodando o bootstrap wild-cluster com 999 réplicas (sinais aleatórios
sorteados por cluster, 6 possibilidades de sinal combinando $2^6 = 64$
padrões possíveis), a estatística t observada de 3,2 cai no percentil 91 da
distribuição bootstrap — correspondendo a um valor-p bilateral de
aproximadamente 0,09, mais alto (mais conservador) do que o valor-p
assintótico original de cerca de 0,003. A conclusão muda de "fortemente
significativo" para "sugestivo, mas não conclusivo a 5%".

## 11. Exemplo de código simples

```python
import numpy as np
import statsmodels.formula.api as smf

def wild_cluster_bootstrap(df, formula, cluster_col, n_boot=999, seed=0):
    rng = np.random.default_rng(seed)
    modelo_restrito = smf.ols(formula, data=df).fit()
    residuos = modelo_restrito.resid
    ajustado = modelo_restrito.fittedvalues
    clusters = df[cluster_col].unique()

    t_boot = []
    for _ in range(n_boot):
        sinais = {c: rng.choice([-1, 1]) for c in clusters}
        peso = df[cluster_col].map(sinais).values
        y_sintetico = ajustado + residuos * peso
        df_boot = df.assign(y_sintetico=y_sintetico)
        modelo_boot = smf.ols(formula.replace(formula.split("~")[0].strip(), "y_sintetico"),
                               data=df_boot).fit(cov_type="cluster",
                                                  cov_kwds={"groups": df_boot[cluster_col]})
        t_boot.append(modelo_boot.tvalues["tratamento"])
    return np.array(t_boot)
```

![Distribuição wild-cluster bootstrap comparada à referência t assintótica, com 6 clusters](../../../assets/figures/wild-cluster-bootstrap-distribution-pt.png)

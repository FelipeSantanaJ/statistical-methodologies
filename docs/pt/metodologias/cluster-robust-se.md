# Erros-padrão robustos a cluster

## 1. Que problema isso resolve?

O cálculo padrão de erro-padrão assume que cada observação da amostra traz
informação nova e independente das demais. Mas e quando várias observações
vêm do mesmo grupo — a mesma loja, a mesma turma, a mesma região — e se
parecem entre si por razões que nada têm a ver com a variável que você está
testando? Tratar essas observações como independentes faz o erro-padrão
parecer menor do que realmente é, e pode levar a declarar "significativo"
algo que não é.

## 2. Intuição

Pense em medir a satisfação de clientes em 20 lojas, com 50 respostas por
loja — 1.000 observações no total. Se cada loja tem sua própria cultura de
atendimento, gerente, localização e clientela, respostas da mesma loja
tendem a se parecer entre si por causa desses fatores compartilhados, não só
por coincidência. Na prática, você não tem 1.000 pedaços independentes de
informação — tem algo mais perto de 20 "blocos" de informação, cada um
formado por respostas correlacionadas entre si. Calcular o erro-padrão como
se fossem 1.000 observações independentes exagera a precisão da estimativa.

## 3. Explicação simples

Cada observação nova dentro do mesmo cluster carrega menos informação
adicional do que uma observação de um cluster diferente, porque parte do que
ela mostra já era previsível a partir das outras observações do mesmo grupo.
O erro-padrão robusto a cluster reconhece essa correlação interna e ajusta o
cálculo para refletir o número efetivo de "unidades independentes de
informação" — que fica mais perto do número de clusters do que do número
total de observações.

## 4. Exemplo conceitual fácil

Uma rede de academias testa um novo programa de treino em 8 unidades
(tratamento) contra outras 8 unidades (controle), com cerca de 40 alunos por
unidade. Alunos da mesma unidade compartilham o mesmo instrutor, o mesmo
horário de pico, a mesma vizinhança — fatores que afetam o resultado
independentemente do programa testado. Um erro-padrão que ignora isso trata
os 640 alunos como 640 fontes independentes de evidência; na prática, a
evidência real está muito mais próxima de vir de 16 unidades.

## 5. Como funciona, em linhas gerais

Em vez de assumir que os erros do modelo são independentes entre todas as
observações, o erro-padrão robusto a cluster permite que os erros sejam
correlacionados dentro de cada cluster (sem exigir uma forma específica dessa
correlação) e apenas assume independência **entre** clusters diferentes. A
matriz de variância-covariância dos coeficientes é recalculada somando as
contribuições cluster por cluster, em vez de observação por observação — o
que produz, tipicamente, um erro-padrão maior (mais conservador, mais
honesto) do que o cálculo ingênuo.

## 6. O que o resultado significa

O ponto estimado do efeito não muda — só o erro-padrão em volta dele. Um
intervalo de confiança calculado com erro-padrão robusto a cluster é mais
largo, refletindo com mais fidelidade a real incerteza da estimativa, dado
que a quantidade efetiva de informação independente é menor do que o número
bruto de linhas na base de dados.

## 7. Como interpretar

Se um resultado era "significativo" com o erro-padrão ingênuo e deixa de ser
com o erro-padrão robusto a cluster, isso não é um defeito do método — é a
correção mostrando que a confiança original estava artificialmente inflada.
Quanto mais forte a correlação dentro dos clusters e quanto mais desigual o
tamanho dos clusters, maior costuma ser essa diferença.

## 8. Quando é útil

Sempre que a unidade de aleatorização ou de coleta de dados for diferente da
unidade de análise — por exemplo, um experimento randomizado por loja mas
analisado no nível do cliente, uma pesquisa domiciliar em que várias pessoas
do mesmo domicílio respondem, ou dados organizados por região geográfica ao
longo de vários períodos de tempo.

## 9. Cuidados importantes

Com **poucos clusters** (regra prática comum: menos de 30-40), mesmo o
erro-padrão robusto a cluster pode ser instável e enviesado para baixo — a
correção assintótica que o sustenta depende de ter clusters suficientes para
funcionar bem. Nesse cenário, métodos alternativos como inferência por
randomização ou bootstrap wild-cluster costumam ser preferíveis (veja os
documentos correspondentes).

## 10. Um exemplo pequeno com números

Num modelo simples com 1.000 observações em 20 clusters, suponha que o
coeficiente estimado de interesse seja 5,0. O erro-padrão ingênuo (tratando
as 1.000 observações como independentes) é 0,45, dando uma estatística
t ≈ 11,1 — fortemente significativo. Ao recalcular como erro-padrão robusto a
cluster, considerando a correlação dentro de cada uma das 20 lojas, o
erro-padrão sobe para 1,60, dando t ≈ 3,1 — ainda significativo, mas com uma
margem de confiança bem mais realista.

## 11. Exemplo de código simples

```python
import statsmodels.formula.api as smf

modelo = smf.ols("satisfacao ~ tratamento", data=df).fit(
    cov_type="cluster",
    cov_kwds={"groups": df["loja_id"]},
)
print(modelo.summary())
```

![Comparação entre o intervalo de confiança calculado com erro-padrão ingênuo e com erro-padrão robusto a cluster](../../../assets/figures/cluster-robust-se-ci-comparison-pt.png)

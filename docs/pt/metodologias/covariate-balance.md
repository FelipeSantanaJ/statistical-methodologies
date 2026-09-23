# Balanceamento de covariáveis e ajuste por covariáveis

*Pressupõe os fundamentos de teste A/B — veja [Fundamentos de teste A/B](./ab-testing.md).*

## 1. Que problema isso resolve?

Um experimento foi randomizado, mas será que os dois grupos realmente saíram
parecidos em características que existiam antes do experimento começar —
idade dos usuários, tempo de uso prévio do produto, comportamento histórico?
E, separadamente: dado que existem essas características medidas antes do
experimento, dá para usá-las para tornar a estimativa do efeito mais
precisa, mesmo quando os grupos já estão bem balanceados? São duas perguntas
relacionadas, mas diferentes, e é comum confundi-las.

## 2. Intuição

A checagem de balanceamento é uma auditoria: com grupos formados por sorteio,
características que não deveriam ter relação nenhuma com a atribuição —
porque foram medidas antes do experimento sequer existir — devem estar
distribuídas de forma parecida entre os grupos. Se estiverem muito
diferentes, isso é sinal de alerta sobre a randomização, não uma
característica normal do desenho experimental.

Já o ajuste por covariáveis é outra coisa: mesmo com randomização perfeita,
sempre existe alguma variação de usuário para usuário que não tem nada a ver
com o tratamento. Se uma característica medida antes do experimento (como o
valor de compra do mês anterior) ajuda a prever a métrica que está sendo
testada, "descontar" essa característica da comparação reduz o ruído da
estimativa — sem viesar o resultado, porque a característica foi medida
antes de qualquer efeito do tratamento poder existir.

## 3. Explicação simples

Para balanceamento: compara-se, para cada covariável de interesse, a média
(ou proporção) entre o grupo controle e o grupo tratamento, geralmente
através da diferença padronizada de médias — a diferença dividida por um
desvio-padrão combinado, o que permite comparar covariáveis em escalas bem
diferentes (idade em anos, gasto em reais) numa régua comum.

Para ajuste: em vez de comparar só as médias brutas dos dois grupos,
ajusta-se um modelo que já leva em conta essas covariáveis pré-experimento
(uma regressão, por exemplo), ou usa-se pós-estratificação — dividir a
amostra em estratos definidos pelas covariáveis e combinar as estimativas
dentro de cada estrato. O resultado é uma estimativa do mesmo efeito, mas
com erro-padrão menor.

![Gráfico de balanceamento (love plot) mostrando a diferença padronizada de cada covariável entre os grupos, com uma faixa de referência em torno de zero](../../../assets/figures/covariate-balance-love-plot-pt.png)

## 4. Exemplo conceitual fácil

Um app de assinatura testa uma nova política de preço. Antes de olhar
qualquer resultado do experimento, a equipe compara idade média, tempo de
assinatura anterior e gasto médio do mês anterior entre o grupo controle e o
grupo tratamento. Todas as três estão bem próximas entre os grupos — sinal
de que a randomização funcionou. Depois, ao estimar o efeito da nova
política sobre a receita, a equipe usa o gasto do mês anterior como
covariável de ajuste, porque sabe que esse gasto passado é um bom preditor
do gasto futuro — isso deixa a estimativa do efeito mais precisa, com um
intervalo de confiança mais estreito, sem mudar seu significado.

## 5. Como funciona, em linhas gerais

**Balanceamento (checagem pré-experimento):**
1. Lista-se as covariáveis relevantes, medidas antes do início do
   experimento (nunca depois — covariáveis pós-tratamento podem já ter sido
   afetadas pelo próprio experimento).
2. Calcula-se a diferença padronizada de médias entre os grupos para cada
   covariável.
3. Compara-se cada diferença a um limite de referência comum (0,1 é um valor
   frequentemente usado na literatura) — abaixo disso, considera-se
   balanceamento aceitável.

**Ajuste por covariáveis (redução de variância):**
1. Escolhem-se covariáveis pré-experimento que sejam boas preditoras da
   métrica de interesse.
2. Ajusta-se um modelo (regressão linear simples, ou uma técnica como CUPED)
   que usa essas covariáveis para explicar parte da variação da métrica que
   não tem relação com o tratamento.
3. A estimativa do efeito do tratamento, depois desse ajuste, tem a mesma
   interpretação de antes, mas com erro-padrão reduzido.

## 6. O que o resultado significa

Balanceamento aceitável em todas as covariáveis observadas dá mais confiança
de que os grupos eram comparáveis antes do experimento começar — reforçando
a leitura causal do teste de efeito. O ajuste por covariáveis, por sua vez,
não muda a interpretação do efeito estimado (ainda é a diferença causada
pelo tratamento); ele só reduz a incerteza em torno dessa estimativa,
permitindo detectar efeitos menores com a mesma amostra, ou obter a mesma
precisão com uma amostra menor.

## 7. Como interpretar

Um desbalanceamento em uma covariável não invalida automaticamente o
experimento, mas pede investigação — pode ser apenas um falso positivo (com
muitas covariáveis testadas, algumas vão parecer desbalanceadas por acaso) ou
pode ser sinal de um problema real de randomização, situação em que um teste
de Sample Ratio Mismatch complementar é o próximo passo natural. Balanceamento
bom em covariáveis observadas nunca garante balanceamento em covariáveis não
observadas — é uma evidência a favor da randomização, não uma prova completa.

## 8. Quando é útil

A checagem de balanceamento deve ser rotina em todo experimento randomizado,
como parte da validação de que a randomização funcionou. O ajuste por
covariáveis é especialmente valioso quando a métrica primária tem alta
variabilidade entre usuários (o que é comum, por exemplo, em métricas de
receita ou de engajamento) e existe uma covariável pré-experimento fortemente
correlacionada com ela — nesses casos, o ganho de precisão pode ser
substancial.

## 9. Cuidados importantes

- Nunca use uma covariável medida depois do início do experimento para
  ajuste ou checagem de balanceamento — ela pode já ter sido afetada pelo
  próprio tratamento, o que introduz viés em vez de reduzir ruído.
- Ajuste por covariáveis não "conserta" um desbalanceamento real na
  atribuição — ele serve para reduzir variância quando a randomização já
  funcionou, não como substituto de uma randomização quebrada.
- Testar balanceamento em dezenas de covariáveis ao mesmo tempo aumenta a
  chance de encontrar alguma "desbalanceada" por acaso — olhar o padrão
  geral, não reagir isoladamente a uma covariável isolada fora do limite.
- A escolha de quais covariáveis usar para ajuste deve ser feita antes de
  olhar os resultados do experimento, para não introduzir viés de seleção
  retroativo.

## 10. Um exemplo pequeno com números

Um app de assinatura roda um experimento com 8.000 usuários por braço.
Comparando o gasto médio do mês anterior ao experimento: controle R$ 42,10
(desvio-padrão R$ 18,40), tratamento R$ 42,80 (desvio-padrão R$ 18,90). A
diferença padronizada de médias é:

$$
SMD = \frac{42{,}80 - 42{,}10}{\sqrt{(18{,}40^2 + 18{,}90^2)/2}} \approx 0{,}037
$$

Bem abaixo do limite de referência de 0,1 — balanceamento aceitável. Ao
estimar o efeito da nova política de preço sobre a receita do mês seguinte,
o estimador simples (diferença de médias) produz um IC 95% de largura ±1,05
ponto percentual em torno do efeito estimado; usando o gasto do mês anterior
como covariável de ajuste, o IC cai para aproximadamente ±0,62 ponto
percentual — o mesmo efeito estimado, com bem mais precisão.

## 11. Exemplo de código simples

```python
import numpy as np
import statsmodels.api as sm

# ilustrativo: y = receita no mês do experimento, trat = 1 se tratamento
# gasto_anterior = covariável pré-experimento (gasto no mês anterior)
X_ajustado = sm.add_constant(np.column_stack([trat, gasto_anterior]))
modelo = sm.OLS(y, X_ajustado).fit(cov_type="HC1")

print(modelo.summary())
# O coeficiente de 'trat' é o efeito ajustado; seu erro-padrão tende a ser
# menor que o de uma regressão sem a covariável, quando ela é preditiva.
```

O coeficiente associado ao indicador de tratamento é a estimativa ajustada
do efeito; comparar seu erro-padrão ao de uma regressão sem a covariável
mostra diretamente o ganho de precisão obtido.

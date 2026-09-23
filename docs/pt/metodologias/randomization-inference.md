# Inferência por randomização (teste de permutação)

## 1. Que problema isso resolve?

Testes estatísticos comuns (teste t, por exemplo) dependem de aproximações
que funcionam bem quando há muitas observações. Mas e quando um experimento
tem poucas unidades — poucas lojas, poucas cidades, poucas turmas — porque a
aleatorização aconteceu num nível agregado, não no nível de cada pessoa? Com
poucas unidades, essas aproximações deixam de ser confiáveis. A inferência
por randomização resolve isso sem depender de nenhuma aproximação: ela usa a
própria aleatoriedade do desenho do experimento para construir o teste.

## 2. Intuição

Se o tratamento foi atribuído por sorteio, existe um número finito e
conhecido de formas como esse sorteio poderia ter saído. A pergunta central
do método é: "entre todas as formas possíveis de sortear quem seria tratado,
que fração delas produziria um efeito tão grande quanto (ou maior que) o
efeito que eu de fato observei?" Se a resposta for "quase nenhuma", o
resultado observado é incomum o suficiente para ser evidência de um efeito
real, não apenas do sorteio que calhou de acontecer.

## 3. Explicação simples

O método reembaralha, entre as unidades disponíveis, todas as combinações
possíveis (ou uma amostra grande delas) de quem seria "tratamento" e quem
seria "controle", recalculando a estatística de interesse (geralmente a
diferença de médias) para cada reembaralhamento. Isso gera uma distribuição
inteira de resultados possíveis sob a hipótese de que o tratamento não teve
efeito nenhum. O valor-p é a fração dessa distribuição que é tão extrema
quanto o resultado realmente observado.

## 4. Exemplo conceitual fácil

Considere um experimento com apenas 4 lojas, das quais 2 serão sorteadas
para receber um novo layout de vitrine e 2 permanecerão como estão. Existem
exatamente $\binom{4}{2} = 6$ formas diferentes de escolher quais 2 lojas
recebem o tratamento. Cada uma dessas 6 formas produz uma diferença de
vendas diferente entre "tratamento" e "controle". A distribuição de
referência do teste é formada por essas 6 diferenças possíveis — nada mais.

## 5. Como funciona, em linhas gerais

1. Calcula-se a estatística observada (por exemplo, a diferença de médias
   entre o grupo tratado e o grupo controle, na atribuição real do
   experimento).
2. Enumeram-se todas as reatribuições possíveis de tratamento/controle entre
   as mesmas unidades (ou, quando o número de combinações é grande demais
   para enumerar, sorteia-se uma amostra grande de reatribuições, tipicamente
   milhares).
3. Para cada reatribuição, recalcula-se a mesma estatística, mantendo os
   valores observados de cada unidade fixos — só a rotulagem tratamento/
   controle muda.
4. O valor-p é a proporção dessas estatísticas recalculadas que é igual ou
   mais extrema que a estatística observada na atribuição real.

## 6. O que o resultado significa

Um valor-p baixo diz que a atribuição real do experimento produziu um
resultado incomum, comparado a todas as outras formas como o sorteio
poderia ter saído. Isso é evidência de que o tratamento teve efeito — sem
depender de nenhuma suposição sobre a forma da distribuição dos dados.

## 7. Como interpretar

A validade do método depende inteiramente de a atribuição ao tratamento
ter sido de fato aleatória (ou de o desenho permitir tratar as
reatribuições como igualmente prováveis). Diferente de testes que assumem
normalidade ou amostra grande, aqui a única suposição necessária é a
aleatoriedade real da atribuição — o que faz do método especialmente
confiável quando essa aleatoriedade é garantida, e especialmente
inadequado quando não é.

## 8. Quando é útil

Muito útil quando o número de unidades experimentais é pequeno — poucas
zonas geográficas, poucas lojas, poucas turmas — situação comum em
experimentos randomizados no nível de cluster (geografia, loja, unidade
organizacional), em que testes assintóticos tradicionais perdem
confiabilidade.

## 9. Cuidados importantes

Com poucas unidades, o número de reatribuições possíveis também é pequeno,
o que limita a granularidade do valor-p — com 4 lojas divididas 2 a 2, por
exemplo, o menor valor-p possível é 1/6 ≈ 0,167, nunca menor que isso,
mesmo com um efeito enorme. Esse é um limite estrutural do método com
amostras muito pequenas, não um defeito de implementação.

## 10. Um exemplo pequeno com números

Seis lojas participam de um experimento, três sorteadas para tratamento e
três para controle. As vendas semanais observadas são: 12, 15, 9, 22, 18, 11
(em milhares de reais), com as três primeiras sendo o grupo de tratamento na
atribuição real. A diferença de médias observada é
$(12+15+9)/3 - (22+18+11)/3 = 12{,}0 - 17{,}0 = -5{,}0$.

Existem $\binom{6}{3} = 20$ formas possíveis de escolher quais 3 lojas
seriam tratamento. Calculando a diferença de médias para cada uma das 20
combinações, obtém-se a distribuição de referência completa. Nesse exemplo,
6 das 20 combinações produzem uma diferença tão extrema quanto (ou mais
extrema que) −5,0 em valor absoluto — dando um valor-p bilateral de
6/20 = 0,30. Não é um resultado significativo: entre as 20 formas possíveis
de sortear o tratamento, uma diferença tão grande quanto a observada não é
particularmente incomum.

## 11. Exemplo de código simples

```python
import numpy as np
from itertools import combinations

vendas = np.array([12.0, 15.0, 9.0, 22.0, 18.0, 11.0])
tratamento_real = {0, 1, 2}  # índices das 3 lojas tratadas de fato

def diferenca(idx_tratamento, idx_controle):
    return vendas[list(idx_tratamento)].mean() - vendas[list(idx_controle)].mean()

todas_unidades = set(range(6))
diferencas = []
for combo in combinations(range(6), 3):
    combo = set(combo)
    diferencas.append(diferenca(combo, todas_unidades - combo))

diferencas = np.array(diferencas)
observada = diferenca(tratamento_real, todas_unidades - tratamento_real)
valor_p = np.mean(np.abs(diferencas) >= abs(observada))
print(valor_p)
```

![Distribuição de referência por permutação, com todas as 20 reatribuições possíveis e a diferença observada destacada](../../../assets/figures/randomization-inference-permutation-distribution-pt.png)

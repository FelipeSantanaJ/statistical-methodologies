# Decomposição de desigualdade (Theil, Gini, quantis ponderados)

## 1. Que problema isso resolve?

Quando se fala em "desigualdade de renda", é fácil pensar só em um número —
mas de onde vem essa desigualdade? Quanto dela é porque diferentes grupos
(por região, por gênero, por qualquer outro recorte) têm rendas médias
diferentes, e quanto é porque, dentro de cada grupo, já existe muita
variação entre quem ganha pouco e quem ganha muito? Essa família de
ferramentas — o índice de Theil, o índice de Gini, e quantis ponderados —
ajuda a responder essas perguntas.

## 2. Intuição

Pense em duas fontes de desigualdade que podem coexistir. Primeira: grupos
diferentes podem ter rendas médias diferentes entre si — isso é desigualdade
"entre grupos". Segunda: mesmo dentro de um único grupo, algumas pessoas
ganham muito mais que outras — isso é desigualdade "dentro do grupo". O
índice de Theil tem uma propriedade matemática valiosa: ele consegue separar
esses dois componentes de forma exata, sem sobra e sem dupla contagem. Já o
índice de Gini mede a concentração de renda dentro de uma única distribuição
(um grupo, ou a população toda), numa escala de 0 (igualdade perfeita) a 1
(um indivíduo com tudo, o resto com nada). Quantis ponderados são apenas
pontos de corte — "o que caracteriza os 10% mais ricos deste grupo?" — que
usam o peso amostral de cada observação para estimar corretamente esses
cortes numa pesquisa com amostragem complexa.

## 3. Explicação simples

O índice de Theil calcula, essencialmente, uma medida de dispersão baseada
em entropia — quanto mais desigual a distribuição, maior o índice. Sua
propriedade de decomponibilidade exata permite escrever:

$$
\text{Desigualdade total} = \text{Desigualdade entre grupos} + \text{Desigualdade dentro dos grupos}
$$

Essa soma não é uma aproximação — as duas partes somam exatamente o total.
O índice de Gini, por outro lado, não tem essa propriedade de
decomponibilidade exata da mesma forma simples — ele é calculado
separadamente para cada grupo (ou para a população como um todo), e serve
para comparar o quão concentrada é a distribuição dentro de cada recorte.

![Barra empilhada mostrando a divisão da desigualdade total de Theil entre a parcela "entre grupos" e a parcela "dentro dos grupos"](../../../assets/figures/inequality-decomposition-theil-pt.png)

## 4. Exemplo conceitual fácil

Imagine uma empresa com dois departamentos. Se todo mundo no Departamento A
ganhasse exatamente o mesmo salário, e todo mundo no Departamento B também
ganhasse um salário fixo (só que diferente do A), toda a desigualdade da
empresa viria da diferença entre os dois salários — 100% "entre grupos", 0%
"dentro dos grupos". Na prática, dentro de qualquer departamento real também
existe variação de salário entre as pessoas — e o índice de Theil separa
exatamente quanto da desigualdade total vem de cada uma dessas duas fontes.

## 5. Como funciona, em linhas gerais

1. Calcula-se o índice de Theil para a população inteira, uma medida de
   dispersão relativa da renda em relação à média.
2. Calcula-se o índice de Theil dentro de cada grupo separadamente (usando
   só as observações daquele grupo).
3. A parcela "entre grupos" é calculada como se cada pessoa dentro de um
   grupo recebesse a renda média do seu grupo — captura só a variação entre
   as médias dos grupos.
4. A parcela "dentro dos grupos" é a média ponderada (pela participação de
   cada grupo na renda total) dos índices de Theil calculados dentro de cada
   grupo.
5. As duas parcelas somadas reproduzem exatamente o índice de Theil total.
6. Paralelamente, o índice de Gini é calculado dentro de cada grupo para
   comparar concentração, e quantis ponderados são estimados dentro de cada
   grupo usando os pesos amostrais de cada observação.

## 6. O que o resultado significa

Se a parcela "entre grupos" for pequena em relação ao total, isso significa
que a maior parte da desigualdade de renda está distribuída dentro de cada
grupo, não entre eles — mesmo que a diferença média entre os grupos seja
grande e estatisticamente significativa. As duas coisas não se contradizem:
um gap entre grupos pode ser real e importante, e ainda assim representar
uma fração pequena da desigualdade total, porque a desigualdade dentro de
cada grupo também é grande.

## 7. Como interpretar

É um erro comum concluir que "só 7% da desigualdade vem da raça, então a
desigualdade racial não é importante". Isso confunde duas perguntas
diferentes: (1) o gap médio entre grupos é grande e significativo? e (2)
que fração da variância total de renda esse gap explica? A resposta à
primeira pergunta pode ser "sim, é grande e significativo" mesmo quando a
resposta à segunda é "uma fração pequena do total" — porque a desigualdade
dentro de cada grupo, por si só, já é enorme. Contextualizar o tamanho da
parcela "entre grupos" é importante, mas não anula a importância do gap em
si.

Da mesma forma, um Gini mais baixo num grupo não significa necessariamente
"situação melhor" — pode simplesmente refletir uma distribuição mais
comprimida perto da base, ou seja, todo mundo naquele grupo ganhando pouco
de forma relativamente parecida, o que é diferente de "renda alta e bem
distribuída".

## 8. Quando é útil

Quando você quer contextualizar o tamanho de um gap entre grupos dentro do
quadro geral de desigualdade — por exemplo, mostrar que, apesar de a maior
parte da desigualdade de renda estar dentro de cada grupo racial (não entre
eles), o gap entre grupos ainda é grande e estatisticamente robusto, e
merece atenção por si só.

## 9. Cuidados importantes

- A fração "entre grupos" tende a ser pequena quando os grupos comparados
  são muito amplos e heterogêneos internamente (como grandes categorias
  demográficas) — isso é esperado e não deve ser usado para minimizar o gap.
- O índice de Theil exige valores estritamente positivos da variável de
  interesse (não funciona diretamente com renda zero ou negativa sem
  ajustes).
- Ao comparar índices de Gini entre grupos, sempre verificar se as
  distribuições subjacentes são comparáveis (mesma unidade, mesmo período) e
  lembrar que Gini mais baixo não é sinônimo de "melhor".
- Quantis ponderados exigem o uso correto dos pesos amostrais da pesquisa —
  ignorar os pesos produz estimativas enviesadas quando a amostragem não é
  simples aleatória.

## 10. Um exemplo pequeno com números

Suponha uma população hipotética dividida em dois grupos:

- Grupo A: renda média = 4.000, Theil interno = 0,25.
- Grupo B: renda média = 2.800, Theil interno = 0,30.
- Grupo A representa 40% da renda total da população; Grupo B, 60%.

O índice de Theil "entre grupos" (calculado a partir da diferença das
médias, ponderada pela participação na renda) resulta em aproximadamente
0,04. O índice de Theil "dentro dos grupos" é a média ponderada dos dois
Theils internos: 0,4 × 0,25 + 0,6 × 0,30 = 0,28. Somando as duas partes, o
Theil total é aproximadamente 0,32.

Isso significa que a parcela "entre grupos" representa cerca de 0,04 / 0,32
≈ 12,5% da desigualdade total — a maior parte (87,5%) vem da desigualdade
que já existe dentro de cada grupo, mesmo com uma diferença de renda média
substancial entre os grupos (4.000 vs. 2.800, uma diferença de mais de 40%).

## 11. Exemplo de código simples

```python
import numpy as np

def theil_index(renda):
    renda = np.asarray(renda, dtype=float)
    media = renda.mean()
    return np.mean((renda / media) * np.log(renda / media))

def gini_index(renda):
    renda = np.sort(np.asarray(renda, dtype=float))
    n = len(renda)
    indices = np.arange(1, n + 1)
    return (2 * np.sum(indices * renda) - (n + 1) * np.sum(renda)) / (n * np.sum(renda))

# dados ilustrativos
grupo_a = np.array([...])  # rendas individuais, Grupo A
grupo_b = np.array([...])  # rendas individuais, Grupo B

theil_total = theil_index(np.concatenate([grupo_a, grupo_b]))
theil_a = theil_index(grupo_a)
theil_b = theil_index(grupo_b)

participacao_a = grupo_a.sum() / (grupo_a.sum() + grupo_b.sum())
participacao_b = 1 - participacao_a

theil_dentro = participacao_a * theil_a + participacao_b * theil_b
theil_entre = theil_total - theil_dentro

percentil_90_a = np.average(np.quantile(grupo_a, 0.9))  # com pesos amostrais, usar np.average ponderado
```

Para pesquisas com amostragem complexa (pesos, estratos, conglomerados),
bibliotecas como `samplics` em Python, ou o pacote `survey` em R, calculam
quantis e índices de desigualdade ponderados corretamente, incluindo seus
erros-padrão.

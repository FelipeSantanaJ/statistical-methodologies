# Visão geral — todas as metodologias, em linguagem simples

Este documento explica, sem fórmulas e sem jargão desnecessário, cada
metodologia estatística usada no portfólio. A ideia é simples: você não precisa
saber estatística para entender **que pergunta cada método responde** e **o que
ele te permite concluir** — e, tão importante quanto isso, **o que ele não te
permite concluir**.

Cada seção segue o mesmo roteiro: uma pergunta concreta, a ideia por trás do
método, o que o resultado quer dizer, e um limite importante.

Para uma explicação mais detalhada de qualquer um destes métodos, veja a pasta
[`metodologias/`](../metodologias/) (nível intermediário) ou
[`completo/`](../completo/) (nível técnico completo).

---

## 1. Teste t de Welch

**A pergunta:** dois grupos têm médias diferentes numa amostra. Essa diferença é
provavelmente real, ou pode ter surgido só por acaso, por causa da variação
natural de quem calhou de estar em cada amostra?

**A ideia:** se você sorteasse repetidamente pequenas amostras de duas
populações que na verdade têm a mesma média, ainda assim as médias amostrais
quase nunca sairiam idênticas. O teste mede o quão incomum é a diferença que
você observou, dado o tamanho das amostras e a variabilidade dentro de cada
grupo — sem exigir que os dois grupos tenham a mesma variabilidade interna, o
que o torna mais seguro que a versão clássica (Student) quando os grupos são
desiguais em tamanho ou dispersão.

**O que o resultado significa:** um valor-p baixo diz que uma diferença desse
tamanho seria rara se, na população, as médias fossem realmente iguais. Isso é
evidência a favor de uma diferença real — não prova de que ela seja grande ou
importante na prática.

**O que ele não diz:** por que a diferença existe, nem se ela é causada por
alguma coisa específica.

---

## 2. Decomposição de Oaxaca-Blinder

**A pergunta:** dois grupos ganham salários diferentes, em média. Quanto dessa
diferença vem do fato de os grupos terem, em média, características diferentes
(mais ou menos anos de estudo, por exemplo), e quanto sobra mesmo depois de
levar essas características em conta?

**A ideia:** o método ajusta um modelo estatístico que relaciona salário a
características observáveis para cada grupo separadamente, depois pergunta:
"se o Grupo B tivesse as mesmas características do Grupo A, mas continuasse
sendo pago do seu próprio jeito, qual seria a diferença esperada?" Isso separa
o gap em uma parte **explicada** (diferença de características) e uma parte
**não explicada** (o que sobra).

**O que o resultado significa:** a parte não explicada é o que não pode ser
atribuído às características medidas. Ela é, com frequência, interpretada
como um sinal possível de discriminação — mas essa conclusão exige suposições
muito mais fortes do que o método sozinho garante: pode haver características
relevantes que simplesmente não foram medidas.

**O que ele não diz:** o método não prova causalidade nem isola
discriminação — ele decompõe uma diferença observada, não explica sua origem
causal.

---

## 3. Decomposição por RIF (Recentered Influence Function)

**A pergunta:** o Oaxaca-Blinder decompõe a diferença nas **médias**. E se a
diferença entre grupos não for igual em todos os pontos da distribuição — se
for maior entre quem ganha pouco, ou entre quem ganha muito?

**A ideia:** em vez de olhar só a média, o método permite decompor a diferença
em qualquer ponto da distribuição — por exemplo, na mediana, ou no percentil
90. Ele faz isso transformando cada observação numa medida de "quanto ela
contribui" para aquele ponto específico da distribuição, e depois aplica a
mesma lógica do Oaxaca-Blinder sobre essa medida transformada.

**O que o resultado significa:** permite enxergar padrões que a média esconde
— por exemplo, um gap pequeno no meio da distribuição mas grande nas pontas.

**O que ele não diz:** cada ponto da distribuição é estimado com sua própria
margem de erro, geralmente maior nas pontas (onde há menos dados) — resultados
ali merecem mais cautela.

---

## 4. Decomposição de desigualdade (Theil, Gini, quantis ponderados)

**A pergunta:** quanto da desigualdade total de uma variável (renda, por
exemplo) vem de diferenças **entre** grupos, e quanto vem de diferenças
**dentro** de cada grupo?

**A ideia:** o índice de Theil tem uma propriedade matemática útil chamada
decomponibilidade exata: a desigualdade total pode ser separada, sem sobras,
em uma parcela "entre grupos" e uma parcela "dentro dos grupos". O Gini mede
concentração dentro de um grupo (quão distante aquele grupo está de uma
distribuição perfeitamente igual). Quantis ponderados estimam, dentro de cada
grupo, valores de corte como "o que caracteriza os 10% mais ricos daquele
grupo".

**O que o resultado significa:** é comum, em recortes demográficos amplos como
raça ou gênero, que a maior parte da desigualdade total esteja dentro de cada
grupo — isso não diminui a importância de um gap entre grupos que seja grande
e estatisticamente significativo; apenas mostra que a desigualdade tem várias
fontes ao mesmo tempo.

**O que ele não diz:** um Gini mais baixo num grupo não significa
necessariamente "situação melhor" — pode só refletir uma distribuição mais
comprimida perto da base.

---

## 5. Índice de dissimilaridade de Duncan

**A pergunta:** dois grupos estão distribuídos de forma parecida entre
diferentes categorias (ocupações, por exemplo), ou um grupo está concentrado em
certas categorias enquanto o outro está em outras?

**A ideia:** o índice mede, essencialmente, qual fração de um dos grupos
precisaria "trocar de categoria" para que as duas distribuições ficassem
idênticas. Um valor de zero significa distribuições idênticas; um valor de um
(ou 100%) significa segregação completa.

**O que o resultado significa:** um índice alto indica que os grupos
raramente ocupam as mesmas categorias — um sinal de segregação ocupacional,
por exemplo.

**O que ele não diz:** o índice não diz por que a segregação existe, nem
distingue entre concentração voluntária, barreiras de acesso, ou diferenças de
qualificação.

---

## 6. Teste de quebra estrutural

**A pergunta:** uma série ao longo do tempo mudou de padrão num momento
específico e conhecido — um evento, uma lei, uma crise?

**A ideia:** o método compara o comportamento da série antes e depois de uma
data pré-definida, testando se os dois pedaços parecem vir do mesmo processo ou
de processos diferentes.

**O que o resultado significa:** uma quebra significativa é evidência de que
algo mudou naquele momento — mas, se vários eventos aconteceram perto um do
outro (uma pandemia perto de uma reforma, por exemplo), o teste não consegue
sozinho dizer qual dos dois causou a mudança.

**O que ele não diz:** isso é evidência de correlação temporal, não de
causalidade — e um teste que olha só uma data pré-definida não é uma busca por
quebras desconhecidas em qualquer ponto da série.

---

## 7. Diferenças-em-diferenças

**A pergunta:** uma política ou evento teve efeito causal sobre um grupo
afetado, comparado a um grupo não afetado?

**A ideia:** compara a mudança ao longo do tempo no grupo afetado com a
mudança ao longo do tempo no grupo não afetado. Se os dois grupos já vinham
seguindo trajetórias parecidas antes do evento (as chamadas "tendências
paralelas"), a diferença nas mudanças pode ser atribuída ao evento. Testes de
placebo aplicam o mesmo raciocínio a datas falsas — se aparecer um "efeito"
mesmo numa data sem mudança real de política, isso é sinal de alerta.

**O que o resultado significa:** quando as tendências paralelas se sustentam e
o desenho é bem executado, o método tem uma leitura causal — mais forte que
uma simples comparação antes/depois.

**O que ele não diz:** "não encontramos efeito" não é o mesmo que "não há
efeito" — um desenho com poucos pontos de dado, ou amostra pequena, pode
simplesmente não ter força estatística para detectar um efeito real.

---

## 8. Análise de transições em painel

**A pergunta:** as pessoas de um grupo saem do desemprego, ou entram na
formalidade, mais rápido ou mais devagar que as de outro grupo?

**A ideia:** algumas pesquisas domiciliares entrevistam a mesma pessoa mais de
uma vez ao longo do tempo. Isso permite acompanhar transições individuais reais
(desempregado → empregado, por exemplo), em vez de só comparar retratos
isolados de momentos diferentes.

**O que o resultado significa:** taxas de transição diferentes entre grupos
mostram diferenças de mobilidade real, não só de composição num único
momento.

**O que ele não diz:** o pareamento entre entrevistas de uma mesma pessoa pode
falhar (troca de morador no domicílio, por exemplo) — a taxa de sucesso do
pareamento importa para a confiabilidade do resultado.

---

## 9. Testes A/B

**A pergunta:** uma mudança específica (num produto, num processo) realmente
melhora o resultado que importa, ou o que parece melhora é só ruído?

**A ideia:** divide-se aleatoriamente um grupo de pessoas em dois — metade vê
a versão nova, metade continua na versão antiga — e compara-se o resultado
médio entre os dois grupos, com um teste de significância e um intervalo de
confiança em volta do efeito estimado.

**O que o resultado significa:** como a divisão é aleatória, uma diferença
significativa entre os grupos pode ser atribuída à mudança testada, não a
outras diferenças entre as pessoas.

**O que ele não diz:** só vale se a randomização realmente funcionou — daí a
importância de sempre checar isso antes de confiar no resultado (ver o próximo
item).

---

## 10. Teste de Sample Ratio Mismatch (SRM)

**A pergunta:** a divisão entre os grupos do experimento realmente saiu como
planejada?

**A ideia:** se você planejou 50/50 mas o sistema, por algum bug, colocou 55%
das pessoas num grupo e 45% no outro, isso é sinal de que algo quebrou na
randomização — e qualquer efeito medido a partir daí não é confiável.

**O que o resultado significa:** um SRM significativo é um alarme: pare e
investigue antes de interpretar qualquer resultado do experimento.

**O que ele não diz:** o teste detecta que a proporção está errada, não diz
automaticamente por quê — isso exige investigação separada.

---

## 11. Checagem de balanceamento e ajuste por covariáveis

**A pergunta:** os dois grupos do experimento eram realmente parecidos antes de
a mudança ser aplicada?

**A ideia:** compara-se características que já existiam antes do experimento
(idade, histórico de uso, por exemplo) entre os dois grupos. Se estiverem
parecidas, a randomização funcionou. Essas mesmas características também podem
ser usadas para "limpar" um pouco do ruído da estimativa de efeito, deixando-a
mais precisa.

**O que o resultado significa:** grupos balanceados dão mais confiança de que
qualquer diferença de resultado veio da mudança testada, não de uma diferença
prévia entre os grupos.

**O que ele não diz:** balanceamento nas características medidas não garante
balanceamento em características não medidas.

---

## 12. Teste de não-inferioridade

**A pergunta:** uma métrica de segurança ou risco (por exemplo, taxa de fraude)
não piorou além de um limite aceitável?

**A ideia:** ao contrário de um teste comum, que pergunta "há alguma
diferença?", este pergunta apenas "essa métrica não piorou mais do que X?" —
numa única direção.

**O que o resultado significa:** quando o teste passa, há evidência de que a
métrica se manteve dentro do aceitável. Quando não passa, não significa
necessariamente que a métrica piorou muito — significa que não há evidência
suficiente de que ficou dentro da margem combinada.

**O que ele não diz:** a escolha da margem aceitável é uma decisão de negócio,
não estatística — o teste não diz qual margem é "certa".

---

## 13. Teste de heterogeneidade (interação) e efeito de novidade

**A pergunta:** o efeito de uma mudança é igual para todo mundo, ou maior para
alguns subgrupos? E o efeito se mantém ao longo do tempo, ou é só um "efeito
novidade" que passa?

**A ideia:** um teste formal de interação verifica se a diferença de efeito
entre subgrupos é grande o suficiente para não ser só ruído amostral. Olhar o
efeito ao longo das semanas depois do lançamento mostra se ele decai.

**O que o resultado significa:** encontrar um efeito concentrado num subgrupo
específico muda a decisão prática — pode-se lançar só para aquele subgrupo, em
vez de para todos.

**O que ele não diz:** testar muitos subgrupos aumenta a chance de encontrar
uma diferença "significativa" por acaso — um resultado de heterogeneidade
isolado merece mais cautela do que um confirmado por várias fontes de
evidência.

---

## 14. Erros-padrão robustos a cluster

**A pergunta:** e se as observações dentro de um mesmo grupo (uma loja, uma
região, uma unidade de pesquisa) não forem realmente independentes entre si?

**A ideia:** o cálculo comum de erro-padrão assume que cada observação é
independente. Quando várias observações vêm do mesmo cluster e se parecem
entre si, tratar todas como independentes faz o erro-padrão parecer menor do
que realmente é. O ajuste por cluster corrige isso.

**O que o resultado significa:** com o ajuste, o intervalo de confiança fica
mais largo (e mais honesto) do que seria sem ele.

**O que ele não diz:** com poucos clusters, mesmo o erro-padrão ajustado pode
não ser confiável — aí entram métodos alternativos (itens 15 e 16).

---

## 15. Inferência por randomização

**A pergunta:** com poucos grupos no experimento (poucas lojas, poucas
regiões), como confiar num valor-p calculado da forma tradicional?

**A ideia:** em vez de assumir uma fórmula teórica, o método reembaralha as
atribuições de tratamento/controle entre os grupos de todas as formas
possíveis (ou muitas delas), calculando o efeito em cada reembaralhamento. O
valor-p vem de comparar o efeito observado com essa distribuição de efeitos
"se a atribuição tivesse sido outra".

**O que o resultado significa:** é uma forma de inferência que não depende de
suposições sobre a distribuição dos dados — só da aleatoriedade da própria
atribuição.

**O que ele não diz:** exige que a atribuição ao tratamento tenha sido de fato
aleatória.

---

## 16. Bootstrap wild-cluster

**A pergunta:** outra forma de fazer inferência confiável com poucos clusters.

**A ideia:** em vez de reamostrar clusters inteiros (o que funciona mal quando
há poucos), o método reamostra os resíduos do modelo, multiplicando-os por
sinais aleatórios (+1 ou -1) por cluster, e reconstrói a estatística de teste
muitas vezes para formar uma distribuição de referência.

**O que o resultado significa:** costuma concordar com a inferência por
randomização quando ambos são aplicáveis — usar mais de um método e ver se
concordam é uma forma de checar a robustez da conclusão.

**O que ele não diz:** ainda depende de algumas suposições sobre o modelo
ajustado, mesmo sendo mais robusto que a fórmula clássica.

---

## 17. Poder estatístico e Efeito Mínimo Detectável (MDE)

**A pergunta:** antes de rodar um experimento, qual é o menor efeito que ele
tem chance real de detectar?

**A ideia:** depende do tamanho da amostra, da variabilidade da métrica e do
nível de confiança desejado. Calcular isso antes evita rodar um experimento
caro que nunca teria conseguido enxergar um efeito do tamanho que interessa.

**O que o resultado significa:** um MDE alto (comparado ao efeito que você
esperaria de forma realista) é um sinal de que o experimento, do jeito que
está desenhado, provavelmente não vai dar uma resposta útil.

**O que ele não diz:** não detectar efeito num experimento com MDE alto não
significa que não há efeito — só que o desenho não tinha força para ver.

---

## 18. Transbordamento espacial (canibalização)

**A pergunta:** o efeito positivo medido numa área tratada é ganho real, ou é
atividade "roubada" de áreas vizinhas de controle?

**A ideia:** compara áreas de controle que ficam perto de áreas tratadas com
áreas de controle mais distantes — se as próximas tiverem resultado pior, isso
sugere que parte do "efeito" positivo é só deslocamento, não criação líquida.

**O que o resultado significa:** ajuda a estimar o efeito líquido real de uma
intervenção, não só o efeito local aparente.

**O que ele não diz:** isolar completamente o transbordamento é difícil — o
método dá uma estimativa aproximada, não uma medição exata.

---

## 19. Decomposição de coorte / retenção

**A pergunta:** por que uma métrica agregada mudou de repente — o que
especificamente está causando isso?

**A ideia:** em vez de olhar só o número agregado, separa-se a base em
subgrupos (coortes de entrada, segmentos, canais) e compara-se como cada um
contribuiu para a mudança — muitas vezes revelando que várias causas
sobrepostas, não uma só, explicam o total.

**O que o resultado significa:** permite agir sobre a causa específica, em vez
de reagir ao sintoma agregado.

**O que ele não diz:** a decomposição é descritiva — dizer que um subgrupo
"contribuiu mais" não prova que ele foi a causa raiz sem investigação
adicional.

---

## 20. Decomposição de crescimento

**A pergunta:** o crescimento de um negócio veio de expansão para novos
lugares/produtos, ou de melhora real no que já existia?

**A ideia:** separa o crescimento total em uma parte de expansão (novos
mercados, novas lojas) e uma parte "comparável" (crescimento no que já
existia há tempo suficiente para comparação justa) — e depois, dentro do
comparável, separa quanto veio de preço, quanto veio de volume e quanto veio
de mudança no mix de produtos vendidos.

**O que o resultado significa:** um crescimento total impressionante pode
esconder uma base madura estagnada ou até encolhendo.

**O que ele não diz:** a decomposição não diz se a estratégia de expansão foi
uma boa escolha — só separa de onde o número total veio.

---

## 21. Regressão de Poisson (contagens, com efeitos fixos)

**A pergunta:** o que explica quantos gols um time marca — força do próprio
ataque, força da defesa adversária, e o fato de jogar em casa ou fora?

**A ideia:** para variáveis de contagem (número de eventos, como gols), a
regressão de Poisson modela essa contagem em função de fatores explicativos.
Efeitos fixos por time capturam a força específica de cada equipe, isolando o
efeito de interesse (jogar em casa, por exemplo).

**O que o resultado significa:** o coeficiente do fator de interesse,
transformado adequadamente, vira um fator multiplicativo — "jogar em casa
multiplica o número esperado de gols por X", já descontada a força dos times
envolvidos.

**O que ele não diz:** o modelo assume uma relação específica entre os fatores
e a contagem esperada — vale checar se essa suposição é razoável para os
dados em questão.

---

## 22. Tendência por mínimos quadrados ponderados

**A pergunta:** uma métrica está subindo, caindo, ou estável ao longo do
tempo, para cada unidade que estou comparando (um time, um clube, uma
região)?

**A ideia:** ajusta-se uma linha reta aos dados ao longo do tempo, dando mais
peso aos períodos com mais observações (mais confiáveis). Em vez de decidir
"subindo ou caindo" só olhando se a inclinação é positiva ou negativa, olha-se
o intervalo de confiança dessa inclinação: se o intervalo inteiro for
positivo, a tendência é de alta; se for inteiro negativo, é de queda; se
cruzar o zero, é considerada estável (não há evidência suficiente de
tendência).

**O que o resultado significa:** essa classificação evita declarar "tendência"
em cima de ruído — exige que a evidência seja forte o bastante para excluir a
hipótese de estabilidade.

**O que ele não diz:** com poucos períodos de dados, o intervalo de confiança
tende a ser largo, e a maioria das unidades acaba classificada como
"estável" simplesmente por falta de dados suficientes para decidir — isso não
é o mesmo que dizer que elas de fato não mudam.

---

## 23. Regressão logística

**A pergunta:** dado o valor de uma ou mais variáveis, qual é a probabilidade
de um desfecho binário acontecer — um cliente cancelar, um time cair, um
paciente responder a um tratamento?

**A ideia:** em vez de prever diretamente um número entre 0 e 1 (o que uma
regressão linear comum não garante), a regressão logística modela o
logaritmo da razão de chances do desfecho como uma combinação linear das
variáveis explicativas. Essa transformação garante que a probabilidade
prevista, ao ser convertida de volta, fique sempre entre 0 e 1 — o resultado
é uma curva em formato de S, achatada nos extremos e mais inclinada no meio.

**O que o resultado significa:** o coeficiente de cada variável, transformado
adequadamente, vira uma razão de chances — "cada ponto a mais nessa variável
multiplica a chance do desfecho por X". A qualidade do modelo como
classificador é avaliada à parte, tipicamente pela AUC (o quanto o modelo
separa quem teve o desfecho de quem não teve) e por validação fora da
amostra.

**O que ele não diz:** quando uma variável separa quase perfeitamente as duas
classes, a estimativa fica instável (quase-separação) — o sinal do efeito
continua valendo, mas o intervalo de confiança exige cautela. E um coeficiente
estatisticamente significativo não garante, sozinho, que o modelo classifique
bem — são perguntas diferentes.

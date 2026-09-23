# Teste de não-inferioridade

*Pressupõe os fundamentos de teste A/B — veja [Fundamentos de teste A/B](./ab-testing.md).*

## 1. Que problema isso resolve?

Nem toda métrica de um experimento é "quanto maior, melhor". Algumas são
métricas de guardrail: coisas que não podem piorar além de um certo ponto,
mesmo que a métrica principal melhore bastante — taxa de fraude, tempo de
carregamento, taxa de erro, reclamações de suporte. A pergunta nesse caso não
é "essa métrica mudou?", é mais específica: "essa métrica não piorou mais do
que eu consigo tolerar?". Um teste de duas pontas comum, desenhado para
perguntar se há qualquer diferença, não responde bem a essa pergunta —
porque ele trata "melhorou muito" e "não piorou muito" da mesma forma,
quando na prática só a segunda é o que importa para uma métrica de
guardrail.

## 2. Intuição

Pense na diferença entre dois tipos de pergunta. Um teste comum pergunta:
"essa métrica é diferente daquela?" — em qualquer direção. Um teste de
não-inferioridade pergunta algo mais estreito: "essa métrica não é pior que
aquela por mais de X?" — só numa direção, e permitindo explicitamente que
ela seja um pouco pior, até um limite definido como aceitável de antemão.
Essa margem X não é um número que a estatística escolhe; é uma decisão de
negócio, tomada antes do experimento, sobre quanto de piora é tolerável em
troca do que se ganha em outro lugar.

## 3. Explicação simples

Em vez de testar se a diferença é exatamente zero, testa-se se a diferença é
menor que a margem de não-inferioridade combinada — normalmente construindo
o intervalo de confiança da diferença e verificando se ele fica inteiramente
abaixo dessa margem (para uma métrica onde "maior é pior", como taxa de
fraude). Se o limite superior do intervalo de confiança estiver abaixo da
margem, há evidência de não-inferioridade. Se o intervalo cruzar a margem,
não há evidência suficiente — o que não significa necessariamente que a
métrica piorou muito, apenas que não dá para descartar essa possibilidade
com confiança.

![Estimativa pontual e intervalo de confiança da diferença de fraude, comparados à margem de não-inferioridade](../../../assets/figures/non-inferiority-margem-pt.png)

## 4. Exemplo conceitual fácil

Uma empresa lança um novo modelo de detecção de fraude, mais rápido, mas com
uma pequena chance de ser um pouco menos preciso. A equipe de risco define,
antes do experimento, que um aumento de até 0,5 ponto percentual na taxa de
fraude é aceitável, dado o ganho de velocidade. O experimento roda, e a
diferença observada na taxa de fraude entre o novo modelo e o modelo atual é
pequena, com um intervalo de confiança que fica inteiramente abaixo de 0,5
ponto percentual. Isso é evidência de não-inferioridade: mesmo sem provar que
o novo modelo é exatamente igual ou melhor, há confiança suficiente de que
ele não piora a fraude além do que foi definido como tolerável.

## 5. Como funciona, em linhas gerais

1. Define-se a margem de não-inferioridade antes do experimento — uma
   decisão de negócio, não estatística, sobre quanto de piora é tolerável.
2. Formulam-se as hipóteses de forma unilateral: a hipótese nula é que a
   métrica piorou mais do que a margem; a hipótese alternativa é que ela não
   piorou mais do que a margem.
3. Roda-se o experimento normalmente, coletando a diferença observada e seu
   intervalo de confiança, geralmente com um nível de confiança de um lado
   só (por exemplo, 95% unilateral, equivalente a um IC de 90% bilateral).
4. Compara-se o limite relevante do intervalo de confiança (o limite que
   indica "pior") com a margem definida.
5. Se esse limite estiver dentro da margem aceitável, conclui-se
   não-inferioridade.

## 6. O que o resultado significa

Concluir não-inferioridade significa que há evidência estatística de que a
métrica não piorou além da margem definida — não significa que a métrica é
igual, nem que ela melhorou. Um resultado inconclusivo (quando o intervalo de
confiança cruza a margem) significa apenas que a amostra não trouxe evidência
suficiente para descartar uma piora maior que a margem — não é o mesmo que
concluir que a métrica de fato piorou.

## 7. Como interpretar

A margem de não-inferioridade precisa ser definida antes de olhar os dados
do experimento e deve refletir um julgamento de negócio explícito: quanto
dessa métrica a organização está disposta a "gastar" em troca de outro
ganho. Não existe margem "estatisticamente correta" — ela é uma escolha, e
diferentes margens levam a diferentes conclusões sobre o mesmo dado. Também
vale lembrar que "não inferior" não é sinônimo de "sem custo" — mesmo dentro
da margem, uma piora pequena e consistente pode se acumular ao longo do
tempo ou de escala.

## 8. Quando é útil

Em qualquer experimento onde exista uma métrica de guardrail com um limite
de tolerância claro — segurança, risco, performance técnica, satisfação
mínima do cliente. É comum usá-lo em conjunto com um teste de efeito
tradicional sobre a métrica primária: a métrica principal é testada da forma
usual (há diferença?), enquanto métricas de guardrail são testadas por
não-inferioridade (a piora, se houver, está dentro do tolerável?).

## 9. Cuidados importantes

- A margem precisa ser fixada antes do experimento — escolher a margem
  depois de ver o resultado, para "fazer o teste passar", invalida a
  interpretação do teste.
- Um resultado de não-inferioridade não é o mesmo que "a métrica não
  mudou" — ela pode ter piorado um pouco, só que dentro do que foi
  considerado aceitável.
- Amostra pequena tende a produzir intervalos de confiança largos, que
  cruzam a margem mesmo quando o efeito real é pequeno — um resultado
  inconclusivo pede atenção ao poder estatístico do desenho, não conclusão
  apressada de que a métrica piorou.
- Vale checar a direção certa da margem: para métricas onde "maior é
  pior" (fraude, erro), a margem limita o quanto a métrica pode subir; para
  métricas onde "menor é pior" (satisfação, retenção), a lógica se inverte.

## 10. Um exemplo pequeno com números

Uma empresa testa um novo modelo de detecção de fraude contra o modelo
atual, com margem de não-inferioridade definida em 0,5 ponto percentual
(um aumento na taxa de fraude maior que isso seria inaceitável). A taxa de
fraude observada é 2,10% no grupo controle (modelo atual) e 2,02% no grupo
tratamento (modelo novo) — uma diferença de -0,08 ponto percentual (o novo
modelo teve fraude ligeiramente menor). O intervalo de confiança de 95% para
essa diferença fica aproximadamente entre -0,34 e +0,18 ponto percentual.
Como o limite superior do intervalo (+0,18) está bem abaixo da margem de
0,5 ponto percentual, conclui-se não-inferioridade: há evidência de que o
novo modelo não piora a fraude além do tolerável — e, nesse caso, a
estimativa central sugere até uma leve melhora, embora o intervalo não
permita afirmar isso com a mesma confiança que a não-inferioridade.

## 11. Exemplo de código simples

```python
import numpy as np
from statsmodels.stats.proportion import confint_proportions_2indep

margem = 0.5  # pontos percentuais; decisão de negócio, não estatística

fraude_controle = (252, 12000)   # ilustrativo: (casos, total)
fraude_tratamento = (242, 12000) # ilustrativo

ic_baixo, ic_alto = confint_proportions_2indep(
    fraude_tratamento[0], fraude_tratamento[1],
    fraude_controle[0], fraude_controle[1],
    method="wald",
)
ic_baixo_pp, ic_alto_pp = ic_baixo * 100, ic_alto * 100

nao_inferior = ic_alto_pp < margem
print(f"IC 95%: [{ic_baixo_pp:.2f}, {ic_alto_pp:.2f}] p.p. | margem: {margem} p.p.")
print(f"Não-inferioridade concluída: {nao_inferior}")
```

A decisão não depende de um valor-p único, mas de comparar o limite superior
do intervalo de confiança diretamente com a margem definida de antemão.

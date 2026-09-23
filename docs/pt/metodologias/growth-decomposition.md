# Decomposição de crescimento (total, comparável e preço-volume-mix)

## 1. Que problema isso resolve?

Uma rede de lojas fecha o trimestre com receita 12% maior que no ano anterior. A diretoria comemora — mas alguém pergunta: "esse crescimento veio de vender mais para os mesmos clientes, ou simplesmente de termos aberto oito lojas novas?" E, dentro do que já existia, "vendemos mais unidades, ou só aumentamos o preço?" Sem separar essas peças, um número de crescimento agregado pode esconder tanto uma operação saudável quanto uma que só está mascarando queda de volume com reajustes de preço.

## 2. Intuição

Crescimento total é uma soma de coisas muito diferentes: lojas novas que nunca existiram no período anterior, e lojas antigas que estavam lá nos dois períodos. Comparar isso tudo junto é como comparar o crescimento de peso de uma pessoa que fez academia com o de uma família que teve um bebê — o segundo número cresce por um motivo completamente diferente do primeiro.

## 3. Explicação simples

O método separa o crescimento em duas perguntas sucessivas:

**Pergunta 1 — de onde veio o crescimento?** Divide a receita total em lojas "comparáveis" (que existiam em ambos os períodos, também chamadas *like-for-like*) e lojas novas (aberturas, expansão geográfica). Só o crescimento comparável mede se o negócio que já existia está indo melhor.

**Pergunta 2 — dentro do crescimento comparável, o que mudou?** Decompõe em três efeitos: **preço** (os mesmos itens ficaram mais caros ou mais baratos), **volume** (vendeu-se mais ou menos unidades) e **mix** (a composição do que foi vendido mudou — por exemplo, mais itens de ticket alto no carrinho).

## 4. Exemplo conceitual fácil

Imagine uma cafeteria que vendia só um tipo de café a R$5. No mês seguinte, vende a mesma quantidade de xícaras, mas passou a cobrar R$5,50. A receita subiu — só por efeito **preço**, sem mudança de volume nem de mix. Agora imagine que, em vez disso, ela manteve o preço mas vendeu mais xícaras: isso é efeito **volume**. E se ela passou a vender mais itens de um combo mais caro (café + bolo) em vez do café avulso, isso é efeito **mix** — a composição das vendas mudou, mesmo que preço e volume unitário não tenham se alterado sozinhos.

## 5. Como funciona, em linhas gerais

1. Classifica cada unidade (loja, região, canal) como "comparável" — presente em ambos os períodos — ou "nova".
2. Calcula o crescimento total como a diferença de receita entre os dois períodos.
3. Isola a parcela vinda de unidades novas (receita das unidades que só existem no período mais recente).
4. O restante é o crescimento comparável — só entre unidades presentes nos dois períodos.
5. Dentro do crescimento comparável, decompõe a variação de receita em efeito preço (mantendo o mix e o volume de unidades fixos, variando só o preço médio), efeito volume (mantendo preço e mix fixos, variando a quantidade) e efeito mix (o resíduo, capturando mudança na composição do que é vendido).

Cada componente responde à pergunta "quanto teria sido o crescimento se só esse fator tivesse mudado, mantendo os outros constantes?" — por isso a soma dos três efeitos fecha exatamente o crescimento comparável total.

## 6. O que o resultado significa

Um crescimento total positivo pode conter uma base comparável estagnada ou até encolhendo, compensada por expansão geográfica. E um crescimento comparável positivo pode vir majoritariamente de preço (o que levanta a pergunta: até quando dá para repassar preço sem perder volume?) ou de volume real (sinal mais robusto de demanda).

## 7. Como interpretar

Volume subindo é geralmente o sinal mais saudável — indica demanda real crescendo. Preço subindo isoladamente, sem volume acompanhando, pode ser inflação repassada ou power de precificação, mas não é, sozinho, evidência de mais clientes ou mais consumo. Mix positivo pode indicar sucesso em upsell, ou simplesmente uma mudança na demanda do mercado que nada tem a ver com estratégia interna — vale investigar a causa antes de comemorar.

## 8. Quando é útil

Sempre que a métrica de crescimento reportada mistura fontes estruturalmente diferentes: expansão versus operação existente, preço versus quantidade. É a lógica por trás do "crescimento comparável" (*same-store sales*, *like-for-like*) usado em relatórios de varejo, redes de franquia e análises de portfólio de produtos — nesses contextos é comum usar exatamente esse tipo de decomposição para separar quanto da receita adicional veio de abrir novos pontos de venda versus vender mais nos pontos já existentes.

## 9. Cuidados importantes

- A decomposição preço-volume-mix depende da ordem em que os efeitos são calculados quando há interação entre eles (por exemplo, preço e volume mudando ao mesmo tempo) — diferentes convenções de cálculo produzem números ligeiramente diferentes para cada componente individual, embora a soma total seja sempre a mesma.
- "Comparável" precisa de uma definição consistente de janela de tempo (ex.: loja precisa estar aberta há pelo menos 12 meses completos) — mudar esse critério muda os números.
- Mix pode acabar sendo tratado como resíduo que absorve erros de mensuração dos outros dois efeitos; sempre checar se o valor de mix é plausível dado o contexto do negócio.

## 10. Um exemplo pequeno com números

Uma rede fictícia teve receita de R$48 milhões no ano anterior e R$53,2 milhões no ano atual — crescimento total de R$5,2 milhões (+10,8%). Dessas, R$3,6 milhões vieram de lojas novas abertas no período. O crescimento comparável foi, portanto, R$1,6 milhão. Decompondo esse valor: preço contribuiu com +R$2,1 milhões, volume com −R$1,4 milhão (queda de unidades vendidas nas lojas antigas) e mix com +R$0,9 milhão. Ou seja: o crescimento comparável só ficou positivo porque preço e mix compensaram uma queda real de volume — um sinal de alerta que o número agregado de +10,8% sozinho não mostrava.

![Decomposição em cascata do crescimento de receita](../../../assets/figures/growth-decomposition-waterfall-pt.png)

## 11. Exemplo de código simples

```python
import pandas as pd

# receita por loja, dois períodos, com quantidade vendida
df = pd.DataFrame({
    "loja": ["A", "B", "C", "D"],
    "comparavel": [True, True, True, False],  # D é loja nova
    "receita_anterior": [12.0, 15.0, 18.0, 0.0],
    "receita_atual": [12.8, 14.1, 19.7, 3.6],
    "qtd_anterior": [2400, 3000, 3600, 0],
    "qtd_atual": [2280, 2820, 3760, 720],
})

comp = df[df["comparavel"]]

receita_anterior_total = df["receita_anterior"].sum()
receita_atual_total = df["receita_atual"].sum()
crescimento_total = receita_atual_total - receita_anterior_total

crescimento_lojas_novas = df.loc[~df["comparavel"], "receita_atual"].sum()
crescimento_comparavel = (
    comp["receita_atual"].sum() - comp["receita_anterior"].sum()
)

preco_anterior = comp["receita_anterior"].sum() / comp["qtd_anterior"].sum()
preco_atual = comp["receita_atual"].sum() / comp["qtd_atual"].sum()

efeito_volume = (comp["qtd_atual"].sum() - comp["qtd_anterior"].sum()) * preco_anterior
efeito_preco = (preco_atual - preco_anterior) * comp["qtd_atual"].sum()
efeito_mix = crescimento_comparavel - efeito_volume - efeito_preco

print(f"Crescimento total: {crescimento_total:.2f}")
print(f"  Lojas novas: {crescimento_lojas_novas:.2f}")
print(f"  Comparável: {crescimento_comparavel:.2f}")
print(f"    Preço: {efeito_preco:.2f} | Volume: {efeito_volume:.2f} | Mix: {efeito_mix:.2f}")
```

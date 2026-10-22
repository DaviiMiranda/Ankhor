# O quadro de religação do bunker: árvore geradora mínima (Kruskal)

O puzzle do gerador do Bunker ([`../fases/bunker.md`](../fases/bunker.md), seção 3) é o problema clássico da **árvore geradora mínima**: ligar todos os pontos de um grafo gastando o mínimo de cabo.

---

## 1. No jogo

O quadro de religação mostra sete pontos do bunker e doze trechos de cabo possíveis, cada um com o comprimento em metros. O jogador liga e desliga trechos. O ponto acende quando a energia chega até ele, a partir do gerador. O carretel tem **23 m** de cabo: o quadro só religa quando **todos os pontos têm energia e o cabo usado cabe no carretel**.

| Trecho | m | Trecho | m |
|---|---|---|---|
| Elevador – Corredor A | 1 | Gerador – Elevador | 6 |
| Gerador – Corredor B | 2 | Corredor B – Corredor A | 7 |
| Corredor B – Comporta | 3 | Corredor A – Sala de dados | 8 |
| Corredor B – Elevador | 4 | Gerador – Comporta | 9 |
| Corredor A – Arsenal | 5 | Arsenal – Sala de dados | 10 |
| | | Comporta – Sala de dados | 11 |
| | | Elevador – Arsenal | 12 |

Ligar todos os trechos dá 78 m: tudo acende, mas passa do carretel.

---

## 2. A matemática

Um grafo com $n$ vértices é **conexo** quando existe caminho entre quaisquer dois vértices. Uma **árvore geradora** é um conjunto de arestas que deixa o grafo conexo **sem ciclos**; ela tem sempre $n - 1$ arestas (aqui, 6). A **árvore geradora mínima** é a de menor soma de pesos.

**Kruskal** constrói essa árvore de um jeito guloso:

1. Ordene as arestas do menor peso para o maior.
2. Percorra a lista. Pegue a aresta se ela liga dois pedaços **ainda separados**; se ela fecharia um ciclo (as duas pontas já estão no mesmo pedaço), pule.
3. Pare quando tiver $n - 1$ arestas.

No quadro:

| Aresta | m | O que acontece |
|---|---|---|
| Elevador – Corredor A | 1 | pega |
| Gerador – Corredor B | 2 | pega |
| Corredor B – Comporta | 3 | pega |
| Corredor B – Elevador | 4 | pega: junta {Gerador, Corredor B, Comporta} com {Elevador, Corredor A} |
| Corredor A – Arsenal | 5 | pega |
| Gerador – Elevador | 6 | pula: já estão no mesmo pedaço (fecharia um ciclo) |
| Corredor B – Corredor A | 7 | pula |
| Corredor A – Sala de dados | 8 | pega: 6 arestas, fim |

Total: $1 + 2 + 3 + 4 + 5 + 8 = 23$ m, exatamente o carretel.

**Por que só existe uma resposta.** Todos os pesos são diferentes, e com pesos distintos a árvore geradora mínima é **única**. Além disso, qualquer conjunto de trechos que liga tudo contém uma árvore geradora, que custa pelo menos 23 m. Se tiver qualquer trecho a mais, passa de 23. Então "ligar tudo com até 23 m" só é possível com a árvore mínima, e o jogo não precisa conferir a resposta: basta conferir a conexão e o comprimento.

**Por que o guloso funciona** (a propriedade do corte): para qualquer divisão dos vértices em dois grupos, a aresta mais leve que atravessa a divisão está em toda árvore geradora mínima. O Kruskal sempre pega a aresta mais leve que junta dois pedaços separados, então nunca erra.

---

## 3. No código

`scripts/sistemas/painel_religacao.gd`:

- `PONTOS` e `CABOS` são o grafo (vértices com a posição na tela e arestas com o peso).
- `arvore_minima()` é o Kruskal, com um **union-find** simples: cada ponto aponta para um "representante" do pedaço dele (`_raiz()`), e juntar dois pedaços é fazer um representante apontar para o outro.
- `pontos_alcancados()` espalha a energia a partir do gerador pelos trechos ligados (uma busca no grafo, repetida até nada mudar) e diz quantos pontos acenderam.
- O quadro religa quando `pontos_alcancados()` tem os sete pontos e `cabo_usado()` cabe no `carretel`. A marca `bunker_energia` libera o elevador e o arsenal.

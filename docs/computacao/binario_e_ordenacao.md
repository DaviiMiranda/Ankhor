# Puzzles de computação: sistema binário e ordenação por trocas

Dois puzzles do Centro de Convivência ([`../fases/centro_de_convivencia.md`](../fases/centro_de_convivencia.md), seção 8) são conteúdo de computação que o jogador resolve com as mãos: a **trava do plotter** da Gráfica Quântica (sistema binário) e a **arara inteligente** da Loja Universitária (ordenação e inversões).

---

## 1. A trava do plotter: números em binário

**No jogo.** O painel da trava tem 7 chaves, cada uma com um peso escrito embaixo: 64, 32, 16, 8, 4, 2 e 1. A etiqueta do plotter diz que o código é **quantos avisos ainda faltam imprimir** na ordem parada. A Ordem de Impressão diz que eram 4.000 e saíram 3.912, então faltam **88**. O jogador liga as chaves que somam 88 e confirma.

**A matemática.** Com $n$ chaves, a chave $i$ (contando da esquerda, de 0) vale $2^{n-1-i}$. Um conjunto de chaves ligadas $b_0 b_1 \dots b_{n-1}$ (1 = ligada) representa o número

$$v = \sum_{i=0}^{n-1} b_i \cdot 2^{\,n-1-i}$$

que é exatamente a leitura do número $b_0 b_1 \dots b_{n-1}$ na base 2. Todo inteiro de 0 a $2^n - 1$ tem **uma única** combinação de chaves (a representação binária é única), então existe uma só resposta. Para achá-la, o jogador faz o algoritmo guloso de sempre: liga a maior chave que ainda cabe e subtrai.

| Chave | 64 | 32 | 16 | 8 | 4 | 2 | 1 |
|---|---|---|---|---|---|---|---|
| Sobra antes | 88 | 24 | 24 | 8 | 0 | 0 | 0 |
| Ligada? | 1 | 0 | 1 | 1 | 0 | 0 | 0 |

$88 = 64 + 16 + 8 = 1011000_2$.

**No código** (`scripts/sistemas/painel_bits.gd`): `_peso(i)` é `1 << (quantidade_chaves - 1 - i)` (o deslocamento de bits, que multiplica por 2 a cada casa) e `_valor()` soma os pesos das chaves ligadas. Errar não tem castigo; com 7 chaves são 128 combinações, então chutar não compensa.

---

## 2. A arara inteligente: ordenação por trocas vizinhas

**No jogo.** A arara tem 5 moletons fora de ordem: **G, PP, GG, M, P**. O jogador escolhe um par de vizinhos e troca os dois, até ficar **PP, P, M, G, GG**. O painel conta as trocas e, no fim, mostra quantas o jogador usou e o mínimo possível.

**A matemática.** Numere os tamanhos (PP = 0, P = 1, M = 2, G = 3, GG = 4). A arara vira a sequência $a = (3, 0, 4, 2, 1)$. Uma **inversão** é um par de posições $i < j$ com $a_i > a_j$ (um maior antes de um menor). A arara começa com **6 inversões**:

$(3,0), (3,2), (3,1), (4,2), (4,1), (2,1)$.

Trocar dois **vizinhos** fora de ordem desfaz **exatamente uma** inversão (só o par trocado muda de ordem; a posição relativa dos outros não muda). Por isso:

- o número **mínimo** de trocas para ordenar é o número de inversões (aqui, 6);
- o jogador sempre consegue chegar nele: basta trocar só pares que estão fora de ordem (é o que o **Bubble Sort** faz);
- uma troca de um par que já estava em ordem **cria** uma inversão, e custa duas trocas a mais no total.

A arara ordenada é a sequência com 0 inversões. O painel verifica isso depois de cada troca.

**No código** (`scripts/sistemas/painel_ordenacao.gd`): `inversoes()` conta os pares com dois laços ($O(n^2)$, com $n = 5$ não precisa de mais), e a peça fica verde quando está na casa certa. O mínimo mostrado no fim é `inversoes()` da ordem inicial.

---

## 3. Os outros dois puzzles da fase

- **O cofre do bufê** (Self Nebulosa) é um código de 3 dígitos (`cofre.tscn`, ver [`../mecanicas/cofre_e_codigos.md`](../mecanicas/cofre_e_codigos.md)): as cubas do prato do dia, na ordem do cardápio, **619**.
- **O quadro do bar** (Churrasco Solar) é uma **ordem topológica** pequena. O checklist dá restrições de "vem antes": exaustor → grelha → geladeira, e o neon por último. Isso é um grafo dirigido sem ciclos (um DAG) com 4 vértices, e a ordem de ligar os disjuntores é uma ordenação topológica dele. Como as restrições formam uma cadeia, a ordem é única: exaustor (2), grelha (4), geladeira (1), neon (3). Errar desarma tudo e faz um estalo que os robôs ouvem pela mesma BFS de som dos passos (`ruido_ao_desarmar` no `QuadroEnergia`, em células de 16 px).

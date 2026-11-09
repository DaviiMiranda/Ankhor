# Cabos e energia: máscara de bits, BFS e busca com poda

O minigame da **Aranha 07** ([`../mecanicas/aranha_do_apagao.md`](../mecanicas/aranha_do_apagao.md)) é uma grade de peças de cabo que o jogador gira até a energia ir da central ao núcleo. O tabuleiro vem de `scripts/sistemas/grade_de_cabos.gd` (`GradeDeCabos`) e usa três ideias da disciplina: **representação binária** das peças, **BFS** para a energia e **busca em profundidade com retrocesso e poda** para garantir que o tabuleiro tem solução.

## 1. Cada peça é um número de 4 bits

Uma peça é um conjunto de lados abertos. Cada lado vale um bit:

| Lado | Norte | Leste | Sul | Oeste |
|---|---|---|---|---|
| Bit | `0001` (1) | `0010` (2) | `0100` (4) | `1000` (8) |

Os formatos ficam assim: reto (`N|S` = 5), curva (`N|L` = 3), T (`N|L|S` = 7), cruz (15), ponta (1) e vazio (0). Duas peças vizinhas **se ligam** quando o lado de uma que olha para a outra e o lado oposto da vizinha estão os dois abertos; é um `E` bit a bit.

## 2. Girar é um deslocamento circular

Girar 90° no sentido horário leva cada lado ao seguinte (N→L→S→O→N). Em bits, é um deslocamento de uma casa para a esquerda **com o bit que sai voltando pela direita**:

$$m' = ((m \ll 1) \mid (m \gg 3)) \mathbin{\&} 15$$

Exemplo: a curva `N|L` (`0011` = 3) vira `0110` (6) = `L|S`. A cruz (15) e o vazio (0) não mudam (girá-los não faz nada), o reto tem **2 posições** diferentes e a curva, o T e a ponta têm 4. Por isso o número de giros para acertar uma peça vai de 0 a 3 e, para o reto, fica em 0 ou 1.

## 3. A energia é uma BFS

Cada giro recalcula a energia: uma **busca em largura** parte da peça de entrada (coluna 0, na linha da central), **se ela estiver aberta para o oeste**, e visita cada vizinho a que a peça atual se liga (o lado que olha para a vizinha **e** o lado oposto dela abertos). As peças alcançadas são as **energizadas** (acendem em ciano) e a distância em passos desde a entrada vai para `distancias`, que o desenho usa para a onda de luz correr pelo cabo. O tabuleiro está **ligado** quando a peça da última coluna, na linha do núcleo, é alcançada **e** está aberta para o leste (para o núcleo).

BFS é a escolha certa aqui: em grafo não ponderado ela acha tudo o que é alcançável e a distância mínima de cada nó, em tempo $O(V + E)$ com $V$ no máximo 24 peças.

## 4. Garantir que existe solução: DFS com retrocesso e poda

Sortear peças ao acaso quase nunca dá um tabuleiro resolúvel. O gerador faz o contrário: **primeiro sorteia o caminho, depois monta as peças em volta dele**.

1. **Caminho.** A entrada e a saída são linhas sorteadas (a entrada na coluna 0 e a saída na última). Uma busca em profundidade sai da entrada e tenta chegar à saída por células ainda não usadas, sem repetir célula. A cada passo tenta as quatro direções **em ordem aleatória** (embaralhadas por Fisher-Yates, é o que dá variedade) e, se um galho não chega, **volta atrás** (retrocesso). Se chegar à saída com menos peças que o mínimo do nível, também volta atrás.
2. **Poda por distância de Manhattan.** Antes de descer, confere se ainda cabe: se as peças já postas mais a distância de Manhattan até a saída passam do máximo do nível, o galho é cortado, porque nem o caminho mais reto chegaria a tempo. Isso evita perder tempo em becos que nunca chegam. Se em 80 tentativas nenhum caminho aparecer (não aconteceu), o gerador cai numa linha reta pela primeira fileira.
3. **Peças certas.** Cada célula do caminho recebe a peça com os lados que ligam ao caminho anterior e ao seguinte; a primeira liga com a central (oeste) e a última com o núcleo (leste). As **células fora do caminho** recebem enfeites sorteados de `ENFEITES` (retos, curvas, Ts, cruz, pontas, vazios), que não resolvem nada mas confundem o olhar.
4. **Embaralhar.** Cada peça é girada de 0 a 3 vezes ao acaso. O tabuleiro só vale se **não estiver já ligado** e se o total de giros para resolver ficar entre **4** e **1,5 por peça do caminho** (arredondado para cima); senão, sorteia de novo, até 200 vezes. Esgotadas as 200, o jogo fica com o último sorteio (nos 12 mil tabuleiros medidos isso nunca aconteceu).

O teto de giros importa: sem ele, os piores sorteios pediam de 21 a 29 giros em 15 a 18 s, o que ninguém consegue. `MAXIMO_DE_GIROS_POR_PECA` (1,5) corta esses casos.

`giros_para_resolver()` soma, para cada peça do caminho, o número de giros até a posição certa (0 a 3; 0 ou 1 para o reto). É o que o teste usa para conferir a faixa e o que dá a coluna "giros" da tabela do minigame.

## 5. Resultado medido

Por nível, com 3 mil tabuleiros sorteados (script de teste no Godot, fora do repositório): **nenhum** sem solução, **nenhum** já ligado, **nenhum** fora da faixa de giros, e o pior sorteio levou menos de **0,5 ms**.

| Grade | Caminho (peças) | Giros: média | Giros: pior |
|---|---|---|---|
| 5 × 3 | 7 a 9 | 9,0 | 14 |
| 5 × 4 | 8 a 11 | 10,8 | 17 |
| 6 × 4 | 9 a 13 | 12,8 | 20 |
| 6 × 4 | 10 a 14 | 13,8 | 21 |

## Para a apresentação

- **Estrutura de dados:** a grade é um vetor de inteiros de 4 bits, com índice $i = linha \cdot colunas + coluna$.
- **Operação com bits:** o giro é um `rotate left` de 4 bits.
- **Grafos:** a grade é um grafo em que cada peça é um vértice e as arestas dependem da rotação; a BFS descobre a componente conexa da central.
- **Algoritmos:** DFS com retrocesso e poda (branch and bound simples) para construir; BFS para avaliar.

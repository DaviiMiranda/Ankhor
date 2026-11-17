# Fila, pilha, grafo em grade e arranjos — o Corredor do Tempo

O Corredor do Tempo (Labirinto) tem quatro salinhas, cada uma com uma coisa dos anos 80 que o jogador precisa acertar antes que o relógio zere. Cada uma usa uma ideia diferente de computação ou de matemática. A mecânica está em [`../mecanicas/corredor_do_tempo.md`](../mecanicas/corredor_do_tempo.md).

| Sala | Puzzle | Conteúdo |
|---|---|---|
| Jogos | Genius | **fila** (FIFO) e crescimento exponencial ($4^n$) |
| Micros | digitar o comando | **pilha** (LIFO) e comparação de cadeias |
| Telefone | girar cabos até ligar a central ao telefone | **grafo** em grade, **máscaras de bits** e **busca em largura** (BFS) |
| Filmes | ano de cada quadro | **arranjos** simples |

---

## 1. Fila (Genius)

O Genius mostra uma sequência de cores, e o jogador repete **na mesma ordem**: a primeira cor que entrou é a primeira que precisa sair. É uma **fila** (*first in, first out*). No código, a sequência é um `Array[int]` e um índice `_posicao` aponta a próxima cor esperada: cada tecla certa avança o índice, e a rodada fecha quando ele chega ao fim. Uma tecla errada desconta 5 s, e a mesma sequência é mostrada de novo.

**Por que fica difícil tão rápido:** com 4 cores, uma sequência de $n$ cores pode ser uma de $4^n$ possibilidades. As rodadas têm 3, 4 e 5 cores:

$$4^3 = 64 \qquad 4^4 = 256 \qquad 4^5 = 1024$$

Cada cor a mais multiplica por 4 as sequências possíveis: crescimento **exponencial**. Como no brinquedo, a sequência da rodada seguinte é a mesma com uma cor sorteada no fim (`append`), e as luzes ficam 15% mais rápidas por rodada (de 0,45 s acesas para 0,38 s e 0,33 s).

Os tons são os do Genius/Simon original, 415, 311, 252 e 209 Hz, gerados em `gerar_efeitos_corredor_tempo.py`.

## 2. Pilha e comparação de cadeias (micro)

A tela verde do micro pede três comandos, em ordem: `LOAD ANCORA`, `LIST` e `RUN`. O que o jogador digita é uma **pilha** de caracteres (*last in, first out*): cada tecla empilha uma letra no fim (`_digitado += letra`), e o **Backspace desempilha** a última (`_digitado.left(-1)`). Não dá para apagar uma letra do meio sem apagar as que vieram depois, que é exatamente o comportamento de uma pilha.

O `Enter` executa: a linha digitada é comparada com o comando esperado (`strip_edges()` tira os espaços das pontas, e as letras já entram em maiúscula). Igual, o micro responde (`SEARCHING FOR ANCORA`, `LOADING`, `READY.`) e pede o próximo. Diferente, responde `?SYNTAX ERROR`, como os BASIC dos anos 80, e desconta 5 s; o comando continua o mesmo.

As teclas do painel são lidas em `_input`, que roda antes do `_unhandled_input` de todo o resto do jogo. Assim, digitar `N` ou `I` não abre o caderno nem o inventário, e o `E` de `LOAD` não conta como "interagir".

## 3. Grafo em grade, bits e BFS (telefone)

O jogador liga a **central** (à esquerda) ao **telefone** (à direita) girando peças de cabo numa grade de 7 × 5. Cada peça só gira 90° para a direita (`E`); o tabuleiro é o mesmo problema de "encanamento" de jogos como *Pipe Mania*.

**A peça é um número de 4 bits.** Cada lado da peça é um bit: norte = 1, leste = 2, sul = 4, oeste = 8. A peça é a soma dos lados que ela liga:

| Peça | Lados | Máscara |
|---|---|---|
| reta | norte + sul | $1 + 4 = 5$ |
| curva | norte + leste | $1 + 2 = 3$ |
| T | norte + leste + sul | $1 + 2 + 4 = 7$ |
| cruz | os quatro | $15$ |
| ponta | norte | $1$ |
| vazio | nenhum | $0$ |

**Girar é deslocar os bits.** Girar 90° para a direita leva o norte para o leste, o leste para o sul, o sul para o oeste e o oeste para o norte: é um deslocamento circular de 1 bit para a esquerda, dentro de 4 bits:

$$m' = \big((m \ll 1) \mathbin{|} (m \gg 3)\big) \mathbin{\&} 15$$

Ex.: a curva norte+leste ($0011_2 = 3$) vira leste+sul ($0110_2 = 6$). Girar duas vezes dá o lado oposto, e é assim que o código acha "o lado do vizinho que me olha de volta" (`_oposta`). A reta só tem 2 posições distintas ($5 \to 10 \to 5$), e a cruz e o vazio não mudam nunca (o jogo nem gasta o giro nelas).

**A grade é um grafo.** Cada célula é um vértice. Duas células vizinhas estão ligadas (há uma aresta) quando o lado de uma que aponta para a outra **e** o lado da outra que aponta de volta estão ligados, ou seja, as duas pontas de cabo se encontram. Cabo que aponta para a parede ou para uma peça que não encosta nele não liga nada.

**O sinal é uma busca em largura (BFS).** O jogo começa da célula da central (se ela tem lado oeste) e visita os vizinhos ligados, depois os vizinhos desses, e assim por diante, com uma fila (`pop_front` e `append`). As células visitadas são as que ficam **verdes**: é o sinal chegando. Com $V = 35$ células e no máximo 4 arestas por célula, a busca custa $O(V + E)$, e roda a cada giro. A linha está ligada quando o sinal alcança a célula do telefone **e** ela tem o lado leste.

**Como o tabuleiro é sorteado (e por que sempre tem solução).**

1. Sorteia a linha da central e a do telefone.
2. Sorteia um **caminho sem repetir célula** da central ao telefone com **busca em profundidade com volta atrás** (`_estender`): a cada passo, tenta os 4 lados em ordem aleatória, e se um beco não leva à saída, desfaz o último passo e tenta outro. É o mesmo método que sorteia o labirinto do Labirinto (`docs/fases/labirinto.md`, seção 2).
3. O caminho precisa ter de **11 a 15 células**. Para a busca não perder tempo, ela **poda**: se o caminho já tem $n$ células e a distância de Manhattan até a saída é $d$ (quantos passos, no mínimo, ainda faltam), então $n + d > 15$ não serve e a busca volta na hora.
4. Cada célula do caminho recebe a peça que liga o lado de onde o caminho veio ao lado para onde ele vai: **reta** se os dois lados são opostos, **curva** se são vizinhos. As outras células recebem uma peça **enfeite** sorteada (reta, curva, T, cruz, ponta ou vazio) para confundir.
5. Gira cada peça um número sorteado de vezes (de 0 a 3). Se por azar o tabuleiro já estiver ligado, sorteia os giros de novo.

Como o caminho foi desenhado antes de embaralhar, **sempre há solução**: basta girar cada peça do caminho de volta. Um teste com 20 000 tabuleiros sorteados confirmou 0 sem solução e 0 já ligados, e o pior tempo de geração foi cerca de 2 ms.

**Paridade (curiosidade para a apresentação).** A grade é **bipartida**: pintando as células como um tabuleiro de xadrez, cada passo troca de cor. Por isso, o número de passos de um caminho entre duas células tem sempre a mesma paridade que a distância de Manhattan entre elas: se a central e o telefone ficam em linhas de mesma paridade, o caminho tem 6 passos horizontais mais um número par de passos verticais, e as células do caminho são 11, 13 ou 15 (nunca 12 ou 14); se as paridades diferem, são 12 ou 14. O sorteio respeita isso sozinho, porque só aceita caminhos que realmente chegam à saída.

**Quanto trabalho dá.** Uma curva tem 4 posições, e o número de giros para pô-la certa é 0, 1, 2 ou 3 (média 1,5); uma reta tem 2 posições (0 ou 1, média 0,5). Num caminho típico de 14 células, medido no mesmo teste, são uns **15 giros** (mais o movimento do cursor), umas 30 teclas no total. Sem a dica do sinal verde, o jogador teria de adivinhar a ordem das peças de um espaço de até $4^{35} \approx 1{,}2 \times 10^{21}$ posições; com a BFS desenhada, ele resolve **da central para o telefone, uma peça de cada vez**, e a busca vira linear.

## 4. Arranjos (filmes: os quadros de De Volta para o Futuro)

São três quadros e cinco anos para escolher: **1985, 1987, 1989, 1990 e 1991**. Três estão certos (os lançamentos das partes I, II e III) e dois são falsos. Cada ano serve a um quadro só.

**Quantas respostas existem?** Dar um ano diferente a cada quadro é um **arranjo simples** de 5 elementos tomados 3 a 3:

$$A(5, 3) = \frac{5!}{(5-3)!} = 5 \cdot 4 \cdot 3 = 60$$

Só uma das 60 está certa. Se o jogo só dissesse "certo" ou "errado" depois de os três anos estarem escolhidos, chutar teria 1 chance em 60.

**Por que a dica por quadro muda tudo:** o painel confere **um quadro por vez**, e o ano que já acertou sai das opções. Assim, o primeiro quadro tem 5 anos possíveis, o segundo 4 e o terceiro 3. A conta deixa de ser um **produto** e vira uma **soma**:

$$\underbrace{5 \cdot 4 \cdot 3 = 60}_{\text{conferir tudo junto}} \qquad \text{contra} \qquad \underbrace{5 + 4 + 3 = 12}_{\text{conferir um por vez}}$$

No pior caso são 12 tentativas, das quais 9 erradas (4 + 3 + 2), ou seja, 45 s de castigo. Chutando sem repetir ano, o ano certo está numa posição qualquer entre as $n$ opções, então a média é $(n+1)/2$ tentativas por quadro: $3 + 2{,}5 + 2 = 7{,}5$ tentativas, umas 4,5 erradas (cerca de 22 s). Quem lê as etiquetas das fitas na mesa acerta de primeira, mas gasta o tempo da leitura. É a mesma ideia de por que uma senha não deve dizer qual letra está errada: conferir as partes separadamente transforma a multiplicação em soma.

No código, `_ano_usado(opcao)` diz se o ano já foi dado a um quadro travado, e o cursor pula esses anos. Ele anda em círculo pelas opções com `posmod(i + passo, 5)`, o resto da divisão que nunca dá negativo: da última opção, a seta para a direita volta à primeira.

## 5. O relógio do corredor

- **Progresso:** com $p = $ tempo gasto / tempo total $\in [0, 1]$, o relógio anda em $p$ de 0 a 1. Até 2026-11-08 a curva $p^{1{,}6}$ também empurrava a barra de ansiedade; a ansiedade saiu do jogo e $p$ só guia o tique-taque.
- **Tique-taque:** o intervalo entre tiques é a interpolação linear $\text{lerp}(1{,}0;\ 0{,}22;\ p^{1{,}3})$ segundos.

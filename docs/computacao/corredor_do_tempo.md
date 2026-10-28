# Fila, pilha, pulsos e arranjos — o Corredor do Tempo

O Corredor do Tempo (Labirinto) tem quatro salinhas, cada uma com uma coisa dos anos 80 que o jogador precisa acertar antes que o relógio zere. Cada uma usa uma ideia diferente de computação ou de matemática. A mecânica está em [`../mecanicas/corredor_do_tempo.md`](../mecanicas/corredor_do_tempo.md).

| Sala | Puzzle | Conteúdo |
|---|---|---|
| Jogos | Genius | **fila** (FIFO) e crescimento exponencial ($4^n$) |
| Micros | digitar o comando | **pilha** (LIFO) e comparação de cadeias |
| Telefone | discar 1876 no disco | discagem por **pulsos** e ângulos |
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

## 3. Discagem por pulsos (telefone)

O jogador disca no telefone de disco o ano do primeiro telefone, **1876** (a dica é o selo do centenário, carimbado em 1976: cem anos antes).

Num telefone de disco, cada número manda uma quantidade de **pulsos** para a central: o 1 manda 1, o 2 manda 2… e o 0 manda **10**, por isso fica depois do 9 no disco. A central conta os pulsos para saber o número. O jogo imita isso:

- **Onde fica cada furo:** com o batente a $60°$, o furo de um número que manda $p$ pulsos fica a $60° - p \cdot 30°$. O 1 fica logo ao lado do batente, e o 0 dá quase uma volta inteira.
- **Discar:** o disco gira $p \cdot 30°$ no sentido horário (o furo chega ao batente) e volta sozinho a 10 pulsos por segundo, como os aparelhos de verdade. A cada $30°$ de volta toca um clique: $\lceil \text{giro} / 30° \rceil$ diminuiu, então passou um pulso.
- **Quanto demora:** a volta de um número com $p$ pulsos leva $p \times 0{,}1$ s. Discar 1876 manda $1 + 8 + 7 + 6 = 22$ pulsos, 2,2 s só de volta. Um número cheio de zeros e noves demoraria muito mais, e com o relógio correndo isso pesa.

Errar o ano mostra "NÚMERO INEXISTENTE", desconta 5 s e limpa o que foi discado.

## 4. Arranjos (filmes: os quadros de De Volta para o Futuro)

São três quadros e cinco anos para escolher: **1985, 1987, 1989, 1990 e 1991**. Três estão certos (os lançamentos das partes I, II e III) e dois são falsos. Cada ano serve a um quadro só.

**Quantas respostas existem?** Dar um ano diferente a cada quadro é um **arranjo simples** de 5 elementos tomados 3 a 3:

$$A(5, 3) = \frac{5!}{(5-3)!} = 5 \cdot 4 \cdot 3 = 60$$

Só uma das 60 está certa. Se o jogo só dissesse "certo" ou "errado" depois de os três anos estarem escolhidos, chutar teria 1 chance em 60.

**Por que a dica por quadro muda tudo:** o painel confere **um quadro por vez**, e o ano que já acertou sai das opções. Assim, o primeiro quadro tem 5 anos possíveis, o segundo 4 e o terceiro 3. A conta deixa de ser um **produto** e vira uma **soma**:

$$\underbrace{5 \cdot 4 \cdot 3 = 60}_{\text{conferir tudo junto}} \qquad \text{contra} \qquad \underbrace{5 + 4 + 3 = 12}_{\text{conferir um por vez}}$$

No pior caso são 12 tentativas, das quais 9 erradas (4 + 3 + 2), ou seja, 45 s de castigo. Chutando sem repetir ano, o ano certo está numa posição qualquer entre as $n$ opções, então a média é $(n+1)/2$ tentativas por quadro: $3 + 2{,}5 + 2 = 7{,}5$ tentativas, umas 4,5 erradas (cerca de 22 s). Quem lê as etiquetas das fitas na mesa acerta de primeira, mas gasta o tempo da leitura. É a mesma ideia de por que uma senha não deve dizer qual letra está errada: conferir as partes separadamente transforma a multiplicação em soma.

No código, `_ano_usado(opcao)` diz se o ano já foi dado a um quadro travado, e o cursor pula esses anos. Ele anda em círculo pelas opções com `posmod(i + passo, 5)`, o resto da divisão que nunca dá negativo: da última opção, a seta para a direita volta à primeira.

## 5. O relógio do corredor e a ansiedade

- **Pressão:** com $p = $ tempo gasto / tempo total $\in [0, 1]$, a pressão sobre a ansiedade é $p^{1{,}6}$. A curva cresce devagar no começo e rápido no fim: com metade do tempo gasto a pressão é 0,33; com 90%, 0,84. É o "quanto menor o tempo, maior a ansiedade".
- **Tique-taque:** o intervalo entre tiques é a interpolação linear $\text{lerp}(1{,}0;\ 0{,}22;\ p^{1{,}3})$ segundos.
- **Piso da ansiedade:** a barra é atualizada como antes (sobe com robôs por perto, desce longe deles) e, no fim, `valor = max(valor, pressão)`.

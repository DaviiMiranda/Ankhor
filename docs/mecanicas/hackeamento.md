# Hackeamento de portas

O **notebook** abre portas trancadas com um minigame. Perto de uma porta trancada (44 px), a tecla do espaço do notebook gasta 25% da bateria e abre a tela do minigame. O jogo fica pausado enquanto ela está aberta.

- **Vencer:** a porta destranca (e continua destrancada na sessão).
- **Perder:** aviso "Hack falhou". A bateria já foi gasta e dá para tentar de novo.
- **Esc:** cancela. A bateria também já foi gasta.

Robôs ainda usam o hack por tempo (2,5 s). Só as portas têm minigame por enquanto.

## Nós de controle (Labirinto)

O Labirinto usa o mesmo notebook e os mesmos minigames em **nós de controle** (`cenas/sistemas/no_hackeavel.tscn`, script `no_hackeavel.gd`, que herda de `Porta`): terminais de console dentro de salões de uma entrada só. Diferenças em relação à porta:

- **Não gasta bateria** do notebook (`gasto_hack = 0`): a fase não pode travar por falta de carga, e o jogador pode errar à vontade (o perigo é o robô, não a bateria). O notebook funciona mesmo com a bateria zerada.
- O jogo continua pausado enquanto o minigame está aberto.
- Cada nó tem uma luz que passa do vermelho ao verde quando é invadido.
- A dificuldade sobe do primeiro ao terceiro nó: **fácil, médio, difícil** (tipo aleatório).
- `rede_do_labirinto.gd` conta os nós (marcas `labirinto_no_1`, `_2`, `_3`), avisa "Nó N de 3 invadido" e, no terceiro, marca `labirinto_saida_liberada`, toca a transmissão `zane_labirinto_01` e destrava a saída.

## Dificuldade e escolha do minigame

Cada `Porta` tem dois campos no Inspetor:

| Campo | Valores |
|---|---|
| `dificuldade_hack` | Fácil, Médio, Difícil |
| `minigame_hack` | Aleatório, Sequência, Sincronia |

## Sequência

Quatro setas acendem em ordem. Depois, o jogador repete com as setas ou WASD. Errar gasta uma falha e a sequência é mostrada de novo.

| | Fácil | Médio | Difícil |
|---|---|---|---|
| Tamanho | 4 | 6 | 8 |
| Tempo de cada seta acesa | 0,70 s | 0,50 s | 0,32 s |
| Falhas permitidas | 3 | 2 | 1 |

## Sincronia

Um cursor vai e volta numa barra. Apertar `E` (ou Enter) dentro da zona verde conta um acerto, a zona muda de lugar e o cursor fica 12% mais rápido. Apertar fora gasta uma falha.

| | Fácil | Médio | Difícil |
|---|---|---|---|
| Acertos necessários | 3 | 4 | 5 |
| Largura da zona | 24% | 15% | 9% |
| Velocidade inicial (barras por segundo) | 0,9 | 1,3 | 1,8 |
| Falhas permitidas | 3 | 2 | 1 |

## Onde está o código

| O quê | Onde |
|---|---|
| Enums de dificuldade e tipo | `scripts/sistemas/hackeamento.gd` |
| Tela que hospeda o minigame (pausa, Esc, resultado) | `cenas/interface/tela_hackeamento.tscn` |
| Nó de controle (alvo do notebook, sem gasto de bateria) | `scripts/sistemas/no_hackeavel.gd` e `cenas/sistemas/no_hackeavel.tscn` |
| Base dos minigames | `scripts/interface/hackeamento/minigame_hack.gd` |
| Sequência e Sincronia | `scripts/interface/hackeamento/minigame_sequencia.gd`, `minigame_sincronia.gd` e as cenas em `cenas/interface/hackeamento/` |

Para criar outro minigame: estenda `MinigameHack`, implemente `preparar()`, `tratar_entrada()` e chame `finalizar(sucesso)`; depois inclua a cena em `CENAS` de `tela_hackeamento.gd` e um valor em `Hackeamento.Tipo`.

## Para testar

Na `sala_teste` há seis portas trancadas, da esquerda para a direita: Sequência fácil, médio, difícil e Sincronia fácil, médio e difícil (a última fica depois da porta dos robôs). Pegue o notebook, equipe e use perto de cada uma.

# A Aranha 07 e o apagão

Um evento que se repete na **ala do escritório** (a fase do Zane, no Labirinto): as luzes da sala apagam, uma robô-aranha aparece longe e vem andando devagar na direção do Zane, e ele tem poucos segundos para **hackear** o núcleo dela antes que ela chegue. Hackeou, ela some e a luz volta. Falhou, ela alcança o Zane, tira **1 coração** e some também. Acontece **algumas vezes** durante a fase.

A Aranha 07 **não está no Enredo** nem na ficha dos robôs: é um robô a mais que o Davi pediu para a fase. Ela segue a regra do mundo (um robô do Carlos), mas é um evento, não uma patrulha. A decisão está registrada em [`../decisoes.md`](../decisoes.md).

## Como corre um evento

| # | Fase | O que acontece |
|---|---|---|
| 1 | **Espera** | Entre 20 e 40 s sem nada. O relógio só corre quando o Zane está vivo, no controle, **sem diálogo aberto**, sem outra tela em tempo real aberta e sem nenhum robô da sala perseguindo. |
| 2 | **Apagão** | O som de corrente cortada toca, a luz da sala pisca, a escuridão fica quase preta e as luzes do cenário somem. Os **outros robôs da sala param** (`fator_de_velocidade = 0`) durante todo o evento. Passa 1 s de escuro. |
| 3 | **Aproximação** | A Aranha aparece com um piscar a **150 px** do Zane (ou menos, se o chão não der), vista só pelo brilho dos olhos vermelhos, e anda em linha reta. O Zane fica parado e a **tela de hack** abre no topo. O aviso diz "Apagão! Hackeie a Aranha antes que ela chegue." |
| 4a | **Hack feito** | A tela mostra "NÚCLEO 07 DOMINADO", a Aranha pisca e some, e a luz volta com um clarão de religar. Não custa vida. |
| 4b | **Tempo esgotado** | A Aranha dá o bote, a tela mostra "SEM TEMPO", o Zane perde **1 coração** (`Vida.receber_dano`) e ela some. A luz volta do mesmo jeito. |
| 5 | **Depois** | O Zane volta a andar, os robôs voltam ao que faziam e a espera recomeça, com no mínimo 25 s desde o fim do evento. |

**O relógio é um só.** O tempo que a barra do hack mostra **é** a distância que falta para a Aranha chegar, dividida pela velocidade dela (`AranhaDoApagao.segundos_restantes()`). Por isso a barra e a aranha andam juntas, e a aranha cresce na tela conforme chega (escala de 45% a 100% do tamanho final).

## Quantas vezes e quando para

- No máximo **4 eventos** por jogo (`eventos_maximos`). A conta fica em `Progresso`, nas marcas `escritorio_aranha_1` a `escritorio_aranha_4`: sair da sala ou morrer e voltar ao checkpoint não zera.
- O evento vale nas **quatro salas** (Recepção, Arquivo, Reuniões e Segurança) e o intervalo mínimo entre dois eventos vale para a ala toda, não por sala.
- Com as **três travas soltas** (marca `escritorio_tres_travas`) a espera para: o Zane não é mais incomodado depois de abrir a porta restrita.
- Se o Zane **morre** durante o evento, ele é abortado: a tela e a aranha somem e os robôs são soltos.
- O relógio da espera **não corre** com um diálogo aberto, com um puzzle em tempo real aberto, com o jogo pausado ou com um robô perseguindo o Zane: o apagão nunca chega por cima disso.

## O minigame: Intrusão

Uma grade de peças de cabo. A **central** (ícone de raio, cor ciano) fica na esquerda e o **núcleo** da Aranha (vermelho) na direita. O jogador gira as peças até que a energia, que sai da central, **chegue ao núcleo**. As peças que já recebem energia acendem em ciano, então dá para ver o caminho crescendo.

| Tecla | Efeito |
|---|---|
| Setas | mover o cursor entre as peças |
| `E` (ou Enter) | girar a peça sob o cursor 90° |

O visual é de propósito **diferente** do outro minigame de conexões do projeto (preto e vermelho, cabos em ângulo chanfrado, tremor e tique-taque nos últimos 5 s, barra com o olho da Aranha andando até o fim). Enquanto a tela está aberta, tudo que for outra tecla é descartado, e o inventário, a pausa e o aviso do HUD não abrem (`Hackeamento.tela_em_tempo_real`).

### Dificuldade por evento

A grade, o comprimento do caminho que o jogador precisa refazer e o tempo mudam a cada evento (`HackDaAranha.NIVEIS`). Os giros são medidos no gerador, ver [`../computacao/cabos_e_energia.md`](../computacao/cabos_e_energia.md).

| Evento | Grade | Caminho (peças) | Giros para resolver (média / pior) | Tempo |
|---|---|---|---|---|
| 1º | 5 × 3 | 7 a 9 | 9,0 / 14 | 18 s |
| 2º | 5 × 4 | 8 a 11 | 10,8 / 17 | 18 s |
| 3º | 6 × 4 | 9 a 13 | 12,8 / 20 | 17 s |
| 4º | 6 × 4 | 10 a 14 | 13,8 / 21 | 16 s |

Os giros são o mínimo de rotações que o tabuleiro sorteado exige (de 4 até 1,5 por peça do caminho), medido em 3 mil sorteios por nível num script de teste fora do repositório. O 4º evento é puxado de propósito (cerca de 1 giro por segundo na média): se o grupo achar demais, é só mexer nos números de `NIVEIS`.

## Onde está cada coisa

| Arquivo | O que faz |
|---|---|
| `cenas/sistemas/apagao_da_aranha.tscn` + `scripts/salas/apagao_da_aranha.gd` (`ApagaoDaAranha`) | O coordenador: espera, apagão, aproximação, resultado. Fica como filho de cada sala do escritório. |
| `cenas/personagens/aranha_do_apagao.tscn` + `scripts/personagens/aranha_do_apagao.gd` (`AranhaDoApagao`) | O robô: anda reto até o Zane, cresce, gingado, passos e o bote. Os olhos têm material sem luz, então brilham no escuro. |
| `cenas/interface/hack_da_aranha.tscn` + `scripts/interface/hack_da_aranha.gd` (`HackDaAranha`) | A tela do minigame e o desenho dela. |
| `scripts/sistemas/grade_de_cabos.gd` (`GradeDeCabos`) | O tabuleiro: sorteia um caminho garantidamente possível, embaralha e calcula a energia. |
| `assets/modelagem/personagens/gerar_aranha.py` | Recorta a aranha da imagem de referência (`aranha_referencia/aranha_07.webp`) e gera `aranha.png` e `aranha_olhos.png`. |

O coordenador é um nó solto nas salas, sem mexer nas cenas dos puzzles: é só uma instância de `apagao_da_aranha.tscn` no fim de `recepcao.tscn`, `arquivo.tscn`, `reunioes.tscn` e `seguranca.tscn`.

### Ajustes (no Inspetor do `ApagaoDaAranha`)

| Campo | Padrão | O que muda |
|---|---|---|
| `segundos_minimos` / `segundos_maximos` | 20 / 40 | sorteio da primeira espera de cada sala |
| `segundos_entre_eventos` | 25 | intervalo mínimo entre dois eventos |
| `eventos_maximos` | 4 | quantos eventos o jogo todo tem |
| `distancia_do_aparecimento` | 150 | de que distância a aranha aparece (px) |
| `segundos_de_escuro_antes` | 1 | o escuro antes de ela surgir |
| `marca_que_encerra` | `escritorio_tres_travas` | a marca de `Progresso` que acaba com os eventos |

## Para conferir em jogo

O tempo de cada nível, o tamanho das grades e o número de eventos foram escolhidos no papel e medidos por script, **não jogados**. Vale testar com quem nunca viu o minigame; a tela de hack fica no alto e o Zane não aparece no escuro (só a Aranha, pelos olhos): se o grupo quiser ver o Zane, é só deixar uma luz mínima no `COR_DO_APAGAO`.

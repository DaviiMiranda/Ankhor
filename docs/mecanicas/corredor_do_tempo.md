# Corredor do Tempo (Labirinto)

> **Status:** jogável. As salinhas dos jogos, dos micros e do telefone têm arte própria gerada por script (`gerar_salas_da_epoca.py`); a dos filmes usa as paredes da sala dos anos 80 do Bunker, com os quadros de `gerar_corredor_tempo.py`.
> **Onde:** uma porta com luz âmbar no meio do Labirinto (`HH` no mapa), entre os nós 1 e 2. É **opcional**: não faz parte do caminho dos três nós.

## A ideia

Um corredor do subsolo onde quem construiu a Âncora testava a calibração da máquina com coisas dos anos 80. Quatro salinhas, cada uma com um puzzle sobre uma coisa da época: **videogames, filmes, computadores e telefones**. Um relógio só conta para o corredor inteiro: o tique-taque acelera conforme o tempo acaba. Se o relógio zera, é **game over** (volta ao último checkpoint).

## Como se joga

1. O Gabriel entra pela porta âmbar. Depois do fade de entrada, a porta **tranca atrás dele** (som de ferrolho), aparece o aviso e o relógio começa: **2:00**.
2. No corredor há quatro portas, com placa: **JOGOS**, **FILMES**, **MICROS** e **TELEFONE**. A ordem é livre.
3. Em cada salinha, `E` no objeto abre o painel. O Gabriel fica parado enquanto o painel está aberto, mas **o relógio não para** (só a pausa do jogo o para). `Esc` fecha sem perder o tempo já gasto.
4. **Errar** toca o erro e **tira 5 s do relógio** ("-5 s" pisca ao lado do mostrador). Em todas as salas, o erro **repete só a etapa em que o jogador estava**: o que já foi acertado continua acertado. A exceção é o **telefone**: girar um cabo não é errar, então ali não há castigo, só o relógio correndo.
5. Quando os quatro estão alinhados, o relógio para, tocam os quatro sinos, a porta de saída destrava e aparece, na mesa do fim do corredor, a **Folha de calibração** (o bilhete do Carlos, assinado só "C.").
6. Vencido uma vez, fica vencido (marca `corredor_tempo_vencido` em `Progresso`): o relógio não volta a correr e os mecanismos dizem que já estão no tempo certo.

## As quatro salinhas

| Sala | Como é | Puzzle | Acertos |
|---|---|---|---|
| **Jogos** | Fliperama no escuro: parede roxa com tubos de neon magenta e ciano, cartaz do alienígena de 8 bits, carpete preto com confete neon, dois fliperamas e o Genius num pedestal | **Genius**: o brinquedo mostra uma sequência de cores com som; o jogador repete com as setas (cima verde, direita vermelho, baixo azul, esquerda amarelo). Rodadas de 3, 4 e 5 cores, cada uma mais rápida. Errar mostra a mesma sequência de novo | 3 rodadas |
| **Filmes** | Sala de estar com papel de parede bege (a dos anos 80 do Bunker) e os três quadros de *De Volta para o Futuro* | Escolher um quadro (setas e `E`) e depois o ano de lançamento entre **cinco** (1985, 1987, 1989, 1990, 1991; três certos). Errar repete o mesmo quadro; acertar trava em verde e o ano sai das opções. As **etiquetas das fitas VHS**, na mesa, dão os anos | 3 quadros |
| **Micros** | Um CPD de escritório: parede bege com a faixa laranja de firma, gabinete de fita magnética, painel de luzes, piso elevado, mesa com o micro e cadeira | **Digitar o comando** no teclado de verdade, na tela verde: `LOAD ANCORA`, `LIST` e `RUN`, cada um com `Enter` (o comando pedido aparece embaixo do painel). `Backspace` corrige. Comando errado: `?SYNTAX ERROR` e o mesmo comando de novo | 3 comandos |
| **Telefone** | Sala de casa: lambri de madeira, piso de taco, prateleira com as listas telefônicas amarelas, o selo emoldurado (só enfeite), um orelhão e a mesinha com o telefone de disco vermelho | **Ligar a central ao telefone girando cabos.** O painel mostra uma grade de 7 × 5 peças de cabo (reto, curva, T, cruz, ponta e vazio). A central fica à esquerda e o telefone à direita, em linhas sorteadas. Setas escolhem a peça e `E` gira a peça 90° no sentido horário. Os cabos ligados à central ficam **verdes**: é o sinal chegando. Quando o sinal alcança o telefone, a linha está ligada. Não há "tentar": liga sozinho, e não existe erro nem castigo. O tabuleiro é sorteado a cada visita à sala (e guardado se o jogador sair com `Esc`); sempre tem solução, e o caminho certo tem de 11 a 15 peças | 1 linha |

A computação e a matemática de cada um (fila, pilha, grafo em grade, arranjos) estão em [`../computacao/corredor_do_tempo.md`](../computacao/corredor_do_tempo.md).

## O relógio

- **Mostrador** no canto de cima à direita (`m:ss`). Nos últimos **15 s** vira décimos (`8.7`), fica vermelho e pisca.
- **Tique-taque:** o intervalo entre tiques cai de 1 s para 0,22 s conforme o tempo passa.
- **Sem ansiedade:** até 2026-11-08 o relógio impunha um piso à barra de ansiedade do Gabriel (efeitos de tela e mais gasto de estamina). A ansiedade saiu do jogo: o relógio agora só mostra o tempo e acelera o tique-taque.
- **Tempo zerado:** o Gabriel perde as 3 vidas de uma vez; aparece a tela de morte e ele volta ao último checkpoint. O progresso das salas é perdido: na próxima entrada o desafio recomeça do zero.

## Ajustar

| O quê | Onde |
|---|---|
| Tempo total, segundos críticos, ritmo do tique, curva da pressão | Inspetor de `cenas/sistemas/relogio_do_corredor.tscn` (`segundos_totais`, `segundos_criticos`, `intervalo_tique_*`, `expoente_pressao`) |
| Castigo por erro | Inspetor de cada mecanismo (`segundos_de_castigo`) |
| Genius: tamanho inicial, tempo de cada luz, aceleração | Inspetor de `genius_dos_jogos.tscn` |
| Comandos do micro, anos dos filmes | constantes `COMANDOS` e `ANOS_DE_LANCAMENTO` / `OPCOES_DE_ANO` nos scripts |
| Telefone: tamanho da grade, comprimento do caminho certo, peças enfeite | constantes `COLUNAS`, `LINHAS`, `MIN_CELULAS_DO_CAMINHO`, `MAX_CELULAS_DO_CAMINHO` e `ENFEITES` em `scripts/sistemas/linha_do_telefone.gd` (a grade de 7 × 5 com células de 18 px enche o painel de 180 × 98; mudar `COLUNAS`/`LINHAS` exige mudar `LADO` para caber) |

## Arquivos

| Arquivo | O que é |
|---|---|
| `cenas/salas/labirinto/corredor_do_tempo.tscn` + `scripts/salas/corredor_do_tempo.gd` | o corredor: começa o relógio, tranca a saída, mostra o bilhete depois de vencer |
| `cenas/salas/labirinto/sala_dos_jogos.tscn`, `sala_dos_filmes.tscn`, `sala_dos_micros.tscn`, `sala_do_telefone.tscn` | as quatro salinhas |
| `cenas/sistemas/relogio_do_corredor.tscn` + `scripts/sistemas/relogio_do_corredor.gd` | o relógio. Fica em todas as cinco cenas; o tempo restante e os mecanismos alinhados são `static`, então continuam valendo na troca de sala |
| `cenas/sistemas/mecanismo_do_tempo.tscn` + `scripts/sistemas/mecanismo_do_tempo.gd` | a base dos mecanismos: painel, acerto, erro, castigo. Cada mecanismo é uma cena herdada com o próprio script: `genius_dos_jogos`, `quadros_dos_filmes`, `micro_dos_comandos` e `linha_do_telefone` |
| `cenas/cenario/labirinto/` | as peças das salas dos jogos, dos micros e do telefone (paredes, chão e objetos) |
| `dados/documentos/folha_calibracao_carlos.tres` | o bilhete |
| `dados/documentos/etiquetas_fitas_carlos.tres` | a dica dos filmes |
| `dados/documentos/selo_centenario_telefone.tres` | o selo do centenário do telefone, só enfeite: era a dica do telefone quando o puzzle era discar 1876 |
| `assets/modelagem/audio/gerar_efeitos_corredor_tempo.py` | os sons (tique, acerto, erro, alinhado, trava, vitória e os quatro tons do Genius) |
| `assets/modelagem/salas/labirinto/gerar_salas_da_epoca.py` | a arte das salas dos jogos, dos micros e do telefone (neon, CPD, lambri, taco, Genius, orelhão, telefone de disco) |
| `assets/modelagem/salas/labirinto/gerar_corredor_tempo.py` | os três quadros dos filmes (desenhos próprios, não os cartazes) |
| `assets/modelagem/salas/labirinto/gerar_labirinto.py` | a porta `HH` no mapa e o sprite `porta_corredor_tempo.png` |

### Criar outro mecanismo

Estenda `MecanismoDoTempo` e implemente `_preparar()`, `_avancar(delta)`, `_acertou()`, `_ao_acertar()`, `_ao_errar()` e `_desenhar(centro)` (desenho com `desenho.draw_*`, num quadro de 180 × 98). Opcionais: `_tratar_entrada(evento)` para outras teclas além de `E` e `Esc` (devolve `true` se usou a tecla; o Genius, os filmes e o telefone usam), `_erro_zera_acertos()` devolvendo `false` para um erro não apagar o que já foi acertado, e `_texto_do_visor()` para trocar o "ACERTOS 0/3" do visor por outro texto (o telefone mostra os cabos com sinal; chame `_mostrar_visor()` sempre que o texto mudar). Quem precisa de todas as teclas (o micro) lê em `_input`. Um mecanismo que confere a resposta fora do `E` chama `_tentar()` ele mesmo. Crie uma cena herdada de `mecanismo_do_tempo.tscn` trocando o script, com um `id` novo, e aumente `MECANISMOS` no relógio.

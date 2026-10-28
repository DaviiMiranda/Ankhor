# Corredor do Tempo (Labirinto)

> **Status:** jogável (arte de cenário reaproveitada do Bunker; máquina dos anéis e quadros dos filmes gerados por script).
> **Onde:** uma porta com luz âmbar no meio do Labirinto (`HH` no mapa), entre os nós 1 e 2. É **opcional**: não faz parte do caminho dos três nós.

## A ideia

Um corredor do subsolo onde quem construiu a Âncora testava a calibração da máquina com objetos dos anos 80. Quatro salinhas, cada uma com um mecanismo que precisa ser alinhado **no tempo certo**. Um relógio só conta para o corredor inteiro: quanto menos tempo sobra, mais a ansiedade do Gabriel sobe. Se o relógio zera, é **game over** (volta ao último checkpoint).

## Como se joga

1. O Gabriel entra pela porta âmbar. Depois do fade de entrada, a porta **tranca atrás dele** (som de ferrolho), aparece o aviso e o relógio começa: **2:00**.
2. No corredor há quatro portas, com placa: **DISCO**, **FILMES**, **PÊNDULO** e **ANÉIS**. A ordem é livre.
3. Em cada salinha, `E` no mecanismo abre o painel. O Gabriel fica parado enquanto o painel está aberto, mas **o relógio não para** (só a pausa do jogo o para). `Esc` fecha sem perder o tempo já gasto.
4. **Errar** (apertar `E` fora da hora) toca o arranhão, **zera os acertos daquele mecanismo e tira 5 s do relógio** ("-5 s" pisca ao lado do mostrador).
5. Quando os quatro estão alinhados, o relógio para, tocam os quatro sinos, a porta de saída destrava e aparece, na mesa do fim do corredor, a **Folha de calibração** (o bilhete do Carlos, assinado só "C.").
6. Vencido uma vez, fica vencido (marca `corredor_tempo_vencido` em `Progresso`): o relógio não volta a correr e os mecanismos dizem que já estão no tempo certo.

## Os quatro mecanismos

| Sala | Mecanismo | O que fazer | Acertos | Fica mais difícil a cada acerto |
|---|---|---|---|---|
| Disco | Toca-discos | o disco gira com uma faixa verde; `E` quando a faixa passa sob a agulha | 3 | gira 35% mais rápido e a faixa encolhe 25% |
| Filmes | Três quadros de *De Volta para o Futuro* (partes I, II e III) | embaixo de cada quadro, um visor de anos rola de 1980 a 1995 e volta; `E` quando ele mostra o **ano de lançamento** do filme (1985, 1989, 1990), um quadro por vez. As **etiquetas das fitas VHS**, na mesa da sala, dão os anos (ler custa tempo do relógio) | 3 (um por quadro) | o visor fica 30% mais rápido e recomeça num ano sorteado |
| Pêndulo | Pêndulo | o peso balança; `E` quando ele está dentro da faixa verde do arco | 3 | balança 20% mais rápido, a faixa encolhe 20% e muda de lugar |
| Anéis | Três anéis concêntricos | cada anel gira numa velocidade e sentido; `E` quando a fenda do anel aceso passa pela trava vermelha. Travado, ele fica verde e acende o próximo | 3 (um por anel) | o próximo anel é menor e mais rápido. Errar destrava todos |

A matemática de cada um (movimento harmônico, diferença de ângulos, contador modular) está em [`../computacao/oscilacao_e_ritmo.md`](../computacao/oscilacao_e_ritmo.md).

## O relógio e a ansiedade

- **Mostrador** no canto de cima à direita (`m:ss`). Nos últimos **15 s** vira décimos (`8.7`), fica vermelho e pisca.
- **Tique-taque:** o intervalo entre tiques cai de 1 s para 0,22 s conforme o tempo passa.
- **Ansiedade:** o relógio impõe um **piso** à barra de ansiedade do Gabriel: `pressão = (tempo gasto / tempo total)^1,6`. A barra nunca fica abaixo da pressão (robôs por perto ainda podem subi-la mais). Com ela vêm os efeitos de tela que a ansiedade já tinha (oscilação, separação de cores, vinheta vermelha) e o gasto maior de estamina ao correr. Ao vencer ou morrer, a pressão volta a zero.
- **Tempo zerado:** o Gabriel perde as 3 vidas de uma vez; aparece a tela de morte e ele volta ao último checkpoint. O progresso das salas é perdido: na próxima entrada o desafio recomeça do zero.

## Ajustar

| O quê | Onde |
|---|---|
| Tempo total, segundos críticos, ritmo do tique, curva da pressão | Inspetor de `cenas/sistemas/relogio_do_corredor.tscn` (`segundos_totais`, `segundos_criticos`, `intervalo_tique_*`, `expoente_pressao`) |
| Castigo por erro, acertos necessários | Inspetor de cada mecanismo (`segundos_de_castigo`, `acertos_para_alinhar`) |
| Velocidades, janelas e quanto apertam por acerto | Inspetor de cada mecanismo (`cenas/sistemas/*_do_tempo.tscn`, `quadros_dos_filmes.tscn`) |

## Arquivos

| Arquivo | O que é |
|---|---|
| `cenas/salas/labirinto/corredor_do_tempo.tscn` + `scripts/salas/corredor_do_tempo.gd` | o corredor: começa o relógio, tranca a saída, mostra o bilhete depois de vencer |
| `cenas/salas/labirinto/sala_do_disco.tscn`, `sala_dos_filmes.tscn`, `sala_do_pendulo.tscn`, `sala_dos_aneis.tscn` | as quatro salinhas (paredes e carpete da sala dos anos 80 do Bunker) |
| `cenas/sistemas/relogio_do_corredor.tscn` + `scripts/sistemas/relogio_do_corredor.gd` | o relógio. Fica em todas as cinco cenas; o tempo restante e os mecanismos alinhados são `static`, então continuam valendo na troca de sala |
| `cenas/sistemas/mecanismo_do_tempo.tscn` + `scripts/sistemas/mecanismo_do_tempo.gd` | a base dos mecanismos: painel, acerto, erro, castigo. Cada mecanismo é uma cena herdada com o próprio script (`toca_discos_do_tempo`, `quadros_dos_filmes`, `pendulo_do_tempo`, `aneis_do_tempo`) |
| `dados/documentos/folha_calibracao_carlos.tres` | o bilhete |
| `dados/documentos/etiquetas_fitas_carlos.tres` | as etiquetas das fitas VHS na sala dos filmes (a dica dos anos) |
| `assets/modelagem/audio/gerar_efeitos_corredor_tempo.py` | os sons (tique, acerto, erro, alinhado, trava, vitória) |
| `assets/modelagem/salas/labirinto/gerar_corredor_tempo.py` | a máquina dos anéis e os três quadros dos filmes (desenhos próprios, não os cartazes) |
| `assets/modelagem/salas/labirinto/gerar_labirinto.py` | a porta `HH` no mapa e o sprite `porta_corredor_tempo.png` |

### Criar outro mecanismo

Estenda `MecanismoDoTempo` e implemente `_preparar()`, `_avancar(delta)`, `_acertou()`, `_ao_acertar()`, `_ao_errar()` e `_desenhar(centro)` (desenho com `desenho.draw_*`, num quadro de 180 × 98). Crie uma cena herdada de `mecanismo_do_tempo.tscn` trocando o script, com um `id` novo, e aumente `MECANISMOS` no relógio.

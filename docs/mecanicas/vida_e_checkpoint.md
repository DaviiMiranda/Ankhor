# Mecânicas — Vida e Checkpoint

## 1. Vida

- O Gabriel tem **3 corações** (canto de cima à esquerda da tela).
- **Um toque de robô tira 1 coração.** A tela pisca vermelho, toca a pancada e o Gabriel é empurrado para longe do robô.
- Depois de levar dano, ele fica **1,5 s invulnerável** (o sprite pisca): dá tempo de fugir. O robô que atacou também para por ~1,3 s antes de voltar a perseguir.
- **Zerou:** o jogo pausa, aparece *VOCÊ FOI PEGO* e, em 3 s, o jogo volta ao **último checkpoint** com a vida cheia.

## 2. Checkpoint

- No labirinto, os checkpoints são **postos de emergência**: um poste com uma caixa de luz. Apagado, a luz é vermelha e fraca.
- Passar pelo posto **salva o checkpoint**: a luz fica verde, toca o som de relé com dois bipes, o HUD mostra *Checkpoint salvo* e **os corações voltam a 3**.
- Só um checkpoint fica ativo por vez (o último por onde o Gabriel passou).
- **Ao morrer**, a fase é recarregada inteira (robôs voltam ao lugar de origem) e o Gabriel aparece no último posto.
- **Sem checkpoint na fase**, morrer recomeça a fase do início.
- O que **não** é desfeito ao morrer: itens pegos (a lanterna não reaparece, pilhas usadas não voltam), anotações do caderno e transmissões já ouvidas.
- **Entrar numa fase pelo menu** (Novo jogo ou Fases) apaga checkpoint, vida, inventário, caderno e rádio.

> O GDD prevê que **dormir numa sala segura** salve o jogo. O checkpoint não substitui isso: ele é o "voltar ao último ponto" durante uma fase. O save em arquivo (dormir) ainda não existe.

---

## 3. Onde está no projeto

| O quê | Onde |
|---|---|
| Vida (autoload `Vida`): corações, invulnerabilidade, sinais `mudou`, `dano_recebido`, `morreu` | `scripts/sistemas/vida.gd` |
| Checkpoints (autoload `Checkpoints`): qual está ativo, onde, e `voltar()` | `scripts/sistemas/checkpoints.gd` |
| Posto de checkpoint | `cenas/sistemas/checkpoint.tscn`, `scripts/sistemas/checkpoint.gd` |
| Tela de morte | `cenas/interface/tela_morte.tscn` (está no `modelo_sala.tscn`: toda sala nova herda) |
| Corações e flash de dano | `cenas/interface/hud.tscn` |
| Posicionar o Gabriel no checkpoint ao carregar a sala | `scripts/salas/sala.gd` (`_posicionar_no_checkpoint`) |
| Empurrão e piscar ao levar dano | `scripts/personagens/gabriel.gd` |

**Sinais:** o robô chama `Vida.receber_dano(1, posição)`. Quem precisa reagir escuta os sinais de `Vida`: o HUD (corações, flash, som), o Gabriel (empurrão) e a tela de morte (`morreu`). Ninguém conhece ninguém diretamente.

## 4. Como pôr um checkpoint numa sala

Arraste `cenas/sistemas/checkpoint.tscn` para o nó `Objetos` da sala, no lugar em que o Gabriel deve reaparecer (a origem é o pé do poste). Se quiser um nome fixo para ele, preencha `id`; senão vale o nome do nó.

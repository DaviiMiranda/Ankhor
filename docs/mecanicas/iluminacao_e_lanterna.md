# Mecânicas — Iluminação e Lanterna

> Até 2026-09-29 a luz do jogo vinha de fungos bioluminescentes (pote de fungos). Os fungos saíram: agora a luz é **elétrica** (ver [`../decisoes.md`](../decisoes.md)).

## 1. O problema da escuridão

O campus em 3026 é quase todo escuro. O pouco que ainda tem energia são os **sistemas de emergência** do centro de pesquisa da Âncora: luminárias de emergência de parede (as de dois faróis), lampiões a pilha largados pelo chão e os postos de checkpoint. O resto depende da lanterna do Gabriel.

---

## 2. A lanterna

- **O que é:** uma lanterna de mão comum, a pilha. É um gadget: fica num dos 3 espaços e liga/desliga com a tecla do espaço (`1`, `2` ou `3`).
- **O feixe:** um cone de luz que sai da **mão** do Gabriel e aponta para onde ele está andando (a última direção do movimento). Em volta da mão fica um brilho fraco, que ilumina o próprio Gabriel.
- **O dilema (ver vs. ser visto):**
  - **Ligada:** o jogador enxerga corredores, pilhas e bilhetes. Mas **os robôs enxergam o Gabriel de mais longe**: o alcance da visão deles é multiplicado (Sentinela ×1,7, Rastreador ×1,3).
  - **Desligada:** o Gabriel some no escuro; o jogador anda quase às cegas, guiado pelas luminárias e pelo brilho vermelho dos olhos dos robôs.
- **Bateria:** 4 minutos de uso contínuo. A luz enfraquece com a carga, e abaixo de 15% ela **pisca**.
- **Pilhas:** espalhadas pelo mapa (no labirinto, nos becos sem saída; na Biblioteca, duas no lado escuro). `E` perto de uma pilha troca a bateria (só aparece se a lanterna não estiver cheia). A pilha some depois de usada e não volta.

### Sombras
No labirinto, as paredes bloqueiam o feixe (o `LightOccluder2D` de cada fileira de blocos): o chão atrás de uma parede fica escuro. Um segundo feixe, sem sombra, ilumina só as paredes, para o jogador ver o bloco em que a luz bate. Detalhes em [`../fases/labirinto.md`](../fases/labirinto.md).

---

## 3. Luzes do cenário

| Luz | Onde | Como é |
|---|---|---|
| Luminária de emergência (arandela) | Paredes da Biblioteca, peça `parede_arandela` do kit | Caixa com dois faróis; luz quente que treme e às vezes pisca |
| Lampião de emergência | Chão da Biblioteca e cruzamentos do labirinto (`cenas/cenario/objetos/lampada.tscn`) | Luz quente, treme e pisca (`scripts/salas/luz_tremula.gd`) |
| Posto de checkpoint | Labirinto | Luz verde quando o checkpoint está salvo |
| Placa SAÍDA | Porta de saída do labirinto | Luz verde |

---

## 4. Cápsulas de clarão (ainda não feito)

A defesa de emergência do GDD continua prevista, agora sem fungos: um **flash descartável** que, disparado perto de um robô, sobrecarrega o sensor óptico por 3 a 5 segundos (o ponto fraco que o Baltazar descreve no diário). Máximo de 2 por vez. Ainda não implementado.

---

## 5. Onde está no projeto

| O quê | Onde |
|---|---|
| Lanterna (gadget) | `cenas/itens/lanterna.tscn`, `scripts/itens/lanterna.gd`, `dados/itens/lanterna.tres` |
| Pilha no chão | `cenas/itens/pilha_no_chao.tscn`, `scripts/itens/pilha_no_chao.gd` |
| Textura do feixe (cone) | `assets/sprites/cenario/luzes/luz_cone.png`, gerada por `assets/modelagem/salas/labirinto/gerar_labirinto.py` |
| Luz que treme | `scripts/salas/luz_tremula.gd`, `cenas/cenario/luzes/luz_lampada.tscn` |
| Ícones (lanterna, pilha) | `assets/modelagem/interface/gerar_interface.py` |

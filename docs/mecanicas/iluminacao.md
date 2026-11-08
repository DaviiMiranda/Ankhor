# Mecânicas — Iluminação

> Até 2026-09-29 a luz do jogo vinha de fungos bioluminescentes (pote de fungos). Os fungos saíram e a luz virou **elétrica**. Em 2026-11-08 a **lanterna** do Gabriel também saiu do jogo (ver [`../decisoes.md`](../decisoes.md)): agora a luz vem só do cenário.

## 1. O problema da escuridão

O campus em 3026 é quase todo escuro. O pouco que ainda tem energia são os **sistemas de emergência** do centro de pesquisa da Âncora: luminárias de emergência de parede (as de dois faróis), lampiões a pilha largados pelo chão e os postos de checkpoint. O Gabriel não carrega luz própria: ele anda pelas poças de luz do cenário e guarda o resto para o **raio de visão** e para o brilho vermelho dos olhos dos robôs.

---

## 2. Luz e robôs (ver vs. ser visto)

- **Luz que revela.** Perto de uma luz que revela (as luminárias de emergência da Biblioteca, o luar do Bloco de salas, as luzes marcadas com `revela_quem_passa`) e com o **notebook ligado**, os robôs enxergam o Gabriel de mais longe: o alcance da visão deles é multiplicado por `fator_luz` (Sentinela ×1,7, Rastreador ×1,3; a Mariposa ×7, de 40 para 280 px). O código está em `scripts/personagens/robo.gd`: `luz_do_jogador_acesa()` olha o notebook e `_jogador_iluminado()` olha as luzes do cenário.
- **No escuro.** Longe das luzes, o Gabriel é difícil de ver, mas o jogador também anda quase às cegas, guiado pelas luminárias e pelos olhos dos robôs.
- **Pilhas.** Espalhadas pelo mapa. `E` perto de uma pilha recarrega o notebook (se ele não estiver cheio) ou guarda a pilha para fabricar balas na aba Criação ([`itens_e_inventario.md`](itens_e_inventario.md)). A pilha some depois de usada e não volta.

### Sombras
No labirinto, as paredes bloqueiam a luz (o `LightOccluder2D` de cada fileira de blocos): o chão atrás de uma parede fica escuro. Uma segunda luz, sem sombra, ilumina só as paredes, para o jogador ver o bloco em que a luz bate. Detalhes em [`../fases/labirinto.md`](../fases/labirinto.md).

### Raio de visão
Uma sala pode limitar tudo o que o Gabriel enxerga a um **círculo em volta dele**: dentro do `raio_livre` se vê normalmente, entre `raio_livre` e `raio_escuro` a escuridão cresce em pixels "xadrez" (dithering), e depois disso fica tudo preto, inclusive os olhos dos robôs. Os raios são em pixels do mundo (a câmera tem zoom 2) e o círculo é centrado no peito do Gabriel (`deslocamento_do_centro`, padrão `(0, -24)`).

Para usar numa sala, instancie `cenas/sistemas/raio_de_visao.tscn` (um `CanvasLayer` na camada 4, abaixo da vinheta e da interface). O script acha o Gabriel pelo grupo `jogador`, converte a posição dele para a tela com a transformada da câmera e passa o centro e os raios ao shader todo quadro. A matemática (distância, `smoothstep`, matriz de Bayer) está comentada em `shaders/raio_de_visao.gdshader`. Hoje só o Labirinto usa (raios 56 e 96).

---

## 3. Luzes do cenário

| Luz | Onde | Como é |
|---|---|---|
| Luminária de emergência (arandela) | Paredes da Biblioteca, peça `parede_arandela` do kit | Caixa com dois faróis; luz quente que treme e às vezes pisca |
| Lampião de emergência | Chão da Biblioteca e cruzamentos do labirinto (`cenas/cenario/objetos/lampada.tscn`) | Luz quente, treme e pisca (`scripts/salas/luz_tremula.gd`) |
| Posto de checkpoint | Labirinto | Luz verde quando o checkpoint está salvo |
| Placa SAÍDA | Porta de saída do labirinto | Luz verde |
| Farol da Sentinela | Testa da Sentinela | Cone vermelho que mostra para onde ela olha (textura `luz_cone.png`) |

---

## 4. Onde está no projeto

| O quê | Onde |
|---|---|
| Pilha no chão | `cenas/itens/pilha_no_chao.tscn`, `scripts/itens/pilha_no_chao.gd` |
| Textura do cone do farol | `assets/sprites/cenario/luzes/luz_cone.png`, gerada por `assets/modelagem/salas/labirinto/gerar_labirinto.py` |
| Raio de visão | `cenas/sistemas/raio_de_visao.tscn`, `scripts/sistemas/raio_de_visao.gd`, `shaders/raio_de_visao.gdshader` |
| Luz que treme | `scripts/salas/luz_tremula.gd`, `cenas/cenario/luzes/luz_lampada.tscn` |
| Posição da mão em cada vista e quadro | `scripts/personagens/maos_do_gabriel.gd` (gerado por `assets/modelagem/personagens/medir_maos_gabriel.py`) e `posicao_da_mao()` em `scripts/personagens/gabriel.gd` (usada pelo braço de hack do Zane) |

> **Se o sprite do Gabriel mudar** (nova arte, outro corte de roupa), rode `python assets/modelagem/personagens/medir_maos_gabriel.py`: ele acha a mão (o único pedaço de pele abaixo do moletom) em cada quadro de cada vista e refaz `maos_do_gabriel.gd`. O medidor segue uma mão só pela tira (com a velocidade dela, para não confundir quando as duas se cruzam), preenche por interpolação os quadros em que ela some atrás do corpo e reduz o balanço a 60%.

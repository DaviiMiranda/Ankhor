# Mecânicas — Iluminação e Lanterna

> Até 2026-09-29 a luz do jogo vinha de fungos bioluminescentes (pote de fungos). Os fungos saíram: agora a luz é **elétrica** (ver [`../decisoes.md`](../decisoes.md)).

## 1. O problema da escuridão

O campus em 3026 é quase todo escuro. O pouco que ainda tem energia são os **sistemas de emergência** do centro de pesquisa da Âncora: luminárias de emergência de parede (as de dois faróis), lampiões a pilha largados pelo chão e os postos de checkpoint. O resto depende da lanterna do Gabriel.

---

## 2. A lanterna

- **O que é:** uma lanterna pequena, a pilha, de aço azulado escuro, com botão vermelho e uma alça de pulso, que o Gabriel leva na mão. É um gadget: fica num dos 3 espaços e liga/desliga com a tecla do espaço (`1`, `2` ou `3`).
- **O feixe:** um cone de luz que sai da **lente da lanterna**, na mão do Gabriel, e aponta para onde ele está andando (a última direção do movimento). Em volta da lente fica um brilho fraco, que ilumina o próprio Gabriel.
- **Na mão:** com a lanterna equipada, uma peça pequena de aço azulado (14 × 8 px em resolução dobrada, 7 × 4 px no jogo, com o botão vermelho em cima e um ponto claro na lente) aparece na mão do Gabriel, ligada ou apagada. Ela acompanha a mão em cada quadro da caminhada, gira para a direção da mira e espelha quando ele olha para a esquerda. Nas vistas de costas ela fica escondida pelo corpo, e a luz continua saindo da lente. `Gabriel.posicao_da_mao()` devolve o ponto da mão na vista e no quadro em que ele está.
- **O dilema (ver vs. ser visto):**
  - **Ligada:** o jogador enxerga corredores, pilhas e bilhetes. Mas **os robôs enxergam o Gabriel de mais longe**: o alcance da visão deles é multiplicado (Sentinela ×1,7, Rastreador ×1,3).
  - **Desligada:** o Gabriel some no escuro; o jogador anda quase às cegas, guiado pelas luminárias e pelo brilho vermelho dos olhos dos robôs.
- **Bateria:** 4 minutos de uso contínuo. A luz enfraquece com a carga, e abaixo de 15% ela **pisca**.
- **Pilhas:** espalhadas pelo mapa (no labirinto, nos becos sem saída; na Biblioteca, duas no lado escuro). `E` perto de uma pilha troca a bateria (só aparece se a lanterna não estiver cheia). A pilha some depois de usada e não volta.
- **O que só a lanterna mostra:** no Labirinto, a parede falsa do esconderijo do Baltazar parece concreto liso. Com o feixe apontado para ela, aparecem os riscos (o Cruzeiro do Sul e uma cruz) e dá para afastar o painel. A força da luz naquele ponto é calculada com o mesmo cone do feixe (produto escalar entre a direção do olhar e a direção até a parede): ver [`../fases/labirinto.md`](../fases/labirinto.md), seção 3.

### Sombras
No labirinto, as paredes bloqueiam o feixe (o `LightOccluder2D` de cada fileira de blocos): o chão atrás de uma parede fica escuro. Um segundo feixe, sem sombra, ilumina só as paredes, para o jogador ver o bloco em que a luz bate. Detalhes em [`../fases/labirinto.md`](../fases/labirinto.md).

### Raio de visão
Independente da lanterna, uma sala pode limitar tudo o que o Gabriel enxerga a um **círculo em volta dele**: dentro do `raio_livre` se vê normalmente, entre `raio_livre` e `raio_escuro` a escuridão cresce em pixels "xadrez" (dithering), e depois disso fica tudo preto, inclusive o feixe da lanterna e os olhos dos robôs. Os raios são em pixels do mundo (a câmera tem zoom 2) e o círculo é centrado no peito do Gabriel (`deslocamento_do_centro`, padrão `(0, -24)`).

Para usar numa sala, instancie `cenas/sistemas/raio_de_visao.tscn` (um `CanvasLayer` na camada 4, abaixo da vinheta e da interface). O script acha o Gabriel pelo grupo `jogador`, converte a posição dele para a tela com a transformada da câmera e passa o centro e os raios ao shader todo quadro. A matemática (distância, `smoothstep`, matriz de Bayer) está comentada em `shaders/raio_de_visao.gdshader`. Hoje só o Labirinto usa (raios 56 e 96).

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
| Raio de visão | `cenas/sistemas/raio_de_visao.tscn`, `scripts/sistemas/raio_de_visao.gd`, `shaders/raio_de_visao.gdshader` |
| Luz que treme | `scripts/salas/luz_tremula.gd`, `cenas/cenario/luzes/luz_lampada.tscn` |
| Ícones (lanterna, pilha) | `assets/modelagem/interface/gerar_interface.py` |
| Sprite da lanterna na mão (14 × 8 px) | `assets/sprites/itens/lanterna_mao.png`, gerado por `gerar_interface.py` (função `lanterna_mao`) |
| Imagem da tela de item novo | `assets/sprites/itens/lanterna_detalhe.png`, da foto de referência, preparada por `assets/modelagem/itens/preparar_detalhe.py` |
| Posição da mão em cada vista e quadro | `scripts/personagens/maos_do_gabriel.gd` (gerado por `assets/modelagem/personagens/medir_maos_gabriel.py`) e `posicao_da_mao()` em `scripts/personagens/gabriel.gd` |

> **Se o sprite do Gabriel mudar** (nova arte, outro corte de roupa), rode `python assets/modelagem/personagens/medir_maos_gabriel.py`: ele acha a mão (o único pedaço de pele abaixo do moletom) em cada quadro de cada vista e refaz `maos_do_gabriel.gd`. A pedra continua saindo do peito (`PEITO_NO_QUADRO`, que também precisa ser conferido). Na sala de teste em que `C` troca de personagem, os pontos são os do Gabriel, então a lanterna dos outros fica aproximada.

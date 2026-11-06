# Mecânicas — Combate do Centro de Convivência

> **Status:** em teste. Valem só no **Centro de Convivência**: o robô atirador e a arma de impulso. Os números são um primeiro chute para o grupo ajustar jogando.
> **O Gabriel continua sem ser combatente** (ver o Enredo Principal): nada aqui mata um robô. A arma só **afasta**, o clarão só **paralisa**.

---

## 1. Robô atirador (`RoboAtirador`)

Um robô novo (`cenas/personagens/robo_atirador.tscn`, script `scripts/personagens/robo_atirador.gd`), **só na Praça Central** (o andar de baixo do Centro de Convivência). Ele herda tudo do `Robo` (patrulha, visão, audição, atordoado) e acrescenta o tiro. Visualmente é a Sentinela pintada de azul, com os olhos e a luz ciano: é um **placeholder** até a arte própria ficar pronta.

**Como ele ataca, em ordem:**

1. Vê o Gabriel e entra em `PERSEGUINDO`, como qualquer robô.
2. Chega a `distancia_de_tiro` (130 px) e para: a partir daí ele **mira**. Se o Gabriel chegar perto demais (`distancia_ideal`, 95 px) o robô fica parado, em vez de avançar para a garra.
3. **Mira rastreando** (0,7 s): uma linha vermelha fina sai do peito dele e acompanha o Gabriel. Toca o som de carga.
4. **Mira travada** (0,4 s): a linha fica branca e grossa e **para de seguir**. É a janela para sair da linha ou se proteger atrás de uma mesa.
5. **Dispara** um raio (`RaioAtirado`) na direção travada. Depois recarrega por 2,2 s antes de mirar de novo.

**O raio** viaja a 310 px/s, tira **1 de vida** e some ao acertar. **Mesas, árvores e paredes (camada 8) param o raio**, o mesmo que cortam a visão dos robôs: ficar atrás de uma mesa protege. 

**Quando a mira cancela:** o robô fica atordoado (clarão ou arma de impulso), ou o Gabriel se esconde (nicho), ou morre.

**Conteúdo de computação:** a direção da mira é o vetor unitário `(alvo − robô) / |alvo − robô|`; o tamanho da linha é um **raio de colisão** (`intersect_ray`) até a primeira parede; a decisão "ver para atirar" é o mesmo **campo de visão por produto escalar** dos outros robôs (ver [`../computacao/ia_e_perseguicao.md`](../computacao/ia_e_perseguicao.md)). Os estados de mira (rastreando, travada, recarga) são uma **máquina de estados** pequena em cima da máquina do `Robo`.

---

## 2. Arma de impulso (`arma_impulso`)

- **Onde está:** dentro do **cofre do cinema** (`cinema_cabine`, código 7-2-4). O prêmio do cofre, que era uma cápsula de clarão, passou a ser a arma. Ela já vem com **2 balas**.
- **Como usa: travar e apertar de novo.** É um gadget; vai para um dos 3 espaços. **Aperte** a tecla do espaço (`1`, `2` ou `3`): o Gabriel para, aparece um **cone** de 30° no chão e a **mira trava no robô mais próximo** (até 150 px), com uma marca em volta dele. A mira **acompanha** o robô enquanto ele anda; se ele sai de alcance ou some, ela passa para o próximo mais perto. **Aperte a mesma tecla de novo** para atirar. `Shift` **cancela** sem gastar bala. Se não houver nenhum robô por perto, a mira fica livre: aponte com `WASD` (8 direções; sem apertar nada, mira para onde o Gabriel olha). Morrer ou trocar de gadget no meio também cancela. 
- **O que faz:** uma onda de choque dentro do cone, de **30° de abertura e 150 px de alcance** (média distância), medida a partir dos pés do Gabriel. **Empurra os robôs que estão dentro** para longe e os deixa **paralisados por 0,9 s**. A força cai com a distância: quem está colado é jogado a ~400 px/s, quem está na borda a ~170 px/s. Robô fora do cone não sente nada. O empurrão é um `_impulso` no `Robo`, que perde velocidade por atrito (420 px/s²), então o robô desliza e para.
- **Custo: balas.** Cada disparo gasta **1 bala** (no máximo **6**). As balas **não se recarregam sozinhas**: criam-se na aba **Criação** do inventário, a **3 pilhas por bala** (seção 2.1). Entre dois disparos, 0,45 s.
- **Visual e som:** o cone ciano translúcido enquanto mira; ao soltar, dois arcos ciano que correm pelo cone, um clarão azul e o estouro grave (`impulso_disparo.wav`).

**Conteúdo de computação:** o teste "o robô está no cone?" é um **produto escalar/ângulo entre vetores**: o ângulo entre a direção da mira e o vetor Gabriel→robô tem de ser menor que metade da abertura (15°), e a distância menor que o alcance. O empurrão é uma **soma de vetores** (direção do Gabriel ao robô, normalizada, vezes uma velocidade que cai linearmente com a distância) e o atrito é uma **desaceleração constante** (`move_toward`).

### 2.1 Aba Criação e as pilhas

- **Pilhas guardadas.** Com a arma na mochila, uma pilha achada no chão que **não serve para recarregar** nenhum gadget (lanterna, walkman, notebook) é **guardada** (até **9**) em vez de ficar no chão. Se a lanterna precisa, a pilha continua recarregando a lanterna primeiro. Sem a arma, as pilhas funcionam como sempre.
- **Aba CRIAÇÃO** (`Q` troca de aba): mostra a receita **Bala de impulso: 3 pilhas**, quantas pilhas e balas há e o que falta. `E` cria uma bala. Fica como "Você ainda não tem a arma de impulso" antes de abrir o cofre.
- **No código:** `Criacao` (`scripts/sistemas/criacao.gd`) decide se dá para criar e cria; `PainelCriacao` desenha a aba; o estoque de pilhas fica em `Inventario.estado` (`pilhas.quantidade`), então vai no save.

## 3. Modo combate (a porta de teste)

Para testar tudo isso sem jogar a fase, a **sala de teste** tem uma porta "FASES (TESTE)" que leva à `sala_teste_fases`, com uma porta por fase:

| Placa | Destino | Observação |
|---|---|---|
| **CONVIVÊNCIA (COMBATE)** | `praca_central`, no meio da praça (1000, 330) | Liga o **modo combate** (abaixo) |
| BLOCO DE SALAS | `corredor_terreo` | Itens no máximo, sem modo combate |
| LABIRINTO | `labirinto` | idem |
| BUNKER | `entrada` do bunker | idem |
| D-TEC (LABORATÓRIO) | `emergencia` | idem |
| ZANE (CÂMARA SELADA) | `labirinto/camara_selada` | A mini fase do Zane |
| FIM DO BUNKER | `bunker/central_dados`, pela porta da sala | O começo da cena do fim do Bunker: marca `bunker_energia` (o grupo está na sala) e apaga as marcas da cena (`bunker_confronto_falado`, `bunker_henrique_sumiu`, `bunker_comporta_aberta`), então dá para ver de novo quantas vezes quiser. O confronto começa ao chegar perto do grupo |

As marcas são exports da `PortaDeTeste`: `marcas_ao_entrar` e `marcas_apagadas_ao_entrar` (esta usa `Progresso.desmarcar`). Servem para levar a qualquer ponto de uma fase que dependa de progresso.

Ao entrar na sala de fases, o nó `TudoColetado` deixa a mochila cheia (com as 9 pilhas e as 6 balas): arma de impulso, clarão e pedra primeiro (assim ficam nos 3 espaços de gadget), depois os outros gadgets e as ferramentas. **A Célula de Energia fica de fora**, porque é carga pesada e impede de correr. A mochila tem 12 espaços e há mais itens do que isso, então as chaves ficam de fora quando falta lugar.

**O modo combate** (`scripts/sistemas/modo_combate.gd`, só a porta CONVIVÊNCIA liga):

- **Cápsulas de clarão e balas da arma de impulso são infinitas** (não gastam).
- **Morrer devolve ao meio da praça** (o ponto da porta), com 2 s de proteção, em vez de ao último checkpoint. Os checkpoints do cenário não mudam o ponto de volta.
- **Acaba sozinho** ao voltar ao menu, começar um jogo novo, carregar um save ou sair da fase (tudo que chama `Checkpoints.limpar()`).

---

## 4. Onde está no projeto

| O quê | Arquivo |
|---|---|
| Robô atirador | `scripts/personagens/robo_atirador.gd`, `cenas/personagens/robo_atirador.tscn` |
| Raio | `scripts/sistemas/raio_atirado.gd`, `cenas/sistemas/raio_atirado.tscn` |
| Empurrão do robô | `Robo.empurrar()` em `scripts/personagens/robo.gd` |
| Arma de impulso | `scripts/itens/arma_impulso.gd`, `cenas/itens/arma_impulso.tscn`, `dados/itens/arma_impulso.tres` |
| Criação e pilhas guardadas | `scripts/sistemas/criacao.gd`, `scripts/interface/painel_criacao.gd`, `cenas/interface/painel_criacao.tscn`, `Inventario.pilhas()`, `PilhaNoChao` |
| Modo combate | `scripts/sistemas/modo_combate.gd`, `Checkpoints`, `Vida.proteger()` |
| Sala de fases e portas | `cenas/salas/sala_teste_fases.tscn`, `scripts/sistemas/porta_de_teste.gd`, `cenas/cenario/objetos/placa_de_porta.tscn` |
| Sons e ícones | `assets/modelagem/audio/gerar_efeitos_combate.py`, `assets/modelagem/itens/gerar_arma_impulso.py` |

## 5. Ainda não feito

- Arte própria do robô atirador (hoje é a Sentinela azul) e imagem detalhada da arma (hoje usa o ícone ampliado).
- O robô atirador só existe na praça: ainda não há um segundo atirador nem o dele no segundo andar.
- Decidir se a arma de impulso entra nas outras fases (hoje só no Centro de Convivência, por pedido do Davi).

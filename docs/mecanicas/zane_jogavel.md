# O Zane jogável

O Zane é jogável em um trecho: a **ala do escritório**, a mini fase do fim do Labirinto ([`../fases/labirinto.md`](../fases/labirinto.md), seção 5.1). O corpo é o mesmo do Gabriel (`gabriel.gd`), com a ficha dele aplicada por cima: `scripts/personagens/perfil_zane.gd` (`PerfilZane.aplicar`), chamado pelas salas do escritório (`scripts/salas/sala_do_zane.gd`, classe `SalaDoZane`).

## O que muda em relação ao Gabriel

| | Gabriel | Zane |
|---|---|---|
| Sprites | `gabriel/` | `zane/`: parado, caminhada, **corrida**, **hack** e **casaco** |
| Corrida | curvado, 24 quadros | **ereto**, passo largo e saltado, **48 quadros** |
| Estamina | 100 | **160** (mesmo gasto e mesma regeneração: corre 60% mais tempo) |
| Ansiedade | sim | **não tem**: a barra e o efeito somem da tela (`Ansiedade.desativar()`) |
| Lanterna | pilha de 240 s | **infinita** (`Gabriel.lanterna_infinita`) |
| Itens | o que ele pegou | **kit próprio**: lanterna, flash (2) e braço de hack |
| Inventário | tira a mochila do ombro e abre | **abre a jaqueta** com as duas mãos: o forro tem bolsos com o que ele carrega (`zane_casaco_<vista>.png`) |
| Mãos | `maos_do_gabriel.gd` | `maos_do_zane.gd` (a lanterna fica na mão de metal em quase todas as vistas) |

**O kit é emprestado.** `Inventario.emprestar_kit` guarda a mochila do Gabriel (grade, gadgets, estado e itens vistos) e põe o kit do Zane; `Inventario.devolver_kit` devolve tudo. O kit é emprestado **uma vez**, na primeira sala do escritório, e fica emprestado ao trocar de sala e ao morrer e recomeçar do checkpoint (por isso o flash gasto não volta). Quem devolve é a câmara selada, ao abrir (`camara_selada.gd`). `Inventario.limpar` (novo jogo, escolher fase) também esquece o empréstimo. Os gadgets ficam nas teclas `1` (lanterna) e `2` (flash); o `3` fica livre. O braço de hack tem um **espaço só dele, o 4º**, na tecla `4`: o item tem `vai_no_espaco_do_braco` e vai para `Inventario.braco` em vez dos espaços de gadget. O HUD só mostra esse quarto espaço quando há braço na mochila (o Gabriel continua com três), com a barrinha de recarga e a moldura acesa durante a invasão.

## O braço de hack

`scripts/itens/braco_hack.gd` (item `dados/itens/braco_hack.tres`). Aperte `4` perto de um robô:

1. Escolhe o robô **mais perto, a até 170 px e em linha reta** (um raio contra as paredes, camada 8). Sem alvo, avisa.
2. O Zane **vira para o robô** e **estende o braço de metal** (tira `zane_hack_<vista>.png`, 12 quadros, 0,55 s). Um raio ciano treme da mão até o robô.
3. Abre o **minigame de hack em tempo real** (sempre o de **sincronia**, que usa só o `E`: o outro usa WASD, que o Zane precisa para andar): os robôs continuam andando e o jogo não pausa. A dificuldade depende do robô: **Ronda** fácil, **Sentinela** e **Mariposa** média, **Rastreador**, **Caçador**, **Escafandro** e **Atirador** difícil.
4. **Enquanto hackeia, o robô fica lento:** a 30% da velocidade (`lentidao_do_robo`, aplicada em `Robo.fator_de_velocidade`), para dar tempo de terminar o minigame. Vale do braço estender até ele recolher; depois o robô volta à velocidade normal.
5. **E o Zane também anda bem devagar** (30% da velocidade, sem correr e sem som de passos) e **a direção fica travada** no robô, com o braço esticado. Se ele se afastar mais de 220 px ou perder a linha reta, a conexão cai (sem penalidade).
6. **Deu certo:** o robô fica **desligado por 15 s** (`Robo.atordoar`). **Falhou:** o robô **ouve** (`Robo.fazer_barulho`, alcance 14) e o Zane recolhe o braço. Esc cancela, sem barulho nem penalidade.
7. **Cada robô aguenta 2 falhas.** Na **3ª falha** (mais de 2 erros) o robô **bloqueia o acesso** e não dá mais para hackeá-lo (a contagem fica no próprio robô, `falhas_de_hack`, e vale até a cena recarregar).
8. O implante **esfria por 6 s** antes do próximo uso. Levar dano no meio da invasão a interrompe, sem contar como falha.

**Os efeitos.** Enquanto o braço estende e a invasão corre, a mão de metal brilha em ciano, solta faíscas e acende uma luz que ilumina o braço. O robô alvo fica ciano, pulsando, coberto de faíscas, e com uma luz própria; ao soltar, volta à cor dele. Enquanto o implante esfria, a mão fica **em brasa**: um brilho e uma luz vermelha no braço, com fumaça subindo, que se apagam junto com a recarga (6 s). Tudo é desenhado no próprio `braco_hack.gd` (`_draw`, sem shader), com duas `PointLight2D` na cena `braco_hack.tscn` para o brilho atravessar o escuro da sala.

Diferente do notebook do Gabriel, que só desliga o robô **por trás**, o braço do Zane funciona de frente e de longe, mas expõe mais: o Zane fica lento e à vista enquanto a invasão corre, e cada robô só aguenta 2 falhas.

## Como os sprites são feitos

`assets/modelagem/personagens/gerar_zane_movimentos.py` (Blender, sem janela): a corrida (mesma ideia da do Gabriel, com a matemática no cabeçalho do arquivo), o gesto do braço (Catmull-Rom entre poses-chave) e a **tabela das mãos** (`maos_do_zane.gd`) seguindo a mão 3D em cada quadro. Rode de novo se o modelo do Zane mudar (`gerar_zane.py`).

O gesto do inventário sai de `assets/modelagem/personagens/gerar_zane_casaco.py`: a frente da jaqueta vira duas abas presas na costura do lado, que giram para fora (a matemática está no cabeçalho). O `Gabriel` guarda as tiras do gesto em `tiras_do_gesto_da_mochila`, e a ficha do Zane troca pelas do casaco.

Os ícones do braço de hack saem de `assets/modelagem/itens/gerar_braco_hack.py`.

# O Zane jogável

O Zane é jogável em um trecho: a **ala do escritório**, a mini fase do fim do Labirinto ([`../fases/labirinto.md`](../fases/labirinto.md), seção 5.1). O corpo é o mesmo do Gabriel (`gabriel.gd`), com a ficha dele aplicada por cima: `scripts/personagens/perfil_zane.gd` (`PerfilZane.aplicar`), chamado pelas salas do escritório (`scripts/salas/sala_do_zane.gd`, classe `SalaDoZane`).

## O que muda em relação ao Gabriel

| | Gabriel | Zane |
|---|---|---|
| Sprites | `gabriel/` | `zane/`: parado, caminhada, **corrida** e **hack** |
| Corrida | curvado, 24 quadros | **ereto**, passo largo e saltado, **48 quadros** |
| Estamina | 100 | **200** (mesmo gasto e mesma regeneração: corre o dobro do tempo) |
| Ansiedade | sim | **não tem**: a barra e o efeito somem da tela (`Ansiedade.desativar()`) |
| Lanterna | pilha de 240 s | **infinita** (`Gabriel.lanterna_infinita`) |
| Itens | o que ele pegou | **kit próprio**: lanterna, flash (2) e braço de hack |
| Mãos | `maos_do_gabriel.gd` | `maos_do_zane.gd` (a lanterna fica na mão de metal em quase todas as vistas) |

**O kit é emprestado.** `Inventario.emprestar_kit` guarda a mochila do Gabriel (grade, gadgets, estado e itens vistos) e põe o kit do Zane; `Inventario.devolver_kit` devolve tudo. O kit é emprestado **uma vez**, na primeira sala do escritório, e fica emprestado ao trocar de sala e ao morrer e recomeçar do checkpoint (por isso o flash gasto não volta). Quem devolve é a câmara selada, ao abrir (`camara_selada.gd`). `Inventario.limpar` (novo jogo, escolher fase) também esquece o empréstimo. Os gadgets ficam nas teclas `1` (lanterna), `2` (flash) e `3` (braço de hack).

## O braço de hack

`scripts/itens/braco_hack.gd` (item `dados/itens/braco_hack.tres`). Aperte `3` perto de um robô:

1. Escolhe o robô **mais perto, a até 170 px e em linha reta** (um raio contra as paredes, camada 8). Sem alvo, avisa.
2. O Zane **vira para o robô** e **estende o braço de metal** (tira `zane_hack_<vista>.png`, 12 quadros, 0,55 s). Um raio ciano treme da mão até o robô.
3. Abre o **minigame de hack em tempo real** (sempre o de **sincronia**, que usa só o `E`: o outro usa WASD, que o Zane precisa para andar): os robôs continuam andando e o jogo não pausa. A dificuldade depende do robô: **Ronda** fácil, **Sentinela** e **Mariposa** média, **Rastreador**, **Caçador**, **Escafandro** e **Atirador** difícil.
4. **Enquanto hackeia, o Zane anda bem devagar** (30% da velocidade, sem correr e sem som de passos) e **a direção fica travada** no robô, com o braço esticado. Se ele se afastar mais de 220 px ou perder a linha reta, a conexão cai (sem penalidade).
5. **Deu certo:** o robô fica **desligado por 15 s** (`Robo.atordoar`). **Falhou:** o robô **ouve** (`Robo.fazer_barulho`, alcance 14) e o Zane recolhe o braço. Esc cancela, sem barulho nem penalidade.
6. **Cada robô aguenta 2 falhas.** Na **3ª falha** (mais de 2 erros) o robô **bloqueia o acesso** e não dá mais para hackeá-lo (a contagem fica no próprio robô, `falhas_de_hack`, e vale até a cena recarregar).
7. O implante **esfria por 6 s** antes do próximo uso. Levar dano no meio da invasão a interrompe, sem contar como falha.

Diferente do notebook do Gabriel, que só desliga o robô **por trás**, o braço do Zane funciona de frente e de longe, mas expõe mais: o Zane fica lento e à vista enquanto a invasão corre, e cada robô só aguenta 2 falhas.

## Como os sprites são feitos

`assets/modelagem/personagens/gerar_zane_movimentos.py` (Blender, sem janela): a corrida (mesma ideia da do Gabriel, com a matemática no cabeçalho do arquivo), o gesto do braço (Catmull-Rom entre poses-chave) e a **tabela das mãos** (`maos_do_zane.gd`) seguindo a mão 3D em cada quadro. Rode de novo se o modelo do Zane mudar (`gerar_zane.py`).

Os ícones do braço de hack saem de `assets/modelagem/itens/gerar_braco_hack.py`.

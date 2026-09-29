# Registro de decisões

Toda decisão de design, história ou técnica que muda o jogo entra aqui, **a mais recente no topo**. Se algo contradiz o GDD, vale o que está aqui.

Formato:

```
## AAAA-MM-DD — título curto
**Decisão:** o que ficou decidido.
**Por quê:** o motivo, em uma ou duas frases.
**Afeta:** o que precisa mudar (GDD, código, arte, roteiro).
```

---

## 2026-09-29 — Revelação central aprovada, Clarice viva e dois finais
**Decisão:**
- A **revelação central** está aprovada. Gabriel é o paradoxo da Âncora: ela nasce do caderno dele, esquecido na Biblioteca em 2026. A fenda não puxa por acaso, e sim quem esteve no chão da Biblioteca. Os sonhos são ciclos que falharam. A premissa "a fenda puxa pessoas aleatórias" passa a ser o que o jogador acredita até a revelação.
- **Clarice está viva.** O jogador acha que ela morreu, mas ela fala com Gabriel **por ligação**, pelos telefones velhos do campus, e é a única que lembra dos loops.
- **Dois finais:**
  - **Feliz:** os dois ficam juntos em 2026. Exige a pesquisa completa do professor e todas as ligações da Clarice atendidas.
  - **Triste:** cada um volta ao seu tempo, ele esquece, e ela escolhe nunca procurá-lo para quebrar o loop.

**Por quê:** decisão do Davi. Dá uma relação central e emocional à história, e os finais usam a regra do GDD de que o que o jogador descobriu muda o final.
**Afeta:** `docs/historia/revelacao_central.md`, `docs/personagens/antecessores.md`, `docs/historia/README.md`, `docs/gdd.md`, `docs/fases/biblioteca.md`. **Em aberto:** onde a Clarice está escondida; onde estão as partes da pesquisa do professor.

## 2026-09-29 — Personagens secundários: os antecessores
**Decisão:** entram na documentação as fichas das pessoas puxadas antes de Gabriel:
- **Mestre Baltazar** (~1750): some sem deixar corpo. Na Biblioteca fica o acampamento dele entre as raízes da árvore, com a luneta e o diário que mostra o ponto fraco dos sensores ópticos.
- **Inspetor Agostinho** (1978): deixa um mapa antigo com passagens secretas.
- **Clarice** (1994, a aluna já decidida): deixa disquetes e senhas.
- **Seu Valdir** (2008, o segurança já decidido): fala com Gabriel pelo rádio e dá dicas de patrulha. No fim se descobre que ele morreu há décadas e o rádio só repete as gravações dele.
- **O professor** (2019): a pesquisa dele virou a cadeira de Gabriel, e em 3026 ele apaga o nome do criador da Âncora.
- **Zane** (2123): deixa áudios que apontam para um usuário de 2026.

Todos foram puxados **no mesmo lugar**, o chão onde hoje fica a Biblioteca. Cada época tem um visual próprio de bilhete, e a Biblioteca só usa Baltazar, Clarice e Valdir. A revelação central que veio junto (Gabriel como paradoxo da Âncora, sonhos como loops, bilhetes de "G." dos ciclos anteriores) foi registrada como proposta; foi aprovada na entrada acima.
**Por quê:** proposta de personagens recebida pelo grupo, com os ajustes pedidos pelo Davi. Dá rosto aos bilhetes e liga cada pista a uma mecânica.
**Afeta:** `docs/personagens/antecessores.md` (novo), `docs/historia/revelacao_central.md` (novo), `docs/historia/README.md`, `docs/personagens/README.md`, `docs/gdd.md`, `docs/mecanicas/sono_e_sonhos.md`, `docs/fases/biblioteca.md`. **Em aberto:** se a pessoa de 2041 continua; como terminais e rádio funcionam se "nada elétrico funciona"; a revelação central.

## 2026-09-27 — Scripts GDScript sem comentários
**Decisão:** os scripts `.gd` não têm nenhum comentário (nem `#` nem `##`). O código se explica pelos nomes, em português. A explicação de algoritmos e da matemática fica em `docs/` (ex.: `docs/computacao/`). Geradores em Python (`assets/modelagem/`) e shaders continuam comentados. O guia de montar salas e as imagens de catálogo do kit (`docs/imagens/`) saíram; o catálogo do kit agora só é gerado com `CATALOGO=1`.
**Por quê:** decisão do Davi, para enxugar o código.
**Afeta:** todos os `scripts/*.gd`, `CLAUDE.md` (Convenções), `CONTRIBUTING.md`, agentes `artista`, `revisor` e `sistemas`, `assets/modelagem/cenario/gerar_kit.py`.

## 2026-09-27 — Biblioteca ainda maior ao sul, com o acervo
**Decisão:** a Biblioteca cresceu mais 120 px para o sul: passa de 300 para 420 px de altura, e a faixa onde o Gabriel anda vai de y 122 a 416. O fundo da parte sul é a área mais escura da sala (longe dos buracos do teto, iluminada só por fungos) e tem o **acervo**: duas fileiras de estantes em pé com corredores entre elas, para o Gabriel se esconder dos robôs. Dos lados, um canto desabado (esquerda) e um canto de leitura (direita). Tudo com objetos do kit de cenário.
**Por quê:** pedido do Davi: aumentar mais o mapa para a parte sul.
**Afeta:** `cenas/salas/biblioteca.tscn` (tamanho, limites, objetos e luzes novos), `gerar_biblioteca.py` (chão e primeiro plano), `docs/guia_montar_salas.md` e `docs/fases/biblioteca.md`.

## 2026-09-26 — Nome do jogo: Ankhor, e inimigos são robôs
**Decisão:** O jogo agora se chama oficialmente **Ankhor** (substitui o provisório "Projeto The Game"). Os inimigos que patrulham o campus passam a ser **robôs** (substitui o conceito anterior de Insones). As pessoas puxadas de outras épocas (aluna de 1994, segurança de 2008, professor de 2019 e a pessoa de 2041 a definir) deixaram **bilhetes** pelo campus explicando melhor os acontecimentos (textos a serem escritos pelo Davi).
**Por quê:** Decisão do Davi (definindo nome oficial, a natureza robótica dos inimigos e a forma de entrega de narrativa das pessoas de outras épocas).
**Afeta:** GDD, README, `decisoes.md`, `CLAUDE.md`, `project.godot`, `docs/personagens/` e `docs/mecanicas/`.

## 2026-09-26 — Premissa da Fenda Temporal e a Âncora (Ano 3026)
**Decisão:** Em 3026 (mil anos no futuro), a Unifor é um centro de pesquisa em física do tempo. A explosão de um aparelho chamado **Âncora** rasgou o tempo dentro do campus. A fenda encosta em momentos aleatórios do passado e puxa quem estiver perto — numa madrugada de 2026, puxou Gabriel da Biblioteca. A fenda está crescendo e, se não for fechada, vai engolir o passado do campus, incluindo o tempo de Gabriel. Gabriel não é o primeiro a ser puxado: antes dele vieram uma aluna de 1994, um segurança de 2008, um professor de 2019 e alguém de 2041, e ninguém conseguiu. A primeira fase do jogo é a Biblioteca.
**Por quê:** Definição da história principal e ponto de partida do jogo pelo Davi.
**Afeta:** `docs/gdd.md`, `docs/visao_geral/conceito.md`, `docs/historia/README.md`, `docs/fases/README.md`, `docs/fases/biblioteca.md` e `docs/personagens/gabriel.md`.

## 2026-09-26 — Tela cheia em Full HD (F11 alterna)
**Decisão:** o jogo abre em tela cheia e continua desenhado em 320 × 180, ampliado por número inteiro: 6× num monitor Full HD (1920 × 1080). `F11` alterna para janela de 1280 × 720 (4×) e volta.
**Por quê:** pedido do Davi (resolução Full HD). Mudar a resolução BASE para 1920 × 1080 exigiria refazer toda a arte e deixaria de ser pixel art; ampliar por inteiro mantém a arte e a fonte nítidas.
**Afeta:** `project.godot` (modo de janela, autoload `Tela`, ação `tela_cheia`) e `scripts/sistemas/tela.gd`. Ao rodar pelo editor (F5/F6), o jogo também abre em tela cheia: `F11` volta para a janela.

## 2026-09-26 — Sistema de itens, inventário e gadgets
**Decisão:** o Gabriel pega itens com `E`, guarda num inventário em grade de 3 × 4 (aberto com `Tab` ou `I`, pausa o jogo) e equipa até 3 gadgets, usados com as teclas `1`, `2` e `3`. O primeiro item é a lanterna, que é o **pote de fungos** do GDD: fica no chão da Biblioteca, perto de onde o Gabriel acorda. A carga dura 4,5 minutos destampado e recarrega nos fungos do cenário.
**Por quê:** pedido do Davi. Os 3 espaços correspondem às ferramentas equipáveis previstas (pote, cápsulas de clarão, arremesso), e a grade é o "inventário em grade (matriz)" do GDD, item 2.4.
**Afeta:** `project.godot` (autoload `Inventario` e ações `interagir`, `inventario`, `gadget_1` a `gadget_3`), `scripts/personagens/gabriel.gd`, `cenas/salas/modelo_sala.tscn` e `biblioteca.tscn` (HUD e inventário), `cenas/cenario/objetos/fungo.tscn` (colônia de recarga). Detalhes em `docs/mecanicas/itens_e_inventario.md`. **Em aberto:** `iluminacao_e_fungos.md` diz que a cápsula de clarão usa `Q`; com os espaços de gadget, ela usaria a tecla do espaço dela. O grupo decide qual fica.

## 2026-09-26 — Biblioteca maior, com a parte sul
**Decisão:** a Biblioteca cresceu para a frente (o "sul" da sala, na direção da câmera): passa de 180 para 300 px de altura, e a faixa onde o Gabriel anda vai de y 122 a 296. A câmera agora anda também na vertical. A parte sul foi mobiliada só com objetos do kit de cenário.
**Por quê:** pedido do Davi: a Biblioteca precisa ser maior.
**Afeta:** `scripts/salas/sala.gd` (novo campo `altura`, que qualquer sala pode usar), `scripts/salas/guias_sala.gd`, `cenas/salas/biblioteca.tscn`, `gerar_biblioteca.py` (chão e primeiro plano) e `docs/guia_montar_salas.md`.

## 2026-09-25 — Biblioteca e movimento 2.5D no estilo FNAF: Into the Pit
**Decisão:** a Biblioteca foi refeita do zero no estilo de *FNAF: Into the Pit*, e o jogador anda em todas as direções dentro da faixa de chão (esquerda/direita e fundo/frente da sala), passando na frente e atrás dos objetos (y-sort). W/S (e as setas ↑/↓) passam a ser mover para cima/baixo; agachar fica no Ctrl (e no C).
**Por quê:** pedido do Davi: a sala precisa ter profundidade de verdade, como em *Into the Pit*, e não só um corredor lateral.
**Afeta:** `project.godot` (ações `mover_cima`, `mover_baixo`, `agachar`), `scripts/personagens/gabriel.gd` (sem gravidade, colisão só nos pés), `cenas/salas/biblioteca.tscn`, arte em `assets/sprites/salas/biblioteca/` (gerada por `assets/modelagem/salas/biblioteca/gerar_biblioteca.py`) e `docs/mecanicas/movimentacao_e_terreno.md`. A "transição de planos" com W em portas e escadas (mecânicas, item 4) precisa de outra tecla ou de interação quando for implementada.

## 2026-09-24 — Nome do jogo: Projeto The Game
**Decisão:** o jogo se chama Projeto The Game (substitui o provisório "VIGÍLIA"). O estimulante da história continua se chamando VIGÍLIA-7.
**Por quê:** escolha do grupo.
**Afeta:** README, GDD, CLAUDE.md e `project.godot` — já atualizados.

## 2026-09-24 — Protagonista se chama Gabriel
**Decisão:** o nome do protagonista é Gabriel (substitui o provisório "Téo").
**Por quê:** escolha do grupo.
**Afeta:** GDD e roteiro — já atualizados em `docs/gdd.md`.

## 2026-09-24 — Roteiro e mecânicas definidos durante o projeto
**Decisão:** o GDD atual é ponto de partida. História e mecânicas vão sendo fechadas a cada sprint e registradas aqui.
**Por quê:** o grupo prefere descobrir o jogo fazendo, em vez de fechar tudo antes.
**Afeta:** tudo; conferir este arquivo antes de implementar algo grande.

## 2026-09-24 — Fluxo de trabalho com git
**Decisão:** GitHub Flow — `main` protegida, uma branch por tarefa, Pull Request com revisão obrigatória do Davi (e de outro integrante nos PRs do Davi).
**Por quê:** evita que uma mudança quebre o jogo de todo mundo e garante que alguém sempre revise.
**Afeta:** `CONTRIBUTING.md`.

## 2026-09-24 — Premissa: mil anos no futuro, na Unifor
**Decisão:** o jogo se passa na Unifor abandonada, mil anos depois; o protagonista acorda sem saber o que aconteceu e investiga. Estilo pixel art 2.5D lateral, inspirado em *FNAF: Into the Pit*.
**Por quê:** exigência de ambientação na Unifor, e o estilo 2D cabe no tamanho do grupo.
**Afeta:** GDD itens 1 a 4.

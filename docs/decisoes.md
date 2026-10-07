# Registro de decisões

Toda decisão de design, história ou técnica que muda o jogo entra aqui, **a mais recente no topo**. Se algo contradiz o GDD, vale o que está aqui.

> [!IMPORTANT]
> Para **história, mundo e personagens**, a lei do projeto é o [Enredo Principal](historia/enredo_principal.md), que vale acima deste registro. Toda decisão de história entra **no mesmo PR** aqui (o histórico de quando e por que mudou) e no Enredo Principal (como a história está agora). Entradas antigas abaixo podem citar nomes e ideias que não valem mais.

Formato:

```
## AAAA-MM-DD — título curto
**Decisão:** o que ficou decidido.
**Por quê:** o motivo, em uma ou duas frases.
**Afeta:** o que precisa mudar (GDD, código, arte, roteiro).
```

---

## 2026-10-07 — Planejamento da Biblioteca no estilo Resident Evil
**Decisão:** a Biblioteca passa a ser planejada como uma fase de **salas ligadas por portas trancadas**, no estilo *Resident Evil*: cabine, salão principal (o centro), balcão, acervo sul, sala de manutenção (sala segura), sala de terminais, ala leste e uma sala de obras raras que só abre mais tarde. Para sair, o jogador busca a chave da manutenção no acervo, religa a energia, lê o código da grade no disquete da Clarice, abre a grade da ala leste e atende a primeira ligação da Clarice, que destranca a porta de saída. A Sentinela fica no salão e o Rastreador no acervo; com a energia, as luzes acendem e a rota da Sentinela muda. O mezanino, cogitado, foi descartado.
**Por quê:** pedido do Davi: uma fase com mais caminhos e cadeados, em vez de um salão só.
**Afeta:** `docs/fases/biblioteca.md` (reescrito). Para implementar: dividir `cenas/salas/biblioteca.tscn` em salas, chave como item, quadro de energia, painel de código e grade, luzes que acendem, telefone, disquete da Clarice e os dois robôs.

## 2026-10-07 — O Carlos é o antagonista (ideia 23), o pesquisador é o Henrique
**Decisão:**
- **Ideia 23 aprovada, com partes ainda em aberto.** O antagonista é o **Carlos**, cientista de 3026 que criou a Âncora. Na época dele, a sociedade e o planeta estavam muito ruins, e o pouco que sobrou da humanidade foi para outro planeta. Ele ficou, por um objetivo egoísta: é obcecado pelos **anos 80** e quer usar a Âncora para ir viver lá. A Âncora é imprecisa: cada tentativa dele abre a fenda no chão da Biblioteca e puxa gente por acaso. Ele controla os robôs. A **Âncora** e o laboratório dele ficam no **D-Tec**, a parte de tecnologia da Unifor, no **Bloco M**. O **Bloco J foi descartado**.
- Em aberto, nas pendências do Enredo (12.2): como ele consegue o conhecimento (consciências roubadas, super IA ou as duas), se a IA continua existindo, por que os robôs caçam, e o resto da ficha dele.
- **Ideia 13 aprovada:** o pesquisador de 2019 se chama **Henrique**. A ficha virou `henrique.md`.
- **O Henrique engana o grupo**: esconde a ligação que tem com o Carlos (trabalha para ele ou foi enganado por ele, pendente). Quando o grupo descobre a mentira, todos vão atrás do Carlos. Isso resolve a pendência "Algum personagem atrapalha?" e entra no Enredo como "A virada", antes do Ato 4.
- **Ideias 20, 21 e 22 descartadas** (o pesquisador mentiu, o cientista que morreu, o drone).

**Por quê:** decisão do Davi.
**Afeta:** `docs/historia/enredo_principal.md` (seções 1, 2, 3, 4, 6, 7, 8, 11 e 12), a ficha nova `docs/historia/personagens/carlos.md`, `pesquisador.md` → `henrique.md`, as fichas de Clarice, Zane, Gabriel e robôs, `docs/historia/outras_ideias.md`, `docs/historia/template_documento.md`, `docs/README.md`, `docs/gdd.md`, `CLAUDE.md` e o agente `roteirista`.

## 2026-10-07 — Visual do Baltazar e do Rafael, com os sprites do Gabriel
**Decisão:**
- **Baltazar:** tricórnio de feltro, cabelo comprido preso com fita, casaca **vinho** aberta até a coxa (gasta, com remendo) e canhões largos, colete marrom com botões de latão, camisa de linho, calções, meias e sapato de fivela; a **luneta** de latão numa bandoleira de couro e o **anel** de ouro na mão direita. **Cor de identificação: vinho**, o tom do pau-brasil, um eco escuro do vermelho do Gabriel (a mesma família). Postura cerimoniosa e curiosa, passo curto.
- **Rafael:** uniforme de vigilante de 2008 **grande para ele**: camisa de manga curta **azul-celeste** com dragonas e bolsos azul-marinho, emblema amarelo na manga e no boné, crachá, calça azul-marinho e coturno; bigodinho ralo para parecer mais velho; **rádio HT** e lanterna antiga no cinto. **Cor de identificação: azul-celeste.** Peito estufado, passo de ronda.
- Os dois têm o **mesmo conjunto de sprites do Gabriel**: cinco vistas em 96 × 112, caminhada (12 quadros) e respiração (8 quadros) em cada vista, e três retratos de 80 × 80 (Baltazar: normal, encantado, aflito; Rafael: normal, rindo, triste).
- O roteiro de um personagem em pé (renderizar, juntar a paleta e gravar) virou `comum.gerar_em_pe`. O Zane passou a usar e saiu idêntico.

**Por quê:** pedido do Davi. O visual segue a direção de arte das fichas: o Baltazar "rapaz do século XVIII, de sítio, roupa gasta, luneta e anel visíveis"; o Rafael "uniforme de 2008 um pouco largo, tentando parecer mais velho, rádio e lanterna no cinto".
**Afeta:** `assets/modelagem/personagens/` (`comum.py`, `gerar_zane.py`, `gerar_baltazar.py` e `gerar_rafael.py` novos), `assets/sprites/personagens/baltazar/` e `rafael/` (novos), as fichas `baltazar.md` e `rafael.md` (direção de arte e arquivos), `CLAUDE.md`. Ainda não há cena de nenhum dos dois.

## 2026-10-07 — Visual do Zane, e Clarice e Zane com os sprites do Gabriel
**Decisão:**
- **Visual do Zane:** braço direito de prótese de metal com linhas de luz ciano, olho direito de implante, placa na têmpora e porta na nuca; jaqueta técnica curta **amarelo-ácido** com painéis grafite, zíper na diagonal e gola alta, com a manga do braço de metal cortada no ombro; camiseta preta comprida, calça larga com tiras, botas de sola branca grossa com friso de luz; cabelo raspado dos lados com o topo descolorido num topete. Postura confiante: peito aberto, queixo erguido, passo largo. **Cor de identificação: amarelo-ácido** (Gabriel vermelho, Clarice verde-azulado). O ciano dos implantes é o mesmo da interface holográfica dos áudios dele.
- **Clarice e Zane têm o mesmo conjunto de sprites do Gabriel**, nos mesmos tamanhos: cinco vistas em pé (lado, frente, 3/4, costas, 3/4 de costas) em 96 × 112, a caminhada (12 quadros) e a respiração (8 quadros) em cada vista, e três retratos de 80 × 80. A Clarice continua com os sprites sentados na estação do bunker.
- A caminhada, a respiração e o retrato passaram para o `comum.py`, usados pelos três. Os sprites do Gabriel e os sprites antigos da Clarice saíram idênticos.

**Por quê:** pedido do Davi: os dois personagens com todas as dimensões do Gabriel. O visual do Zane segue a direção de arte da ficha dele (implantes visíveis, roupa de um futuro que ninguém reconhece, destoar de todos).
**Afeta:** `assets/modelagem/personagens/` (`comum.py`, `gerar_gabriel.py`, `gerar_clarice.py`, `gerar_zane.py` novo), `assets/sprites/personagens/clarice/` e `zane/` (novo), `docs/historia/personagens/zane.md` (direção de arte e arquivos). Ainda não há cena do Zane nem da Clarice andando no Godot.

## 2026-10-07 — Ideias 6, 7 e 15 aprovadas: o Zane fica, o Baltazar volta e os esconderijos
**Decisão:**
- **Ideia 6:** no fim, **o Zane escolhe ficar em 3026** para tentar domar a IA por dentro, em vez de voltar para 2123.
- **Ideia 7:** **o Baltazar quer ficar em 3026, mas precisa voltar**, ou a família de Gabriel não existe. Gabriel tem que convencê-lo.
- **Ideia 15, com ajustes do Davi:** o **bunker** fica com a Clarice e o pesquisador (e depois o Zane); o **posto de guarda** fica com o Rafael; o **Baltazar** tem um esconderijo **dentro da Biblioteca** (no lugar do terraço da ideia original); a **Diana** fica numa das **salas de aula do Bloco de salas** (no lugar do posto de guarda da ideia original).

**Por quê:** aprovação do Davi das ideias 6, 7 e 15 de `docs/historia/outras_ideias.md`.
**Afeta:** `docs/historia/enredo_principal.md` (seções 5, 6, Atos 2 e 4 e pendências 12.1 e 12.3), as fichas de Baltazar, Zane, Gabriel, Clarice, pesquisador, Rafael e Diana, `docs/fases/bloco_de_salas.md`, e `docs/historia/outras_ideias.md` (as três ideias saíram).

## 2026-10-07 — A Âncora fica no Bloco J, e cada personagem tem a sua ficha completa
**Decisão:**
- A **Âncora** está no **Bloco J**, o bloco de tecnologia da Unifor. A fenda continua se abrindo no chão da Biblioteca.
- A descrição dos personagens (história, personalidade e relações) **saiu do Enredo Principal** e foi para as fichas em `docs/historia/personagens/`, **uma por personagem**. As fichas fazem parte do Enredo Principal e têm a mesma autoridade. O Enredo, na seção 4, ficou só com as regras do grupo, a lista de fichas e a IA.
- A pasta `personagens/` tem **só as fichas** (mais a dos robôs). O índice dela saiu, e o modelo de ficha foi para `docs/historia/template_personagem.md`.

**Por quê:** pedido do Davi.
**Afeta:** `docs/historia/enredo_principal.md` (seções 1, 2.2, 3, 4 e 7.2), as fichas de `docs/historia/personagens/`, `docs/historia/template_personagem.md`, `CLAUDE.md`, `docs/README.md`, `docs/gdd.md`, `docs/historia/README.md`, `docs/historia/roteiro/README.md`, `docs/historia/template_documento.md`, `docs/dialogos/template_dialogo.md`, os agentes `roteirista` e `artista`, `clarice/visual.md` e `gerar_clarice.py`.

## 2026-10-07 — Personagens e roteiro dentro de `docs/historia/`, uma ficha por personagem
**Decisão:**
- As pastas `docs/personagens/` e `docs/roteiro/` passam a ficar dentro de `docs/historia/`, junto do Enredo Principal.
- `antecessores.md` (versão antiga, com loops e personagens mortos) foi apagado. No lugar, **uma ficha por personagem**: `gabriel.md`, `baltazar.md`, `diana.md`, `clarice.md`, `rafael.md`, `pesquisador.md` e `zane.md`, além de `robos.md`.
- As fichas **não repetem a personalidade**, que fica só no Enredo Principal (a lei do projeto). Guardam o que a produção precisa: onde o personagem aparece, como chega ao jogador, função no jogo, parte para consertar a Âncora, suporte dos registros, direção de arte, arquivos e pendências. O `template_personagem.md` segue esse formato.
- `revelacao_central.md` (a história antiga, com loops) foi **apagado**; o texto continua no histórico do git. O `docs/historia/README.md` virou um índice curto que manda começar pelo Enredo Principal, sem repetir nada dele. O `template_documento.md` foi refeito com os campos reais do recurso `Documento` (`id`, `titulo`, `autor`, `papel`, `paginas`, `anotacao`), o papel de cada época e os limites de texto.

**Por quê:** pedido do Davi: deixar as fichas de personagem congruentes com o Enredo Principal e perto dele.
**Afeta:** `docs/historia/personagens/` e `docs/historia/roteiro/` (movidos), todos os links para as pastas antigas (docs, agentes, `CLAUDE.md`, `CONTRIBUTING.md`, `README.md`, comentários dos geradores em `assets/modelagem/`), `assets/sprites/personagens/clarice/visual.md` (dias no bunker, sem loops), `docs/mecanicas/registros_e_caderno.md` (sem os bilhetes de "G."), `docs/historia/README.md`, `docs/historia/template_documento.md` e `docs/historia/revelacao_central.md` (apagado).

## 2026-10-07 — Menu principal com a arte nova (imagem única)
**Decisão:** o menu principal troca a cena renderizada no Blender (três camadas) por **uma imagem só**, a partir da imagem de referência enviada pelo Davi: estante com livros e papéis, relógio, monitor CRT bege com o bilhete, luminária apagada, teclado, pilha de livros e caneca de café. O texto que vinha pintado na tela do monitor foi apagado por `assets/modelagem/menu/preparar_menu.py`, e o Godot desenha o menu por cima, nas mesmas posições e cores da imagem: título "ANKHOR" em 16 com brilho, itens em 8 a cada 14 px, barra azul de seleção de ponta a ponta do vidro. As telas de Fases, Opções e Controles usam o mesmo vidro. A luminária da imagem está apagada, então a piscada da luminária saiu; ficaram a tremulação do brilho da tela, o efeito CRT (mais leve, porque a imagem já tem linhas) e a vinheta escura nas bordas.
**Por quê:** pedido do Davi: trocar completamente a tela de menu pela imagem de referência.
**Afeta:** `assets/sprites/menu/menu_cena.png` (novo; saíram `menu_fundo`, `menu_mesa` e `menu_frente`), `assets/modelagem/menu/preparar_menu.py` e `menu_referencia.webp` (novos), `cenas/menu_principal.tscn` (o nó `Mesa` virou `Monitor`), `scripts/menu_principal.gd`. O `gerar_menu.py` fica, porque a cutscene `seg_acordar` reaproveita a cabine.

## 2026-10-06 — Enredo Principal vira a lei do projeto, personalidades, Diana e Rafael
**Decisão:**
- O **Enredo Principal** (`docs/historia/enredo_principal.md`) passa a ser a **lei do projeto** para história, mundo e personagens, acima de qualquer outro documento, inclusive deste registro. Em caso de dúvida em qualquer parte do jogo, vale o que ele diz. Mudanças de história entram no mesmo PR nele e aqui.
- **O policial de 1978 (Agostinho) vira mulher e se chama Diana**: recruta da polícia, dramática, ansiosa e impulsiva. **Valdir passa a se chamar Rafael** ("Seu Rafael").
- **Zane é homem**, e o defeito dele é confiar demais na tecnologia (a impulsividade ficou só com a Diana).
- **Gabriel é irônico**, de ironia seca, e é isso que combina com o sarcasmo da Clarice: os dois se provocam no mesmo tom.
- **Ordem de chegada:** o Zane é o último a chegar e Gabriel é o penúltimo. A fenda pulsa durante o jogo, e Gabriel recebe o Zane. A ordem dos outros cinco está pendente.
- Cada personagem ganhou uma **ficha de personalidade** (essência, traços, como fala, o que quer, o que teme, defeito e arco) e o grupo ganhou um quadro de relações entre eles.

**Por quê:** decisão do Davi: um documento único e profissional para consultar em caso de dúvida, e nomes e personalidades definidos antes de escrever falas e desenhar os personagens.
**Afeta:** `docs/historia/enredo_principal.md`, `CLAUDE.md`, `docs/README.md`, `docs/gdd.md`, `docs/historia/README.md`, `docs/personagens/README.md`, os agentes `roteirista`, `artista` e `sistemas`. As transmissões do rádio viraram `dados/transmissoes/rafael_01.tres` e `rafael_02.tres` (com "Aqui é o Seu Rafael"), e os gatilhos em `cenas/salas/biblioteca.tscn` viraram `GatilhoRafael1` e `GatilhoRafael2`. Comentários dos geradores de áudio e interface, `assets/audio/README.md`, `docs/fases/biblioteca.md` e `docs/mecanicas/` também. `revelacao_central.md` e `antecessores.md` continuam com a versão antiga, marcados como fora de uso.

## 2026-10-06 — Nova linha da história: a fenda é um acaso
**Decisão:**
- **Saem** os loops, os bilhetes de "G.", a Clarice como "a única que lembra" e a revelação de que Gabriel é o paradoxo da Âncora. Também foi descartada a ideia de a fenda ser um teste.
- **A fenda é um acaso.** A Âncora é **só uma máquina**: abandonada, falhou em 3026 e abriu uma fenda no chão da Biblioteca que pulsa e puxa, a cada poucos dias, quem estiver no ponto em alguma época. Os personagens precisam descobrir o que aconteceu e como voltar, e cada um traz uma parte para consertar a Âncora.
- **3026:** a humanidade abandonou a Terra e uma **IA** dominou. A IA não tem rosto. Para ela, humanos são invasores, e por isso os robôs atacam. Ser pego dá game over e volta ao checkpoint.
- **Personagens:** todos com **cerca de 20 anos**, todos com ligação com a região da Unifor, todos **vivos**, puxados com dias de diferença. Gabriel encontra cada um ao longo do jogo. Cada um tem um esconderijo, e um lugar como o bunker pode abrigar 2 ou 3. O personagem de **2041 foi cortado**. O professor de 2019 vira um aluno de iniciação científica (nome em aberto). Agostinho vira recruta da polícia, e Valdir, um segurança jovem.
- **Família Magalhães:** Gabriel se chama **Gabriel Magalhães**, e o **Baltazar** é antepassado dele. Gabriel descobre isso jogando, por um **anel desgastado** da avó que está no inventário desde o começo, igual ao do Baltazar. Gabriel conta para o Baltazar.
- **Clarice:** a relação dela com Gabriel vai sendo desenvolvida ao longo do jogo. O final dos dois está em aberto.
- **Pendentes:** o objetivo da IA; quem criou a Âncora (talvez um descendente de Gabriel); Gabriel falhando na tela enquanto o Baltazar estiver fora de 1750; prazo da fenda; como cada um volta; se alguém escolhe ficar; se algum personagem atrapalha; o nome do pesquisador.

**Por quê:** decisão do Davi: uma história mais simples e humana, com personagens vivos para interagir ao longo do jogo.
**Afeta:** `docs/historia/enredo_principal.md` (reescrito, com as pendências no fim). Ainda descrevem a versão antiga e precisam ser revistos: `docs/historia/revelacao_central.md`, `docs/personagens/antecessores.md`, `docs/mecanicas/sono_e_sonhos.md`, `docs/gdd.md`, `CLAUDE.md` (premissa) e as falas de loop em `dados/dialogos/clarice_primeiro_encontro.json`.

## 2026-10-06 — Menu principal mais claro, com a luminária acesa
**Decisão:** a cena do menu continua sendo a cabine de estudo da Biblioteca à noite, mas fica mais clara e legível: a **luminária de mesa está acesa** (luz quente no canto direito da mesa), tem uma caneca de café, uma pilha de livros maior à esquerda e a estante aparece melhor, com papéis largados nas prateleiras. O monitor está gasto: rachaduras na moldura, LED verde de ligado aceso, e teclas amareladas, afundadas ou faltando. A tela do monitor ganhou fundo com um leve clarão no centro, título com brilho, barra de seleção na largura toda da tela e, no efeito CRT, cantos arredondados e uma faixa clara que desce devagar. As bordas da cena escurecem com a mesma vinheta pixelada das salas, e a luz da luminária na mesa oscila de leve e de vez em quando falha por um instante, como lâmpada velha: na falha, a mesa fica mais escura que o normal. O cenário não se mexe mais com o mouse (a paralaxe saiu, e `scripts/camada_paralaxe.gd` foi apagado). O retângulo da tela não mudou (x 90–230, y 24–126).
**Por quê:** pedido do Davi, a partir de uma imagem de referência; o menu antigo era escuro demais e quase não se via a cena.
**Afeta:** `assets/modelagem/menu/gerar_menu.py` (e os PNGs de `assets/sprites/menu/`), `cenas/menu_principal.tscn`, `scripts/menu_principal.gd`, `shaders/tela_crt.gdshader`.

## 2026-10-02 — Trilha própria do Bunker
**Decisão:** o Bunker ganha uma trilha própria, mais escura que a da Biblioteca: Dó frígio, sem andamento, com o Dó grave "respirando", cordas graves, aço gemendo, um baque distante lá em cima e, na segunda metade, a fita da Clarice (quatro notas de piano elétrico gasto). Toca em todas as salas do bunker. O zumbido do bunker perdeu a ventilação que subia e descia: ficou só o transformador e um sopro grave constante.
**Por quê:** pedido do Davi: o som do bunker parecia mar (era a ventilação, um ruído largo pulsando a cada 2 s) e não combinava; pediu algo mais obscuro.
**Afeta:** `assets/modelagem/audio/gerar_trilha_bunker.py` e `assets/audio/musica/bunker/bunker_trilha.ogg` (novos), `cenas/sistemas/musica_bunker.tscn` (nova, usa `musica_fase.gd`), as 9 salas de `cenas/salas/bunker/`, `gerar_efeitos_bunker.py` e `bunker_zumbido.wav`, `assets/audio/README.md`, `docs/fases/bunker.md`.

## 2026-10-02 — Sem agachar
**Decisão:** o Gabriel não agacha mais. Saíram a ação `agachar` (`Ctrl` / `C`), a velocidade de 50%, o achatamento do sprite, a redução do alcance de visão dos robôs (×0,6) e o passo silencioso. Para não ser ouvido, o jogador agora anda em vez de correr; para não ser visto, apaga a lanterna e sai do cone.
**Por quê:** pedido do Davi.
**Afeta:** `project.godot` (ação `agachar`), `scripts/personagens/gabriel.gd` (o sinal `passo_dado` agora só leva `correndo`), `scripts/personagens/robo.gd`, `scripts/sistemas/passos.gd`, `cenas/menu_principal.tscn` (lista de controles), `docs/computacao/ia_e_perseguicao.md`, `docs/fases/labirinto.md`, `docs/mecanicas/movimentacao_e_terreno.md` (pisos alagados pedem andar devagar; as frestas que pediam agachar saíram), `docs/personagens/`, `docs/sugestao-melhoramento-futuro.md`.

## 2026-10-01 — Tela de pausa
**Decisão:** `Esc` (ou `P`, ou Start no controle) pausa o jogo em qualquer sala e abre a tela **PAUSADO**: Continuar, Opções (tela cheia e os três volumes, os mesmos do menu), **Voltar ao menu principal** (pede confirmação, porque o jogo ainda não salva e o progresso da fase se perde; o cursor começa em "Cancelar") e Sair do jogo. `Esc` dentro da pausa volta um passo. A pausa não abre por cima do inventário, de um documento, do diálogo ou da tela de morte (o `Esc` desses continua fechando eles), nem no menu e nas cutscenes. O jogo também pausa sozinho quando a janela perde o foco.
**Por quê:** pedido do Davi: poder voltar ao menu principal durante o jogo.
**Afeta:** `cenas/interface/tela_pausa.tscn` e `scripts/interface/tela_pausa.gd` (autoload `Pausa`), `project.godot` (autoload e ação `pausar`), `scripts/sistemas/configuracoes.gd` (as contas de volume saíram do menu e agora servem ao menu e à pausa), `scripts/menu_principal.gd`, `cenas/menu_principal.tscn` (lista de controles).

## 2026-09-30 — Gabriel e Clarice em resolução dobrada
**Decisão:** o projeto passa a usar o stretch **`canvas_items`** (antes `viewport`): a lógica, as câmeras e a interface continuam em 320×180, mas a imagem é desenhada na resolução da janela. Com isso, **Gabriel e Clarice ganham sprites com o dobro de pixels** (Gabriel 96 × 112 por quadro, a estação da Clarice 160 × 128, retratos 80 × 80), mostrados com escala 0,5: no mesmo tamanho na tela, com o dobro de detalhe (rosto, óculos, texto nos monitores). O cenário, os objetos, os robôs e a interface continuam em 1×. **Efeito colateral:** as luzes (PointLight2D) também são calculadas na resolução da janela e ficaram mais suaves. O efeito CRT do menu foi ajustado para continuar com uma linha por pixel do jogo.
**Por quê:** pedido do Davi. Com 48 px de altura, polígono a mais quase não aparecia (testado: mais gomos e luz suave só mudavam a folha de referência). Uma imagem comparando as duas resoluções na mesma cena decidiu.
**Afeta:** `project.godot` (`window/stretch/mode`), `gerar_gabriel.py` e `gerar_clarice.py` (`RESOLUCAO = 2`), todos os sprites dos dois, `gabriel.tscn` e `clarice.tscn` (escala 0,5), `gabriel.gd` (agachar respeita a escala), `caixa_dialogo.tscn` (retrato 80 × 80 em 40 × 40), `shaders/tela_crt.gdshader`. Os robôs e o Vigia podem ir para 2× do mesmo jeito, se o grupo quiser.

## 2026-09-30 — Salas fundas e personagens com mais detalhe
**Decisão:** (1) as **salas** do Bloco de salas e do Bunker passam a ser **fundas, mais altas que largas** (400 × 480 a 640 × 720), em vez de faixas compridas que pareciam corredor. A parede do fundo guarda as peças que contam a sala, e o chão desce para a câmera com o conteúdo organizado como a sala seria de verdade (fileiras de carteiras, de beliches, de macas, corredores de servidores e de estantes). Os **corredores continuam compridos**. Para isso o kit ganhou as peças de **chão de fundo** (repetem para baixo) e a **parede lateral**. (2) **Gabriel e Clarice** com mais polígonos: `DETALHE = 3` (cones e esferas com o triplo de gomos, quinas arredondadas) e sombreamento suave nas curvas, mais detalhes pequenos (cordões do capuz, cadarço, zíper e fivelas da mochila, sobrancelhas; na Clarice, mais cachos, zíper, bolsos e um botton).
**Por quê:** pedido do Davi: mais definição nos personagens, e as salas pareciam corredores.
**Afeta:** `comum.py` (`DETALHE`, `SUAVE`, `achatar_sombra`; os robôs e o Vigia ficam como estavam até alguém rodar os scripts deles com outro valor), `gerar_gabriel.py` e `gerar_clarice.py` e todos os sprites dos dois, `gerar_kit.py` e `gerar_bunker.py` (peças de fundo e laterais), as 12 salas de aula e as 7 salas do bunker.

## 2026-09-30 — Nova fase: Bunker, e a Clarice em pessoa
**Decisão:** começou a fase **Bunker**: o bunker de pesquisa embaixo do núcleo da Âncora, com dois setores (A e B, ligados por escada), 9 salas abertas (entrada, dois corredores, dormitório, refeitório, enfermaria, central de dados, gerador e depósito) e **seis portas lacradas** para fazer depois (escotilha da superfície, elevador, arsenal, laboratório, arquivo e a comporta do núcleo). A **Clarice aparece em pessoa** na central de dados, sentada na estação de trabalho dela, fixa ali, e **conversa** com o Gabriel. Entrou junto o **sistema de diálogos** (JSON em `dados/dialogos/`, caixa com retrato, texto letra por letra e escolhas) e o design completo dela, modelado no Blender.
**Por quê:** pedido do Davi.
**Muda o que estava decidido:** a ficha da Clarice dizia que ela era **só voz** (ligações) e que os dois **só se viam no final** ("é a primeira vez que se veem", na cena final da revelação central). O bunker resolve o "em aberto" de **onde ela está escondida**, mas o grupo precisa decidir: (a) o bunker fica perto do fim e a cena final muda, ou (b) as ligações continuam e o bunker é o primeiro encontro, com a cena final reescrita. Os diálogos de exemplo funcionam nos dois casos.
**Afeta:** `cenas/salas/bunker/` (9 cenas), kit do bunker (`gerar_bunker.py`, `cenas/cenario/bunker/`), luzes `luz_tubo` e `luz_emergencia`, `cenas/personagens/clarice.tscn`, `gerar_clarice.py`, sistema de diálogos (`scripts/sistemas/dialogos.gd`, autoload `Dialogos`, `cenas/interface/caixa_dialogo.tscn` no `modelo_sala.tscn`, `conversa_npc.gd`), `scripts/sistemas/porta.gd` (portas bloqueadas e som próprio), `dados/fases/08_bunker.tres` e o menu Fases, `gerar_efeitos_bunker.py`, docs (`fases/bunker.md`, `dialogos/`, `antecessores.md`).

## 2026-09-30 — Nova fase: Bloco de salas
**Decisão:** começou a fase **Bloco de salas** (os "Blocos de aula" do GDD): um bloco de dois andares, cada andar um corredor com **6 salas de aula** (101 a 106 no térreo, 201 a 206 no 1º andar), ligados por uma escada. O térreo está meio enterrado na areia e escuro; o 1º andar tem o teto aberto, sol e mato. Cada sala tem uma ideia própria para não ficar repetitivo (sala comum, invadida pela duna, barricada, laboratório, sala escura com robô desmontado, árvore, auditório, sala dos professores, chão que cedeu, sala "intacta demais", depósito). As lousas têm os tracinhos contados do GDD. Entra no menu Fases no lugar de "Blocos de aula". **É noite:** céu escuro com estrelas, luar pelas janelas e buracos e poucos lampiões; corredores de 2560 px e salas de 800 a 1280 px. Uma lanterna fica no começo do corredor (item único que o Gabriel já tem não aparece de novo no chão).
**Por quê:** pedido do Davi.
**Afeta:** `cenas/salas/bloco_de_salas/` (14 cenas novas), kit de cenário (`gerar_kit.py`: lousa, quadro de avisos, escadas, carteiras), `dados/fases/03_blocos_de_aula.tres`, `docs/fases/bloco_de_salas.md`. **Em aberto:** objetivo e história, robôs, ligação com a porta de saída da Biblioteca.

## 2026-09-30 — Biblioteca mais larga: ala leste
**Decisão:** a Biblioteca cresceu para a direita, de 960 para **1440 px** (4,5 telas de largura; a altura continua 420). A parte nova, depois da coluna onde a sala terminava, é a **ala leste** (sala de periódicos): terceiro buraco no teto com uma árvore nova, mesas, cabines e um segundo acervo no fundo sul. A porta de saída para os Blocos de aula foi para o fim da ala leste.
**Por quê:** pedido do Davi: a Biblioteca precisa ser maior, e desta vez na horizontal.
**Afeta:** `gerar_biblioteca.py` (medidas, parede, chão, primeiro plano, buracos), as 4 imagens em `assets/sprites/salas/biblioteca/`, `cenas/salas/biblioteca.tscn` (tamanho, limites, câmera, objetos, luzes, raios de sol) e `docs/fases/biblioteca.md`.

## 2026-09-30 — Gadgets em teste: cápsula de clarão, pedra e notebook
**Decisão:** os três gadgets sugeridos foram implementados **só na sala de teste**, para o grupo jogar e decidir: cápsula de clarão (paralisa os robôs perto, no máximo 2), pedra (barulho que atrai robôs, no máximo 5) e notebook (hackeia porta trancada ou robô por trás, gasta bateria, deixa o Gabriel parado e visível). Robôs ganharam o estado `ATORDOADO`. Ainda **em aberto:** em que fase cada um aparece (sugestão: clarão e pedra cedo, notebook na fase 3 ou 4), se o notebook usa as mesmas pilhas da lanterna e se cada gadget vem de uma das pessoas que vieram antes do Gabriel.
**Por quê:** pedido do Davi, para testar as ideias antes de colocar numa fase.
**Afeta:** `scripts/personagens/robo.gd`, `scripts/sistemas/inventario.gd` (itens que empilham), `scripts/itens/item.gd`, gadgets em `cenas/itens/` e `dados/itens/`, `scripts/sistemas/porta.gd` (porta trancada e som), sala de teste. Detalhes em `docs/mecanicas/itens_e_inventario.md`.

## 2026-09-30 — Aviso de pegar item mostra só a tecla
**Decisão:** perto de um item no chão ou de uma pilha, o aviso mostra só `[E]`, sem "Pegar lanterna" ou "Trocar a pilha". O nome aparece na mensagem depois de pegar e a descrição fica no inventário. Documentos continuam com `[E] Ler...`.
**Por quê:** pedido do Davi. O texto entregava o que era o item antes de o jogador chegar nele; só a tecla deixa a tela mais limpa, como nos jogos de terror de referência.
**Afeta:** `scripts/interface/hud.gd`, `scripts/itens/item_no_chao.gd`, `scripts/itens/pilha_no_chao.gd`, `docs/mecanicas/itens_e_inventario.md`.

## 2026-09-30 — Tela de Opções no menu e canais de áudio
**Decisão:** o botão **Opções** do menu abre uma tela com tela cheia, efeito CRT, **volume geral**, **música** e **efeitos**, e um atalho para a lista de **Controles**. As escolhas ficam salvas em `user://configuracoes.cfg` pelo autoload `Configuracoes`. O áudio passa a ter dois canais (*buses*) além do Master: **Musica** (trilhas do menu, das fases e do labirinto) e **Efeitos** (todo o resto). Todo som novo precisa escolher um dos dois no Inspetor (`Bus`), senão ignora o volume da tela de Opções.
**Por quê:** pedido do Davi, para o jogador ajustar som e vídeo sem sair do jogo.
**Afeta:** `cenas/menu_principal.tscn`, `scripts/menu_principal.gd`, `scripts/sistemas/configuracoes.gd` (novo), `scripts/sistemas/tela.gd`, `default_bus_layout.tres` (novo), `project.godot` (autoload) e todas as cenas com `AudioStreamPlayer`.

## 2026-09-30 — Destaque nos coletáveis e anotações dentro do inventário
**Decisão:** todo item coletável no cenário (itens no chão e pilhas) ganha um **destaque**: uma luz fraca que pulsa em volta e um brilho de pixel que pisca em cima do desenho, visível no escuro. O **Caderno do Gabriel** deixa de ser uma tela separada e vira a aba **ANOTAÇÕES** do inventário, com um cabeçalho de abas **ITENS | ANOTAÇÕES**. `Tab`/`I` abrem em Itens, `N` abre em Anotações e `Q` troca de aba. As anotações ficam numa lista, com um ponto nas não lidas, e o texto da escolhida aparece ao lado, em páginas de 7 linhas.
**Por quê:** pedido do Davi: os itens sumiam no escuro, e ter itens e anotações numa tela só, organizada por abas, deixa tudo mais fácil de achar.
**Afeta:** `cenas/itens/` (novo `destaque_coletavel.tscn`), `cenas/interface/tela_inventario.tscn`, `cenas/interface/painel_anotacoes.tscn` (novo), `tela_caderno.tscn` (removida), as salas que tinham a tela do caderno, `project.godot` (ação `trocar_aba`), `docs/mecanicas/`.

## 2026-09-30 — Fonte Galmuri7 no tamanho 8
**Decisão:** a fonte do jogo passa a ser a **Galmuri7** (OFL), nos tamanhos 8 e 16, no lugar da Ark Pixel 10. Todo texto que era 10 vira 8, e todo título que era 20 vira 16. A altura da linha continua 14 px, então nenhuma caixa de texto mudou de tamanho.
**Por quê:** pedido do Davi. O texto em 10 estava grande, mas a Ark Pixel é desenhada para 10 px, e no tamanho 8 as letras deformavam e ficavam ruins de ler. A Galmuri7 é desenhada para 8 px: ocupa quase o mesmo espaço (uma frase de teste mede 164 px, contra 152 da Ark em 8 e 186 da Ark em 10), fica nítida e tem todos os acentos do português. A Fusion Pixel 8px também foi testada, mas perde o acento das maiúsculas (Ã, É, Ç).
**Afeta:** `assets/fontes/`, `cenas/interface/tema_jogo.tres`, `cenas/interface/fonte_jogo.tres` (novo), as cenas com `font_size` próprio (`botao_pular`, `espaco_item`, `hud`, `tela_inventario`, `tela_morte`, `menu_principal`, `saida_fase`), `CLAUDE.md` e `docs/personagens/antecessores.md`.

## 2026-09-29 — Fonte Ark Pixel e labirinto sem checkpoints
**Decisão:** a fonte do jogo passa a ser a **Ark Pixel 10** (OFL), nos tamanhos 10 e 20, no lugar da Tiny5, que era pequena demais para ler. As telas com texto foram ajustadas: os papéis dos bilhetes cresceram para 248 × 156 px com 8 linhas por página, a legenda do rádio ficou mais alta e a lista de Fases do menu passou a rolar. Os textos do diário, do bilhete e das anotações foram encurtados um pouco para caber. O **labirinto não tem mais checkpoints**: a fase é pequena, e morrer recomeça do início. O sistema de checkpoint continua pronto para fases maiores.
**Por quê:** pedido do Davi (a Tiny5 estava ruim de ler; a Ark Pixel foi a mais legível na comparação com Micro 5, Bytesized, Press Start 2P, Kenney Mini, Kenney Pixel e Fusion Pixel).
**Afeta:** `cenas/interface/tema_jogo.tres`, `assets/fontes/`, `CLAUDE.md`, todas as telas com texto, `gerar_interface.py` (papéis), `dados/documentos/`, `gerar_labirinto.py` e `dados/labirinto/mapa_labirinto.tres`.

## 2026-09-29 — Fim dos fungos: lanterna a pilha e luzes de emergência
**Decisão:** saem os fungos bioluminescentes (pote de fungos, colônias, fungos pintados no cenário). A luz passa a ser elétrica: o Gabriel usa uma **lanterna a pilha** (feixe em cone, bateria de 4 min, recarregada com **pilhas** achadas no mapa) e o cenário tem **luminárias de emergência** de parede e **lampiões** no chão, que tremem e piscam. As cápsulas de clarão continuam previstas, como flash descartável.
**Por quê:** pedido do Davi.
**Afeta:** `gerar_biblioteca.py`, `gerar_kit.py` e `gerar_interface.py` (arte refeita), `cenas/salas/biblioteca.tscn` e `sala_exemplo.tscn`, itens (`lanterna`, `pilha_no_chao`), `docs/mecanicas/iluminacao_e_lanterna.md` (antes `iluminacao_e_fungos.md`), GDD e docs que citavam fungos.

## 2026-09-29 — Vida, checkpoint, Labirinto, robôs e menu Fases
**Decisão:**
- **Vida:** 3 corações; toque de robô tira 1, com 1,5 s de invulnerabilidade; zerou, volta ao último **checkpoint** com vida cheia.
- **Checkpoint:** postos de emergência no mapa; passar por um salva a posição e recupera os corações.
- **Labirinto:** segunda fase jogável, um subsolo escuro com saída marcada. A ordem na história está a definir.
- **Robôs:** os dois primeiros tipos, a **Sentinela** (visão) e o **Rastreador** (audição), modelados no Blender e com IA: máquina de estados, cone de visão por produto escalar, audição por BFS, perseguição por A\* e patrulha por cadeia de Markov.
- **Trilha adaptativa** do labirinto em duas camadas.
- **Menu Fases**, com todas as fases previstas. As que ainda não existem aparecem apagadas.

**Por quê:** pedido do Davi. Cobre boa parte dos conteúdos de computação exigidos pela disciplina.
**Afeta:** `project.godot` (autoloads `Vida` e `Checkpoints`), `cenas/salas/labirinto.tscn` e `scripts/labirinto/`, `cenas/personagens/robo_*.tscn`, `scripts/personagens/robo.gd`, HUD, Gabriel, `sala.gd`, menu. Detalhes em `docs/mecanicas/vida_e_checkpoint.md`, `docs/fases/labirinto.md` e `docs/computacao/ia_e_perseguicao.md` (seção 5).

## 2026-09-29 — Leitura de documentos, Caderno do Gabriel e rádio do Valdir
**Decisão:**
- Os documentos dos antecessores abrem numa tela de leitura que **pausa o jogo**, com um papel diferente para cada época.
- O que for útil vira uma anotação no **Caderno do Gabriel**, aberto com a tecla **N**.
- O **rádio do Valdir** é um item comum. Com ele no inventário, gatilhos no mapa tocam transmissões, com legenda e chiado, **sem pausar o jogo**.
- Na Biblioteca entraram o acampamento e o diário do Baltazar, o robô desmontado, os riscos de estrelas na árvore, o terminal com o bilhete da Clarice e duas transmissões do Valdir.
**Por quê:** pedido do Davi (itens 1 a 3 do que faltava implementar dos antecessores).
**Afeta:** `project.godot` (autoloads `Caderno` e `Radio`, ação `caderno`), `cenas/salas/biblioteca.tscn`, `cenas/salas/modelo_sala.tscn`, HUD, inventário, menu. Detalhes em `docs/mecanicas/registros_e_caderno.md`.

## 2026-09-29 — Revelação central aprovada, Clarice viva e o final
**Decisão:**
- A **revelação central** está aprovada. Gabriel é o paradoxo da Âncora: ela nasce do caderno dele, esquecido na Biblioteca em 2026. A fenda não puxa por acaso, e sim quem esteve no chão da Biblioteca. Os sonhos são ciclos que falharam. A premissa "a fenda puxa pessoas aleatórias" passa a ser o que o jogador acredita até a revelação.
- **Clarice está viva.** O jogador acha que ela morreu, mas ela fala com Gabriel **por ligação**, pelos telefones velhos do campus, e é a única que lembra dos loops.
- **Um só final, por enquanto: o feliz.** Com a pesquisa do professor, Gabriel recalibra a Âncora, e os dois ficam juntos em 2026. Chegou a ser escrito um final triste (cada um volta ao seu tempo e os dois nunca mais se veem), que saiu por decisão do Davi. O texto dele está no histórico do PR #33, se o grupo quiser de volta.

**Por quê:** decisão do Davi. Dá uma relação central e emocional à história, e fecha o loop com os dois juntos.
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

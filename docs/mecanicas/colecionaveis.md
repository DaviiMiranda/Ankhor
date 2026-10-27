# Mecânicas — Colecionáveis (uma coleção por fase, uma recompensa no quarto)

Cada fase esconde uma **coleção**: algumas peças espalhadas pelas salas, que o jogador acha por exploração, sem nenhuma pista no caminho principal. Quando junta todas, o **quarto do Gabriel** (o visor 3D da sala segura, ver [`visor_3d.md`](visor_3d.md)) ganha uma coisa nova. É uma recompensa só para quem procurou: não abre porta, não dá item e não muda a história.

Hoje existem cinco coleções, todas de **3 peças**:

| Fase | Coleção (`id`) | Peça | Recompensa no quarto |
|---|---|---|---|
| Biblioteca | `biblioteca` | **Pingente de farol** | Um **farol** aceso na mesa do Gabriel |
| Bloco de salas | `bloco_de_salas` | **Disquete colorido** (a cara dos disquetes da Clarice) | Uma **pilha de disquetes** na mesa, ao lado do farol |
| Labirinto | `labirinto` | **Pingente de chapéu** (as borlas do tricórnio do Baltazar) | O **tricórnio** na mesa, sobre o teclado do notebook, com os três pingentes nas pontas |
| Centro de Convivência | `centro_de_convivencia` | **Botão de jaqueta** (da jaqueta da Diana) | A **jaqueta** dela jogada na cama, com a camiseta listrada aparecendo |
| Bunker | `bunker` | **Chip hexagonal** (dos óculos do Zane) | Os **óculos** dele acesos no criado-mudo, com os três chips na armação |

## 1. As coleções

### 1.1 Biblioteca: pingentes de farol

| | |
|---|---|
| **Peça** | Pingente de farol: um pingente de metal com a forma do símbolo dos Faroleiros (torre, lanterna e três raios para cima), em âmbar. O símbolo está no [Enredo Principal](../historia/História_Completa.md), seção 2.4 |
| **Recompensa** | Um farol aceso na **mesa** do Gabriel, ao lado do notebook, com a luz pulsando devagar |

Todas ficam no chão, longe do caminho principal, com o mesmo brilho dos outros itens:

| Nº | Sala | Onde |
|---|---|---|
| 1 | Salão principal (2) | No fundo sul, perto do entulho e dos livros do canto esquerdo |
| 2 | Sala de terminais (8) | No canto esquerdo, ao lado dos livros caídos |
| 3 | Acervo sul (4) | Num dos corredores de baixo, entre as estantes (o Rastreador patrulha ali) |

As posições são `position` dos nós `PingenteFarol1`, `PingenteFarol2` e `PingenteFarol3` em `cenas/salas/biblioteca/salao.tscn`, `terminais.tscn` e `acervo.tscn`.

### 1.2 Bloco de salas: disquetes da Clarice

| | |
|---|---|
| **Peça** | Disquete de 3,5" **preto**, com os adesivos rosa e amarelo da Clarice e uma linha de caneta na etiqueta (o disquete azul das senhas, da Biblioteca, continua sendo outro item). O texto diz só "Parece coisa da Clarice": não diz por que estão espalhados |
| **Recompensa** | Uma pilha de três disquetes jogados na **mesa**, na frente do farol, perto da beira |

Ficam em salas que **não estão no caminho obrigatório** do bloco (nada a ver com a cadeia de chaves e códigos):

| Nº | Sala | Onde |
|---|---|---|
| 1 | 105 | No canto esquerdo, atrás das cadeiras, perto da pilha |
| 2 | 106 | Do lado esquerdo, entre as cadeiras e o entulho, longe da árvore |
| 3 | 202 | No meio da sala, perto da árvore da esquerda |

As posições são `position` dos nós `DisqueteClarice1`, `DisqueteClarice2` e `DisqueteClarice3` em `cenas/salas/bloco_de_salas/sala_105.tscn`, `sala_106.tscn` e `sala_202.tscn`.

### 1.3 Labirinto: pingentes do chapéu do Baltazar

| | |
|---|---|
| **Peça** | Pingente de chapéu: uma borla de fio vinho (a cor do Baltazar) presa a uma argola de latão, dessas que enfeitam as abas de um tricórnio. O chapéu é o objeto-símbolo do Baltazar (ficha em [`baltazar.md`](../historia/personagens/baltazar.md)). O texto não diz por que os pingentes estão soltos pelo subsolo |
| **Recompensa** | O **tricórnio** do Baltazar deitado sobre o teclado do notebook, com os três pingentes nas pontas das abas |

Aqui **a terceira peça tem uma trava**:

| Nº | Onde | Quando dá para pegar |
|---|---|---|
| 1 | Beco sem saída na ponta esquerda do labirinto, na parte de baixo do mapa (bloco 1, 31) | Sempre |
| 2 | Beco sem saída do corredor de cima, **perto da parede falsa** (bloco 13, 7) | Sempre |
| 3 | **Dentro do esconderijo do Baltazar**, no pé do cartaz de estrelas (bloco 18, 2) | **Só depois do primeiro encontro** com o Baltazar |

Até o primeiro encontro terminar (a marca `conheceu_baltazar`, que o diálogo `baltazar_labirinto_primeiro_encontro.json` grava ao acabar), o pingente 3 **não aparece**: não tem desenho, nem brilho, nem aviso **[E]**. Quando a conversa fecha, ele surge no chão. Quem entra na sala, vê o Baltazar e sai sem falar com ele não consegue pegá-lo. Como o pingente 2 fica no corredor logo abaixo da parede falsa, ele serve de pista de que há algo por ali.

As peças 1 e 2 são as letras `1` e `2` do mapa e a peça 3 é a letra `3` no desenho do esconderijo (`MODELO_ESCONDERIJO`), ambas em `assets/modelagem/salas/labirinto/gerar_labirinto.py` (ver a legenda em [`../fases/labirinto.md`](../fases/labirinto.md)). Quem coloca as três no mundo é `scripts/salas/labirinto.gd` (`_colocar_colecionavel`).

### 1.4 Centro de Convivência: botões da jaqueta da Diana

| | |
|---|---|
| **Peça** | Botão de jaqueta: botão grande de couro marrom-caramelo com aro dourado e quatro furos, a cor e a cara da jaqueta dela (`assets/sprites/personagens/diana/visual.md`; a jaqueta é o objeto-símbolo dela, [`diana.md`](../historia/personagens/diana.md)). O texto não diz por que os botões estão soltos |
| **Recompensa** | A **jaqueta** marrom-caramelo de gola larga, com bolsos e punhos, aberta sobre a camiseta listrada, jogada sobre a colcha da cama do Gabriel |

As três ficam no **mezanino**, a parte opcional da fase, em salas que não têm nada a ver com o caminho da Célula de Energia:

| Nº | Sala | Onde |
|---|---|---|
| 1 | Loja Universitária (`loja_uni`) | Entre o balcão do caixa e o cesto de promoção (410, 176) |
| 2 | Gráfica Quântica (`grafica`) | No espaço entre a estante de resmas e a copiadora (310, 180) |
| 3 | Cine Andrômeda (`cinema`), hall | Perto do cordão de fila e do abajur de chão (410, 200) |

São `BotaoJaqueta1` a `BotaoJaqueta3` nas cenas dessas salas.

### 1.5 Bunker: chips dos óculos do Zane

| | |
|---|---|
| **Peça** | Chip hexagonal: o hexágono do peito da jaqueta do Zane, em corpo escuro com borda e trilha ciano-verde, a cor da interface dele (`assets/sprites/personagens/zane/visual.md`; os óculos são o objeto-símbolo dele, [`zane.md`](../historia/personagens/zane.md)). O texto diz só que se encaixa na armação de um visor |
| **Recompensa** | Os **óculos** do Zane (armação grafite, lente verde acesa e os três chips hexagonais brilhando) em cima do criado-mudo, ao lado do despertador, com uma luz ciano fraca |

| Nº | Sala | Onde |
|---|---|---|
| 1 | Dormitório (`dormitorio`) | No corredor entre as fileiras de beliches (170, 280) |
| 2 | Refeitório (`refeitorio`) | No corredor do meio, entre as duas fileiras de mesas (240, 360) |
| 3 | Depósito (`deposito`, setor B) | Entre as estantes de metal, na fileira de cima (240, 190). O Rastreador patrulha o corredor do setor B |

São `ChipOculos1` a `ChipOculos3` nas cenas dessas salas.

## 2. O que o jogador vê

1. Ao pegar, abre a tela **Novo item** (a mesma dos itens da mochila), com o desenho da peça, a descrição e a contagem: **1 de 3**, **2 de 3**, **3 de 3**. No terceiro, a tela acrescenta "Os três estão com você." A peça **não vai para a mochila**: fica guardada só na coleção.
2. No **quadro branco** do quarto, uma linha por coleção mostra o progresso: *Pingentes de farol: 2 de 3*, *Disquetes da Clarice: 0 de 3*, *Pingentes do chapéu: 1 de 3*, *Botões da jaqueta* e *Chips dos óculos*. Com cinco coleções o quadro ficou cheio: o espaçamento entre as linhas (`ENTRELINHA` em `quadro_do_visor.gd`) foi apertado para tudo caber. Uma sexta linha já não cabe sem mais ajuste.
3. Com as três peças de uma coleção, a recompensa aparece no quarto. Com menos, o quarto fica como estava. As coleções são independentes.
4. No quarto, dá para **examinar** cada recompensa: olhando para ela, **[E] Examinar: <nome>** leva a câmera até a peça, que sobe um pouco e gira com **WASD** (ou setas) ou o **mouse**, com um painel de nome e descrição. **Esc** afasta. Detalhes em [`visor_3d.md`](visor_3d.md), seção 3.1.

## 3. Como funciona

### 3.1 Os dados

Uma coleção é um recurso `Colecao` (`scripts/sistemas/colecao.gd`), um arquivo por fase em `dados/colecoes/`:

| Campo | Para quê |
|---|---|
| `id` | Nome da coleção (`biblioteca`, `bloco_de_salas`, `labirinto`), usado nas chaves do save |
| `nome` | Aparece no quadro branco (*Pingentes de farol*) |
| `item` | Um `Item` só para mostrar a peça na tela Novo item (nome, descrição, ícone e sprite de chão). Ele **não** entra no inventário |
| `total` | Quantas peças tem |
| `texto_completa` | Frase extra na tela Novo item quando a coleção fecha |
| `nome_da_recompensa` | Título do painel ao examinar a recompensa no quarto (*Farol de mesa*) e do aviso **[E] Examinar** |
| `descricao_da_recompensa` | Texto do painel ao examinar. Só descreve o que se vê, sem afirmar nada de história |

### 3.2 O estado

O autoload **`Colecionaveis`** (`scripts/sistemas/colecionaveis.gd`) guarda o que já foi achado num dicionário `pecas` (chave `"biblioteca:2"`, valor `true`) e responde:

- `coletar(colecao, numero)`: marca a peça e avisa com os sinais `coletado` e, ao fechar, `completada`;
- `tem(id, numero)`, `quantidade(id)` e `completa(colecao)`;
- `todas()`: lista as coleções de `dados/colecoes/` (o quadro branco usa para escrever uma linha por coleção);
- `limpar()`: chamado em **Novo jogo** (`menu_principal.gd`) e ao carregar um save.

O estado entra no **save** (`Salvamento`, seção `colecionaveis`): quem salvou com 2 pingentes volta com 2. Como o visor lê o mesmo estado que vai para o save, a recompensa aparece no quarto na hora, sem precisar salvar antes.

### 3.3 A peça no mundo

`ColecionavelNoMundo` (`cenas/itens/colecionavel_no_mundo.tscn`, `scripts/itens/colecionavel_no_mundo.gd`) é um `Interagivel` como o `ItemNoChao`: sprite pequeno no chão (o `sprite_chao` do item), o brilho de colecionável (`DestaqueColetavel`) e o aviso **[E]**. Cada peça diz **de qual coleção é** (`colecao`) e **qual número é** (`numero`, de 1 até `total`). Se a peça já foi coletada, ela some sozinha ao entrar na sala (`queue_free` no `_ready`), então voltar à sala não faz a peça reaparecer.

Ao interagir, ele chama `Colecionaveis.coletar` e `ItemNovo.mostrar_novo(colecao.item_com_progresso(n))`, que monta uma cópia do item com a contagem na descrição.

**Peça com trava.** O campo `marca_necessaria` (vazio por padrão) guarda o nome de uma marca de `Progresso`. Enquanto a marca não existe, o desenho e o brilho ficam escondidos e `pode_interagir()` devolve `false` (então nem o aviso aparece). O nó escuta `Progresso.mudou` e mostra a peça no instante em que a marca é gravada. Só os filhos são escondidos, não o nó da peça: quem mostra e esconde o conteúdo do esconderijo do Baltazar é a parede falsa, que mexe na visibilidade do nó inteiro.

### 3.4 As recompensas no quarto

- **Farol** (`FarolDaMesa`, `cenas/visor/farol_da_mesa.tscn`, `scripts/visor/farol_da_mesa.gd`): um `Node3D` com o modelo e uma `OmniLight3D` âmbar. No `_ready`, fica **visível só se `Colecionaveis.completa(colecao)`**; invisível, também desliga a luz e o `_process`. A luz pulsa entre `energia_minima` e `energia_maxima` em `periodo_pulso` segundos, com uma onda $\frac{1 - \cos(2\pi t / T)}{2}$ (começa e termina devagar, como as luzes do jogo). Está em cima da escrivaninha, na ponta da frente (longe dos papéis, do notebook e da luminária), virado para a cadeira.
- **Disquetes** (`DisquetesDaMesa`, `cenas/visor/disquetes_da_mesa.tscn`) e **tricórnio** (`ChapeuDoNotebook`, `cenas/visor/chapeu_do_notebook.tscn`): `Node3D` com o script `RecompensaDoQuarto` (`scripts/visor/recompensa_do_quarto.gd`), que só faz o `visible` valer `Colecionaveis.completa(colecao)`. Sem pulso e sem luz própria: a escrivaninha já é iluminada pela luminária. Os três objetos ficam na **escrivaninha**, na faixa livre da frente, porque os papéis lidos cobrem o resto do tampo: o farol em z 0,3, os **disquetes** logo na frente dele (x -1,95, z 0,44, girados 10°) e o **tricórnio** sobre o teclado do notebook (x -2,29, y 0,78, z 0,3), a 55% do tamanho do modelo para caber nos 24 cm do teclado sem encostar na tela. Ele fica menor que um chapéu de verdade: é um enfeite, como o farol de 18 cm.

- **Jaqueta** (`JaquetaDaCama`, `cenas/visor/jaqueta_da_cama.tscn`) e **óculos** (`OculosDoCriado`, `cenas/visor/oculos_do_criado.tscn`): também com o `RecompensaDoQuarto`. A jaqueta fica **sobre a colcha** (a colcha está a 0,545 m do chão; a 0,5 a jaqueta sumia dentro dela), a 75% do tamanho do modelo, com a gola para o lado da cabeceira. Os óculos ficam em pé no canto livre do **criado-mudo** (x 2,13, y 0,53, z 1,27), virados para o quarto, com uma `OmniLight3D` ciano fraca.

Todas as cinco recompensas são **examináveis**: `RecompensaDoQuarto` é um `FocoVisor` (o `FarolDaMesa` herda dele e só acrescenta o pulso da luz). Para ajustar de onde a câmera olha, mude `direcao_da_camera` da instância em `sala_visor.tscn`; o tamanho do enquadramento sai do modelo sozinho (`ocupacao` só muda o quanto a peça enche a tela).

A **mesa não tem mais lugar**: os papéis lidos cobrem o tampo e a faixa livre da frente já tem o farol, os disquetes e o tricórnio. Por isso a jaqueta e os óculos foram para a cama e o criado-mudo.

Os **modelos** saem do Blender sem abrir a janela (como rodar e as medidas estão no começo de cada arquivo):

| Modelo | Gerador |
|---|---|
| `assets/modelos/farol_mesa.glb` | `assets/modelagem/cenario/gerar_farol_mesa.py` |
| `assets/modelos/disquetes_mesa.glb` | `assets/modelagem/cenario/gerar_disquetes_mesa.py` |
| `assets/modelos/chapeu_baltazar.glb` | `assets/modelagem/cenario/gerar_chapeu_baltazar.py` |
| `assets/modelos/jaqueta_diana.glb` | `assets/modelagem/cenario/gerar_jaqueta_diana.py` |
| `assets/modelos/oculos_zane.glb` | `assets/modelagem/cenario/gerar_oculos_zane.py` |

O **desenho em pixel** das peças (ícone e chão) sai de `assets/modelagem/itens/gerar_pingente_farol.py`, `gerar_disquete_colecionavel.py`, `gerar_pingente_chapeu.py`, `gerar_botao_jaqueta.py` e `gerar_chip_oculos.py`.

## 4. Como pôr uma coleção nova (outra fase)

1. Crie o `Item` da peça em `dados/itens/` (nome, descrição, ícone 16 × 16 e `sprite_chao`).
2. Crie a `Colecao` em `dados/colecoes/` (um `.tres` com o `id` da fase, o `nome`, o `item`, o `total`).
3. Ponha `colecionavel_no_mundo.tscn` nas salas da fase, com `colecao` e `numero` de 1 até `total`. Para travar uma peça atrás de um acontecimento, preencha `marca_necessaria`. (Num mapa gerado, como o do Labirinto, a sala cria as peças pelas letras do mapa.)
4. Preencha `nome_da_recompensa` e `descricao_da_recompensa` na `Colecao`.
5. Crie a recompensa no quarto: uma cena com o script `RecompensaDoQuarto` (um `Node3D` com `colecao` e o modelo, que **precisa se chamar `Modelo`**), posta em `sala_visor.tscn` com a `direcao_da_camera`. Ela já nasce examinável. O quadro branco já ganha a linha sozinho.

## 5. Pendências

- **De quem são os pingentes de farol** e por que estão espalhados pela Biblioteca. O Enredo Principal ainda não decidiu onde os Faroleiros estão hoje nem se aparecem no jogo (seção "Pendências" dele). Até lá, o texto não afirma nada. O mesmo vale para os disquetes (por que estão fora do posto da Clarice) e para os pingentes do chapéu (como foram parar no subsolo).
- **Mais coleções** (D-Tec): pede uma peça e uma recompensa no quarto. Sobram a estante, o móvel da TV, o chão e as paredes; a mesa, a cama e o criado-mudo estão ocupados. O quadro branco já está no limite.
- A recompensa só aparece no **visor**. Não há conquista nem contador na pausa do inventário.
- As **posições** das peças e o tamanho/posição dos modelos no quarto são primeira versão, para ajustar jogando (nada foi testado dentro do Godot ainda).

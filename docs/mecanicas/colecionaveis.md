# Mecânicas — Colecionáveis (uma coleção por fase, uma recompensa no quarto)

Cada fase esconde uma **coleção**: algumas peças espalhadas pelas salas, que o jogador acha por exploração, sem nenhuma pista no caminho principal. Quando junta todas, o **quarto do Gabriel** (o visor 3D da sala segura, ver [`visor_3d.md`](visor_3d.md)) ganha uma coisa nova. É uma recompensa só para quem procurou: não abre porta, não dá item e não muda a história.

Hoje existem três coleções, todas de **3 peças**:

| Fase | Coleção (`id`) | Peça | Recompensa no quarto |
|---|---|---|---|
| Biblioteca | `biblioteca` | **Pingente de farol** | Um **farol** aceso na mesa do Gabriel |
| Bloco de salas | `bloco_de_salas` | **Disquete colorido** (a cara dos disquetes da Clarice) | Uma **pilha de disquetes** na mesa, ao lado do farol |
| Labirinto | `labirinto` | **Pingente de chapéu** (as borlas do tricórnio do Baltazar) | O **tricórnio** na mesa, sobre o teclado do notebook, com os três pingentes nas pontas |

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

## 2. O que o jogador vê

1. Ao pegar, abre a tela **Novo item** (a mesma dos itens da mochila), com o desenho da peça, a descrição e a contagem: **1 de 3**, **2 de 3**, **3 de 3**. No terceiro, a tela acrescenta "Os três estão com você." A peça **não vai para a mochila**: fica guardada só na coleção.
2. No **quadro branco** do quarto, uma linha por coleção mostra o progresso: *Pingentes de farol: 2 de 3*, *Disquetes da Clarice: 0 de 3*, *Pingentes do chapéu: 1 de 3*.
3. Com as três peças de uma coleção, a recompensa aparece no quarto. Com menos, o quarto fica como estava. As três coleções são independentes.

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

Os **modelos** saem do Blender sem abrir a janela (como rodar e as medidas estão no começo de cada arquivo):

| Modelo | Gerador |
|---|---|
| `assets/modelos/farol_mesa.glb` | `assets/modelagem/cenario/gerar_farol_mesa.py` |
| `assets/modelos/disquetes_mesa.glb` | `assets/modelagem/cenario/gerar_disquetes_mesa.py` |
| `assets/modelos/chapeu_baltazar.glb` | `assets/modelagem/cenario/gerar_chapeu_baltazar.py` |

O **desenho em pixel** das peças (ícone e chão) sai de `assets/modelagem/itens/gerar_pingente_farol.py`, `gerar_disquete_colecionavel.py` e `gerar_pingente_chapeu.py`.

## 4. Como pôr uma coleção nova (outra fase)

1. Crie o `Item` da peça em `dados/itens/` (nome, descrição, ícone 16 × 16 e `sprite_chao`).
2. Crie a `Colecao` em `dados/colecoes/` (um `.tres` com o `id` da fase, o `nome`, o `item`, o `total`).
3. Ponha `colecionavel_no_mundo.tscn` nas salas da fase, com `colecao` e `numero` de 1 até `total`. Para travar uma peça atrás de um acontecimento, preencha `marca_necessaria`. (Num mapa gerado, como o do Labirinto, a sala cria as peças pelas letras do mapa.)
4. Crie a recompensa no quarto: uma cena com o script `RecompensaDoQuarto` (um `Node3D` com `colecao` e o modelo), posta em `sala_visor.tscn`. O quadro branco já ganha a linha sozinho.

## 5. Pendências

- **De quem são os pingentes de farol** e por que estão espalhados pela Biblioteca. O Enredo Principal ainda não decidiu onde os Faroleiros estão hoje nem se aparecem no jogo (seção "Pendências" dele). Até lá, o texto não afirma nada. O mesmo vale para os disquetes (por que estão fora do posto da Clarice) e para os pingentes do chapéu (como foram parar no subsolo).
- **Mais coleções** (Convivência, Bunker, D-Tec): cada uma pede uma peça e uma recompensa no quarto. A faixa livre da mesa acabou (farol, disquetes e tricórnio); sobram o criado-mudo, a estante, o móvel da TV, a cama, o chão e as paredes.
- A recompensa só aparece no **visor**. Não há conquista nem contador na pausa do inventário.
- As **posições** das peças e o tamanho/posição dos modelos no quarto são primeira versão, para ajustar jogando (nada foi testado dentro do Godot ainda).

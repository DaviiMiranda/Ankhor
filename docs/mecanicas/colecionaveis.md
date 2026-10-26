# Mecânicas — Colecionáveis (uma coleção por fase, uma recompensa no quarto)

Cada fase esconde uma **coleção**: algumas peças espalhadas pelas salas, que o jogador acha por exploração, sem nenhuma pista no caminho principal. Quando junta todas, o **quarto do Gabriel** (o visor 3D da sala segura, ver [`visor_3d.md`](visor_3d.md)) ganha uma coisa nova. É uma recompensa só para quem procurou: não abre porta, não dá item e não muda a história.

Hoje só existe a coleção da **Biblioteca**: três **pingentes de farol**, que acendem um **farol** em 3D na mesa do Gabriel.

## 1. A coleção da Biblioteca

| | |
|---|---|
| **Peça** | Pingente de farol: um pingente de metal com a forma do símbolo dos Faroleiros (torre, lanterna e três raios para cima), em âmbar. O símbolo está no [Enredo Principal](../historia/História_Completa.md), seção 2.4 |
| **Quantas** | 3 |
| **Recompensa** | Um farol aceso na **mesa** do Gabriel, no quarto do visor 3D |

### 1.1 Onde estão

Todas ficam no chão, longe do caminho principal, com o mesmo brilho dos outros itens:

| Nº | Sala | Onde |
|---|---|---|
| 1 | Salão principal (2) | No fundo sul, perto do entulho e dos livros do canto esquerdo |
| 2 | Sala de terminais (8) | No canto esquerdo, ao lado dos livros caídos |
| 3 | Acervo sul (4) | Num dos corredores de baixo, entre as estantes (o Rastreador patrulha ali) |

A ordem de pegar não importa. As posições são `position` dos nós `PingenteFarol1`, `PingenteFarol2` e `PingenteFarol3` em `cenas/salas/biblioteca/salao.tscn`, `terminais.tscn` e `acervo.tscn`.

### 1.2 O que o jogador vê

1. Ao pegar, abre a tela **Novo item** (a mesma dos itens da mochila), com o desenho do pingente, a descrição e a contagem: **1 de 3**, **2 de 3**, **3 de 3**. No terceiro, a tela acrescenta "Os três estão com você." O pingente **não vai para a mochila**: fica guardado só na coleção.
2. No **quadro branco** do quarto, uma linha nova mostra o progresso: *Pingentes de farol: 2 de 3*.
3. Com os três, o **farol** aparece na mesa do quarto, ao lado do notebook, acesa na cor âmbar, com a luz pulsando devagar. Com menos de três, a mesa fica como estava.

O texto do pingente não diz de quem ele era nem por que está ali: o Enredo Principal ainda não responde onde os Faroleiros estão hoje (ver Pendências).

## 2. Como funciona

### 2.1 Os dados

Uma coleção é um recurso `Colecao` (`scripts/sistemas/colecao.gd`), um arquivo por fase em `dados/colecoes/`:

| Campo | Para quê |
|---|---|
| `id` | Nome da coleção (`biblioteca`), usado nas chaves do save |
| `nome` | Aparece no quadro branco (*Pingentes de farol*) |
| `item` | Um `Item` só para mostrar a peça na tela Novo item (nome, descrição, ícone e sprite de chão). Ele **não** entra no inventário |
| `total` | Quantas peças tem |
| `texto_completa` | Frase extra na tela Novo item quando a coleção fecha |

### 2.2 O estado

O autoload **`Colecionaveis`** (`scripts/sistemas/colecionaveis.gd`) guarda o que já foi achado num dicionário `pecas` (chave `"biblioteca:2"`, valor `true`) e responde:

- `coletar(colecao, numero)`: marca a peça e avisa com os sinais `coletado` e, ao fechar, `completada`;
- `tem(id, numero)`, `quantidade(id)` e `completa(colecao)`;
- `todas()`: lista as coleções de `dados/colecoes/` (o quadro branco usa para escrever uma linha por coleção);
- `limpar()`: chamado em **Novo jogo** (`menu_principal.gd`) e ao carregar um save.

O estado entra no **save** (`Salvamento`, seção `colecionaveis`): quem salvou com 2 pingentes volta com 2. Como o visor lê o mesmo estado que vai para o save, o farol aparece no quarto na hora, sem precisar salvar antes.

### 2.3 A peça no mundo

`ColecionavelNoMundo` (`cenas/itens/colecionavel_no_mundo.tscn`, `scripts/itens/colecionavel_no_mundo.gd`) é um `Interagivel` como o `ItemNoChao`: sprite pequeno no chão (o `sprite_chao` do item), o brilho de colecionável (`DestaqueColetavel`) e o aviso **[E]**. Cada peça diz **de qual coleção é** (`colecao`) e **qual número é** (`numero`, de 1 até `total`). Se a peça já foi coletada, ela some sozinha ao entrar na sala (`queue_free` no `_ready`), então voltar à sala não faz o pingente reaparecer.

Ao interagir, ele chama `Colecionaveis.coletar` e `ItemNovo.mostrar_novo(colecao.item_com_progresso(n))`, que monta uma cópia do item com a contagem na descrição.

### 2.4 O farol no quarto

`FarolDaMesa` (`cenas/visor/farol_da_mesa.tscn`, `scripts/visor/farol_da_mesa.gd`) é um `Node3D` com o modelo e uma `OmniLight3D` âmbar. No `_ready`, ele fica **visível só se `Colecionaveis.completa(colecao)`**; invisível, também desliga a luz e o `_process`. A luz pulsa entre `energia_minima` e `energia_maxima` em `periodo_pulso` segundos, com uma onda $\frac{1 - \cos(2\pi t / T)}{2}$ (começa e termina devagar, como as luzes do jogo). O nó está em `cenas/visor/sala_visor.tscn`, em cima da escrivaninha, na ponta da frente (longe dos papéis, do notebook e da luminária), virado para a cadeira.

O **modelo** (`assets/modelos/farol_mesa.glb`) sai do Blender por `assets/modelagem/cenario/gerar_farol_mesa.py` (como rodar e as medidas estão no começo do arquivo): torre em quatro faixas de latão, galeria, lanterna de vidro aceso (material com brilho próprio), telhado e os **três raios em leque**, também com brilho próprio, que o *glow* do quarto transforma em halo. Tem 18 cm de altura. O **desenho em pixel** do pingente (ícone e chão) sai de `assets/modelagem/itens/gerar_pingente_farol.py`.

## 3. Como pôr uma coleção nova (outra fase)

1. Crie o `Item` da peça em `dados/itens/` (nome, descrição, ícone 16 × 16 e `sprite_chao`).
2. Crie a `Colecao` em `dados/colecoes/` (um `.tres` com o `id` da fase, o `nome`, o `item`, o `total`).
3. Ponha `colecionavel_no_mundo.tscn` nas salas da fase, com `colecao` e `numero` de 1 até `total`.
4. Crie a recompensa no quarto: uma cena como `farol_da_mesa.tscn` (um `Node3D` com `colecao` e o modelo), posta em `sala_visor.tscn`. O quadro branco já ganha a linha sozinho.

## 4. Pendências

- **De quem são os pingentes** e por que estão espalhados pela Biblioteca. O Enredo Principal ainda não decidiu onde os Faroleiros estão hoje nem se aparecem no jogo (seção "Pendências" dele). Até lá, o texto não afirma nada.
- **Mais coleções** (Bloco de salas, Convivência, Bunker, D-Tec): cada uma pede uma peça e uma recompensa no quarto. O quarto só tem uma mesa e uma estante livre hoje.
- A recompensa só aparece no **visor**. Não há conquista nem contador na pausa do inventário.

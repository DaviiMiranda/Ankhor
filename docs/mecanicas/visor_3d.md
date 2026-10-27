# Mecânicas — O visor 3D: o quarto do Gabriel (salvar em primeira pessoa)

Quando o Gabriel põe os óculos do Zane na sala segura ([`sala_segura.md`](sala_segura.md)), o jogo **vira 3D em primeira pessoa**. Ele aparece no **próprio quarto, a mente dele materializada**: o quarto de 2026 do prólogo (`seg_prologo`, cena 2), com a janela do pôr do sol, a escrivaninha, a estante, a cama e as paredes cheias de pôsteres (Fortaleza com jangada, um jogo de nave, o robô de olhos vermelhos, a folha de equações de Modelagem e Simulação, um calendário de 2026, a flâmula da Unifor e a foto da equipe do jogo, na parede do fundo, entre a estante e a TV), só que sem teto. As paredes terminam numa linha ciano e, acima delas, é o escuro, cheio de pontos de luz coloridos, cortado de vez em quando por estrelas cadentes e luzes que passam rápido (só no céu, nunca dentro do quarto). É um quarto lembrado, não um quarto de verdade.

O quarto guarda o jogo até ali. Tudo o que aparece nele vem do estado do jogo naquele momento (o mesmo que vai para o save):

| Onde | O que mostra | De onde vem |
|---|---|---|
| **TV de tubo**, no móvel do fundo | o menu de salvar | `Salvamento` |
| **Mural de cortiça**, em cima da cama | um cartão para cada anotação do caderno, presos com alfinete e ligados por um fio vermelho, na ordem em que foram anotados | `Caderno.anotacoes` |
| **Escrivaninha**, embaixo da janela | os documentos que o Gabriel já leu, jogados em cima da mesa, cada um no papel dele (caderno, pergaminho...) | os documentos de `dados/documentos/` que já têm anotação no caderno |
| **Farol**, na ponta da frente da escrivaninha | um farol aceso em 3D, só depois de juntar os três pingentes de farol da Biblioteca (ver [`colecionaveis.md`](colecionaveis.md)) | `Colecionaveis` |
| **Disquetes**, na escrivaninha, na frente do farol | uma pilha de três disquetes coloridos, só depois de juntar os três disquetes do Bloco de salas | `Colecionaveis` |
| **Tricórnio**, sobre o teclado do notebook, na escrivaninha | o chapéu do Baltazar com os três pingentes nas pontas, só depois de juntar os três pingentes do Labirinto (um deles só aparece depois do primeiro encontro com o Baltazar) | `Colecionaveis` |
| **Jaqueta**, sobre a colcha da cama | a jaqueta da Diana, só depois de juntar os três botões do Centro de Convivência | `Colecionaveis` |
| **Óculos**, no criado-mudo, ao lado do despertador | os óculos do Zane com os três chips acesos, só depois de juntar os três chips do Bunker | `Colecionaveis` |
| **Quadro branco**, ao lado da TV | os números do jogo: fase, documentos lidos, transmissões ouvidas, anotações, portas destrancadas, itens na mochila, o progresso de cada coleção (*Pingentes de farol: 2 de 3*, *Disquetes da Clarice*, *Pingentes do chapéu*, *Botões da jaqueta*, *Chips dos óculos*) e o último save | `Caderno`, `Radio`, `Porta`, `Inventario`, `Colecionaveis`, `Salvamento` |

Nada disso é texto novo de história: os cartões e os papéis mostram os títulos que já existem, e o texto completo é o mesmo que o jogador leu no caminho. Ao tirar os óculos, ele volta para a sala segura 2D, no mesmo lugar, e toca a animação de devolver os óculos ao pedestal.

## 1. Como o jogador usa

| Onde | Teclas |
|---|---|
| Andando no quarto | **WASD** (ou setas) anda, **mouse** olha, **Esc** tira os óculos |
| Perto de um dos quatro lugares, virado para ele | aparece **[E] Usar a tela**, **[E] Olhar o mural**, **[E] Ver os papéis** ou **[E] Ler o quadro**; E leva a câmera até lá |
| Na TV | **W/S** (ou ↑/↓) escolhe, **E** (ou Enter) confirma, **Esc** afasta a câmera |
| No mural ou na mesa | **WASD** (ou setas) escolhe o papel (fica com borda ciano), **E** abre para ler, **Esc** afasta a câmera |
| Lendo | **E** vira a página, **setas** folheiam, **Esc** fecha (a mesma tela de leitura dos documentos do jogo) |
| No quadro | **Esc** afasta a câmera |
| Numa recompensa de coleção (farol, disquetes, tricórnio, jaqueta, óculos) | **WASD** (ou setas) e o **mouse** giram a peça, **Esc** afasta a câmera. Detalhes na seção 3.1 |

O menu da TV tem **Salvar jogo** e **Voltar** (que tira os óculos). Em cima ele mostra a data e a hora do último save, ou "Nenhum jogo salvo". Ao salvar, toca o som de salvar, aparece **Jogo salvo** (ou **Não foi possível salvar**) e o quadro branco já mostra a hora nova. Dá para salvar quantas vezes quiser.

Salvar faz o mesmo que antes: a vida volta a 3 e o pedestal vira o checkpoint da fase. **Entrar no visor e sair sem salvar não muda nada.** O HUD da sala segura só mostra "Jogo salvo" na volta se o jogador salvou.

A pausa (Esc) não abre dentro do visor: lá o Esc serve para afastar ou tirar os óculos.

## 2. Como a troca entre 2D e 3D funciona

A sala segura **não é recarregada**. O autoload `Visor` (`scripts/sistemas/visor.gd`):

1. **`abrir(cena, posição)`**, chamado pela `MaquinaDeSalvar` com a tela já escura: tira a sala 2D da árvore de cenas (`remove_child`), **sem apagar**, e põe a cena 3D no lugar. A sala fica guardada na memória, com o Gabriel parado de óculos no rosto, a máquina no meio da animação e tudo o mais como estava.
2. **`salvar()`**, chamado pelo menu da TV: limpa a vida, marca o checkpoint e grava o arquivo (`Salvamento.salvar`) com a cena e a posição que a máquina passou.
3. **`fechar()`**, ao tirar os óculos: apaga a cena 3D, devolve a sala 2D à árvore e emite **`fechado(salvou)`**.

A `MaquinaDeSalvar` fica esperando esse sinal (`await Visor.fechado`). Quando ele chega, ela clareia a tela e toca a animação de tirar os óculos de trás para a frente, como antes.

Por que não recarregar a sala: não precisa passar a posição do Gabriel nem um "estou voltando do visor" entre cenas, e nada da sala se perde (itens no chão, portas, música). Cuidados que isso exigiu:

- A `SalaSegura` liga o sinal que remove robôs em `_enter_tree` (antes era em `_ready`, que não roda de novo quando a sala volta à árvore).
- O som de salvar saiu da máquina e foi para a TV (`cenas/visor/menu_visor.tscn`).
- O quarto tem a **própria** tela de leitura (`TelaDocumento`) e a chama direto. Ele **não** usa `Caderno.ler()`: esse sinal também chegaria à tela de leitura da sala 2D, que está guardada fora da árvore.

## 3. Os quatro lugares (`FocoVisor`)

TV, mural, mesa e quadro são todos um **`FocoVisor`** (`scripts/visor/foco_visor.gd`), cada um na sua cena em `cenas/visor/`. O `FocoVisor` diz:

- onde está e para onde está virado: o centro é a posição do nó, o eixo **+Z** aponta para fora da superfície (de onde a câmera olha) e o **+Y** é o "para cima" da imagem;
- o tamanho da área que a câmera enquadra (`tamanho`) e de que distância dá para usar (`alcance`);
- o texto do aviso (`texto_acao`) e a dica de teclas quando a câmera está lá (`dica_focado`);
- o que fazer com as teclas (`receber`), ao chegar (`focar`) e ao sair (`soltar`).

A `SalaVisor` (`scripts/visor/sala_visor.gd`) só cuida do jogador, da câmera e de repassar as teclas. Para pôr um quinto lugar no quarto (a estante, por exemplo), crie uma cena com um script que herda de `FocoVisor` e ponha no quarto: o aviso, a câmera e as teclas já funcionam.

O mural e a mesa montam os papéis com o `PapelDoVisor` (`scripts/visor/papel_do_visor.gd`): a folha com a textura de papel do jogo, o título em `Label3D` com a fonte Galmuri7 e a borda ciano de quando está escolhido. Cada papel tem uma posição e um giro sorteados com o **id** dele como semente, então fica sempre no mesmo lugar, mas parece jogado.

### 3.1 Examinar as recompensas das coleções

As cinco recompensas do quarto ([`colecionaveis.md`](colecionaveis.md)) também são `FocoVisor`, pelo `RecompensaDoQuarto` (`scripts/visor/recompensa_do_quarto.gd`): o farol, os disquetes, o tricórnio, a jaqueta e os óculos. O aviso é **[E] Examinar: <nome>**. Só existem no quarto virtual: a sala segura 2D não tem examinar.

- **Só quem completou a coleção pode examinar.** Sem as três peças a recompensa fica invisível e **nem entra no grupo dos focos**, então não tem aviso.
- **A peça é levantada e gira.** Ao chegar, ela sobe 8 cm (`altura_ao_examinar`) e o jogador a gira: **WASD** ou setas (140°/s, `graus_por_segundo`) ou o **mouse** (`sensibilidade_do_mouse`). Ao afastar, ela desce e volta suavemente à pose de antes (0,3 s). Uma luz branca fraca acende só enquanto se examina, para a peça aparecer bem mesmo no canto escuro do quarto.
- **Um painel mostra o nome e a descrição** (`Painel` em `sala_visor.tscn`, preenchido por `FocoVisor.titulo_focado` e `descricao_focada`). Nada além da peça ganha painel: TV, mural, mesa e quadro devolvem texto vazio. O texto vem da `Colecao` (`nome_da_recompensa` e `descricao_da_recompensa`, em `dados/colecoes/`) e só descreve o que se vê, sem afirmar nada de história.
- **De onde a câmera olha** é a `direcao_da_camera` de cada peça (de onde sai a câmera, em relação à peça; só a direção conta, o tamanho não). A distância vem do tamanho real do modelo e de `ocupacao`.

A conta do giro está na seção 5 ("Girar a peça").

**Limites:** o mural mostra as **24** anotações mais recentes (6 × 4) e a mesa os **15** primeiros documentos lidos (5 × 3). O jogo tem 13 documentos hoje.

## 4. A imagem e o céu

O 3D é desenhado num `SubViewport` **na resolução real da janela** (1920 × 1080 em Full HD), não nos 640 × 360 do resto do jogo. Assim os textos do mural, da mesa e do quadro ficam legíveis mesmo de longe: em 640 × 360, uma letra a 3 m de distância ocupava um ou dois pixels. As texturas continuam em pixel art com filtro **Nearest** (papéis, janela, pôsteres, fonte), então os pixels delas continuam nítidos; só as bordas dos móveis ficam lisas, com antisserrilhado **MSAA 2×**.

Quem cuida disso é `_ajustar_resolucao` em `scripts/visor/sala_visor.gd`: desenha o 3D do tamanho da janela e encolhe a imagem (`scale`) para caber nos 640 × 360 da interface. Ela roda de novo quando a janela muda de tamanho. Para voltar ao visual pixelado, baixe `resolucao_do_3d` no nó raiz da cena (0,33 em Full HD dá os mesmos 640 × 360 de antes; os textos de longe voltam a ficar ilegíveis).

Não há efeito CRT por cima da visão: só a tela da TV tem CRT, porque ali ele é a própria TV.

**O céu:** as estrelas são um `CPUParticles3D` (nó `Estrelas`) que nasce numa caixa de 14 × 3 × 14 m entre 3,3 m e 6,3 m de altura, acima das paredes (2,8 m): elas sobem devagar e nunca entram no quarto. Cada uma ganha uma cor sorteada de uma paleta (ciano, rosa, âmbar, violeta, verde, vermelho, branco: `color_initial_ramp`), acende e apaga ao longo da vida (`color_ramp`, só no alfa) e brilha um pouco por causa do *glow* do ambiente. O material some quando a estrela fica a menos de 1,2 m da câmera (`distance_fade`), para nenhuma virar um quadrado grande na frente dos olhos.

O menu da TV é uma cena de interface comum (`MenuVisor`), desenhada noutro `SubViewport`, de **192 × 144** (4:3, como a tela). A imagem desse viewport vira a textura da tela da TV (material sem sombreamento, filtro Nearest). Como esse `SubViewport` não está dentro de um container, ele não recebe teclas sozinho: a TV repassa as teclas para ele com `push_input` enquanto a câmera está nela.

A janela, o pôster do robô e o de 8 bits são **recortes da ilustração do prólogo** (`assets/sprites/cutscenes/seg_prologo/cena_02_quarto.png`), copiados para `assets/sprites/cenario/visor/` pelo `gerar_texturas_quarto.py`. São cópias de propósito: se o quarto usasse a ilustração do prólogo direto, o Godot poderia detectar o uso em 3D e trocar a compressão dela, borrando a cutscene. Os outros pôsteres são desenhados pixel a pixel pelo mesmo script. A foto da equipe (`poster_equipe.png`) sai da foto `assets/modelagem/cenario/foto_equipe_referencia.jpg`, reduzida a 124 × 56 pixels, com 48 cores e moldura. Todos são `Sprite3D`; a janela não sofre a luz do quarto (brilha como o pôr do sol), os pôsteres sofrem.

### Estrelas cadentes e luzes rápidas

O `EstrelasCadentes` (`cenas/visor/estrelas_cadentes.tscn`, `scripts/visor/estrelas_cadentes.gd`) solta uma a cada 1 a 3,5 s (sorteado). Seis em cada dez são **estrelas cadentes**: brancas, azuladas ou douradas, rápidas (9 a 14 m/s), caindo de leve, por 0,5 a 0,9 s. As outras são **luzes que viajam**: das cores do céu, mais lentas (5 a 8 m/s), quase na horizontal, por 1 a 1,8 s.

Cada uma é um rastro de 22 pontos (quadradinhos virados para a câmera, somando luz: `BLEND_MODE_ADD`), do maior e mais forte na cabeça ao menor e mais fraco na cauda. O rastro inteiro anda em linha reta e o brilho sobe e desce como $\sin(\pi p)$, com $p$ indo de 0 a 1 ao longo do voo: nasce apagado, fica mais forte no meio e some no fim. As cores passam de 1 (HDR) para o *glow* do ambiente acender um halo em volta.

Para ser vista de dentro do quarto, cada uma é sorteada para **passar por um ponto em cima do quarto** (até 2,2 m do centro, entre 4 m e 6 m de altura) e começa meio voo antes dele. Se ela cai, o voo é encurtado para o fim não descer abaixo de 3,4 m: nada atravessa o quarto.

## 5. A matemática

### Texturas sem UV (mapeamento triplanar)

As tábuas do chão, o papel de parede, a cortiça, os tecidos e as madeiras são ladrilhos pequenos de pixel art (`gerar_texturas_quarto.py`) aplicados pelo `TexturasDoQuarto` (`scripts/visor/texturas_do_quarto.gd`), que troca o material de cada parte do modelo pelo **nome** do material do Blender (Chao, Parede, Madeira...). O modelo não tem UV desdobrado: a textura é projetada **pela posição no mundo**. Para um ponto $(x, y, z)$ com normal $ec{n}$, o Godot lê a textura em três projeções:

$$\text{cor}_x = T(z, y)\qquad \text{cor}_y = T(x, z)\qquad \text{cor}_z = T(x, y)$$

e mistura as três com pesos $|n_x|, |n_y|, |n_z|$ (normalizados). Nas caixas do quarto a normal sempre aponta num eixo só, então cada face usa uma projeção pura: o chão usa $(x, z)$, a parede do fundo $(x, y)$, as laterais $(z, y)$. A escala `uv1_scale` $= 1/m$ faz o ladrilho se repetir a cada $m$ metros (0,8 m no piso: quatro tábuas de 20 cm). Como a textura é medida em metros do mundo, um móvel grande e um pequeno têm o mesmo tamanho de veio, e nada fica esticado. As texturas são importadas com **mipmaps** (cópias menores, para não tremerem de longe) e com o filtro *Nearest* (pixel nítido de perto).



### Para onde o jogador está virado (produto escalar)

O aviso **[E] ...** aparece para o lugar que estiver ao alcance e mais à frente do jogador, com as medidas **no plano do chão** (sem a altura, para funcionar mesmo de perto, quando a TV fica abaixo da linha dos olhos). Com $\hat{o}$ = direção do olhar e $\hat{t}$ = direção até o lugar, os dois normalizados:

$$\hat{o} \cdot \hat{t} = \cos\theta \geq 0{,}8 \quad\Rightarrow\quad \theta \leq 36{,}9°$$

Entre os que passam, ganha o de maior $\cos\theta$ (o mais no meio da visão). É o mesmo cálculo do campo de visão dos robôs ([`../computacao/geometria_e_shaders.md`](../computacao/geometria_e_shaders.md)), agora em 3D.

### Girar a peça (rotação no espaço do mundo)

O giro é guardado como uma base $G$ (matriz de rotação 3 × 3) **no espaço do mundo**, não no do modelo. Cada passo gira em torno de dois eixos fixos da tela: o **vertical** do mundo $\hat{u}$ (ângulo $\alpha$, do A/D e do mouse na horizontal) e o **eixo da direita da câmera** $\hat{d}$ (ângulo $\beta$, do W/S e do mouse na vertical), com $\hat{d} = \hat{u} \times \hat{f}$ para $\hat{f}$ a direção de onde a câmera olha:

$$G \leftarrow R(\hat{u}, \alpha)\, R(\hat{d}, \beta)\, G$$

Assim, A/D e W/S giram a peça para o lado que o jogador espera, **qualquer que seja o jeito em que a peça está virada no quarto** (os óculos estão girados 90°, por exemplo). Girar só em torno dos eixos do próprio modelo faria o W/S girar para um lado diferente em cada peça. $G$ é reortonormalizada a cada passo, para os erros de arredondamento não deformarem o modelo.

O centro do giro é o centro da **caixa dos vértices** do modelo, calculada ao carregar, e não a origem dele (que está no pé, no chão). Por isso a peça gira em torno de si mesma e não "orbita". A mesma caixa dá o tamanho do enquadramento: a diagonal $\sqrt{w^2 + h^2 + p^2}$ é o maior alcance da peça em qualquer posição, então ela cabe na tela mesmo girando.

Ao afastar, a volta é um **slerp** (interpolação esférica) entre a identidade e o giro atual, em 0,3 s, a mesma ideia do deslize da câmera.

### Onde a câmera para (campo de visão)

A câmera para no eixo do lugar, olhando para o centro, a uma distância $d$ em que ele ocupa uma fração $k$ da imagem (`ocupacao`: 0,8 na TV, 0,85 nos outros). Com a câmera de campo de visão vertical $\varphi$ (60°), a altura que ela enxerga a uma distância $d$ é $2\,d\,\tan(\varphi/2)$, e a largura é isso vezes a proporção da imagem $r = 640/360$. O lugar, de largura $w$ e altura $h$, tem que caber nas duas direções:

$$H = \frac{\max(h,\ w / r)}{k} \qquad d = \frac{H}{2\tan(\varphi/2)}$$

Na TV ($h = 0{,}33$ m), $d \approx 0{,}36$ m; no mural ($2{,}05 \times 1{,}05$ m), o que manda é a largura, e $d \approx 1{,}18$ m. A conta está em `FocoVisor.camera_diante`.

### Tamanho das letras em 3D

Com a câmera parada no lugar, cada pixel da fonte deve virar **um pixel do jogo** (a grade de 640 × 360 da interface; em Full HD, 3 × 3 pixels da tela), o mesmo tamanho das letras do resto do jogo. A câmera enquadra uma altura $H$ em 360 pixels do jogo, então cada um mede $H/360$ metros naquela distância. Esse é o `pixel_size` de cada lugar:

| Lugar | $H$ | `pixel_size` |
|---|---|---|
| Mural | 1,36 m | 0,0037 |
| Quadro | 1,0 m | 0,0028 |
| Mesa | 0,73 m (e a mesa está inclinada) | 0,0024 |

Se mudar o tamanho de um deles, ajuste o `pixel_size` junto (constante `PIXEL_DO_TEXTO` no script).

### A mesa vista de cima (base ortonormal)

A câmera olha a mesa de cima, a 60°, vindo do lado do quarto. Para os papéis ficarem deitados no tampo e com o texto de pé na tela, a mesa monta uma base com três vetores perpendiculares: a normal $\vec{n}$ = para cima, o "topo" $\vec{t}$ = o para cima da câmera projetado no chão, e a "direita" $\vec{d} = \vec{t} \times \vec{n}$ (produto vetorial). Os papéis são postos nessa base (`_plano_do_tampo`).

### O deslize até o lugar

A câmera vai da posição do olhar até esse ponto em 0,6 s, com `Transform3D.interpolate_with`: a posição é interpolada em linha reta e a rotação por **slerp** (interpolação esférica de quatérnios), que gira pelo menor caminho com velocidade constante. A curva de tempo é senoidal (começa e termina devagar). Na volta, o caminho é o mesmo ao contrário.

### Detalhes do quarto (móveis, objetos e bagunça)

O quarto é cheio de pequenos objetos para parecer morado, todos gerados em `gerar_sala_visor.py`:

- **Mesa:** tampo de quina arredondada com a própria textura (`tampo_mesa`: anel de caneca, marca de queimado, pingos de tinta), gaveteiro com três gavetas e puxadores, painel e travessa entre as pernas. Em cima, o **notebook** (teclado, trackpad, dobradiça, tampa inclinada 15° e a tela acesa), a caneca de café, o pote de canetas, a pilha de livros com páginas e a luminária articulada. Tudo isso fica na faixa perto da parede, para os papéis do Godot terem espaço.
- **Móveis macios** (travesseiros, colchão, cobertor, moletom, mochila): caixas com as arestas chanfradas, para não parecerem blocos.
- **Cadeira** com apoios de braço e base de cinco rodízios; **moletom** jogado no encosto, com capuz e mangas; **jaqueta** pendurada na porta.
- **Estante** com uma faixa clara em cada lombada e um objeto no vão de cada prateleira: caixa de arquivo, o robozinho de brinquedo, uma planta, um porta-retrato e revistas. **Cacto** no peitoril, **despertador** (12:00 piscando) no criado-mudo, **videogame** e controle no móvel da TV.
- **Caixas de papelão** (a bagunça de quem não terminou de desfazer a mudança): duas empilhadas no canto do fundo (LIVROS e FRAGIL), uma aberta ao lado, com livros de fora, uma caída perto da cama, com livros espalhados, e uma pequena junto da parede da porta (CABOS). Têm colisão em `Colisao` (`PilhaDeCaixas`, `CaixaAberta`, `CaixaCaida`, `CaixaPequena`). Também há um par de tênis perto da porta e bolas de papel amassado.

Duas técnicas novas do gerador:

- **Chanfro (`arredondar`)**: a função `caixa` aceita um raio e aplica um *Bevel* de 2 segmentos nas arestas, já aplicado antes do export.
- **Quads com UV explícito (`quad`)**: o teclado, a tela do notebook, o mostrador do despertador e a escrita das caixas são retângulos com UV de 0 a 1 (ou um pedaço do atlas `marcas_das_caixas.png`), dados pelos quatro cantos no Godot. O triplanar não serve para eles, porque a imagem tem que cair no lugar certo. No `TexturasDoQuarto`, esses materiais têm `"uv": true`; `"brilho"` acende a imagem como emissão (tela e despertador) e `"recorte"` faz o canetão das caixas ficar transparente em volta das letras.

## 6. O modelo

O quarto é gerado por código no Blender: `assets/modelagem/cenario/gerar_sala_visor.py` (como rodar e as medidas estão no começo do arquivo). Ele exporta `assets/modelos/sala_visor.glb`, em glTF, com materiais simples. As medidas do script estão **em coordenadas do Godot** (o script converte para o Blender), então os números de lá são os mesmos da cena.

A tela da TV é um objeto separado chamado **`Tela`**, um retângulo 4:3 com UV de 0 a 1: a `TelaDoVisor` põe o menu nele. Os cartões, papéis e textos não estão no modelo: são montados no Godot com os dados do jogo.

As formas de colisão (chão, paredes, móvel da TV, estante, escrivaninha, cadeira, cama e criado-mudo) e a posição dos quatro lugares estão em `cenas/visor/sala_visor.tscn`. Se um móvel mudar de lugar no gerador, mude lá também.

## 7. Onde está no projeto

| O quê | Onde |
|---|---|
| Troca 2D ↔ 3D e salvar (autoload `Visor`) | `scripts/sistemas/visor.gd` |
| Quarto (câmera, luzes, colisões, janela, pôsteres) | `cenas/visor/sala_visor.tscn`, `scripts/visor/sala_visor.gd` |
| Jogador em primeira pessoa | `cenas/visor/jogador_visor.tscn`, `scripts/visor/jogador_visor.gd` |
| Os lugares para focar | `scripts/visor/foco_visor.gd` (base), `cenas/visor/tela_do_visor.tscn`, `mural_do_visor.tscn`, `mesa_do_visor.tscn`, `quadro_do_visor.tscn` e os scripts com o mesmo nome |
| Papel com título (mural e mesa) | `scripts/visor/papel_do_visor.gd` |
| Menu da TV | `cenas/visor/menu_visor.tscn`, `scripts/visor/menu_visor.gd`, tema `cenas/interface/tema_tela_crt.tres` |
| Modelo 3D | `assets/modelos/sala_visor.glb`, de `assets/modelagem/cenario/gerar_sala_visor.py` |
| Texturas e pôsteres | `assets/sprites/cenario/visor/`, de `assets/modelagem/cenario/gerar_texturas_quarto.py`; aplicadas por `scripts/visor/texturas_do_quarto.gd` (a parede agora repete a cada 1 m, com riscos e furos de prego) |
| Examinar as recompensas (giro, painel de nome e descrição) | `scripts/visor/recompensa_do_quarto.gd` (e `farol_da_mesa.gd`, que herda dele), `Painel` em `cenas/visor/sala_visor.tscn`, textos em `dados/colecoes/` |
| Estrelas cadentes e luzes rápidas | `cenas/visor/estrelas_cadentes.tscn`, `scripts/visor/estrelas_cadentes.gd` |
| Farol da mesa (recompensa dos pingentes) | `cenas/visor/farol_da_mesa.tscn`, `scripts/visor/farol_da_mesa.gd`, modelo `assets/modelos/farol_mesa.glb` de `assets/modelagem/cenario/gerar_farol_mesa.py` |
| Jaqueta da cama e óculos do criado-mudo (recompensas dos botões e dos chips) | `cenas/visor/jaqueta_da_cama.tscn` e `oculos_do_criado.tscn`, modelos `jaqueta_diana.glb` e `oculos_zane.glb` de `gerar_jaqueta_diana.py` e `gerar_oculos_zane.py` |
| Disquetes da mesa e tricórnio do notebook (recompensas dos disquetes e dos pingentes do chapéu) | `cenas/visor/disquetes_da_mesa.tscn` e `chapeu_do_notebook.tscn`, `scripts/visor/recompensa_do_quarto.gd`, modelos `assets/modelos/disquetes_mesa.glb` e `chapeu_baltazar.glb` de `gerar_disquetes_mesa.py` e `gerar_chapeu_baltazar.py` (em `assets/modelagem/cenario/`) |
| Data do último save | `Salvamento.data_salva()` em `scripts/sistemas/salvamento.gd` |

## 8. Pendências

- **O quarto como a mente do Gabriel** foi decidido pelo Davi (ver `docs/decisoes.md`), mas ainda não está na [História Completa](../historia/História_Completa.md). Os óculos do Zane como máquina de salvar também continuam sem explicação na história (ver [`sala_segura.md`](sala_segura.md), Pendências).
- **Um quarto por save** é a ideia para o futuro: hoje o quarto já mostra o que está no save, mas mudar de aparência com o progresso (coisas novas aparecendo conforme as fases) ainda não existe.
- **Examinar só existe no quarto virtual.** A sala segura 2D e as fases não têm examinar. As coleções que ainda não fecharam não têm o que examinar.
- **A peça gira atravessando o que está perto** (o farol e o tricórnio ficam a poucos centímetros um do outro na mesa). Se incomodar, esconder as outras recompensas enquanto se examina é uma linha em `RecompensaDoQuarto.focar`.
- **Apontar com o mouse** na TV, no mural e na mesa não existe: é tudo por teclado.
- Controle (gamepad) não anda nem olha no visor.

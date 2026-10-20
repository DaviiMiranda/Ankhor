# Mecânicas — O visor 3D: o quarto do Gabriel (salvar em primeira pessoa)

Quando o Gabriel põe os óculos do Zane na sala segura ([`sala_segura.md`](sala_segura.md)), o jogo **vira 3D em primeira pessoa**. Ele aparece no **próprio quarto, a mente dele materializada**: o quarto de 2026 do prólogo (`seg_prologo`, cena 2), com a janela do pôr do sol, a escrivaninha, a estante, a cama e os pôsteres, só que sem teto. As paredes terminam numa linha ciano e, acima delas, é o escuro, com poeira brilhando no ar. É um quarto lembrado, não um quarto de verdade.

O quarto guarda o jogo até ali. Tudo o que aparece nele vem do estado do jogo naquele momento (o mesmo que vai para o save):

| Onde | O que mostra | De onde vem |
|---|---|---|
| **TV de tubo**, no móvel do fundo | o menu de salvar | `Salvamento` |
| **Mural de cortiça**, em cima da cama | um cartão para cada anotação do caderno, presos com alfinete e ligados por um fio vermelho, na ordem em que foram anotados | `Caderno.anotacoes` |
| **Escrivaninha**, embaixo da janela | os documentos que o Gabriel já leu, jogados em cima da mesa, cada um no papel dele (caderno, pergaminho...) | os documentos de `dados/documentos/` que já têm anotação no caderno |
| **Quadro branco**, ao lado da TV | os números do jogo: fase, documentos lidos, transmissões ouvidas, anotações, portas destrancadas, itens na mochila e o último save | `Caderno`, `Radio`, `Porta`, `Inventario`, `Salvamento` |

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

**Limites:** o mural mostra as **24** anotações mais recentes (6 × 4) e a mesa os **15** primeiros documentos lidos (5 × 3). O jogo tem 13 documentos hoje.

## 4. A imagem pixelada

O 3D é desenhado num `SubViewport` de **640 × 360** (a resolução base do jogo) dentro de um `SubViewportContainer` com filtro **Nearest**. A janela amplia essa imagem como amplia o resto do jogo: os pixels ficam grandes e o 3D combina com o pixel art. Por cima vai o mesmo efeito CRT do menu principal (`shaders/tela_crt.gdshader`), mais fraco, e ele obedece à opção **Efeito CRT** das configurações.

Para deixar mais pixelado, ponha `stretch_shrink = 2` no nó `Imagem` de `cenas/visor/sala_visor.tscn` (o 3D passa a ser desenhado em 320 × 180, o mesmo tamanho do cenário 2D). O texto do mural, da mesa e do quadro fica ilegível nesse caso.

O menu da TV é uma cena de interface comum (`MenuVisor`), desenhada noutro `SubViewport`, de **192 × 144** (4:3, como a tela). A imagem desse viewport vira a textura da tela da TV (material sem sombreamento, filtro Nearest). Como esse `SubViewport` não está dentro de um container, ele não recebe teclas sozinho: a TV repassa as teclas para ele com `push_input` enquanto a câmera está nela.

A janela e os pôsteres são **recortes da ilustração do prólogo** (`assets/sprites/cutscenes/seg_prologo/cena_02_quarto.png`), em `Sprite3D` com `region_rect`. A janela não sofre a luz do quarto (brilha como o pôr do sol); os pôsteres sofrem.

## 5. A matemática

### Para onde o jogador está virado (produto escalar)

O aviso **[E] ...** aparece para o lugar que estiver ao alcance e mais à frente do jogador, com as medidas **no plano do chão** (sem a altura, para funcionar mesmo de perto, quando a TV fica abaixo da linha dos olhos). Com $\hat{o}$ = direção do olhar e $\hat{t}$ = direção até o lugar, os dois normalizados:

$$\hat{o} \cdot \hat{t} = \cos\theta \geq 0{,}8 \quad\Rightarrow\quad \theta \leq 36{,}9°$$

Entre os que passam, ganha o de maior $\cos\theta$ (o mais no meio da visão). É o mesmo cálculo do campo de visão dos robôs ([`../computacao/geometria_e_shaders.md`](../computacao/geometria_e_shaders.md)), agora em 3D.

### Onde a câmera para (campo de visão)

A câmera para no eixo do lugar, olhando para o centro, a uma distância $d$ em que ele ocupa uma fração $k$ da imagem (`ocupacao`: 0,8 na TV, 0,85 nos outros). Com a câmera de campo de visão vertical $\varphi$ (60°), a altura que ela enxerga a uma distância $d$ é $2\,d\,\tan(\varphi/2)$, e a largura é isso vezes a proporção da imagem $r = 640/360$. O lugar, de largura $w$ e altura $h$, tem que caber nas duas direções:

$$H = \frac{\max(h,\ w / r)}{k} \qquad d = \frac{H}{2\tan(\varphi/2)}$$

Na TV ($h = 0{,}33$ m), $d \approx 0{,}36$ m; no mural ($2{,}05 \times 1{,}05$ m), o que manda é a largura, e $d \approx 1{,}18$ m. A conta está em `FocoVisor.camera_diante`.

### Tamanho das letras em 3D

Para o texto em `Label3D` ficar nítido, cada pixel da fonte deve virar mais ou menos **um pixel da imagem**. A câmera enquadra uma altura $H$ em 360 pixels, então cada pixel da imagem mede $H/360$ metros naquela distância. Esse é o `pixel_size` de cada lugar:

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
| Data do último save | `Salvamento.data_salva()` em `scripts/sistemas/salvamento.gd` |

## 8. Pendências

- **O quarto como a mente do Gabriel** foi decidido pelo Davi (ver `docs/decisoes.md`), mas ainda não está na [História Completa](../historia/História_Completa.md). Os óculos do Zane como máquina de salvar também continuam sem explicação na história (ver [`sala_segura.md`](sala_segura.md), Pendências).
- **Um quarto por save** é a ideia para o futuro: hoje o quarto já mostra o que está no save, mas mudar de aparência com o progresso (coisas novas aparecendo conforme as fases) ainda não existe.
- **Apontar com o mouse** na TV, no mural e na mesa não existe: é tudo por teclado.
- Controle (gamepad) não anda nem olha no visor.

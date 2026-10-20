# Mecânicas — O visor 3D (salvar em primeira pessoa)

Quando o Gabriel põe os óculos do Zane na sala segura ([`sala_segura.md`](sala_segura.md)), o jogo **vira 3D em primeira pessoa**. Ele está numa sala escura, com uma grade ciano no chão e, na frente dele, uma **TV de tubo num móvel baixo**. A tela da TV é o menu de salvar. Ao tirar os óculos, ele volta para a sala segura 2D, no mesmo lugar, e toca a animação de devolver os óculos ao pedestal.

## 1. Como o jogador usa

| Onde | Teclas |
|---|---|
| Andando na sala | **WASD** (ou setas) anda, **mouse** olha, **Esc** tira os óculos |
| Perto da TV, olhando para ela | aparece **[E] Usar a tela**; E leva a câmera até a tela |
| Na tela | **W/S** (ou ↑/↓) escolhe, **E** (ou Enter) confirma, **Esc** afasta a câmera |

O menu da TV tem **Salvar jogo** e **Voltar** (que tira os óculos). Em cima ele mostra a data e a hora do último save, ou "Nenhum jogo salvo". Ao salvar, toca o som de salvar e aparece **Jogo salvo** (ou **Não foi possível salvar**, se o arquivo não pôde ser gravado). Dá para salvar quantas vezes quiser.

Salvar faz o mesmo que antes: a vida volta a 3 e o pedestal vira o checkpoint da fase. **Entrar no visor e sair sem salvar não muda nada.** O HUD da sala segura só mostra "Jogo salvo" na volta se o jogador salvou.

A pausa (Esc) não abre dentro do visor: lá o Esc serve para afastar da tela ou tirar os óculos.

## 2. Como a troca entre 2D e 3D funciona

A sala segura **não é recarregada**. O autoload `Visor` (`scripts/sistemas/visor.gd`):

1. **`abrir(cena, posição)`**, chamado pela `MaquinaDeSalvar` com a tela já escura: tira a sala 2D da árvore de cenas (`remove_child`), **sem apagar**, e põe a cena 3D no lugar. A sala fica guardada na memória, com o Gabriel parado de óculos no rosto, a máquina no meio da animação e tudo o mais como estava.
2. **`salvar()`**, chamado pelo menu da TV: limpa a vida, marca o checkpoint e grava o arquivo (`Salvamento.salvar`) com a cena e a posição que a máquina passou.
3. **`fechar()`**, ao tirar os óculos: apaga a cena 3D, devolve a sala 2D à árvore e emite **`fechado(salvou)`**.

A `MaquinaDeSalvar` fica esperando esse sinal (`await Visor.fechado`). Quando ele chega, ela clareia a tela e toca a animação de tirar os óculos de trás para a frente, como antes.

Por que não recarregar a sala: não precisa passar a posição do Gabriel nem um "estou voltando do visor" entre cenas, e nada da sala se perde (itens no chão, portas, música). Dois cuidados que isso exigiu:

- A `SalaSegura` liga o sinal que remove robôs em `_enter_tree` (antes era em `_ready`, que não roda de novo quando a sala volta à árvore).
- O som de salvar saiu da máquina e foi para a TV (`cenas/visor/menu_visor.tscn`).

## 3. A imagem pixelada

O 3D é desenhado num `SubViewport` de **640 × 360** (a resolução base do jogo) dentro de um `SubViewportContainer` com filtro **Nearest**. A janela amplia essa imagem como amplia o resto do jogo: os pixels ficam grandes e o 3D combina com o pixel art. Por cima vai o mesmo efeito CRT do menu principal (`shaders/tela_crt.gdshader`), mais fraco, e ele obedece à opção **Efeito CRT** das configurações.

Para deixar mais pixelado, ponha `stretch_shrink = 2` no nó `Imagem` de `cenas/visor/sala_visor.tscn` (o 3D passa a ser desenhado em 320 × 180, o mesmo tamanho do cenário 2D).

O menu da TV é uma cena de interface comum (`MenuVisor`), desenhada noutro `SubViewport`, de **192 × 144** (4:3, como a tela). A imagem desse viewport vira a textura da tela da TV (`_pintar_a_tela`, material sem sombreamento, filtro Nearest). Como o `SubViewport` da TV não está dentro de um container, ele não recebe teclas sozinho: a `SalaVisor` repassa as teclas para ele com `push_input` enquanto a câmera está na tela.

## 4. A matemática

### Olhar para a TV (produto escalar)

O aviso **[E] Usar a tela** aparece quando duas condições valem, ambas medidas **no plano do chão** (sem a altura, para que funcione mesmo de perto, quando a TV fica abaixo da linha dos olhos):

1. a distância até a tela é no máximo `alcance_da_tela` (1,5 m);
2. o jogador está virado para ela. Com $\hat{o}$ = direção do olhar e $\hat{t}$ = direção até a tela, os dois normalizados:

$$\hat{o} \cdot \hat{t} = \cos\theta \geq 0{,}8 \quad\Rightarrow\quad \theta \leq 36{,}9°$$

É o mesmo cálculo do campo de visão dos robôs ([`../computacao/geometria_e_shaders.md`](../computacao/geometria_e_shaders.md)), agora em 3D.

### Onde a câmera para na frente da tela

A câmera para no eixo da tela, olhando para o centro dela, a uma distância $d$ em que a tela ocupa 80% da altura da imagem (`ocupacao_da_tela`). Com a câmera de campo de visão vertical $\varphi$ (60°), a altura que ela enxerga a uma distância $d$ é $2\,d\,\tan(\varphi/2)$. Queremos que a tela, de altura $h$, seja 80% disso:

$$h = 0{,}8 \cdot 2\,d\,\tan\frac{\varphi}{2} \quad\Rightarrow\quad d = \frac{h / 0{,}8}{2\tan(\varphi/2)}$$

Com $h = 0{,}33$ m, $d \approx 0{,}36$ m. A conta está em `_camera_diante_da_tela`, e vale para qualquer tamanho de tela: se o modelo mudar, a câmera se ajusta sozinha.

### O deslize até a tela

A câmera vai da posição do olhar até esse ponto em 0,6 s, com `Transform3D.interpolate_with`: a posição é interpolada em linha reta e a rotação por **slerp** (interpolação esférica de quatérnios), que gira pelo menor caminho com velocidade constante. A curva de tempo é senoidal (começa e termina devagar). Na volta, o caminho é o mesmo ao contrário.

## 5. O modelo

A sala, o móvel e a TV são gerados por código no Blender: `assets/modelagem/cenario/gerar_sala_visor.py` (como rodar e as medidas estão no começo do arquivo). Ele exporta `assets/modelos/sala_visor.glb`, em glTF, com materiais simples. A tela é um objeto separado chamado **`Tela`**, um retângulo 4:3 com UV de 0 a 1: o script do Godot procura esse nome para pôr o menu nele.

As formas de colisão (chão, paredes, móvel com a TV) estão em `cenas/visor/sala_visor.tscn`, no nó `Colisao`, com as medidas da sala (5 × 5 m). Se a sala mudar de tamanho no gerador, mude lá também.

## 6. Onde está no projeto

| O quê | Onde |
|---|---|
| Troca 2D ↔ 3D e salvar (autoload `Visor`) | `scripts/sistemas/visor.gd` |
| Cena 3D (câmera, TV, colisões, luzes) | `cenas/visor/sala_visor.tscn`, `scripts/visor/sala_visor.gd` |
| Jogador em primeira pessoa | `cenas/visor/jogador_visor.tscn`, `scripts/visor/jogador_visor.gd` |
| Menu da TV | `cenas/visor/menu_visor.tscn`, `scripts/visor/menu_visor.gd`, tema `cenas/interface/tema_tela_crt.tres` |
| Modelo 3D | `assets/modelos/sala_visor.glb`, de `assets/modelagem/cenario/gerar_sala_visor.py` |
| Data do último save | `Salvamento.data_salva()` em `scripts/sistemas/salvamento.gd` |

## 7. Pendências

- **O que é essa sala na história** continua em aberto, como os próprios óculos como máquina de salvar (ver [`sala_segura.md`](sala_segura.md), Pendências). A sala não tem nenhum texto de história: só o menu.
- **Apontar com o mouse na TV** não existe: o menu é só por teclado. Dá para fazer projetando o raio do mouse na tela e repassando o clique (por volta de 50 linhas).
- Controle (gamepad) não anda nem olha no visor.

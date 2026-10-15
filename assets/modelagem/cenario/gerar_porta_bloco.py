"""Gera a animação de correr pro lado e a parede da porta do Bloco de salas.

Uso:
    python assets/modelagem/cenario/gerar_porta_bloco.py

A porta do Bloco de salas é uma porta pesada de aço com visor reforçado de
vidro aramado e trava eletromecânica com teclado/maçaneta na folha.
A porta abre correndo para o lado (porta de correr embutida no bolso de parede),
deslizando em trilho superior de aço.

Para gerar as peças de cenário (80x112 px) e os quadros de abertura
(80x88 px a 36 fps, correspondendo ao vão da FolhaPorta a y = 24 px):
  1. Carrega o sprite dedicado da porta ('porta_bloco_sprite.png', 406x697 px)
     e a textura de parede metálica dos corredores ('porta_bloco_referencia.jpg');
  2. Ajusta o batente externo da porta para 56x88 px, centralizado no vão de 80 px
     (x de 12 a 68 px, com 12 px de parede metálica de cada lado);
  3. Gera a peça estática de parede 'parede_porta_bloco.png' (80x112 px),
     com a parede superior acima do batente e a porta fechada;
  4. Computa a animação de deslizamento ("correndo pro lado") da folha:
     - Curva de aceleração e frenagem suave Hermite quintic smootherstep
       S(t) = 6t^5 - 15t^4 + 10t^3;
     - Deslocamento horizontal delta_x(t) de 0 até 44 px para a direita;
     - A folha desliza para o bolso da parede atrás do batente direito;
     - O vão aberto revela o interior escuro da sala de destino com sombra do lintel;
     - O batente externo e os painéis de parede laterais cobrem a folha que entra no bolso;
  5. Grava os 36 quadros PNG (porta_bloco_abrir_00.png a _35.png) e o
     recurso SpriteFrames 'porta_bloco_quadros.tres'.
"""
import pathlib
import sys
import numpy as np
from PIL import Image

RAIZ = pathlib.Path(__file__).resolve().parents[3]
PASTA_QUADROS = RAIZ / "assets/sprites/cenario/bloco_de_salas/porta"
RES_QUADROS = "res://assets/sprites/cenario/bloco_de_salas/porta"
NOME_BASE = "porta_bloco_abrir"

LARGURA_FOLHA = 80
ALTURA_FOLHA = 88
LARGURA_PAREDE = 80
ALTURA_PAREDE = 112

LARGURA_PORTA = 56
ALTURA_PORTA = 88
X_OFFSET_PORTA = (LARGURA_FOLHA - LARGURA_PORTA) // 2  # 12 px

QUANTIDADE_QUADROS = 36
VELOCIDADE = 36.0


def carregar_imagens() -> tuple[Image.Image, Image.Image]:
    caminho_sprite = RAIZ / "assets/modelagem/cenario/porta_bloco_sprite.png"
    caminho_ref = RAIZ / "assets/modelagem/cenario/porta_bloco_referencia.jpg"

    if not caminho_sprite.is_file():
        sys.exit(f"Sprite da porta não encontrado: {caminho_sprite}")
    if not caminho_ref.is_file():
        sys.exit(f"Referência da parede não encontrada: {caminho_ref}")

    sprite = Image.open(caminho_sprite).convert("RGBA")
    ref = Image.open(caminho_ref).convert("RGBA")
    return sprite, ref


def gerar_parede_estatica(sprite_porta: Image.Image, ref_parede: Image.Image) -> Image.Image:
    # Parede superior acima do batente (y de 0 a 24 px)
    topo_24 = ref_parede.crop((335, 0, 681, 76)).resize(
        (LARGURA_PAREDE, ALTURA_PAREDE - ALTURA_FOLHA), Image.Resampling.LANCZOS
    )
    # Fundo do vão e paredes laterais (y de 24 a 112 px)
    fundo_88 = ref_parede.crop((335, 76, 681, 456)).resize(
        (LARGURA_FOLHA, ALTURA_FOLHA), Image.Resampling.LANCZOS
    )

    # Redimensiona porta para 56x88 px
    porta_56x88 = sprite_porta.resize((LARGURA_PORTA, ALTURA_PORTA), Image.Resampling.LANCZOS)

    parede = Image.new("RGBA", (LARGURA_PAREDE, ALTURA_PAREDE))
    parede.paste(topo_24, (0, 0))
    parede.paste(fundo_88, (0, ALTURA_PAREDE - ALTURA_FOLHA))
    parede.paste(porta_56x88, (X_OFFSET_PORTA, ALTURA_PAREDE - ALTURA_FOLHA), porta_56x88)
    return parede


def gerar_quadros_animacao(
    sprite_porta: Image.Image, ref_parede: Image.Image
) -> list[Image.Image]:
    fundo_88 = ref_parede.crop((335, 76, 681, 456)).resize(
        (LARGURA_FOLHA, ALTURA_FOLHA), Image.Resampling.LANCZOS
    )
    porta_56x88 = sprite_porta.resize((LARGURA_PORTA, ALTURA_PORTA), Image.Resampling.LANCZOS)

    canvas_fechado = np.array(fundo_88)
    porta_np = np.array(porta_56x88)

    # Sobrepõe porta fechada no canvas base a x = 12 px
    canvas_fechado[:, X_OFFSET_PORTA : X_OFFSET_PORTA + LARGURA_PORTA] = porta_np

    # Vão interno da folha na porta redimensionada (56x88):
    # Em 56x88: x de 5 a 51 (largura 46), y de 5 a 86 (altura 81)
    # No canvas 80x88: x de 17 a 63 (12 + 5 a 12 + 51)
    x_vao_inicio = X_OFFSET_PORTA + 5
    x_vao_fim = X_OFFSET_PORTA + 51
    y_vao_inicio = 5
    y_vao_fim = 86
    w_folha = x_vao_fim - x_vao_inicio
    h_folha = y_vao_fim - y_vao_inicio

    folha_np = porta_np[y_vao_inicio:y_vao_fim, 5:51].copy()

    # Fundo escuro do vão aberto com gradiente sutil e sombra do lintel
    fundo_escuro = np.zeros((h_folha, w_folha, 4), dtype=np.uint8)
    for dy in range(h_folha):
        sombra = max(0.0, 1.0 - dy / 8.0) * 0.7
        c = int((8 + (dy / float(h_folha)) * 10) * (1.0 - sombra))
        fundo_escuro[dy, :] = [c, c + 1, c + 3, 255]

    deslocamento_max = w_folha - 2  # Deixa 2 px de borda visível dentro do batente ao abrir

    quadros: list[Image.Image] = []
    for i in range(QUANTIDADE_QUADROS):
        t = i / float(QUANTIDADE_QUADROS - 1)
        # Smootherstep quintic
        s_t = t * t * t * (t * (t * 6.0 - 15.0) + 10.0)
        shift = int(round(deslocamento_max * s_t))

        frame = canvas_fechado.copy()

        if shift == 0:
            quadros.append(Image.fromarray(frame))
            continue

        # 1. Desenha o fundo escuro do vão aberto
        frame[y_vao_inicio:y_vao_fim, x_vao_inicio:x_vao_fim] = fundo_escuro

        # 2. Desenha a folha correndo para a direita
        # A folha se desloca para x = x_vao_inicio + shift
        # A porção visível vai de (x_vao_inicio + shift) até x_vao_fim
        if shift < w_folha:
            largura_visivel = w_folha - shift
            frame[
                y_vao_inicio:y_vao_fim,
                x_vao_inicio + shift : x_vao_fim,
            ] = folha_np[:, :largura_visivel]

        # 3. Re-sobrepõe o batente externo da porta e o chão para garantir bordas nítidas
        frame[:, X_OFFSET_PORTA : x_vao_inicio] = porta_np[:, :5]
        frame[:, x_vao_fim : X_OFFSET_PORTA + LARGURA_PORTA] = porta_np[:, 51:]
        frame[:y_vao_inicio, X_OFFSET_PORTA : X_OFFSET_PORTA + LARGURA_PORTA] = porta_np[
            :y_vao_inicio, :
        ]
        frame[y_vao_fim:, X_OFFSET_PORTA : X_OFFSET_PORTA + LARGURA_PORTA] = porta_np[
            y_vao_fim:, :
        ]

        quadros.append(Image.fromarray(frame))

    return quadros


def gravar_sprite_frames(quantidade: int) -> None:
    linhas = ['[gd_resource type="SpriteFrames" format=3]', ""]
    for i in range(quantidade):
        linhas.append(
            f'[ext_resource type="Texture2D" path="{RES_QUADROS}/{NOME_BASE}_{i:02d}.png" id="{i + 1}"]'
        )
    linhas += ["", "[resource]", "animations = [{", '"frames": [{']
    quadros = [
        f'"duration": 1.0,\n"texture": ExtResource("{i + 1}")' for i in range(quantidade)
    ]
    linhas.append("}, {\n".join(quadros) + "\n}],")
    linhas += ['"loop": false,', '"name": &"abrir",', f'"speed": {VELOCIDADE}', "}]", ""]
    (PASTA_QUADROS / "porta_bloco_quadros.tres").write_text("\n".join(linhas), encoding="utf-8")


def main() -> None:
    sprite_porta, ref_parede = carregar_imagens()
    PASTA_QUADROS.mkdir(parents=True, exist_ok=True)

    # 1. Parede estática base (80x112 px)
    parede = gerar_parede_estatica(sprite_porta, ref_parede)
    parede.save(PASTA_QUADROS / "parede_porta_bloco.png")
    print(f"Salva parede estática {LARGURA_PAREDE}x{ALTURA_PAREDE}: {PASTA_QUADROS / 'parede_porta_bloco.png'}")

    # 2. Quadros animados (80x88 px, 36 quadros)
    quadros = gerar_quadros_animacao(sprite_porta, ref_parede)
    for i, quadro in enumerate(quadros):
        quadro.save(PASTA_QUADROS / f"{NOME_BASE}_{i:02d}.png")
    print(f"Salvos {len(quadros)} quadros em {PASTA_QUADROS}")

    # 3. Recurso SpriteFrames
    gravar_sprite_frames(len(quadros))
    print(f"Salvo recurso: {PASTA_QUADROS / 'porta_bloco_quadros.tres'}")


if __name__ == "__main__":
    main()

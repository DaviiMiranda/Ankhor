"""Gera a animação de abrir e a parede da porta do Bloco de salas.

Uso:
    python assets/modelagem/cenario/gerar_porta_bloco.py [caminho/da/referencia.jpg]

A imagem de referência retrata a porta corta-fogo/institucional de aço do Bloco
de salas (3026), com visor reforçado de vidro aramado no centro, maçaneta com
trava eletromecânica à esquerda e três dobradiças pesadas à direita.

Para gerar as peças de cenário (padrão 80x112 px) e os quadros de abertura
(80x88 px a 36 fps, correspondendo ao vão da FolhaPorta a y = 24 px):
  1. Recorta a porta e o batente de aço mantendo proporção exata;
  2. Gera a peça estática de parede 'parede_porta_bloco.png' (80x112 px),
     com a parede superior acima do batente e a porta fechada;
  3. Computa a animação de rotação rígida da folha em projeção perspectiva 2.5D:
     - Eixo de rotação no batente direito (x = 64 px);
     - Suavização temporal Hermite quintic smootherstep S(t) = 6t^5 - 15t^4 + 10t^3;
     - Ângulo de abertura theta(t) de 0° a 84°;
     - Efeito de profundidade z = W * sin(theta), escala de perspectiva s = 1/(1 + z/D);
     - Atenuação difusa Lambertiana L = 0.55 + 0.45 * cos(theta);
     - Bisel metálico visível na borda livre da folha;
     - Fundo do vão preenchido pelo interior escuro da sala de destino;
  4. Grava os quadros PNG (porta_bloco_abrir_00.png a _35.png) e o
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

QUANTIDADE_QUADROS = 36
VELOCIDADE = 36.0

# Coordenadas do recorte na referência original (1024x571)
# Centro em x=508, porta de y=76 a y=456 (380 px)
X_CORTE_ESQ = 335
X_CORTE_DIR = 681
Y_CORTE_PORTA_TOPO = 76
Y_CORTE_CHAO = 456
Y_CORTE_PAREDE_TOPO = 0


def carregar_referencia(caminho: pathlib.Path) -> Image.Image:
    if not caminho.is_file():
        sys.exit(f"Imagem de referência não encontrada: {caminho}")
    return Image.open(caminho).convert("RGBA")


def gerar_parede_estatica(img_ref: Image.Image) -> Image.Image:
    corte_porta = img_ref.crop((X_CORTE_ESQ, Y_CORTE_PORTA_TOPO, X_CORTE_DIR, Y_CORTE_CHAO))
    porta_80x88 = corte_porta.resize((LARGURA_FOLHA, ALTURA_FOLHA), Image.Resampling.LANCZOS)
    corte_topo = img_ref.crop((X_CORTE_ESQ, Y_CORTE_PAREDE_TOPO, X_CORTE_DIR, Y_CORTE_PORTA_TOPO))
    topo_80x24 = corte_topo.resize((LARGURA_PAREDE, ALTURA_PAREDE - ALTURA_FOLHA), Image.Resampling.LANCZOS)

    parede = Image.new("RGBA", (LARGURA_PAREDE, ALTURA_PAREDE))
    parede.paste(topo_80x24, (0, 0))
    parede.paste(porta_80x88, (0, ALTURA_PAREDE - ALTURA_FOLHA))
    return parede


def gerar_quadros_animacao(img_ref: Image.Image) -> list[Image.Image]:
    corte_porta = img_ref.crop((X_CORTE_ESQ, Y_CORTE_PORTA_TOPO, X_CORTE_DIR, Y_CORTE_CHAO))
    base_porta = corte_porta.resize((LARGURA_FOLHA, ALTURA_FOLHA), Image.Resampling.LANCZOS)
    arr_base = np.array(base_porta)

    # Vão interno da folha: x de 15 a 64 (largura 49), y de 6 a 86 (altura 80)
    x_pivot = 64
    x_aberto = 15
    y_topo = 6
    y_base = 86
    largura_folha = x_pivot - x_aberto
    altura_folha = y_base - y_topo

    folha_textura = arr_base[y_topo:y_base, x_aberto:x_pivot].copy()
    quadros: list[Image.Image] = []

    for i in range(QUANTIDADE_QUADROS):
        t = i / float(QUANTIDADE_QUADROS - 1)
        # Smootherstep (curva suave de aceleração e frenagem)
        s_t = t * t * t * (t * (t * 6.0 - 15.0) + 10.0)
        theta_deg = s_t * 84.0
        theta = np.radians(theta_deg)

        frame = arr_base.copy()

        if theta_deg < 0.5:
            quadros.append(Image.fromarray(frame))
            continue

        # 1. Fundo escuro do vão aberto (sala além da porta com sombra superior)
        dark = np.zeros((altura_folha, largura_folha, 4), dtype=np.uint8)
        for dy in range(altura_folha):
            sombra_lintel = max(0.0, 1.0 - dy / 10.0) * 0.7
            c = int((8 + (dy / float(altura_folha)) * 10) * (1.0 - sombra_lintel))
            dark[dy, :] = [c, c + 1, c + 3, 255]
        frame[y_topo:y_base, x_aberto:x_pivot] = dark

        # 2. Projeção perspectiva da folha girando em torno do pivot x=64
        w_proj = max(int(round(largura_folha * np.cos(theta))), 2)
        x_esq = x_pivot - w_proj

        z_profundidade = largura_folha * np.sin(theta)
        persp = 1.0 / (1.0 + z_profundidade / 180.0)
        delta_y = int(round((altura_folha / 2.0) * (1.0 - persp)))

        # Fator de iluminação difusa (a porta gira para dentro do escuro)
        fator_luz = 0.55 + 0.45 * np.cos(theta)

        folha_img = Image.fromarray(folha_textura)
        folha_redim = folha_img.resize((w_proj, altura_folha), Image.Resampling.BILINEAR)
        folha_np = (np.array(folha_redim, dtype=float) * fator_luz).astype(np.uint8)
        folha_np[:, :, 3] = 255

        # 3. Bisel de espessura da chapa de aço visível na borda livre
        largura_bisel = max(int(round(2.5 * np.sin(theta))), 1)
        if theta_deg > 2.0:
            for ty in range(delta_y, altura_folha - delta_y):
                brilho_borda = 0.65 + 0.35 * (1.0 - ty / float(altura_folha))
                cor_borda = np.array([125, 142, 152, 255], dtype=float) * brilho_borda
                x_inicio = max(x_aberto, x_esq - largura_bisel)
                if x_inicio < x_esq:
                    frame[y_topo + ty, x_inicio:x_esq] = cor_borda.astype(np.uint8)

        # 4. Amostragem em perspectiva coluna a coluna
        for col in range(w_proj):
            t_col = col / max(w_proj - 1, 1)
            dy_col = int(round(delta_y * (1.0 - t_col)))
            h_col = altura_folha - 2 * dy_col
            col_img = Image.fromarray(folha_np[:, col : col + 1]).resize(
                (1, h_col), Image.Resampling.BILINEAR
            )
            col_x = x_esq + col
            if x_aberto <= col_x < x_pivot:
                frame[y_topo + dy_col : y_topo + dy_col + h_col, col_x] = np.array(col_img)[:, 0]

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
    caminho_ref = (
        pathlib.Path(sys.argv[1])
        if len(sys.argv) > 1
        else RAIZ / "assets/modelagem/cenario/porta_bloco_referencia.jpg"
    )
    img_ref = carregar_referencia(caminho_ref)

    PASTA_QUADROS.mkdir(parents=True, exist_ok=True)

    # 1. Parede estática base
    parede = gerar_parede_estatica(img_ref)
    parede.save(PASTA_QUADROS / "parede_porta_bloco.png")
    print(f"Salva parede estática {LARGURA_PAREDE}x{ALTURA_PAREDE}: {PASTA_QUADROS / 'parede_porta_bloco.png'}")

    # 2. Quadros animados
    quadros = gerar_quadros_animacao(img_ref)
    for i, quadro in enumerate(quadros):
        quadro.save(PASTA_QUADROS / f"{NOME_BASE}_{i:02d}.png")
    print(f"Salvos {len(quadros)} quadros em {PASTA_QUADROS}")

    # 3. Recurso SpriteFrames
    gravar_sprite_frames(len(quadros))
    print(f"Salvo recurso: {PASTA_QUADROS / 'porta_bloco_quadros.tres'}")


if __name__ == "__main__":
    main()

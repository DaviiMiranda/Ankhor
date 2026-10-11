"""Gera a animação de abrir da porta da Biblioteca a partir de um vídeo.

Uso:
    python assets/modelagem/cenario/gerar_porta_biblioteca.py caminho/do/video.mp4

O vídeo original (animacao_porta_biblioteca1.mp4) tem 1920x1080, 24 quadros por
segundo e 4 s. Só o começo serve: a porta de correr abre entre os quadros 20 e
56, e depois a câmera entra no escuro (zoom), que não vira sprite.

Para cada quadro útil o script:
  1. recorta a porta com o batente de aço (RECORTE, em pixels do vídeo);
  2. reduz para TAMANHO com média de área (cada pixel final é a média de um
     bloco de 880/80 = 11 pixels de largura), que mantém o rabisco da madeira
     sem serrilhado;
  3. grava um PNG por quadro e o SpriteFrames (.tres) da animação "abrir".

A proporção do recorte é a do tamanho final (880/968 = 80/88), então a redução
é a mesma nos dois eixos e a porta não deforma.

Precisa do ffmpeg no PATH.
"""
import pathlib
import shutil
import subprocess
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[3]
PASTA_QUADROS = RAIZ / "assets/sprites/cenario/biblioteca/porta"
RES_QUADROS = "res://assets/sprites/cenario/biblioteca/porta"
NOME_BASE = "porta_biblioteca_abrir"

QUADRO_INICIAL = 18
QUADRO_FINAL = 56

LARGURA_RECORTE = 880
ALTURA_RECORTE = 968
X_RECORTE = 470
Y_RECORTE = 60

LARGURA = 80
ALTURA = 88

VELOCIDADE = 36.0


def gerar_quadros(video: pathlib.Path) -> int:
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        sys.exit("ffmpeg não encontrado no PATH")
    PASTA_QUADROS.mkdir(parents=True, exist_ok=True)
    for antigo in PASTA_QUADROS.glob(f"{NOME_BASE}_*.png"):
        antigo.unlink()
    filtro = (
        f"select='between(n,{QUADRO_INICIAL},{QUADRO_FINAL})',"
        f"crop={LARGURA_RECORTE}:{ALTURA_RECORTE}:{X_RECORTE}:{Y_RECORTE},"
        f"scale={LARGURA}:{ALTURA}:flags=area"
    )
    subprocess.run(
        [
            ffmpeg, "-v", "error", "-y", "-i", str(video),
            "-vf", filtro, "-fps_mode", "passthrough",
            "-start_number", "0",
            str(PASTA_QUADROS / f"{NOME_BASE}_%02d.png"),
        ],
        check=True,
    )
    return len(list(PASTA_QUADROS.glob(f"{NOME_BASE}_*.png")))


def gravar_sprite_frames(quantidade: int) -> None:
    linhas = ["[gd_resource type=\"SpriteFrames\" format=3]", ""]
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
    (PASTA_QUADROS / "porta_biblioteca_quadros.tres").write_text("\n".join(linhas), encoding="utf-8")


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    video = pathlib.Path(sys.argv[1])
    if not video.is_file():
        sys.exit(f"vídeo não encontrado: {video}")
    quantidade = gerar_quadros(video)
    gravar_sprite_frames(quantidade)
    print(f"{quantidade} quadros {LARGURA}x{ALTURA} em {PASTA_QUADROS}")


if __name__ == "__main__":
    main()

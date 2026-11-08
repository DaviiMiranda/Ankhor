"""Texturas procedurais em 512/1024 px, salvas pelo Blender para os dois renderizadores."""

from pathlib import Path

import bpy
import numpy as np


PASTA = Path(__file__).resolve().parents[3] / "assets/sprites/menu/notebook"
MATERIAIS = {
    "Tampo": ("madeira", 0.7, 1.0, 0.0), "Madeira": ("madeira", 0.4, 0.85, 0.0),
    "MadeiraEscura": ("madeira", 0.4, 0.48, 0.0), "Parede": ("parede", 1.0, 1.0, 0.0),
    "Cortina": ("tecido", 0.3, 1.0, 0.0), "MetalNotebook": ("metal", 0.18, 1.0, 0.65),
    "PlasticoNotebook": ("metal", 0.18, 0.42, 0.0), "TeclasNotebook": ("metal", 0.05, 0.36, 0.0),
}


def salvar(nome, valores, dados=False):
    altura, largura = valores.shape[:2]
    imagem = bpy.data.images.new(nome, width=largura, height=altura, alpha=False)
    imagem.colorspace_settings.name = "Non-Color" if dados else "sRGB"
    if valores.ndim == 2:
        valores = np.repeat(valores[:, :, None], 3, axis=2)
    rgba = np.ones((altura, largura, 4), dtype=np.float32)
    rgba[:, :, :3] = np.clip(valores, 0, 1)
    imagem.pixels.foreach_set(rgba.ravel())
    imagem.filepath_raw = str(PASTA / (nome + ".png"))
    imagem.file_format = "PNG"
    imagem.save()
    return imagem


def conjunto(nome, cor, altura, rugosidade, relevo):
    salvar(nome + "_cor", cor)
    salvar(nome + "_rugosidade", rugosidade, True)
    # O gradiente do campo de altura inclina a normal tangente, sem alterar a silhueta.
    dy, dx = np.gradient(altura)
    normal = np.stack((-dx * relevo, -dy * relevo, np.ones_like(dx)), axis=2)
    normal /= np.linalg.norm(normal, axis=2)[:, :, None]
    salvar(nome + "_normal", normal * 0.5 + 0.5, True)


def gerar_texturas():
    PASTA.mkdir(parents=True, exist_ok=True)
    sorteio = np.random.default_rng(20261107)
    tamanho = 1024
    u, v = np.meshgrid(np.arange(tamanho) / tamanho, np.arange(tamanho) / tamanho)
    ruido = sorteio.normal(0, 1, (tamanho, tamanho))
    curva = 0.20 * np.sin(v * np.pi * 4) + 0.06 * np.sin(v * np.pi * 12)
    onda = (np.sin((u * 26 + curva) * np.pi * 2) * 0.5 + 0.5)
    fibra = (np.sin((u * 237 + curva * 8) * np.pi * 2) * 0.5 + 0.5) ** 12
    veio = onda ** 18
    tom = 0.025 * np.sin(u * np.pi * 8) - 0.055 * veio - 0.018 * fibra + ruido * 0.003
    cor = np.array([0.31, 0.175, 0.086]) + tom[:, :, None] * np.array([1.0, 0.7, 0.36])
    conjunto("madeira", cor, onda * 0.15 + fibra * 0.12, 0.52 + veio * 0.16 + ruido * 0.01, 4.0)

    tamanho = 512
    u, v = np.meshgrid(np.arange(tamanho) / tamanho, np.arange(tamanho) / tamanho)
    ruido = sorteio.normal(0, 1, (tamanho, tamanho))
    escovado = np.sin(v * np.pi * 382) * 0.004 + ruido * 0.0018
    cor = np.array([0.14, 0.172, 0.215]) + escovado[:, :, None]
    conjunto("metal", cor, escovado, 0.42 + escovado * 3 + ruido * 0.015, 8.0)

    trama = np.sin(u * np.pi * 256) * np.cos(v * np.pi * 256)
    fios = trama * 0.008 + ruido * 0.002
    cor = np.array([0.25, 0.29, 0.355]) + fios[:, :, None]
    conjunto("tecido", cor, trama * 0.02, np.full_like(u, 0.94), 2.5)

    mancha = np.sin(u * np.pi * 6) * np.sin(v * np.pi * 4) * 0.006
    grao = ruido * 0.003 + mancha
    cor = np.array([0.26, 0.24, 0.235]) + grao[:, :, None]
    conjunto("parede", cor, grao, 0.9 + ruido * 0.008, 5.0)
    gerar_ceu_noturno()


def gerar_ceu_noturno():
    # Céu independente do prólogo: gradiente azul profundo e estrelas de tamanho discreto.
    tamanho = 512
    u, v = np.meshgrid(np.arange(tamanho) / tamanho, np.arange(tamanho) / tamanho)
    cor = np.zeros((tamanho, tamanho, 3))
    for canal, (baixo, alto) in enumerate(((0.018, 0.009), (0.029, 0.014), (0.066, 0.038))):
        cor[:, :, canal] = baixo * (1 - v) + alto * v
    nuvens = (np.sin(u * 13 + v * 6) * np.sin(v * 17 - u * 5) + 1) * 0.0015
    cor += nuvens[:, :, None]
    sorteio = np.random.default_rng(3026)
    for i in range(100):
        x, y = sorteio.integers(3, tamanho - 3, size=2)
        brilho = sorteio.uniform(0.16, 0.52)
        cor[y, x] = (brilho * 0.75, brilho * 0.85, brilho)
        if i % 13 == 0:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                cor[y + dy, x + dx] += brilho * 0.15
    return salvar("ceu_noturno", cor)


def aplicar_materiais():
    for nome, (arquivo, metros, intensidade, metalico) in MATERIAIS.items():
        material = bpy.data.materials.get(nome)
        if material is None:
            continue
        nos, ligacoes = material.node_tree.nodes, material.node_tree.links
        bsdf = nos.get("Principled BSDF")
        bsdf.inputs["Metallic"].default_value = metalico
        posicao = nos.new("ShaderNodeNewGeometry")
        escala = nos.new("ShaderNodeVectorMath")
        escala.operation = "SCALE"
        escala.inputs[3].default_value = 1.0 / metros
        ligacoes.new(posicao.outputs["Position"], escala.inputs[0])
        for sufixo, entrada in (("cor", "Base Color"), ("rugosidade", "Roughness")):
            textura = nos.new("ShaderNodeTexImage")
            textura.image = bpy.data.images.load(str(PASTA / (arquivo + "_" + sufixo + ".png")), check_existing=True)
            textura.interpolation = "Closest"
            textura.projection = "BOX"
            ligacoes.new(escala.outputs["Vector"], textura.inputs["Vector"])
            if sufixo == "cor":
                multiplicar = nos.new("ShaderNodeMixRGB")
                multiplicar.blend_type = "MULTIPLY"
                multiplicar.inputs[0].default_value = 1
                multiplicar.inputs[2].default_value = (intensidade, intensidade, intensidade, 1)
                ligacoes.new(textura.outputs["Color"], multiplicar.inputs[1])
                ligacoes.new(multiplicar.outputs["Color"], bsdf.inputs[entrada])
            else:
                textura.image.colorspace_settings.name = "Non-Color"
                ligacoes.new(textura.outputs["Color"], bsdf.inputs[entrada])
        relevo = nos.new("ShaderNodeTexImage")
        relevo.image = bpy.data.images.load(str(PASTA / (arquivo + "_normal.png")), check_existing=True)
        relevo.image.colorspace_settings.name = "Non-Color"
        relevo.projection = "BOX"
        relevo.interpolation = "Closest"
        ligacoes.new(escala.outputs["Vector"], relevo.inputs["Vector"])
        normal = nos.new("ShaderNodeNormalMap")
        normal.inputs["Strength"].default_value = 0.3
        ligacoes.new(relevo.outputs["Color"], normal.inputs["Color"])
        ligacoes.new(normal.outputs["Normal"], bsdf.inputs["Normal"])

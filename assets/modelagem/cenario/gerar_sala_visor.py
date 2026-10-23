# gerar_sala_visor.py — modela no Blender o quarto que o Gabriel vê quando põe
# os óculos do Zane na sala segura (docs/mecanicas/visor_3d.md). É a mente dele
# materializada: o quarto de 2026 da ilustração do prólogo
# (assets/sprites/cutscenes/seg_prologo/cena_02_quarto.png), com cama,
# escrivaninha embaixo da janela, estante, porta e pôsteres, mais três coisas
# que guardam o jogo até ali:
#
#   - o MURAL de cortiça em cima da cama (as anotações do caderno);
#   - a ESCRIVANINHA (os documentos que ele já leu, jogados em cima);
#   - o QUADRO BRANCO ao lado da TV (os números do jogo).
#
# O que aparece em cima deles (cartões, papéis, texto) é montado no Godot com
# os dados do save; aqui só sai o móvel. As texturas (tábuas, papel de parede,
# cortiça, tecidos...) também são do Godot: saem de gerar_texturas_quarto.py e
# entram por mapeamento triplanar, procurando os materiais pelo NOME que eles
# têm aqui (Chao, Parede, Madeira...). Se renomear um material, renomeie lá
# também (scripts/visor/texturas_do_quarto.gd). A TV de tubo continua no meio da
# parede do fundo, com o menu de salvar na tela.
#
# Não há teto: as paredes terminam numa linha ciano e, acima delas, é o escuro.
# É um quarto lembrado, não um quarto de verdade.
#
# Como rodar (sem abrir a janela do Blender):
#
#   blender -b --factory-startup --python assets/modelagem/cenario/gerar_sala_visor.py
#
# O que sai:
#   assets/modelos/sala_visor.glb   o modelo em glTF binário, só com materiais
#                                   simples (cor, rugosidade e brilho próprio)
#
# ---------------------------------------------------------------------------
# EIXOS: TUDO AQUI ESTÁ EM COORDENADAS DO GODOT
# ---------------------------------------------------------------------------
#
# O Blender usa Z para cima; o glTF e o Godot usam Y para cima. O exportador
# converte sozinho:
#
#     Godot (x, y, z)  =  Blender (x, z, -y)
#
# Para não ter que pensar nessa troca em cada peça, as funções deste script
# (caixa, cilindro) recebem centro e tamanho EM COORDENADAS DO GODOT e fazem a
# conversão por dentro (para_blender). Assim os números daqui são os mesmos
# da cena cenas/visor/sala_visor.tscn (colisões, luzes, mural, mesa, quadro).
#
#     x: da esquerda (-) para a direita (+) de quem entra no quarto
#     y: do chão (0) para cima
#     z: do fundo (-), onde fica a TV, para a porta (+)
#
# Todas as medidas estão em metros. Se mudar algo que o Godot também usa
# (anotado nos comentários), mude lá também.

import math
import os
import random

import bpy
from mathutils import Vector

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
SAIDA = os.path.join(PASTA_PROJETO, "assets", "modelos", "sala_visor.glb")

# Quarto: 5 m x 5 m, paredes de 2,8 m, centrado na origem. (Godot: colisões.)
LARGURA = 5.0
PROFUNDIDADE = 5.0
ALTURA_PAREDE = 2.8
MEIA = LARGURA / 2

# Móvel da TV, no meio da parede do fundo. (Godot: colisão MovelComTV.)
MOVEL_LARGURA = 1.0
MOVEL_PROFUNDIDADE = 0.5
MOVEL_ALTURA = 0.6
MOVEL_Z = -1.9

# TV de tubo: corpo da frente e a "traseira" mais estreita, como os CRTs.
TV_LARGURA = 0.62
TV_ALTURA = 0.5
TV_PROFUNDIDADE = 0.42
TRASEIRA_LARGURA = 0.44
TRASEIRA_ALTURA = 0.38
TRASEIRA_PROFUNDIDADE = 0.2

# Tela 4:3, um pouco acima do meio da frente (os botões ficam embaixo).
TELA_LARGURA = 0.44
TELA_ALTURA = 0.33
TELA_SUBIDA = 0.03

# Mural de cortiça na parede da direita, em cima da cama. (Godot: Mural.)
MURAL_CENTRO = (MEIA, 1.6, -0.3)
MURAL_TAMANHO = (2.05, 1.05)

# Quadro branco na parede do fundo, à direita da TV. (Godot: Quadro.)
QUADRO_CENTRO = (1.55, 1.425, -MEIA)
QUADRO_TAMANHO = (1.3, 0.85)

# Escrivaninha embaixo da janela, na parede da esquerda. (Godot: Mesa.)
MESA_X = -2.17
MESA_Z = -0.2
MESA_ALTURA = 0.76
MESA_COMPRIMENTO = 1.4
MESA_FUNDO = 0.62

# Janela da parede da esquerda: o vidro (a imagem do prólogo) é um Sprite3D
# do Godot de 1 m x 1 m; aqui só sai a moldura em volta. (Godot: Janela.)
JANELA_CENTRO_Y = 1.6
JANELA_CENTRO_Z = MESA_Z
JANELA_LADO = 1.0


def cor(hexa):
    hexa = hexa.lstrip("#")
    return tuple(int(hexa[i:i + 2], 16) / 255 for i in (0, 2, 4)) + (1.0,)


def material(nome, cor_base, rugosidade=0.8, brilho=None, forca_brilho=1.0):
    """Material simples (Principled BSDF): cor, rugosidade e, se pedir, brilho
    próprio (emission). É o que o glTF leva sem perder nada."""
    mat = bpy.data.materials.new(nome)
    mat.use_nodes = True
    no = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    no.inputs["Base Color"].default_value = cor(cor_base)
    no.inputs["Roughness"].default_value = rugosidade
    if brilho:
        no.inputs["Emission Color"].default_value = cor(brilho)
        no.inputs["Emission Strength"].default_value = forca_brilho
    return mat


def para_blender(x, y, z):
    """Ponto do Godot -> ponto do Blender: (x, y, z) -> (x, -z, y)."""
    return (x, -z, y)


def tamanho_para_blender(sx, sy, sz):
    """Tamanho do Godot -> tamanho do Blender (só troca os eixos de lugar)."""
    return (sx, sz, sy)


def caixa(nome, centro, tamanho, mat, giro_y=0.0, inclinar=(0.0, 0.0), arredondar=0.0):
    """Cubo com centro e tamanho no Godot. inclinar = (giro em volta do x, giro
    em volta do z) em graus, aplicado antes do giro_y (em volta do eixo vertical).
    arredondar > 0 chanfra todas as arestas com esse raio (em metros): é o que
    tira o ar de bloco dos móveis macios (travesseiro, moletom, mochila). A
    escala, o giro e o chanfro já saem aplicados: o glTF sai com medidas reais."""
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=para_blender(*centro))
    obj = bpy.context.active_object
    obj.name = nome
    obj.scale = tamanho_para_blender(*tamanho)
    obj.rotation_euler = (math.radians(inclinar[0]), math.radians(-inclinar[1]), math.radians(giro_y))
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    if arredondar > 0:
        bisel = obj.modifiers.new("Bisel", "BEVEL")
        bisel.width = min(arredondar, min(tamanho) * 0.45)
        bisel.segments = 2
        bisel.limit_method = "NONE"
        bpy.ops.object.modifier_apply(modifier="Bisel")
    obj.data.materials.append(mat)
    return obj


def cilindro(nome, centro, raio, altura, mat, lados=12, inclinar=(0.0, 0.0)):
    """Cilindro em pé (eixo vertical), com centro no Godot. inclinar deita ele:
    (90, 0) deixa o eixo ao longo do z, (0, 90) ao longo do x."""
    bpy.ops.mesh.primitive_cylinder_add(radius=raio, depth=altura, vertices=lados, location=para_blender(*centro))
    obj = bpy.context.active_object
    obj.name = nome
    obj.rotation_euler = (math.radians(inclinar[0]), math.radians(-inclinar[1]), 0.0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    obj.data.materials.append(mat)
    return obj


LADOS = {"+z": ((0, 1), (1, 0)), "-z": ((0, -1), (-1, 0)), "+x": ((1, 0), (0, -1)), "-x": ((-1, 0), (0, 1))}
ATLAS_MARCAS = (64, 40)
MARCAS = {"livros": (0, 0, 64, 10), "cabos": (0, 10, 64, 20), "roupas": (0, 20, 64, 30), "fragil": (0, 30, 64, 40)}


def juntar(nome, objetos):
    """Junta vários objetos num só (menos nós e menos chamadas de desenho)."""
    bpy.ops.object.select_all(action="DESELECT")
    for obj in objetos:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = objetos[0]
    bpy.ops.object.join()
    junto = bpy.context.active_object
    junto.name = nome
    return junto


def limpar_cena():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    for mat in list(bpy.data.materials):
        bpy.data.materials.remove(mat)


# ---------------------------------------------------------------------------
# CASCA DO QUARTO
# ---------------------------------------------------------------------------

def quarto(m):
    """Chão (as tábuas são a textura do Godot), quatro paredes (placas de 10 cm
    do lado de FORA do volume, para a face de dentro já apontar para o jogador),
    rodapé e a linha ciano no alto das paredes, onde o quarto "acaba"."""
    caixa("Chao", (0, -0.05, 0), (LARGURA, 0.1, PROFUNDIDADE), m["chao"])

    meio = ALTURA_PAREDE / 2
    juntar("Paredes", [
        caixa("ParedeFundo", (0, meio, -MEIA - 0.05), (LARGURA + 0.2, ALTURA_PAREDE, 0.1), m["parede"]),
        caixa("ParedeFrente", (0, meio, MEIA + 0.05), (LARGURA + 0.2, ALTURA_PAREDE, 0.1), m["parede"]),
        caixa("ParedeEsquerda", (-MEIA - 0.05, meio, 0), (0.1, ALTURA_PAREDE, PROFUNDIDADE), m["parede"]),
        caixa("ParedeDireita", (MEIA + 0.05, meio, 0), (0.1, ALTURA_PAREDE, PROFUNDIDADE), m["parede"]),
    ])

    dentro = MEIA - 0.01
    rodape = []
    linha = []
    for centro, tamanho in [
        ((0, 0, -dentro), (LARGURA, 1, 0.02)),
        ((0, 0, dentro), (LARGURA, 1, 0.02)),
        ((-dentro, 0, 0), (0.02, 1, PROFUNDIDADE)),
        ((dentro, 0, 0), (0.02, 1, PROFUNDIDADE)),
    ]:
        x, _, z = centro
        sx, _, sz = tamanho
        rodape.append(caixa("Rodape", (x, 0.05, z), (sx, 0.1, sz), m["madeira_escura"]))
        linha.append(caixa("LinhaCiano", (x, ALTURA_PAREDE - 0.01, z), (sx, 0.02, sz), m["ciano"]))
    juntar("Rodape", rodape)
    juntar("LinhaDoAlto", linha)

    # Tapete vermelho (a cor do Gabriel) no meio, com uma borda mais escura.
    juntar("Tapete", [
        caixa("TapeteBorda", (0.2, 0.004, 0.4), (2.2, 0.008, 1.6), m["tapete_borda"]),
        caixa("TapeteMeio", (0.2, 0.006, 0.4), (2.0, 0.008, 1.4), m["tapete"]),
    ])


# ---------------------------------------------------------------------------
# TV DE TUBO (o menu de salvar)
# ---------------------------------------------------------------------------

def movel_da_tv(m):
    """Móvel baixo: corpo, tampo com quina arredondada, duas gavetas com
    puxador, quatro pés, e em cima, do lado da TV, o videogame e o controle."""
    frente = MOVEL_Z + MOVEL_PROFUNDIDADE / 2
    partes = [
        caixa("Corpo", (0, MOVEL_ALTURA / 2 + 0.04, MOVEL_Z), (MOVEL_LARGURA - 0.04, MOVEL_ALTURA - 0.12, MOVEL_PROFUNDIDADE - 0.04), m["movel"]),
        caixa("Tampo", (0, MOVEL_ALTURA - 0.02, MOVEL_Z), (MOVEL_LARGURA, 0.04, MOVEL_PROFUNDIDADE), m["movel"], arredondar=0.006),
    ]
    for x in (-0.23, 0.23):
        partes.append(caixa("GavetaTV", (x, 0.3, frente - 0.015), (0.42, 0.26, 0.012), m["madeira_escura"], arredondar=0.003))
        partes.append(cilindro("PuxadorTV", (x, 0.3, frente - 0.002), 0.014, 0.018, m["metal"], inclinar=(90, 0)))
    for x in (-MOVEL_LARGURA / 2 + 0.06, MOVEL_LARGURA / 2 - 0.06):
        for z in (MOVEL_Z - MOVEL_PROFUNDIDADE / 2 + 0.06, MOVEL_Z + MOVEL_PROFUNDIDADE / 2 - 0.06):
            partes.append(caixa("Pe", (x, 0.02, z), (0.05, 0.04, 0.05), m["madeira_escura"]))
    juntar("MovelTV", partes)

    em_cima = MOVEL_ALTURA
    juntar("Videogame", [
        caixa("Console", (-0.41, em_cima + 0.0175, MOVEL_Z + 0.04), (0.16, 0.035, 0.13), m["console"], arredondar=0.006),
        caixa("FendaConsole", (-0.41, em_cima + 0.0265, MOVEL_Z + 0.106), (0.12, 0.004, 0.002), m["notebook"]),
        caixa("Controle", (0.4, em_cima + 0.011, MOVEL_Z + 0.1), (0.11, 0.022, 0.05), m["notebook"], giro_y=-14, arredondar=0.009),
        caixa("BotoesControle", (0.425, em_cima + 0.023, MOVEL_Z + 0.098), (0.02, 0.004, 0.02), m["led"], giro_y=-14),
        haste("CaboControle", (0.35, em_cima + 0.005, MOVEL_Z + 0.08), (0.32, em_cima + 0.004, MOVEL_Z + 0.05), 0.0025, m["notebook"], lados=6),
    ])


def frente_da_tv():
    """z da face da frente do corpo da TV (o lado que olha para o jogador)."""
    return MOVEL_Z + TV_PROFUNDIDADE / 2


def centro_da_tela():
    return (0.0, MOVEL_ALTURA + TV_ALTURA / 2 + TELA_SUBIDA, frente_da_tv() + 0.003)


def tv(m):
    """Corpo da TV, traseira mais estreita, moldura funda em volta da tela,
    dois botões, uma luzinha e a antena em V (duas varetas inclinadas)."""
    base = MOVEL_ALTURA
    _, y_tela, _ = centro_da_tela()
    partes = [
        caixa("Corpo", (0, base + TV_ALTURA / 2, MOVEL_Z), (TV_LARGURA, TV_ALTURA, TV_PROFUNDIDADE), m["corpo_tv"]),
        caixa("Traseira", (0, base + TV_ALTURA / 2, MOVEL_Z - TV_PROFUNDIDADE / 2 - TRASEIRA_PROFUNDIDADE / 2),
              (TRASEIRA_LARGURA, TRASEIRA_ALTURA, TRASEIRA_PROFUNDIDADE), m["corpo_tv"]),
    ]
    borda = 0.025
    z_moldura = frente_da_tv() + 0.006
    partes += [
        caixa("MolduraCima", (0, y_tela + TELA_ALTURA / 2 + borda / 2, z_moldura), (TELA_LARGURA + 2 * borda, borda, 0.012), m["moldura_tv"]),
        caixa("MolduraBaixo", (0, y_tela - TELA_ALTURA / 2 - borda / 2, z_moldura), (TELA_LARGURA + 2 * borda, borda, 0.012), m["moldura_tv"]),
        caixa("MolduraEsq", (-TELA_LARGURA / 2 - borda / 2, y_tela, z_moldura), (borda, TELA_ALTURA, 0.012), m["moldura_tv"]),
        caixa("MolduraDir", (TELA_LARGURA / 2 + borda / 2, y_tela, z_moldura), (borda, TELA_ALTURA, 0.012), m["moldura_tv"]),
    ]
    y_botoes = base + 0.045
    for x in (0.18, 0.24):
        partes.append(caixa("Botao", (x, y_botoes, frente_da_tv() + 0.008), (0.035, 0.035, 0.016), m["botao_tv"]))
    juntar("TV", partes)

    caixa("Led", (-0.24, y_botoes, frente_da_tv() + 0.004), (0.012, 0.012, 0.008), m["led"])

    # Antena: cilindros finos saindo do topo, abertos em V (35 graus para cada
    # lado). Este é o único giro fora do eixo vertical, então é feito direto em
    # coordenadas do Blender: inclinar em volta do Y do Blender move a ponta em X.
    varetas = []
    topo = base + TV_ALTURA
    comprimento = 0.45
    for lado in (-1, 1):
        angulo = math.radians(35) * lado
        bpy.ops.mesh.primitive_cylinder_add(radius=0.004, depth=comprimento, vertices=8)
        vareta = bpy.context.active_object
        vareta.rotation_euler = (0, angulo, 0)
        vareta.location = para_blender(math.sin(angulo) * comprimento / 2, topo + math.cos(angulo) * comprimento / 2, MOVEL_Z - 0.05)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        vareta.data.materials.append(m["metal"])
        varetas.append(vareta)
    varetas.append(caixa("BaseAntena", (0, topo + 0.01, MOVEL_Z - 0.05), (0.08, 0.02, 0.05), m["corpo_tv"]))
    juntar("Antena", varetas)


def tela(m):
    """A tela é um plano 4:3 de frente para o jogador (normal +Z no Godot). O
    plano do Blender nasce deitado (normal +Z do Blender) com o UV de 0 a 1;
    girar 90 graus em X deixa a normal em -Y do Blender (= +Z do Godot), com o
    "para cima" da textura apontando para cima. Visto de frente, u cresce para
    a direita e v para cima: a imagem não sai espelhada."""
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=para_blender(*centro_da_tela()))
    obj = bpy.context.active_object
    obj.name = "Tela"
    obj.rotation_euler = (math.radians(90), 0, 0)
    obj.scale = (TELA_LARGURA, TELA_ALTURA, 1.0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    obj.data.materials.append(m["tela"])


# ---------------------------------------------------------------------------
# OS TRÊS LUGARES QUE GUARDAM O JOGO
# ---------------------------------------------------------------------------

def mural(m):
    """Quadro de cortiça com moldura de madeira, preso na parede da direita.
    A face da cortiça fica em x = MEIA - 0,035, um pouco à frente da moldura."""
    x, y, z = MURAL_CENTRO
    largura, altura = MURAL_TAMANHO
    juntar("Mural", [
        caixa("MolduraMural", (x - 0.015, y, z), (0.03, altura + 0.08, largura + 0.08), m["madeira"]),
        caixa("Cortica", (x - 0.025, y, z), (0.02, altura, largura), m["cortica"]),
    ])


def quadro_branco(m):
    """Quadro branco com moldura de alumínio e a calha das canetas embaixo.
    A face branca fica em z = -MEIA + 0,04."""
    x, y, z = QUADRO_CENTRO
    largura, altura = QUADRO_TAMANHO
    juntar("QuadroBranco", [
        caixa("MolduraQuadro", (x, y, z + 0.015), (largura + 0.05, altura + 0.05, 0.03), m["aluminio"]),
        caixa("Superficie", (x, y, z + 0.035), (largura, altura, 0.01), m["quadro"]),
        caixa("Calha", (x, y - altura / 2 - 0.035, z + 0.05), (largura * 0.6, 0.02, 0.06), m["aluminio"]),
    ])
    juntar("Canetas", [
        caixa("CanetaVermelha", (x - 0.15, y - altura / 2 - 0.018, z + 0.055), (0.12, 0.015, 0.015), m["caneta_vermelha"]),
        caixa("CanetaAzul", (x + 0.02, y - altura / 2 - 0.018, z + 0.055), (0.12, 0.015, 0.015), m["caneta_azul"]),
    ])


def escrivaninha(m):
    """Escrivaninha encostada na parede da esquerda, embaixo da janela: tampo de
    quina arredondada, gaveteiro do lado da porta com três gavetas e puxadores,
    painel e travessa entre as pernas. Em cima, na faixa perto da parede (para os
    papéis do Godot terem espaço no resto do tampo): pilha de livros com
    páginas, pote com canetas, caneca de café e a luminária articulada. O
    notebook tem a própria função."""
    x0 = -MEIA + MESA_FUNDO / 2
    z_porta = MESA_Z + MESA_COMPRIMENTO / 2
    z_fundo = MESA_Z - MESA_COMPRIMENTO / 2
    z_gav = z_porta - 0.22
    frente_gav = x0 + (MESA_FUNDO - 0.04) / 2
    inicio_painel = z_fundo + 0.06
    fim_painel = z_gav - 0.2
    partes = [
        caixa("TampoMesa", (x0, MESA_ALTURA - 0.02, MESA_Z), (MESA_FUNDO, 0.04, MESA_COMPRIMENTO), m["tampo"], arredondar=0.006),
        caixa("Gaveteiro", (x0, (MESA_ALTURA - 0.04) / 2, z_gav), (MESA_FUNDO - 0.04, MESA_ALTURA - 0.04, 0.4), m["madeira"]),
        caixa("PeMesa1", (x0 - MESA_FUNDO / 2 + 0.04, (MESA_ALTURA - 0.04) / 2, z_fundo + 0.04), (0.04, MESA_ALTURA - 0.04, 0.04), m["madeira"]),
        caixa("PeMesa2", (x0 + MESA_FUNDO / 2 - 0.04, (MESA_ALTURA - 0.04) / 2, z_fundo + 0.04), (0.04, MESA_ALTURA - 0.04, 0.04), m["madeira"]),
        caixa("PainelDeFundo", (-MEIA + 0.03, 0.47, (inicio_painel + fim_painel) / 2), (0.015, 0.45, fim_painel - inicio_painel), m["madeira_escura"]),
        caixa("TravessaMesa", (x0, 0.69, z_fundo + 0.04), (MESA_FUNDO - 0.08, 0.05, 0.03), m["madeira"]),
    ]
    for y in (0.60, 0.375, 0.15):
        partes.append(caixa("GavetaFrente", (frente_gav + 0.005, y, z_gav), (0.014, 0.2, 0.36), m["madeira_escura"], arredondar=0.003))
        partes.append(caixa("PuxadorGaveta", (frente_gav + 0.02, y, z_gav), (0.012, 0.012, 0.14), m["metal"]))
        for dz in (-0.06, 0.06):
            partes.append(caixa("PostePuxador", (frente_gav + 0.0135, y, z_gav + dz), (0.012, 0.01, 0.01), m["metal"]))
    juntar("Escrivaninha", partes)

    em_cima = MESA_ALTURA
    pilha = []
    for i, (capa, giro) in enumerate([("livro_verde", -8), ("livro_vinho", 0), ("livro_azul", 8)]):
        pilha += livro(m, "Livro", (-2.36, em_cima + 0.0225 + i * 0.045, -0.78), (0.2, 0.045, 0.28), m[capa], giro)
    juntar("LivrosDaMesa", pilha)

    pote = [cilindro("Pote", (-2.38, em_cima + 0.05, -0.5), 0.035, 0.1, m["metal"], lados=16)]
    for k, (cor_caneta, dx, dz) in enumerate([("lapis", 0.012, 0.0), ("caneta_azul", -0.01, 0.01), ("caneta_vermelha", 0.0, -0.014),
                                              ("notebook", 0.014, 0.012), ("livro_verde", -0.012, -0.008)]):
        pote.append(haste("Caneta", (-2.38 + dx * 0.3, em_cima + 0.03, -0.5 + dz * 0.3),
                          (-2.38 + dx * 3.2, em_cima + 0.16 + 0.01 * k, -0.5 + dz * 3.2), 0.004, m[cor_caneta]))
    juntar("PoteDeLapis", pote)

    cx, cz = -2.37, -0.3
    juntar("Caneca", [
        cilindro("CorpoCaneca", (cx, em_cima + 0.045, cz), 0.04, 0.09, m["caneca"], lados=16),
        cilindro("Cafe", (cx, em_cima + 0.0905, cz), 0.034, 0.002, m["cafe"], lados=16),
        caixa("AlcaCaneca", (cx + 0.052, em_cima + 0.045, cz), (0.012, 0.055, 0.012), m["caneca"], arredondar=0.003),
        caixa("AlcaCima", (cx + 0.044, em_cima + 0.068, cz), (0.026, 0.012, 0.012), m["caneca"]),
        caixa("AlcaBaixo", (cx + 0.044, em_cima + 0.022, cz), (0.026, 0.012, 0.012), m["caneca"]),
    ])

    bx = -2.4
    juntar("Luminaria", [
        cilindro("BaseLuminaria", (bx, em_cima + 0.01, 0.0), 0.065, 0.02, m["notebook"], lados=20),
        haste("BracoBaixo", (bx, em_cima + 0.02, 0.0), (bx + 0.005, em_cima + 0.3, 0.0), 0.007, m["notebook"]),
        caixa("Junta", (bx + 0.005, em_cima + 0.3, 0.0), (0.03, 0.03, 0.03), m["metal"], arredondar=0.008),
        haste("BracoCima", (bx + 0.005, em_cima + 0.3, 0.0), (bx + 0.07, em_cima + 0.37, 0.0), 0.006, m["notebook"]),
        caixa("CupulaLuminaria", (-2.325, em_cima + 0.375, 0.0), (0.16, 0.05, 0.1), m["notebook"], inclinar=(0, -8), arredondar=0.012),
    ])
    caixa("Lampada", (-2.31, em_cima + 0.345, 0.0), (0.08, 0.01, 0.06), m["lampada"])


def cadeira(m):
    """Cadeira de escritório virada para a mesa: assento e encosto acolchoados,
    dois apoios de braço, coluna com capa e base de cinco braços com rodízios.
    No encosto, o moletom vermelho do Gabriel, jogado (peças macias e chanfradas:
    a parte de trás, a dobra por cima, o capuz, uma manga caída e outra no
    assento)."""
    x, z = -1.62, -0.1
    partes = [
        caixa("Assento", (x, 0.47, z), (0.46, 0.07, 0.46), m["cadeira"], arredondar=0.025),
        caixa("Encosto", (x + 0.23, 0.80, z), (0.06, 0.5, 0.44), m["cadeira"], inclinar=(0, -8), arredondar=0.025),
        cilindro("Coluna", (x, 0.26, z), 0.026, 0.4, m["metal"]),
        cilindro("CapaColuna", (x, 0.37, z), 0.036, 0.16, m["cadeira"]),
    ]
    for k in range(5):
        giro = 72 * k + 10
        meio = deslocar((x, 0.075, z), 0.15, 0, giro)
        ponta = deslocar((x, 0.03, z), 0.3, 0, giro)
        partes.append(caixa("BracoBase", meio, (0.3, 0.035, 0.05), m["metal"], giro_y=giro, arredondar=0.01))
        partes.append(cilindro("Rodizio", ponta, 0.025, 0.05, m["notebook"], lados=10))
    for lado in (-1, 1):
        partes.append(caixa("PosteBraco", (x + 0.02, 0.58, z + lado * 0.245), (0.03, 0.2, 0.03), m["cadeira"]))
        partes.append(caixa("ApoioBraco", (x + 0.02, 0.69, z + lado * 0.245), (0.26, 0.035, 0.065), m["cadeira"], arredondar=0.012))
    juntar("Cadeira", partes)

    juntar("Moletom", [
        caixa("MoletomCostas", (x + 0.28, 0.86, z), (0.07, 0.46, 0.46), m["moletom"], inclinar=(0, -8), arredondar=0.025),
        caixa("MoletomDobra", (x + 0.22, 1.09, z), (0.15, 0.07, 0.46), m["moletom"], inclinar=(0, -20), arredondar=0.03),
        caixa("MoletomFrente", (x + 0.17, 0.94, z), (0.05, 0.3, 0.42), m["moletom"], inclinar=(0, -8), arredondar=0.02),
        caixa("MoletomCapuz", (x + 0.34, 0.98, z - 0.02), (0.1, 0.15, 0.26), m["moletom"], inclinar=(0, -10), arredondar=0.04),
        caixa("MoletomMangaCaida", (x + 0.22, 0.72, z + 0.27), (0.09, 0.4, 0.09), m["moletom"], inclinar=(6, 0), arredondar=0.03),
        caixa("MoletomMangaAssento", (x + 0.02, 0.53, z - 0.18), (0.3, 0.07, 0.09), m["moletom"], giro_y=20, arredondar=0.03),
        caixa("MoletomBolso", (x + 0.325, 0.78, z), (0.02, 0.1, 0.24), m["moletom"], inclinar=(0, -8), arredondar=0.008),
    ])


def janela(m):
    """Moldura da janela na parede da esquerda (o vidro é a imagem do Godot), o
    peitoril com um cacto no vasinho e a cortina de quatro dobras, pendurada
    num varão com as pontas arredondadas."""
    x = -MEIA + 0.03
    y, z = JANELA_CENTRO_Y, JANELA_CENTRO_Z
    lado = JANELA_LADO
    borda = 0.06
    juntar("Janela", [
        caixa("JanelaCima", (x, y + lado / 2 + borda / 2, z), (0.06, borda, lado + 2 * borda), m["janela"]),
        caixa("JanelaBaixo", (x, y - lado / 2 - borda / 2, z), (0.06, borda, lado + 2 * borda), m["janela"]),
        caixa("JanelaEsq", (x, y, z + lado / 2 + borda / 2), (0.06, lado, borda), m["janela"]),
        caixa("JanelaDir", (x, y, z - lado / 2 - borda / 2), (0.06, lado, borda), m["janela"]),
        caixa("JanelaMeio", (x + 0.01, y, z), (0.04, lado, 0.03), m["janela"]),
        caixa("Peitoril", (x + 0.05, y - lado / 2 - borda - 0.01, z), (0.16, 0.03, lado + 0.3), m["janela"], arredondar=0.006),
    ])
    topo_peitoril = y - lado / 2 - borda - 0.01 + 0.015
    cacto_z = z - 0.38
    juntar("Cacto", [
        cilindro("VasoCacto", (x + 0.05, topo_peitoril + 0.035, cacto_z), 0.04, 0.07, m["vaso"], lados=14),
        cilindro("TerraCacto", (x + 0.05, topo_peitoril + 0.071, cacto_z), 0.034, 0.003, m["terra"], lados=14),
        cilindro("CorpoCacto", (x + 0.05, topo_peitoril + 0.13, cacto_z), 0.028, 0.12, m["folha"], lados=10),
        esfera("TopoCacto", (x + 0.05, topo_peitoril + 0.19, cacto_z), 0.028, m["folha"]),
        haste("BracoCacto", (x + 0.05, topo_peitoril + 0.12, cacto_z), (x + 0.05, topo_peitoril + 0.15, cacto_z + 0.055), 0.012, m["folha"]),
        haste("BracoCacto2", (x + 0.05, topo_peitoril + 0.11, cacto_z), (x + 0.05, topo_peitoril + 0.15, cacto_z - 0.05), 0.011, m["folha"]),
    ])
    pregas = []
    for i in range(4):
        pregas.append(caixa("Prega", (x + 0.06 + (0.016 if i % 2 else -0.012), y + 0.02, z - lado / 2 - 0.08 - i * 0.075),
                            (0.045, lado + 0.4, 0.085), m["cortina"], arredondar=0.012))
    juntar("Cortina", pregas)
    juntar("VaraoDaCortina", [
        haste("Varao", (x + 0.06, y + lado / 2 + 0.24, z - lado / 2 - 0.02), (x + 0.06, y + lado / 2 + 0.24, z - lado / 2 - 0.42), 0.011, m["metal"], lados=10),
        esfera("PonteiraVarao", (x + 0.06, y + lado / 2 + 0.24, z - lado / 2 - 0.02), 0.02, m["metal"]),
        esfera("PonteiraVarao", (x + 0.06, y + lado / 2 + 0.24, z - lado / 2 - 0.42), 0.02, m["metal"]),
    ])


def estante(m):
    """Estante no canto do fundo, à esquerda: laterais, fundo, cinco prateleiras
    e livros de alturas e cores sorteadas (semente fixa: sai sempre igual), cada
    um com uma faixa clara na lombada. No fim de cada prateleira sobra um vão
    com um objeto: uma caixa de arquivo, o robozinho de brinquedo, uma planta,
    um porta-retrato e uma pilha de revistas. No topo, uma caixa de papelão."""
    sorteio = random.Random(2026)
    x, z = -1.95, -2.3
    largura, altura, fundo = 0.9, 1.9, 0.36
    partes = [
        caixa("LateralEsq", (x - largura / 2 + 0.015, altura / 2, z), (0.03, altura, fundo), m["madeira"]),
        caixa("LateralDir", (x + largura / 2 - 0.015, altura / 2, z), (0.03, altura, fundo), m["madeira"]),
        caixa("FundoEstante", (x, altura / 2, z - fundo / 2 + 0.01), (largura, altura, 0.02), m["madeira_escura"]),
    ]
    prateleiras = [0.03, 0.42, 0.8, 1.18, 1.56, altura - 0.015]
    for y in prateleiras:
        partes.append(caixa("Prateleira", (x, y, z), (largura - 0.04, 0.03, fundo - 0.02), m["madeira"], arredondar=0.004))
    juntar("Estante", partes)

    cores = ["livro_verde", "livro_vinho", "livro_azul", "livro_bege", "livro_cinza"]
    livros = []
    faixas = []
    for y in prateleiras[:-1]:
        xi = x - largura / 2 + 0.05
        limite = x + largura / 2 - 0.05 - 0.27
        while xi < limite:
            esp = sorteio.uniform(0.025, 0.05)
            alt = sorteio.uniform(0.22, 0.32)
            livros.append(caixa("Livro", (xi + esp / 2, y + 0.015 + alt / 2, z + 0.02), (esp, alt, 0.24), m[sorteio.choice(cores)]))
            faixas.append(caixa("FaixaLombada", (xi + esp / 2, y + 0.015 + alt * sorteio.uniform(0.25, 0.7), z + 0.1405), (esp + 0.001, 0.02, 0.003), m["paginas"]))
            xi += esp + 0.004 + (0.025 if sorteio.random() < 0.05 else 0.0)
    juntar("LivrosDaEstante", livros)
    juntar("FaixasDosLivros", faixas)

    xo = x + largura / 2 - 0.17
    base = lambda i: prateleiras[i] + 0.015
    objetos = caixa_de_papelao(m, "CaixaDeArquivo", (xo, base(0) + 0.1, z + 0.02), (0.22, 0.2, 0.24), giro_y=-6)
    b = base(1)
    objetos += [
        caixa("PernaRobo", (xo - 0.02, b + 0.02, z + 0.03), (0.022, 0.04, 0.03), m["robo_corpo"]),
        caixa("PernaRobo", (xo + 0.02, b + 0.02, z + 0.03), (0.022, 0.04, 0.03), m["robo_corpo"]),
        caixa("CorpoRobo", (xo, b + 0.085, z + 0.03), (0.08, 0.09, 0.06), m["robo_corpo"], arredondar=0.008),
        caixa("PeitoRobo", (xo, b + 0.09, z + 0.0615), (0.03, 0.03, 0.003), m["led_vermelho"]),
        caixa("BracoRobo", (xo - 0.055, b + 0.085, z + 0.03), (0.022, 0.07, 0.025), m["robo_corpo"]),
        caixa("BracoRobo", (xo + 0.055, b + 0.085, z + 0.03), (0.022, 0.07, 0.025), m["robo_corpo"]),
        caixa("CabecaRobo", (xo, b + 0.16, z + 0.03), (0.07, 0.055, 0.055), m["robo_corpo"], arredondar=0.008),
        caixa("OlhoRobo", (xo - 0.016, b + 0.162, z + 0.0585), (0.014, 0.012, 0.004), m["led_vermelho"]),
        caixa("OlhoRobo", (xo + 0.016, b + 0.162, z + 0.0585), (0.014, 0.012, 0.004), m["led_vermelho"]),
        haste("AntenaRobo", (xo, b + 0.19, z + 0.03), (xo + 0.012, b + 0.235, z + 0.03), 0.003, m["metal"], lados=6),
        esfera("PontaAntena", (xo + 0.012, b + 0.24, z + 0.03), 0.009, m["led_vermelho"]),
    ]
    b = base(2)
    objetos += [
        cilindro("VasoPlanta", (xo, b + 0.045, z + 0.03), 0.048, 0.09, m["vaso"], lados=14),
        cilindro("TerraPlanta", (xo, b + 0.091, z + 0.03), 0.042, 0.003, m["terra"], lados=14),
    ]
    for k in range(9):
        angulo = k * 2.4
        raio = 0.035 * ((k % 3) / 2 + 0.3)
        objetos.append(esfera("Folha", (xo + math.cos(angulo) * raio, b + 0.12 + 0.012 * (k % 4), z + 0.03 + math.sin(angulo) * raio),
                              0.03, m["folha" if k % 2 else "folha_escura"], (1.0, 0.8, 1.0)))
    b = base(3)
    objetos += [
        caixa("MolduraRetrato", (xo, b + 0.09, z + 0.03), (0.14, 0.18, 0.014), m["madeira_escura"], arredondar=0.003),
        quad_na_caixa("FotoRetrato", (xo, b + 0.09, z + 0.03), (0.14, 0.18, 0.014), 0, "+z", 0.105, 0.145, m["foto"]),
        caixa("ApoioRetrato", (xo, b + 0.07, z - 0.01), (0.03, 0.14, 0.012), m["madeira_escura"]),
    ]
    b = base(4)
    for i, (capa, giro) in enumerate([("livro_vinho", -4), ("livro_azul", 6), ("livro_bege", -8)]):
        objetos += livro(m, "Revista", (xo, b + 0.007 + i * 0.014, z + 0.03), (0.2, 0.014, 0.26), m[capa], giro)
    objetos += caixa_de_papelao(m, "CaixaDoTopo", (x - 0.1, altura + 0.095, z + 0.01), (0.34, 0.19, 0.26), giro_y=10, marca="livros")
    juntar("ObjetosDaEstante", objetos)


def cama(m):
    """Cama de solteiro encostada na parede da direita, com a cabeceira no lado
    do fundo: estrado, cabeceira com remate, colchão, dois travesseiros, cobertor
    amarrotado com uma ponta caída pelo lado do quarto. Do lado da porta, o
    criado-mudo (com gaveta, despertador e livro) e a mochila verde no chão."""
    x = MEIA - 0.5
    z_cabeca, z_pe = -1.35, 0.75
    z = (z_cabeca + z_pe) / 2
    comprimento = z_pe - z_cabeca
    juntar("Cama", [
        caixa("Estrado", (x, 0.15, z), (1.0, 0.3, comprimento), m["madeira"], arredondar=0.01),
        caixa("Cabeceira", (x, 0.45, z_cabeca - 0.03), (1.0, 0.9, 0.06), m["madeira"], arredondar=0.012),
        caixa("RemateCabeceira", (x, 0.92, z_cabeca - 0.03), (1.06, 0.045, 0.09), m["madeira_escura"], arredondar=0.01),
        caixa("Colchao", (x, 0.4, z), (0.94, 0.2, comprimento - 0.06), m["lencol"], arredondar=0.035),
        caixa("Travesseiro", (x + 0.05, 0.55, z_cabeca + 0.25), (0.6, 0.1, 0.32), m["lencol"], giro_y=-6, arredondar=0.045),
        caixa("TravesseiroDeBaixo", (x - 0.02, 0.53, z_cabeca + 0.3), (0.56, 0.09, 0.3), m["lencol"], giro_y=7, arredondar=0.04),
        caixa("Cobertor", (x - 0.02, 0.52, z + 0.35), (0.98, 0.05, comprimento - 0.7), m["cobertor"], arredondar=0.02),
        caixa("Dobra", (x - 0.1, 0.56, z - 0.05), (0.8, 0.05, 0.25), m["cobertor"], giro_y=10, arredondar=0.022),
        caixa("PontaCaida", (x - 0.49, 0.45, z + 0.4), (0.05, 0.25, 0.9), m["cobertor"], arredondar=0.02),
    ])
    juntar("CriadoMudo", [
        caixa("CorpoCriado", (MEIA - 0.25, 0.25, 1.15), (0.42, 0.5, 0.42), m["madeira"], arredondar=0.006),
        caixa("TampoCriado", (MEIA - 0.25, 0.515, 1.15), (0.46, 0.03, 0.46), m["madeira_escura"], arredondar=0.006),
        caixa("GavetaCriado", (MEIA - 0.46, 0.34, 1.15), (0.012, 0.2, 0.34), m["madeira_escura"], arredondar=0.003),
        caixa("PuxadorCriado", (MEIA - 0.475, 0.34, 1.15), (0.012, 0.02, 0.12), m["metal"]),
        caixa("PeCriado", (MEIA - 0.25, 0.012, 1.15), (0.4, 0.024, 0.4), m["madeira_escura"]),
    ])
    juntar("DespertadorNoCriado", [
        caixa("CorpoDespertador", (MEIA - 0.2, 0.57, 1.15), (0.09, 0.08, 0.14), m["despertador_corpo"], arredondar=0.012),
        quad("MostradorDespertador", (MEIA - 0.2 - 0.0455, 0.55, 1.15 - 0.055), (MEIA - 0.2 - 0.0455, 0.55, 1.15 + 0.055),
             (MEIA - 0.2 - 0.0455, 0.59, 1.15 + 0.055), (MEIA - 0.2 - 0.0455, 0.59, 1.15 - 0.055), m["despertador"]),
        haste("SinoEsq", (MEIA - 0.2, 0.61, 1.15 - 0.04), (MEIA - 0.2, 0.635, 1.15 - 0.055), 0.006, m["metal"], lados=8),
        haste("SinoDir", (MEIA - 0.2, 0.61, 1.15 + 0.04), (MEIA - 0.2, 0.635, 1.15 + 0.055), 0.006, m["metal"], lados=8),
    ])
    juntar("LivroDoCriado", livro(m, "LivroCriado", (MEIA - 0.28, 0.5425, 0.92), (0.15, 0.025, 0.21), m["livro_vinho"], 22))

    cx, cz, giro = 1.25, 1.25, 25
    corpo = (cx, 0.21, cz)
    juntar("Mochila", [
        caixa("CorpoMochila", corpo, (0.34, 0.42, 0.2), m["mochila"], giro_y=giro, arredondar=0.05),
        caixa("TopoMochila", deslocar((cx, 0.42, cz), 0, 0, giro), (0.3, 0.05, 0.18), m["mochila"], giro_y=giro, arredondar=0.025),
        caixa("BolsoMochila", deslocar((cx, 0.14, cz), -0.05, 0.11, giro), (0.24, 0.18, 0.06), m["mochila_escura"], giro_y=giro, arredondar=0.02),
        caixa("AbaDoBolso", deslocar((cx, 0.235, cz), -0.05, 0.115, giro), (0.25, 0.04, 0.065), m["mochila_escura"], giro_y=giro, arredondar=0.015),
        caixa("ZiperMochila", deslocar((cx, 0.3, cz), 0, 0.103, giro), (0.26, 0.012, 0.004), m["metal"], giro_y=giro),
        caixa("AlcaDaMochila", deslocar((cx, 0.46, cz), 0, 0, giro), (0.12, 0.03, 0.025), m["mochila_escura"], giro_y=giro, arredondar=0.01),
        caixa("AlcaCaida", deslocar((cx, 0.006, cz), 0.09, 0.3, giro), (0.055, 0.012, 0.32), m["mochila_escura"], giro_y=giro + 8, arredondar=0.004),
        caixa("AlcaCaida", deslocar((cx, 0.006, cz), -0.09, 0.32, giro), (0.055, 0.012, 0.3), m["mochila_escura"], giro_y=giro - 12, arredondar=0.004),
    ])


def porta(m):
    """Porta do quarto na parede da frente (atrás de quem entra): batente, folha
    com quatro almofadas em relevo, três dobradiças, maçaneta de alavanca com
    roseta, o interruptor e uma jaqueta verde pendurada num gancho."""
    x = -1.5
    z = MEIA - 0.02
    face = z - 0.04
    partes = [
        caixa("Batente", (x, 1.05, z + 0.005), (1.0, 2.1, 0.03), m["madeira_escura"]),
        caixa("Folha", (x, 1.02, z - 0.02), (0.86, 2.03, 0.04), m["porta"]),
    ]
    for dx in (-0.2, 0.2):
        partes.append(caixa("AlmofadaCima", (x + dx, 1.5, face - 0.005), (0.34, 0.7, 0.012), m["porta"], arredondar=0.004))
        partes.append(caixa("AlmofadaBaixo", (x + dx, 0.58, face - 0.005), (0.34, 0.62, 0.012), m["porta"], arredondar=0.004))
    for y in (0.25, 1.0, 1.8):
        partes.append(caixa("Dobradica", (x - 0.43, y, face), (0.02, 0.1, 0.015), m["metal"]))
    partes += [
        cilindro("RosetaMacaneta", (x + 0.33, 1.0, face - 0.004), 0.03, 0.01, m["metal"], lados=16, inclinar=(90, 0)),
        caixa("Macaneta", (x + 0.38, 1.0, face - 0.026), (0.1, 0.02, 0.02), m["metal"], arredondar=0.008),
        caixa("PinoMacaneta", (x + 0.33, 1.0, face - 0.016), (0.02, 0.02, 0.02), m["metal"]),
    ]
    juntar("Porta", partes)
    caixa("Interruptor", (x + 0.7, 1.15, z - 0.005), (0.07, 0.11, 0.01), m["lencol"], arredondar=0.003)
    juntar("JaquetaNaPorta", [
        caixa("GanchoDaPorta", (x - 0.2, 1.8, face - 0.015), (0.03, 0.03, 0.03), m["metal"]),
        caixa("CorpoJaqueta", (x - 0.2, 1.5, face - 0.045), (0.32, 0.55, 0.05), m["mochila_escura"], arredondar=0.02),
        caixa("GolaJaqueta", (x - 0.2, 1.8, face - 0.045), (0.18, 0.07, 0.06), m["mochila_escura"], arredondar=0.025),
        caixa("MangaJaqueta", (x - 0.39, 1.42, face - 0.045), (0.08, 0.42, 0.06), m["mochila_escura"], inclinar=(0, 5), arredondar=0.025),
        caixa("MangaJaqueta", (x - 0.01, 1.42, face - 0.045), (0.08, 0.42, 0.06), m["mochila_escura"], inclinar=(0, -5), arredondar=0.025),
        caixa("ZiperJaqueta", (x - 0.2, 1.48, face - 0.0715), (0.012, 0.5, 0.004), m["metal"]),
    ])


def haste(nome, a, b, raio, mat, lados=8):
    """Cilindro fino ligando dois pontos do Godot (braços da luminária, canetas,
    antenas, alças)."""
    pa, pb = Vector(para_blender(*a)), Vector(para_blender(*b))
    direcao = pb - pa
    bpy.ops.mesh.primitive_cylinder_add(radius=raio, depth=direcao.length, vertices=lados, location=(pa + pb) / 2)
    obj = bpy.context.active_object
    obj.name = nome
    obj.rotation_mode = "QUATERNION"
    obj.rotation_quaternion = direcao.to_track_quat("Z", "Y")
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    obj.data.materials.append(mat)
    return obj


def esfera(nome, centro, raio, mat, escala=(1.0, 1.0, 1.0)):
    """Esfera baixa (80 faces), esticada pela escala (no Godot): folhas, bolas
    de papel, pontas de antena."""
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=raio, location=para_blender(*centro))
    obj = bpy.context.active_object
    obj.name = nome
    obj.scale = tamanho_para_blender(*escala)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    obj.data.materials.append(mat)
    return obj


def quad(nome, bl, br, tr, tl, mat, uv=(0.0, 0.0, 1.0, 1.0)):
    """Retângulo com UV explícito, dado pelos quatro cantos NO GODOT, vistos de
    frente: embaixo-esquerda, embaixo-direita, em cima-direita, em cima-esquerda
    (anti-horário, para a normal apontar para quem olha). uv = (u0, v0, u1, v1)
    no sentido do Blender (v cresce para cima). Serve para teclado, tela,
    mostrador e escrita nas caixas, onde a imagem tem que cair no lugar certo
    (o triplanar não resolve isso)."""
    pontos = [para_blender(*p) for p in (bl, br, tr, tl)]
    malha = bpy.data.meshes.new(nome)
    malha.from_pydata(pontos, [], [(0, 1, 2, 3)])
    malha.update()
    u0, v0, u1, v1 = uv
    camada = malha.uv_layers.new(name="UVMap")
    for laco, par in zip(malha.loops, [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]):
        camada.data[laco.index].uv = par
    malha.materials.append(mat)
    obj = bpy.data.objects.new(nome, malha)
    bpy.context.collection.objects.link(obj)
    return obj


def deslocar(centro, dx, dz, giro_y):
    """Ponto a (dx, dz) do centro, no referencial de uma peça girada giro_y
    graus: dx anda ao longo do x da peça e dz ao longo do z dela."""
    c, s = math.cos(math.radians(giro_y)), math.sin(math.radians(giro_y))
    return (centro[0] + dx * c + dz * s, centro[1], centro[2] - dx * s + dz * c)


def uv_da_marca(nome):
    x0, y0, x1, y1 = MARCAS[nome]
    largura, altura = ATLAS_MARCAS
    return (x0 / largura, 1 - y1 / altura, x1 / largura, 1 - y0 / altura)


def quad_na_caixa(nome, centro, tam, giro_y, lado, largura, altura, mat, uv=(0.0, 0.0, 1.0, 1.0), dy=0.0):
    """Quad colado numa face vertical de uma caixa (centro, tam, giro_y como na
    caixa): lado é "+z", "-z", "+x" ou "-x" no referencial da caixa; largura e
    altura em metros; dy sobe ou desce o quad em relação ao centro da caixa."""
    (nx, nz), (rx, rz) = LADOS[lado]
    recuo = (tam[0] if nx else tam[2]) / 2 + 0.0015

    def ponto(a, b):
        return deslocar((centro[0], centro[1] + dy + b, centro[2]), nx * recuo + rx * a, nz * recuo + rz * a, giro_y)

    return quad(nome, ponto(-largura / 2, -altura / 2), ponto(largura / 2, -altura / 2),
                ponto(largura / 2, altura / 2), ponto(-largura / 2, altura / 2), mat, uv)


def livro(m, nome, centro, tam, mat_capa, giro_y=0.0):
    """Livro deitado (tam = comprimento em x, espessura, largura em z): duas
    capas, a lombada do lado -x e o miolo de páginas aparecendo do lado +x."""
    comprimento, espessura, largura = tam
    x, y, z = centro
    return [
        caixa(nome, (x, y - espessura / 2 + 0.003, z), (comprimento, 0.006, largura), mat_capa, giro_y),
        caixa(nome, (x, y + espessura / 2 - 0.003, z), (comprimento, 0.006, largura), mat_capa, giro_y),
        caixa(nome, deslocar((x, y, z), 0.004, 0, giro_y), (comprimento - 0.012, espessura - 0.012, largura - 0.006), m["paginas"], giro_y),
        caixa(nome, deslocar((x, y, z), -comprimento / 2 + 0.004, 0, giro_y), (0.008, espessura, largura), mat_capa, giro_y),
    ]


def notebook(m):
    """Notebook aberto em cima da mesa, de frente para a cadeira (quem senta
    está do lado +x): base de quina arredondada com teclado e trackpad (quads com
    UV), dobradiça, tampa inclinada 15 graus para trás e a tela acesa."""
    y = MESA_ALTURA
    nx, nz = -2.29, 0.28
    topo = y + 0.014
    esquerda, direita = nz + 0.15, nz - 0.15
    juntar("Notebook", [
        caixa("BaseNotebook", (nx, y + 0.007, nz), (0.24, 0.014, 0.34), m["notebook"], arredondar=0.004),
        quad("Teclado", (nx + 0.025, topo + 0.0005, esquerda), (nx + 0.025, topo + 0.0005, direita),
             (nx - 0.105, topo + 0.0005, direita), (nx - 0.105, topo + 0.0005, esquerda), m["teclado"]),
        quad("Trackpad", (nx + 0.095, topo + 0.0005, nz + 0.055), (nx + 0.095, topo + 0.0005, nz - 0.055),
             (nx + 0.045, topo + 0.0005, nz - 0.055), (nx + 0.045, topo + 0.0005, nz + 0.055), m["trackpad"]),
        cilindro("Dobradica", (nx - 0.115, y + 0.016, nz), 0.007, 0.3, m["metal"], lados=10, inclinar=(90, 0)),
    ])
    angulo = math.radians(15)
    para_cima = (-math.sin(angulo), math.cos(angulo))
    para_a_frente = (math.cos(angulo), math.sin(angulo))
    dobradica = (nx - 0.115, y + 0.016)
    centro_tampa = (dobradica[0] + para_cima[0] * 0.11, dobradica[1] + para_cima[1] * 0.11)
    caixa("TampaNotebook", (centro_tampa[0], centro_tampa[1], nz), (0.008, 0.22, 0.34), m["notebook"], inclinar=(0, 15), arredondar=0.003)
    tela_centro = (centro_tampa[0] + para_a_frente[0] * 0.0045 + para_cima[0] * 0.005,
                   centro_tampa[1] + para_a_frente[1] * 0.0045 + para_cima[1] * 0.005)

    def ponto_da_tela(dz, subida):
        return (tela_centro[0] + para_cima[0] * subida, tela_centro[1] + para_cima[1] * subida, nz + dz)

    quad("TelaNotebook", ponto_da_tela(0.15, -0.095), ponto_da_tela(-0.15, -0.095),
         ponto_da_tela(-0.15, 0.095), ponto_da_tela(0.15, 0.095), m["tela_notebook"])


def caixa_de_papelao(m, nome, centro, tam, giro_y=0.0, fita=True, marca=None, aberta=False):
    """Caixa de papelão (tam = x, altura, z; centro no meio do volume) com chanfro,
    fita larga no topo (descendo pelas duas pontas) e, se pedir, canetão ou
    etiqueta na face +z (marca é uma chave de MARCAS). aberta=True faz uma caixa
    sem tampa, de paredes finas, com as quatro abas viradas para fora."""
    w, h, d = tam
    cx, cy, cz = centro
    partes = []
    if not aberta:
        partes.append(caixa(nome, centro, tam, m["papelao"], giro_y, arredondar=0.004))
        if fita:
            partes.append(caixa("Fita", (cx, cy + h / 2 + 0.0015, cz), (0.05, 0.003, d + 0.004), m["fita"], giro_y))
            for sinal in (-1, 1):
                partes.append(caixa("FitaPonta", deslocar((cx, cy + h / 2 - 0.03, cz), 0, sinal * (d / 2 + 0.0015), giro_y),
                                    (0.05, 0.06, 0.003), m["fita"], giro_y))
    else:
        t = 0.006
        partes.append(caixa(nome, deslocar((cx, cy - h / 2 + t / 2, cz), 0, 0, giro_y), (w, t, d), m["papelao"], giro_y))
        for sinal in (-1, 1):
            partes.append(caixa(nome, deslocar((cx, cy, cz), sinal * (w / 2 - t / 2), 0, giro_y), (t, h, d), m["papelao"], giro_y))
            partes.append(caixa(nome, deslocar((cx, cy, cz), 0, sinal * (d / 2 - t / 2), giro_y), (w - 2 * t, h, t), m["papelao"], giro_y))
        abertura = 38
        seno, cosseno = math.sin(math.radians(abertura)), math.cos(math.radians(abertura))
        for sinal in (-1, 1):
            comprimento = d / 2
            dobradica = (cx, cy + h / 2 + seno * comprimento / 2, cz)
            pos = deslocar(dobradica, 0, sinal * (d / 2 + cosseno * comprimento / 2), giro_y)
            partes.append(caixa("Aba", pos, (w, 0.005, comprimento), m["papelao"], giro_y, inclinar=(-sinal * abertura, 0)))
            comprimento = w / 2
            dobradica = (cx, cy + h / 2 + seno * comprimento / 2, cz)
            pos = deslocar(dobradica, sinal * (w / 2 + cosseno * comprimento / 2), 0, giro_y)
            partes.append(caixa("Aba", pos, (comprimento, 0.005, d), m["papelao"], giro_y, inclinar=(0, sinal * abertura)))
    if marca:
        if marca == "fragil":
            largura, altura = 0.2, 0.05
        else:
            largura, altura = min(0.3, w * 0.8), 0.05
        partes.append(quad_na_caixa("Marca", centro, tam, giro_y, "+z", largura, altura, m["marcas"], uv_da_marca(marca), dy=-h * 0.1))
    return partes


def caixas_jogadas(m):
    """As caixas de papelão do quarto de mudança de alguém que não terminou de
    desfazer: duas empilhadas no canto do fundo (LIVROS e FRAGIL), uma aberta ao
    lado, com livros de fora, uma caída de lado perto da cama, vomitando livros
    e papéis, e uma pequena junto da parede da porta (CABOS)."""
    pilha = caixa_de_papelao(m, "CaixaGrande", (2.08, 0.19, -2.2), (0.5, 0.38, 0.4), giro_y=8, marca="livros")
    pilha += caixa_de_papelao(m, "CaixaDeCima", (2.1, 0.38 + 0.15, -2.18), (0.42, 0.3, 0.34), giro_y=-14, marca="fragil")
    juntar("PilhaDeCaixas", pilha)

    aberta = caixa_de_papelao(m, "CaixaAberta", (1.5, 0.14, -2.22), (0.38, 0.28, 0.32), giro_y=-5, aberta=True)
    aberta += livro(m, "LivroNaCaixa", (1.5, 0.3, -2.2), (0.22, 0.04, 0.3), m["livro_bege"], -5)
    aberta += livro(m, "LivroNaCaixa", (1.52, 0.34, -2.2), (0.2, 0.035, 0.28), m["livro_azul"], 12)
    aberta += [caixa("MoletomNaCaixa", (1.45, 0.3, -2.27), (0.2, 0.08, 0.18), m["cobertor"], giro_y=20, arredondar=0.03)]
    juntar("CaixaAbertaComLivros", aberta)

    t = 0.006
    giro = 35
    centro = (0.9, 0.15, -1.3)
    w, h, d = 0.36, 0.3, 0.34
    caida = [caixa("CaixaCaida", deslocar(centro, 0, -d / 2 + t / 2, giro), (w, h, t), m["papelao"], giro)]
    for sinal in (-1, 1):
        caida.append(caixa("CaixaCaida", deslocar(centro, sinal * (w / 2 - t / 2), 0, giro), (t, h, d), m["papelao"], giro))
        caida.append(caixa("CaixaCaida", deslocar((centro[0], centro[1] + sinal * (h / 2 - t / 2), centro[2]), 0, 0, giro), (w - 2 * t, t, d), m["papelao"], giro))
    caida.append(quad_na_caixa("Marca", centro, (w, h, d), giro, "-x", 0.2, 0.05, m["marcas"], uv_da_marca("roupas"), dy=0.0))
    juntar("CaixaCaida", caida)

    espalhados = []
    for i, (capa, dx, dz, giro_livro) in enumerate([("livro_vinho", 0.18, 0.28, 50), ("livro_verde", 0.42, 0.38, 100), ("livro_cinza", 0.12, 0.58, 18)]):
        px_, _, pz = deslocar(centro, dx, dz, giro)
        espalhados += livro(m, "LivroNoChao", (px_, 0.0175, pz), (0.2, 0.035, 0.27), m[capa], giro_livro)
    juntar("LivrosNoChao", espalhados)

    pequena = caixa_de_papelao(m, "CaixaPequena", (0.55, 0.13, 2.3), (0.36, 0.26, 0.3), giro_y=-8, marca="cabos")
    juntar("CaixaPequena", pequena)


def bagunca(m):
    """O que ficou jogado pelo chão: um par de tênis perto da porta e bolas de
    papel amassado debaixo da mesa."""
    tenis = []
    for nome, centro, giro in [("TenisEsq", (-0.85, 0, 2.05), 25), ("TenisDir", (-0.62, 0, 2.2), -50)]:
        tenis += [
            caixa(nome, (centro[0], 0.014, centro[2]), (0.1, 0.028, 0.27), m["tenis_sola"], giro, arredondar=0.01),
            caixa(nome, deslocar((centro[0], 0.063, centro[2]), 0, -0.05, giro), (0.09, 0.07, 0.14), m["tenis"], giro, arredondar=0.025),
            caixa(nome, deslocar((centro[0], 0.048, centro[2]), 0, 0.075, giro), (0.09, 0.04, 0.11), m["tenis"], giro, arredondar=0.02),
            caixa(nome, deslocar((centro[0], 0.082, centro[2]), 0, 0.02, giro), (0.07, 0.006, 0.06), m["tenis_sola"], giro),
            caixa(nome, deslocar((centro[0], 0.06, centro[2]), 0, 0.14, giro), (0.092, 0.012, 0.012), m["tenis_sola"], giro),
        ]
    juntar("Tenis", tenis)
    juntar("PapeisAmassados", [
        esfera("BolaDePapel", (-1.25, 0.03, 0.55), 0.035, m["paginas"], (1.0, 0.9, 1.0)),
        esfera("BolaDePapel", (-1.05, 0.028, 0.72), 0.03, m["paginas"], (1.0, 0.9, 1.1)),
        esfera("BolaDePapel", (-1.45, 0.03, -0.62), 0.033, m["paginas"], (1.1, 0.9, 1.0)),
    ])


def main():
    limpar_cena()
    m = {
        "chao": material("Chao", "#4a3426", rugosidade=0.7),
        "parede": material("Parede", "#55535e", rugosidade=0.95),
        "madeira": material("Madeira", "#6b4a32", rugosidade=0.7),
        "madeira_escura": material("MadeiraEscura", "#3a281c", rugosidade=0.7),
        "ciano": material("LinhaCiano", "#1c6f80", brilho="#3fd8f0", forca_brilho=1.5),
        "tapete": material("Tapete", "#7a2a2e", rugosidade=1.0),
        "tapete_borda": material("TapeteBorda", "#4e1a1e", rugosidade=1.0),
        "movel": material("Movel", "#3a2f2a", rugosidade=0.7),
        "corpo_tv": material("CorpoTV", "#4a4640", rugosidade=0.6),
        "moldura_tv": material("MolduraTV", "#1c1c20", rugosidade=0.4),
        "botao_tv": material("BotaoTV", "#2a2a2e", rugosidade=0.4),
        "metal": material("Metal", "#9aa0a8", rugosidade=0.3),
        "led": material("Led", "#c8d84a", brilho="#e4f25a", forca_brilho=2.0),
        "tela": material("Tela", "#05080c", rugosidade=0.2),
        "cortica": material("Cortica", "#a5763f", rugosidade=1.0),
        "aluminio": material("Aluminio", "#b4b8c0", rugosidade=0.35),
        "quadro": material("Quadro", "#e6e8ec", rugosidade=0.25),
        "caneta_vermelha": material("CanetaVermelha", "#c02a2a", rugosidade=0.5),
        "caneta_azul": material("CanetaAzul", "#2a4ac0", rugosidade=0.5),
        "notebook": material("Notebook", "#2c2e34", rugosidade=0.4),
        "tela_notebook": material("TelaNotebook", "#0e1a26", brilho="#16324a", forca_brilho=0.6),
        "livro_verde": material("LivroVerde", "#3d5a3a", rugosidade=0.8),
        "livro_vinho": material("LivroVinho", "#6a2a30", rugosidade=0.8),
        "livro_azul": material("LivroAzul", "#2e4462", rugosidade=0.8),
        "livro_bege": material("LivroBege", "#b8a27a", rugosidade=0.8),
        "livro_cinza": material("LivroCinza", "#5c5f66", rugosidade=0.8),
        "lapis": material("Lapis", "#d8a830", rugosidade=0.6),
        "lampada": material("Lampada", "#ffe8b0", brilho="#ffd890", forca_brilho=3.0),
        "cadeira": material("Cadeira", "#2a2c32", rugosidade=0.6),
        "moletom": material("Moletom", "#b8292f", rugosidade=0.95),
        "janela": material("Janela", "#d8d2c8", rugosidade=0.5),
        "cortina": material("Cortina", "#8a8f9a", rugosidade=1.0),
        "lencol": material("Lencol", "#d6d8e0", rugosidade=0.9),
        "cobertor": material("Cobertor", "#3d4f74", rugosidade=1.0),
        "mochila": material("Mochila", "#5a6b3c", rugosidade=0.9),
        "mochila_escura": material("MochilaEscura", "#3e4a28", rugosidade=0.9),
        "porta": material("Porta", "#6a4a34", rugosidade=0.7),
        "tampo": material("Tampo", "#7a5638", rugosidade=0.6),
        "papelao": material("Papelao", "#a98150", rugosidade=0.95),
        "fita": material("Fita", "#d8c9a0", rugosidade=0.25),
        "marcas": material("Marcas", "#ffffff", rugosidade=0.9),
        "teclado": material("Teclado", "#202228", rugosidade=0.5),
        "trackpad": material("Trackpad", "#3a3e46", rugosidade=0.3),
        "paginas": material("Paginas", "#e6dcc6", rugosidade=0.9),
        "caneca": material("Caneca", "#cfc8ba", rugosidade=0.3),
        "cafe": material("Cafe", "#2b1a10", rugosidade=0.2),
        "despertador": material("Despertador", "#1a0a0a", brilho="#ff4a3a", forca_brilho=1.0),
        "despertador_corpo": material("DespertadorCorpo", "#2a2a30", rugosidade=0.5),
        "vaso": material("Vaso", "#b5623a", rugosidade=0.85),
        "terra": material("Terra", "#2a1c14", rugosidade=1.0),
        "folha": material("Folha", "#3f7a3a", rugosidade=0.8),
        "folha_escura": material("FolhaEscura", "#2c5a2c", rugosidade=0.8),
        "led_vermelho": material("LedVermelho", "#c02020", brilho="#ff3030", forca_brilho=3.0),
        "robo_corpo": material("RoboCorpo", "#8a9098", rugosidade=0.35),
        "tenis": material("Tenis", "#2a5ea8", rugosidade=0.8),
        "tenis_sola": material("TenisSola", "#e8e4d8", rugosidade=0.7),
        "console": material("Console", "#d8d9dc", rugosidade=0.4),
        "foto": material("Foto", "#8fb0c8", rugosidade=0.5),
    }

    quarto(m)
    movel_da_tv(m)
    tv(m)
    tela(m)
    mural(m)
    quadro_branco(m)
    escrivaninha(m)
    notebook(m)
    cadeira(m)
    janela(m)
    estante(m)
    cama(m)
    porta(m)
    caixas_jogadas(m)
    bagunca(m)

    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=SAIDA, export_format="GLB", export_apply=True)
    print("Modelo salvo em", SAIDA)


main()

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


def caixa(nome, centro, tamanho, mat, giro_y=0.0):
    """Cubo com centro e tamanho no Godot, girado giro_y graus em volta do eixo
    vertical (no Blender, o eixo vertical é o Z: mesmo ângulo, mesmo sentido).
    A escala e o giro já saem aplicados: o glTF sai com medidas reais."""
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=para_blender(*centro))
    obj = bpy.context.active_object
    obj.name = nome
    obj.scale = tamanho_para_blender(*tamanho)
    obj.rotation_euler = (0, 0, math.radians(giro_y))
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    obj.data.materials.append(mat)
    return obj


def cilindro(nome, centro, raio, altura, mat, lados=12):
    """Cilindro em pé (eixo vertical), com centro no Godot."""
    bpy.ops.mesh.primitive_cylinder_add(radius=raio, depth=altura, vertices=lados, location=para_blender(*centro))
    obj = bpy.context.active_object
    obj.name = nome
    obj.data.materials.append(mat)
    return obj


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
    """Móvel baixo: corpo, tampo, um friso de gaveta e quatro pés."""
    partes = [
        caixa("Corpo", (0, MOVEL_ALTURA / 2 + 0.04, MOVEL_Z), (MOVEL_LARGURA - 0.04, MOVEL_ALTURA - 0.12, MOVEL_PROFUNDIDADE - 0.04), m["movel"]),
        caixa("Tampo", (0, MOVEL_ALTURA - 0.02, MOVEL_Z), (MOVEL_LARGURA, 0.04, MOVEL_PROFUNDIDADE), m["movel"]),
        caixa("Gaveta", (0, MOVEL_ALTURA / 2, MOVEL_Z + MOVEL_PROFUNDIDADE / 2 - 0.015), (MOVEL_LARGURA * 0.8, 0.02, 0.01), m["madeira_escura"]),
    ]
    for x in (-MOVEL_LARGURA / 2 + 0.06, MOVEL_LARGURA / 2 - 0.06):
        for z in (MOVEL_Z - MOVEL_PROFUNDIDADE / 2 + 0.06, MOVEL_Z + MOVEL_PROFUNDIDADE / 2 - 0.06):
            partes.append(caixa("Pe", (x, 0.02, z), (0.05, 0.04, 0.05), m["madeira_escura"]))
    juntar("MovelTV", partes)


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
    """Escrivaninha encostada na parede da esquerda, embaixo da janela: tampo,
    gaveteiro do lado da porta e dois pés do lado do fundo. Em cima, o notebook
    aberto, uma pilha de livros, o pote de lápis e a luminária, todos na faixa
    perto da parede, para os papéis do Godot terem espaço no resto do tampo."""
    x0 = -MEIA + MESA_FUNDO / 2
    z_porta = MESA_Z + MESA_COMPRIMENTO / 2
    z_fundo = MESA_Z - MESA_COMPRIMENTO / 2
    juntar("Escrivaninha", [
        caixa("TampoMesa", (x0, MESA_ALTURA - 0.02, MESA_Z), (MESA_FUNDO, 0.04, MESA_COMPRIMENTO), m["madeira"]),
        caixa("Gaveteiro", (x0, (MESA_ALTURA - 0.04) / 2, z_porta - 0.22), (MESA_FUNDO - 0.04, MESA_ALTURA - 0.04, 0.4), m["madeira"]),
        caixa("Gaveta1", (x0 + MESA_FUNDO / 2 - 0.015, 0.55, z_porta - 0.22), (0.01, 0.02, 0.2), m["madeira_escura"]),
        caixa("Gaveta2", (x0 + MESA_FUNDO / 2 - 0.015, 0.3, z_porta - 0.22), (0.01, 0.02, 0.2), m["madeira_escura"]),
        caixa("PeMesa1", (x0 - MESA_FUNDO / 2 + 0.04, (MESA_ALTURA - 0.04) / 2, z_fundo + 0.04), (0.04, MESA_ALTURA - 0.04, 0.04), m["madeira"]),
        caixa("PeMesa2", (x0 + MESA_FUNDO / 2 - 0.04, (MESA_ALTURA - 0.04) / 2, z_fundo + 0.04), (0.04, MESA_ALTURA - 0.04, 0.04), m["madeira"]),
    ])

    em_cima = MESA_ALTURA
    # Notebook aberto, de frente para a cadeira: a base deitada e a tela em pé
    # encostada na janela.
    juntar("Notebook", [
        caixa("BaseNotebook", (-2.32, em_cima + 0.01, 0.28), (0.24, 0.02, 0.34), m["notebook"]),
        caixa("TampaNotebook", (-2.45, em_cima + 0.13, 0.28), (0.015, 0.23, 0.34), m["notebook"]),
    ])
    caixa("TelaNotebook", (-2.44, em_cima + 0.13, 0.28), (0.004, 0.2, 0.31), m["tela_notebook"])

    cores = ["livro_verde", "livro_vinho", "livro_azul"]
    livros = []
    for i, nome_cor in enumerate(cores):
        livros.append(caixa("Livro", (-2.36, em_cima + 0.025 + i * 0.045, -0.78), (0.2, 0.045, 0.28), m[nome_cor], giro_y=8 * (i - 1)))
    juntar("LivrosDaMesa", livros)

    juntar("PoteDeLapis", [
        cilindro("Pote", (-2.38, em_cima + 0.05, -0.5), 0.035, 0.1, m["metal"]),
        caixa("Lapis1", (-2.38, em_cima + 0.12, -0.5), (0.008, 0.1, 0.008), m["lapis"]),
        caixa("Lapis2", (-2.37, em_cima + 0.12, -0.49), (0.008, 0.1, 0.008), m["caneta_azul"]),
    ])

    juntar("Luminaria", [
        cilindro("BaseLuminaria", (-2.4, em_cima + 0.01, 0.0), 0.06, 0.02, m["notebook"]),
        caixa("HasteLuminaria", (-2.4, em_cima + 0.2, 0.0), (0.015, 0.38, 0.015), m["notebook"]),
        caixa("CupulaLuminaria", (-2.33, em_cima + 0.38, 0.0), (0.16, 0.06, 0.1), m["notebook"]),
    ])
    caixa("Lampada", (-2.31, em_cima + 0.345, 0.0), (0.08, 0.01, 0.06), m["lampada"])


def cadeira(m):
    """Cadeira de escritório virada para a mesa, com o moletom vermelho do
    Gabriel jogado no encosto."""
    x, z = -1.62, -0.1
    juntar("Cadeira", [
        caixa("Assento", (x, 0.47, z), (0.44, 0.06, 0.44), m["cadeira"]),
        caixa("Encosto", (x + 0.22, 0.78, z), (0.05, 0.5, 0.42), m["cadeira"]),
        cilindro("Coluna", (x, 0.25, z), 0.025, 0.4, m["metal"]),
        caixa("PeCadeira1", (x, 0.04, z), (0.5, 0.03, 0.05), m["metal"]),
        caixa("PeCadeira2", (x, 0.04, z), (0.05, 0.03, 0.5), m["metal"]),
    ])
    juntar("Moletom", [
        caixa("MoletomCostas", (x + 0.26, 0.85, z), (0.05, 0.42, 0.46), m["moletom"]),
        caixa("MoletomCapuz", (x + 0.27, 1.07, z), (0.08, 0.06, 0.24), m["moletom"]),
        caixa("MoletomManga", (x + 0.1, 0.52, z + 0.2), (0.3, 0.06, 0.08), m["moletom"], giro_y=20),
    ])


def janela(m):
    """Moldura da janela na parede da esquerda (o vidro é a imagem do Godot),
    o peitoril e a cortina caída de um lado."""
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
        caixa("Peitoril", (x + 0.05, y - lado / 2 - borda - 0.01, z), (0.16, 0.03, lado + 0.3), m["janela"]),
    ])
    caixa("Cortina", (x + 0.06, y + 0.02, z - lado / 2 - 0.2), (0.05, lado + 0.4, 0.28), m["cortina"])


def estante(m):
    """Estante no canto do fundo, à esquerda: laterais, fundo, cinco prateleiras
    e livros de alturas e cores sorteadas (semente fixa: sai sempre igual)."""
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
        partes.append(caixa("Prateleira", (x, y, z), (largura - 0.04, 0.03, fundo - 0.02), m["madeira"]))
    juntar("Estante", partes)

    cores = ["livro_verde", "livro_vinho", "livro_azul", "livro_bege", "livro_cinza"]
    livros = []
    for y in prateleiras[:-1]:
        xi = x - largura / 2 + 0.05
        limite = x + largura / 2 - 0.05 - sorteio.uniform(0.0, 0.25)
        while xi < limite:
            esp = sorteio.uniform(0.025, 0.05)
            alt = sorteio.uniform(0.22, 0.32)
            livros.append(caixa("Livro", (xi + esp / 2, y + 0.015 + alt / 2, z + 0.02), (esp, alt, 0.24), m[sorteio.choice(cores)]))
            xi += esp + 0.004
    juntar("LivrosDaEstante", livros)


def cama(m):
    """Cama de solteiro encostada na parede da direita, com a cabeceira no lado
    do fundo: estrado, colchão, travesseiro, cobertor amarrotado e cabeceira.
    Do lado da porta, o criado-mudo e a mochila verde no chão."""
    x = MEIA - 0.5
    z_cabeca, z_pe = -1.35, 0.75
    z = (z_cabeca + z_pe) / 2
    comprimento = z_pe - z_cabeca
    juntar("Cama", [
        caixa("Estrado", (x, 0.15, z), (1.0, 0.3, comprimento), m["madeira"]),
        caixa("Cabeceira", (x, 0.45, z_cabeca - 0.03), (1.0, 0.9, 0.06), m["madeira"]),
        caixa("Colchao", (x, 0.4, z), (0.94, 0.2, comprimento - 0.06), m["lencol"]),
        caixa("Travesseiro", (x + 0.05, 0.55, z_cabeca + 0.25), (0.6, 0.1, 0.32), m["lencol"], giro_y=-6),
        caixa("Cobertor", (x - 0.02, 0.52, z + 0.35), (0.98, 0.05, comprimento - 0.7), m["cobertor"]),
        caixa("Dobra", (x - 0.1, 0.56, z - 0.05), (0.8, 0.05, 0.25), m["cobertor"], giro_y=10),
    ])
    juntar("CriadoMudo", [
        caixa("CorpoCriado", (MEIA - 0.25, 0.25, 1.15), (0.42, 0.5, 0.42), m["madeira"]),
        caixa("PuxadorCriado", (MEIA - 0.47, 0.38, 1.15), (0.01, 0.02, 0.12), m["metal"]),
    ])
    juntar("Mochila", [
        caixa("CorpoMochila", (1.25, 0.21, 1.25), (0.34, 0.42, 0.2), m["mochila"], giro_y=25),
        caixa("BolsoMochila", (1.2, 0.14, 1.36), (0.24, 0.18, 0.06), m["mochila_escura"], giro_y=25),
    ])


def porta(m):
    """Porta do quarto na parede da frente (atrás de quem entra) e o interruptor."""
    x = -1.5
    z = MEIA - 0.02
    juntar("Porta", [
        caixa("Batente", (x, 1.05, z + 0.005), (1.0, 2.1, 0.03), m["madeira_escura"]),
        caixa("Folha", (x, 1.02, z - 0.02), (0.86, 2.03, 0.04), m["porta"]),
        caixa("Macaneta", (x + 0.33, 1.0, z - 0.05), (0.1, 0.02, 0.03), m["metal"]),
    ])
    caixa("Interruptor", (x + 0.7, 1.15, z - 0.005), (0.07, 0.11, 0.01), m["lencol"])


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
    }

    quarto(m)
    movel_da_tv(m)
    tv(m)
    tela(m)
    mural(m)
    quadro_branco(m)
    escrivaninha(m)
    cadeira(m)
    janela(m)
    estante(m)
    cama(m)
    porta(m)

    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=SAIDA, export_format="GLB", export_apply=True)
    print("Modelo salvo em", SAIDA)


main()

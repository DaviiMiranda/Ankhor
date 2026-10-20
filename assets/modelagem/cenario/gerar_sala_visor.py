# gerar_sala_visor.py — modela no Blender a sala 3D que o Gabriel vê quando põe
# os óculos do Zane na sala segura (docs/mecanicas/visor_3d.md): uma sala-caixa
# escura com uma grade ciano no chão, um móvel baixo e, em cima dele, uma TV de
# tubo com antena. A tela da TV é um objeto separado ("Tela"), um retângulo com
# UV de 0 a 1: no Godot ele recebe o menu de salvar como textura.
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
# EIXOS
# ---------------------------------------------------------------------------
#
# O Blender usa Z para cima; o glTF e o Godot usam Y para cima. O exportador
# converte sozinho:
#
#     Blender (x, y, z)  ->  Godot (x, z, -y)
#
# Então o fundo da sala no Blender (y positivo) vira o fundo no Godot (z
# negativo), que é para onde a câmera do Godot olha quando não está girada
# (o eixo -Z). A TV fica encostada nesse fundo, de frente para o jogador.
#
# Todas as medidas estão em metros. As que o Godot também precisa saber
# (tamanho da sala, posição da TV) estão repetidas em cenas/visor/sala_visor.tscn,
# nas formas de colisão. Se mudar aqui, mude lá.

import math
import os

import bpy

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
SAIDA = os.path.join(PASTA_PROJETO, "assets", "modelos", "sala_visor.glb")

# Sala: 5 m x 5 m, 2,8 m de pé-direito, centrada na origem.
LARGURA_SALA = 5.0
PROFUNDIDADE_SALA = 5.0
ALTURA_SALA = 2.8

# Grade do chão: uma linha a cada 0,5 m, finas, com brilho próprio.
PASSO_GRADE = 0.5
ESPESSURA_LINHA = 0.02

# Móvel da TV, encostado no fundo (y positivo no Blender).
MOVEL_LARGURA = 1.0
MOVEL_PROFUNDIDADE = 0.5
MOVEL_ALTURA = 0.6
MOVEL_Y = 1.9

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


def caixa(nome, centro, tamanho, mat):
    """Cubo com o centro e o tamanho (largura x, profundidade y, altura z) dados,
    com a escala já aplicada (o glTF sai com medidas reais, sem escala no nó)."""
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=centro)
    obj = bpy.context.active_object
    obj.name = nome
    obj.scale = tamanho
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat)
    return obj


def juntar(nome, objetos):
    """Junta vários objetos num só (menos nós no Godot)."""
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


def sala(mat_chao, mat_parede, mat_teto):
    """A caixa da sala vista por dentro: chão, teto e cada parede são placas de
    10 cm do lado de FORA do volume da sala. Assim a face de cada placa virada
    para dentro já tem a normal apontando para o jogador, sem inverter nada."""
    meia_l = LARGURA_SALA / 2
    meia_p = PROFUNDIDADE_SALA / 2
    chao = caixa("Chao", (0, 0, -0.05), (LARGURA_SALA, PROFUNDIDADE_SALA, 0.1), mat_chao)
    teto = caixa("Teto", (0, 0, ALTURA_SALA + 0.05), (LARGURA_SALA, PROFUNDIDADE_SALA, 0.1), mat_teto)
    meio = ALTURA_SALA / 2
    paredes = juntar("Paredes", [
        caixa("ParedeFundo", (0, meia_p + 0.05, meio), (LARGURA_SALA, 0.1, ALTURA_SALA), mat_parede),
        caixa("ParedeFrente", (0, -meia_p - 0.05, meio), (LARGURA_SALA, 0.1, ALTURA_SALA), mat_parede),
        caixa("ParedeEsquerda", (-meia_l - 0.05, 0, meio), (0.1, PROFUNDIDADE_SALA, ALTURA_SALA), mat_parede),
        caixa("ParedeDireita", (meia_l + 0.05, 0, meio), (0.1, PROFUNDIDADE_SALA, ALTURA_SALA), mat_parede),
    ])
    return chao, teto, paredes


def grade(mat_linha):
    """Linhas finas no chão, de parede a parede, nos dois sentidos. Ficam 1 mm
    acima do chão para não brigar com ele na hora de desenhar (z-fighting)."""
    linhas = []
    quantas_x = int(LARGURA_SALA / PASSO_GRADE) + 1
    quantas_y = int(PROFUNDIDADE_SALA / PASSO_GRADE) + 1
    for i in range(quantas_x):
        x = -LARGURA_SALA / 2 + i * PASSO_GRADE
        linhas.append(caixa("LinhaX", (x, 0, 0.001), (ESPESSURA_LINHA, PROFUNDIDADE_SALA, 0.002), mat_linha))
    for j in range(quantas_y):
        y = -PROFUNDIDADE_SALA / 2 + j * PASSO_GRADE
        linhas.append(caixa("LinhaY", (0, y, 0.001), (LARGURA_SALA, ESPESSURA_LINHA, 0.002), mat_linha))
    rodape = []
    meia_l = LARGURA_SALA / 2 - 0.01
    meia_p = PROFUNDIDADE_SALA / 2 - 0.01
    for centro, tamanho in [
        ((0, meia_p, 0.08), (LARGURA_SALA, 0.02, 0.02)),
        ((0, -meia_p, 0.08), (LARGURA_SALA, 0.02, 0.02)),
        ((-meia_l, 0, 0.08), (0.02, PROFUNDIDADE_SALA, 0.02)),
        ((meia_l, 0, 0.08), (0.02, PROFUNDIDADE_SALA, 0.02)),
    ]:
        rodape.append(caixa("Rodape", centro, tamanho, mat_linha))
    return juntar("Grade", linhas + rodape)


def movel(mat_movel, mat_detalhe):
    """Móvel baixo: um tampo, o corpo e dois pés na frente."""
    partes = [
        caixa("Corpo", (0, MOVEL_Y, MOVEL_ALTURA / 2 + 0.04), (MOVEL_LARGURA - 0.04, MOVEL_PROFUNDIDADE - 0.04, MOVEL_ALTURA - 0.12), mat_movel),
        caixa("Tampo", (0, MOVEL_Y, MOVEL_ALTURA - 0.02), (MOVEL_LARGURA, MOVEL_PROFUNDIDADE, 0.04), mat_movel),
        caixa("Gaveta", (0, MOVEL_Y - MOVEL_PROFUNDIDADE / 2 + 0.015, MOVEL_ALTURA / 2), (MOVEL_LARGURA * 0.8, 0.01, 0.02), mat_detalhe),
    ]
    for x in (-MOVEL_LARGURA / 2 + 0.06, MOVEL_LARGURA / 2 - 0.06):
        for y in (MOVEL_Y - MOVEL_PROFUNDIDADE / 2 + 0.06, MOVEL_Y + MOVEL_PROFUNDIDADE / 2 - 0.06):
            partes.append(caixa("Pe", (x, y, 0.02), (0.05, 0.05, 0.04), mat_detalhe))
    return juntar("Movel", partes)


def frente_da_tv():
    """y da face da frente do corpo da TV (o lado que olha para o jogador)."""
    return MOVEL_Y - TV_PROFUNDIDADE / 2


def centro_da_tela():
    base = MOVEL_ALTURA
    return (0.0, frente_da_tv() - 0.003, base + TV_ALTURA / 2 + TELA_SUBIDA)


def tv(mat_corpo, mat_moldura, mat_botao, mat_antena, mat_led):
    """Corpo da TV, traseira mais estreita, moldura funda em volta da tela,
    dois botões, uma luzinha e a antena em V (duas varetas inclinadas)."""
    base = MOVEL_ALTURA
    _, y_tela, z_tela = centro_da_tela()
    partes = [
        caixa("Corpo", (0, MOVEL_Y, base + TV_ALTURA / 2), (TV_LARGURA, TV_PROFUNDIDADE, TV_ALTURA), mat_corpo),
        caixa("Traseira", (0, MOVEL_Y + TV_PROFUNDIDADE / 2 + TRASEIRA_PROFUNDIDADE / 2, base + TV_ALTURA / 2),
              (TRASEIRA_LARGURA, TRASEIRA_PROFUNDIDADE, TRASEIRA_ALTURA), mat_corpo),
    ]
    # Moldura: quatro barras em volta da tela, saindo um pouco da frente.
    borda = 0.025
    y_moldura = frente_da_tv() - 0.006
    partes += [
        caixa("MolduraCima", (0, y_moldura, z_tela + TELA_ALTURA / 2 + borda / 2), (TELA_LARGURA + 2 * borda, 0.012, borda), mat_moldura),
        caixa("MolduraBaixo", (0, y_moldura, z_tela - TELA_ALTURA / 2 - borda / 2), (TELA_LARGURA + 2 * borda, 0.012, borda), mat_moldura),
        caixa("MolduraEsq", (-TELA_LARGURA / 2 - borda / 2, y_moldura, z_tela), (borda, 0.012, TELA_ALTURA), mat_moldura),
        caixa("MolduraDir", (TELA_LARGURA / 2 + borda / 2, y_moldura, z_tela), (borda, 0.012, TELA_ALTURA), mat_moldura),
    ]
    z_botoes = base + 0.045
    for x in (0.18, 0.24):
        partes.append(caixa("Botao", (x, frente_da_tv() - 0.008, z_botoes), (0.035, 0.016, 0.035), mat_botao))
    corpo = juntar("TV", partes)

    led = caixa("Led", (-0.24, frente_da_tv() - 0.004, z_botoes), (0.012, 0.008, 0.012), mat_led)

    # Antena: cilindros finos saindo do topo, abertos em V (35 graus para cada lado).
    varetas = []
    topo = base + TV_ALTURA
    comprimento = 0.45
    for lado in (-1, 1):
        angulo = math.radians(35) * lado
        bpy.ops.mesh.primitive_cylinder_add(radius=0.004, depth=comprimento, vertices=8)
        vareta = bpy.context.active_object
        vareta.rotation_euler = (0, angulo, 0)
        # O cilindro nasce centrado; anda meia vareta ao longo da própria inclinação.
        vareta.location = (math.sin(angulo) * comprimento / 2, MOVEL_Y + 0.05, topo + math.cos(angulo) * comprimento / 2)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        vareta.data.materials.append(mat_antena)
        varetas.append(vareta)
    varetas.append(caixa("BaseAntena", (0, MOVEL_Y + 0.05, topo + 0.01), (0.08, 0.05, 0.02), mat_corpo))
    antena = juntar("Antena", varetas)
    return corpo, led, antena


def tela(mat_tela):
    """A tela é um plano 4:3. O plano do Blender nasce deitado (normal +Z) com o
    UV cobrindo de 0 a 1; girar 90 graus em X deixa a normal em -Y (de frente
    para o jogador), com o "para cima" da textura apontando para +Z. Visto de
    frente, u cresce para a direita e v para cima: a imagem não sai espelhada."""
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=centro_da_tela())
    obj = bpy.context.active_object
    obj.name = "Tela"
    obj.rotation_euler = (math.radians(90), 0, 0)
    obj.scale = (TELA_LARGURA, TELA_ALTURA, 1.0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    obj.data.materials.append(mat_tela)
    return obj


def main():
    limpar_cena()
    mat_chao = material("Chao", "#0b1018", rugosidade=0.6)
    mat_parede = material("Parede", "#141b26", rugosidade=0.9)
    mat_teto = material("Teto", "#0a0e15", rugosidade=0.9)
    mat_linha = material("LinhaCiano", "#1c6f80", brilho="#3fd8f0", forca_brilho=1.2)
    mat_movel = material("Movel", "#3a2f2a", rugosidade=0.7)
    mat_detalhe = material("Detalhe", "#1d1a19", rugosidade=0.5)
    mat_corpo = material("CorpoTV", "#4a4640", rugosidade=0.6)
    mat_moldura = material("MolduraTV", "#1c1c20", rugosidade=0.4)
    mat_botao = material("BotaoTV", "#2a2a2e", rugosidade=0.4)
    mat_antena = material("Antena", "#9aa0a8", rugosidade=0.3)
    mat_led = material("Led", "#c8d84a", brilho="#e4f25a", forca_brilho=2.0)
    mat_tela = material("Tela", "#05080c", rugosidade=0.2)

    sala(mat_chao, mat_parede, mat_teto)
    grade(mat_linha)
    movel(mat_movel, mat_detalhe)
    tv(mat_corpo, mat_moldura, mat_botao, mat_antena, mat_led)
    tela(mat_tela)

    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=SAIDA, export_format="GLB", export_apply=True)
    print("Modelo salvo em", SAIDA)


main()

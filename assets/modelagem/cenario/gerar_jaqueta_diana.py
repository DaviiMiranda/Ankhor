# gerar_jaqueta_diana.py — modela no Blender a JAQUETA DA DIANA, que aparece
# jogada na cama do Gabriel, no quarto do visor 3D, quando ele junta os três
# botões do Centro de Convivência (docs/mecanicas/colecionaveis.md).
#
# O desenho segue o visual da Diana (assets/sprites/personagens/diana/visual.md):
# jaqueta marrom-caramelo de gola larga, com bolsos no peito e no quadril e os
# punhos dobrados, aberta sobre a camiseta listrada em amarelo, laranja e creme.
# Está deitada de frente para cima, com as mangas abertas para os lados, e os
# três botões de couro com aro dourado fecham a frente.
#
# Como rodar (sem abrir a janela do Blender):
#
#   blender -b --factory-startup --python assets/modelagem/cenario/gerar_jaqueta_diana.py
#
# O que sai:
#   assets/modelos/jaqueta_diana.glb   o modelo em glTF binário, com o pé no
#                                      chão (y = 0) e centrado em x e z
#
# A jaqueta fica no plano x-y do Blender (x é a largura, y o comprimento, com a
# gola em +y) e tem 3,5 cm de espessura. No Godot, a gola aponta para -Z.
#
# EIXOS: o Blender usa Z para cima e o Godot usa Y; o exportador troca sozinho
# (Godot (x, y, z) = Blender (x, z, -y)). Medidas em metros.

import math
import os

import bpy

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
SAIDA = os.path.join(PASTA_PROJETO, "assets", "modelos", "jaqueta_diana.glb")

ESPESSURA = 0.035
PAINEL_LARGURA = 0.21
PAINEL_COMPRIMENTO = 0.62
ABERTURA = 0.08
OMBRO_X = (PAINEL_LARGURA * 2 + ABERTURA) / 2
OMBRO_Y = PAINEL_COMPRIMENTO / 2 - 0.02
MANGA_COMPRIMENTO = 0.56
MANGA_LARGURA = 0.16
MANGA_ANGULO = 38.0
PUNHO_COMPRIMENTO = 0.06
LISTRAS = 7


def cor(hexa):
    hexa = hexa.lstrip("#")
    return tuple(int(hexa[i:i + 2], 16) / 255 for i in (0, 2, 4)) + (1.0,)


def material(nome, cor_base, rugosidade=0.85, metalico=0.0):
    mat = bpy.data.materials.new(nome)
    mat.use_nodes = True
    no = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    no.inputs["Base Color"].default_value = cor(cor_base)
    no.inputs["Roughness"].default_value = rugosidade
    no.inputs["Metallic"].default_value = metalico
    return mat


def caixa(nome, centro, tamanho, mat, giro_graus=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=centro)
    obj = bpy.context.active_object
    obj.name = nome
    obj.scale = tamanho
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.rotation_euler = (0.0, 0.0, math.radians(giro_graus))
    obj.data.materials.append(mat)
    return obj


def juntar(nome, objetos):
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


def manga(lado, corpo, punho):
    """Uma manga deitada, saindo do ombro para fora e para baixo. 'lado' é -1
    (esquerda) ou 1 (direita). A direção do comprimento é (lado·sen a, -cos a)."""
    angulo = math.radians(MANGA_ANGULO)
    direcao = (lado * math.sin(angulo), -math.cos(angulo))
    giro = math.degrees(math.atan2(-direcao[0], direcao[1]))
    inicio = (lado * OMBRO_X, OMBRO_Y)
    centro = (inicio[0] + direcao[0] * MANGA_COMPRIMENTO / 2, inicio[1] + direcao[1] * MANGA_COMPRIMENTO / 2)
    ponta = (inicio[0] + direcao[0] * (MANGA_COMPRIMENTO - PUNHO_COMPRIMENTO / 2),
             inicio[1] + direcao[1] * (MANGA_COMPRIMENTO - PUNHO_COMPRIMENTO / 2))
    return [
        caixa("Manga%d" % lado, (centro[0], centro[1], ESPESSURA * 0.4), (MANGA_LARGURA, MANGA_COMPRIMENTO, ESPESSURA * 0.8), corpo, giro),
        caixa("Punho%d" % lado, (ponta[0], ponta[1], ESPESSURA * 0.5), (MANGA_LARGURA + 0.01, PUNHO_COMPRIMENTO, ESPESSURA), punho, giro),
    ]


def main():
    limpar_cena()
    corpo = material("Caramelo", "#b0702a")
    claro = material("CarameloClaro", "#c58238")
    escuro = material("CarameloEscuro", "#7a4818")
    bolso = material("Bolso", "#9a5e22")
    latao = material("Latao", "#e0b040", rugosidade=0.4, metalico=0.6)
    listras = [material("ListraAmarela", "#e8b830"), material("ListraLaranja", "#d9742c"), material("ListraCreme", "#f0e2c0")]

    pecas = []
    for lado in (-1, 1):
        pecas.append(caixa("Painel%d" % lado, (lado * (ABERTURA / 2 + PAINEL_LARGURA / 2), 0.0, ESPESSURA / 2),
                           (PAINEL_LARGURA, PAINEL_COMPRIMENTO, ESPESSURA), corpo))
        pecas += manga(lado, corpo, escuro)
        pecas.append(caixa("Gola%d" % lado, (lado * 0.075, PAINEL_COMPRIMENTO / 2 + 0.01, ESPESSURA + 0.005),
                           (0.13, 0.12, 0.012), claro, -lado * 28.0))
        pecas.append(caixa("BolsoPeito%d" % lado, (lado * 0.145, 0.12, ESPESSURA + 0.004), (0.09, 0.08, 0.008), bolso))
        pecas.append(caixa("BolsoQuadril%d" % lado, (lado * 0.145, -0.2, ESPESSURA + 0.004), (0.12, 0.09, 0.008), bolso))

    altura_da_camiseta = ESPESSURA * 0.7
    pecas.append(caixa("Camiseta", (0.0, 0.0, altura_da_camiseta / 2), (ABERTURA + 0.02, PAINEL_COMPRIMENTO - 0.02, altura_da_camiseta), listras[2]))
    faixa = (PAINEL_COMPRIMENTO - 0.04) / LISTRAS
    for i in range(LISTRAS):
        y = PAINEL_COMPRIMENTO / 2 - 0.02 - faixa * (i + 0.5)
        pecas.append(caixa("Listra%d" % i, (0.0, y, altura_da_camiseta + 0.0005), (ABERTURA, faixa * 0.55, 0.001), listras[i % 2]))

    for i, y in enumerate((0.2, 0.0, -0.2)):
        bpy.ops.mesh.primitive_cylinder_add(vertices=14, radius=0.013, depth=0.008,
                                            location=(-ABERTURA / 2 - 0.02, y, ESPESSURA + 0.004))
        botao = bpy.context.active_object
        botao.name = "Botao%d" % i
        botao.data.materials.append(latao)
        pecas.append(botao)

    juntar("Jaqueta", pecas)

    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=SAIDA, export_format="GLB", export_apply=True)
    print("Modelo salvo em", SAIDA)


main()

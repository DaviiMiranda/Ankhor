# gerar_oculos_zane.py — modela no Blender os ÓCULOS DO ZANE, que aparecem no
# criado-mudo do Gabriel, no quarto do visor 3D, quando ele junta os três chips
# do Bunker (docs/mecanicas/colecionaveis.md).
#
# O desenho segue o visual do Zane (assets/sprites/personagens/zane/visual.md):
# um visor que cobre os dois olhos, de armação grafite escuro e lente verde que
# brilha, e a luz ciano-verde da interface dele. Na armação, os três chips
# hexagonais (o hexágono do peito da jaqueta dele), cada um aceso. Estão em pé,
# apoiados nas hastes abertas, com a lente virada para +y.
#
# Como rodar (sem abrir a janela do Blender):
#
#   blender -b --factory-startup --python assets/modelagem/cenario/gerar_oculos_zane.py
#
# O que sai:
#   assets/modelos/oculos_zane.glb   o modelo em glTF binário, com o pé no chão
#                                    (y = 0) e centrado em x e z
#
# A lente e os chips têm material com brilho próprio (como os raios do farol),
# então o glow do quarto os transforma em halo.
#
# EIXOS: o Blender usa Z para cima e o Godot usa Y; o exportador troca sozinho
# (Godot (x, y, z) = Blender (x, z, -y)). No Godot, a lente aponta para -Z.
# Medidas em metros.

import math
import os

import bpy

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
SAIDA = os.path.join(PASTA_PROJETO, "assets", "modelos", "oculos_zane.glb")

ARMACAO_LARGURA = 0.15
ARMACAO_ALTURA = 0.042
ARMACAO_PROFUNDIDADE = 0.022
LENTE_LARGURA = 0.136
LENTE_ALTURA = 0.022
HASTE_COMPRIMENTO = 0.13
HASTE_ESPESSURA = 0.006
HASTE_ALTURA = 0.014
CHIP_RAIO = 0.0085
CHIP_ESPESSURA = 0.003
CHIPS_X = (-0.054, 0.0, 0.054)


def cor(hexa):
    hexa = hexa.lstrip("#")
    return tuple(int(hexa[i:i + 2], 16) / 255 for i in (0, 2, 4)) + (1.0,)


def material(nome, cor_base, rugosidade=0.5, metalico=0.0, brilho=None, forca_brilho=1.0):
    mat = bpy.data.materials.new(nome)
    mat.use_nodes = True
    no = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    no.inputs["Base Color"].default_value = cor(cor_base)
    no.inputs["Roughness"].default_value = rugosidade
    no.inputs["Metallic"].default_value = metalico
    if brilho:
        no.inputs["Emission Color"].default_value = cor(brilho)
        no.inputs["Emission Strength"].default_value = forca_brilho
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


def chip(indice, x, mat):
    """Um chip hexagonal deitado na face da frente da armação, no meio da
    borda de cima (um cilindro de 6 lados virado para +y)."""
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=6, radius=CHIP_RAIO, depth=CHIP_ESPESSURA,
        location=(x, ARMACAO_PROFUNDIDADE / 2 + CHIP_ESPESSURA / 2, ARMACAO_ALTURA - 0.007),
        rotation=(math.pi / 2, 0.0, 0.0))
    obj = bpy.context.active_object
    obj.name = "Chip%d" % indice
    obj.data.materials.append(mat)
    return obj


def main():
    limpar_cena()
    grafite = material("Grafite", "#22262a", rugosidade=0.45, metalico=0.3)
    cinza = material("Cinza", "#4a5258", rugosidade=0.5, metalico=0.3)
    lente = material("Lente", "#16a070", rugosidade=0.15, brilho="#2bffb0", forca_brilho=2.4)
    luz = material("LuzDoChip", "#7affe0", rugosidade=0.2, brilho="#3fe0c0", forca_brilho=4.0)

    pecas = [
        caixa("Armacao", (0, 0, ARMACAO_ALTURA / 2), (ARMACAO_LARGURA, ARMACAO_PROFUNDIDADE, ARMACAO_ALTURA), grafite),
        caixa("Lente", (0, ARMACAO_PROFUNDIDADE / 2 + 0.0008, ARMACAO_ALTURA * 0.4), (LENTE_LARGURA, 0.002, LENTE_ALTURA), lente),
        caixa("BordaDeCima", (0, ARMACAO_PROFUNDIDADE / 2 + 0.0015, ARMACAO_ALTURA - 0.002), (ARMACAO_LARGURA, 0.003, 0.004), cinza),
    ]
    for lado in (-1, 1):
        pecas.append(caixa("Haste%d" % lado,
                           (lado * (ARMACAO_LARGURA / 2 - HASTE_ESPESSURA / 2), -ARMACAO_PROFUNDIDADE / 2 - HASTE_COMPRIMENTO / 2 + 0.004, HASTE_ALTURA / 2),
                           (HASTE_ESPESSURA, HASTE_COMPRIMENTO, HASTE_ALTURA), grafite, -lado * 4.0))
    for i, x in enumerate(CHIPS_X):
        pecas.append(chip(i, x, luz))
    juntar("Oculos", pecas)

    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=SAIDA, export_format="GLB", export_apply=True)
    print("Modelo salvo em", SAIDA)


main()

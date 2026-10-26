# gerar_farol_mesa.py — modela no Blender o FAROL que aparece na mesa do Gabriel
# no quarto do visor 3D quando ele junta os três pingentes da Biblioteca
# (docs/mecanicas/colecionaveis.md).
#
# É o símbolo dos Faroleiros (Enredo Principal, seção 2.4) em 3D, do tamanho de
# um enfeite de mesa (18 cm de altura): a torre mais larga na base, a lanterna
# acesa no topo e os três raios saindo dela para cima, em leque. A cor é o
# âmbar, a luz quente de uma chama.
#
# Como rodar (sem abrir a janela do Blender):
#
#   blender -b --factory-startup --python assets/modelagem/cenario/gerar_farol_mesa.py
#
# O que sai:
#   assets/modelos/farol_mesa.glb   o modelo em glTF binário, com o pé no
#                                   chão (y = 0) e centrado em x e z
#
# O leque dos raios fica no plano x-y do Godot, de frente para +Z. A cena
# (cenas/visor/farol_da_mesa.tscn) gira o modelo para ele olhar para a cadeira.
#
# EIXOS: o Blender usa Z para cima e o Godot usa Y; o exportador troca sozinho
# (Godot (x, y, z) = Blender (x, z, -y)). Aqui tudo é escrito direto em
# coordenadas do Blender, com o leque no plano x-z (Blender), que vira o plano
# x-y no Godot. Medidas em metros.

import math
import os

import bpy

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
SAIDA = os.path.join(PASTA_PROJETO, "assets", "modelos", "farol_mesa.glb")

BASE_RAIO = 0.055
BASE_ALTURA = 0.012
TORRE_RAIO_BAIXO = 0.034
TORRE_RAIO_TOPO = 0.019
TORRE_ALTURA = 0.108
FAIXAS = 4
GALERIA_RAIO = 0.031
GALERIA_ALTURA = 0.006
LANTERNA_RAIO = 0.017
LANTERNA_ALTURA = 0.034
TELHADO_RAIO = 0.023
TELHADO_ALTURA = 0.026
RAIO_COMPRIMENTO = 0.075
RAIO_ESPESSURA = 0.0045
RAIO_AFASTAMENTO = 0.03
ANGULOS_DOS_RAIOS = (-42.0, 0.0, 42.0)


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


def tronco(nome, z_base, altura, raio_baixo, raio_topo, mat, lados=10):
    bpy.ops.mesh.primitive_cone_add(
        vertices=lados, radius1=raio_baixo, radius2=raio_topo, depth=altura,
        location=(0, 0, z_base + altura / 2))
    obj = bpy.context.active_object
    obj.name = nome
    obj.data.materials.append(mat)
    return obj


def raio(nome, angulo, z_inicio, mat):
    direcao = (math.sin(math.radians(angulo)), 0.0, math.cos(math.radians(angulo)))
    meio = RAIO_AFASTAMENTO + RAIO_COMPRIMENTO / 2
    bpy.ops.mesh.primitive_cone_add(
        vertices=6, radius1=RAIO_ESPESSURA, radius2=RAIO_ESPESSURA * 0.3, depth=RAIO_COMPRIMENTO,
        location=(direcao[0] * meio, 0.0, z_inicio + direcao[2] * meio))
    obj = bpy.context.active_object
    obj.name = nome
    obj.rotation_euler = (0.0, math.radians(angulo), 0.0)
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


def main():
    limpar_cena()
    latao = material("Latao", "#e39a32", rugosidade=0.45, metalico=0.1)
    latao_escuro = material("LataoEscuro", "#7a4510", rugosidade=0.5, metalico=0.1)
    ferro = material("Ferro", "#2a1704", rugosidade=0.6, metalico=0.2)
    vidro = material("VidroAceso", "#f2b04a", rugosidade=0.2, brilho="#ff9a2e", forca_brilho=2.6)
    feixe = material("Raio", "#ffb347", rugosidade=0.2, brilho="#ff9f2a", forca_brilho=3.2)

    tronco("Base", 0.0, BASE_ALTURA, BASE_RAIO, BASE_RAIO * 0.94, ferro, lados=16)

    faixa_altura = TORRE_ALTURA / FAIXAS
    faixas = []
    for i in range(FAIXAS):
        raio_a = TORRE_RAIO_BAIXO + (TORRE_RAIO_TOPO - TORRE_RAIO_BAIXO) * i / FAIXAS
        raio_b = TORRE_RAIO_BAIXO + (TORRE_RAIO_TOPO - TORRE_RAIO_BAIXO) * (i + 1) / FAIXAS
        faixas.append(tronco("Faixa%d" % i, BASE_ALTURA + i * faixa_altura, faixa_altura,
                             raio_a, raio_b, latao if i % 2 == 0 else latao_escuro))
    topo_da_torre = BASE_ALTURA + TORRE_ALTURA

    galeria = tronco("Galeria", topo_da_torre, GALERIA_ALTURA, GALERIA_RAIO, GALERIA_RAIO, ferro, lados=10)
    lanterna_z = topo_da_torre + GALERIA_ALTURA
    lanterna = tronco("Lanterna", lanterna_z, LANTERNA_ALTURA, LANTERNA_RAIO, LANTERNA_RAIO, vidro, lados=10)
    colunas = []
    for i in range(4):
        angulo = math.radians(45 + 90 * i)
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            location=(math.cos(angulo) * LANTERNA_RAIO, math.sin(angulo) * LANTERNA_RAIO, lanterna_z + LANTERNA_ALTURA / 2))
        coluna = bpy.context.active_object
        coluna.name = "Coluna%d" % i
        coluna.scale = (0.004, 0.004, LANTERNA_ALTURA)
        coluna.rotation_euler = (0, 0, angulo)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        coluna.data.materials.append(ferro)
        colunas.append(coluna)
    telhado_z = lanterna_z + LANTERNA_ALTURA
    telhado = tronco("Telhado", telhado_z, TELHADO_ALTURA, TELHADO_RAIO, 0.004, latao_escuro, lados=10)

    ponta_do_telhado = telhado_z + TELHADO_ALTURA * 0.55
    raios = [raio("Raio%d" % i, angulo, ponta_do_telhado, feixe) for i, angulo in enumerate(ANGULOS_DOS_RAIOS)]

    base = bpy.data.objects["Base"]
    juntar("Torre", [base] + faixas + [galeria, telhado] + colunas)
    juntar("Raios", raios)

    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=SAIDA, export_format="GLB", export_apply=True)
    print("Modelo salvo em", SAIDA)


main()

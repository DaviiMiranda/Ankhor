# gerar_disquetes_criado.py — modela no Blender a PILHA DE DISQUETES que
# aparece no criado-mudo do Gabriel, no quarto do visor 3D, quando ele junta os
# três disquetes do Bloco de salas (docs/mecanicas/colecionaveis.md).
#
# São três disquetes de 3,5" (9 x 9,4 cm, 3 mm de espessura) jogados um sobre o
# outro, girados de leve, como quem largou ali: corpo preto, obturador de metal
# com a janelinha escura e a etiqueta de papel com os adesivos da Clarice, o
# rosa e o amarelo (assets/sprites/personagens/clarice/visual.md). Cada
# disquete tem uma combinação de adesivos para a pilha não parecer clonada.
#
# Como rodar (sem abrir a janela do Blender):
#
#   blender -b --factory-startup --python assets/modelagem/cenario/gerar_disquetes_criado.py
#
# O que sai:
#   assets/modelos/disquetes_criado.glb   o modelo em glTF binário, com o pé no
#                                         chão (y = 0) e centrado em x e z
#
# EIXOS: o Blender usa Z para cima e o Godot usa Y; o exportador troca sozinho
# (Godot (x, y, z) = Blender (x, z, -y)). Aqui tudo é escrito direto em
# coordenadas do Blender. Medidas em metros.

import math
import os

import bpy

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
SAIDA = os.path.join(PASTA_PROJETO, "assets", "modelos", "disquetes_criado.glb")

LADO = 0.090
PROFUNDIDADE = 0.094
ESPESSURA = 0.0032
FOLGA_ENTRE_DISQUETES = 0.0016
OBTURADOR_LARGURA = 0.046
OBTURADOR_PROFUNDIDADE = 0.030
JANELA_LARGURA = 0.011
JANELA_PROFUNDIDADE = 0.020
ETIQUETA_LARGURA = 0.072
ETIQUETA_PROFUNDIDADE = 0.034
ADESIVO = 0.016
FINO = 0.0003

DISQUETES = (
    {"giro": 0.0, "dx": 0.0, "dy": 0.0, "adesivos": ("rosa",)},
    {"giro": 17.0, "dx": 0.006, "dy": -0.004, "adesivos": ("amarelo",)},
    {"giro": -11.0, "dx": -0.004, "dy": 0.005, "adesivos": ("rosa", "amarelo")},
)


def cor(hexa):
    hexa = hexa.lstrip("#")
    return tuple(int(hexa[i:i + 2], 16) / 255 for i in (0, 2, 4)) + (1.0,)


def material(nome, cor_base, rugosidade=0.5, metalico=0.0):
    mat = bpy.data.materials.new(nome)
    mat.use_nodes = True
    no = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    no.inputs["Base Color"].default_value = cor(cor_base)
    no.inputs["Roughness"].default_value = rugosidade
    no.inputs["Metallic"].default_value = metalico
    return mat


def caixa(nome, centro, tamanho, mat):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=centro)
    obj = bpy.context.active_object
    obj.name = nome
    obj.scale = tamanho
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
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


def disquete(indice, dados, materiais):
    base = indice * (ESPESSURA + FOLGA_ENTRE_DISQUETES)
    topo = base + ESPESSURA
    frente = PROFUNDIDADE / 2
    fundo = -PROFUNDIDADE / 2
    obturador_y = frente - OBTURADOR_PROFUNDIDADE / 2 - 0.004
    etiqueta_y = fundo + ETIQUETA_PROFUNDIDADE / 2 + 0.006
    partes = [
        caixa("Corpo%d" % indice, (0, 0, base + ESPESSURA / 2), (LADO, PROFUNDIDADE, ESPESSURA), materiais["corpo"]),
        caixa("Obturador%d" % indice, (0, obturador_y, topo + FINO),
              (OBTURADOR_LARGURA, OBTURADOR_PROFUNDIDADE, FINO * 2), materiais["metal"]),
        caixa("Janela%d" % indice, (OBTURADOR_LARGURA / 2 - JANELA_LARGURA, obturador_y, topo + FINO * 3),
              (JANELA_LARGURA, JANELA_PROFUNDIDADE, FINO * 2), materiais["janela"]),
        caixa("Etiqueta%d" % indice, (0, etiqueta_y, topo + FINO),
              (ETIQUETA_LARGURA, ETIQUETA_PROFUNDIDADE, FINO * 2), materiais["papel"]),
        caixa("Pauta%d" % indice, (0, etiqueta_y - ETIQUETA_PROFUNDIDADE * 0.18, topo + FINO * 3),
              (ETIQUETA_LARGURA * 0.7, 0.0012, FINO * 2), materiais["caneta"]),
    ]
    lados = {
        "rosa": -ETIQUETA_LARGURA / 2 + ADESIVO / 2 + 0.004,
        "amarelo": ETIQUETA_LARGURA / 2 - ADESIVO / 2 - 0.004,
    }
    for nome in dados["adesivos"]:
        partes.append(caixa("Adesivo%s%d" % (nome, indice), (lados[nome], etiqueta_y + ETIQUETA_PROFUNDIDADE * 0.12, topo + FINO * 3),
                            (ADESIVO, ADESIVO * 0.8, FINO * 2), materiais[nome]))
    junto = juntar("Disquete%d" % indice, partes)
    junto.rotation_euler = (0.0, 0.0, math.radians(dados["giro"]))
    junto.location.x += dados["dx"]
    junto.location.y += dados["dy"]
    bpy.ops.object.select_all(action="DESELECT")
    junto.select_set(True)
    bpy.context.view_layer.objects.active = junto
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=False)
    return junto


def main():
    limpar_cena()
    materiais = {
        "corpo": material("Corpo", "#30303c", rugosidade=0.55),
        "metal": material("Metal", "#b4b4b4", rugosidade=0.35, metalico=0.8),
        "janela": material("Janela", "#14141a", rugosidade=0.6),
        "papel": material("Papel", "#f4f2e0", rugosidade=0.9),
        "caneta": material("Caneta", "#8a8d8a", rugosidade=0.9),
        "rosa": material("Rosa", "#ff6fb0", rugosidade=0.8),
        "amarelo": material("Amarelo", "#ffd23f", rugosidade=0.8),
    }
    disquetes = [disquete(i, d, materiais) for i, d in enumerate(DISQUETES)]
    juntar("PilhaDeDisquetes", disquetes)

    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=SAIDA, export_format="GLB", export_apply=True)
    print("Modelo salvo em", SAIDA)


main()

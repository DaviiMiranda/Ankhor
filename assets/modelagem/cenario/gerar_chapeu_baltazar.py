# gerar_chapeu_baltazar.py — modela no Blender o TRICÓRNIO DO BALTAZAR, que
# aparece sobre o notebook, na mesa do Gabriel, no quarto do visor 3D, quando ele junta
# os três pingentes do Labirinto (docs/mecanicas/colecionaveis.md).
#
# É o objeto-símbolo do Baltazar (docs/historia/personagens/baltazar.docx): um
# chapéu de feltro de copa baixa e três abas dobradas para cima, formando o
# triângulo, com um galão de latão na borda das abas. Nas três pontas do
# triângulo, os três PINGENTES: argola de latão, colarinho e a borla de fio
# vinho, deitada sobre a superfície. O feltro é gasto, sem renda nem galão rico
# (assets/sprites/personagens/baltazar/visual.md: "de sítio, não de corte").
#
# Como rodar (sem abrir a janela do Blender):
#
#   blender -b --factory-startup --python assets/modelagem/cenario/gerar_chapeu_baltazar.py
#
# O que sai:
#   assets/modelos/chapeu_baltazar.glb   o modelo em glTF binário, com o pé no
#                                        chão (y = 0) e centrado em x e z
#
# A GEOMETRIA: três pontas num círculo de raio RAIO_PONTA, a cada 120 graus. O
# fundo das abas é uma placa triangular entre as pontas; sobre cada lado dela
# sobe uma aba, inclinada para fora. A distância do centro ao meio de um lado é
# RAIO_PONTA · cos(60°) (o apótema), e é ali que cada aba nasce.
#
# EIXOS: o Blender usa Z para cima e o Godot usa Y; o exportador troca sozinho
# (Godot (x, y, z) = Blender (x, z, -y)). Aqui tudo é escrito direto em
# coordenadas do Blender. Medidas em metros.

import math
import os

import bmesh
import bpy

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
SAIDA = os.path.join(PASTA_PROJETO, "assets", "modelos", "chapeu_baltazar.glb")

RAIO_PONTA = 0.165
APOTEMA = RAIO_PONTA * math.cos(math.radians(60))
PLACA_ESPESSURA = 0.004
ABA_ALTURA = 0.066
ABA_ALTURA_NA_PONTA = 0.022
ABA_TOPO_RETO = 0.6
ABA_ESPESSURA = 0.005
LADO_DO_TRIANGULO = RAIO_PONTA * math.sqrt(3)
ABA_INCLINACAO = 24.0
GALAO_ALTURA = 0.008
GALAO_EXCESSO = 0.002
COPA_RAIO_BAIXO = 0.078
COPA_RAIO_TOPO = 0.068
COPA_ALTURA = 0.078
FAIXA_ALTURA = 0.012
ARGOLA_RAIO = 0.0075
ARGOLA_FIO = 0.0016
COLARINHO_RAIO = 0.0052
COLARINHO_ALTURA = 0.008
BORLA_RAIO_TOPO = 0.0065
BORLA_RAIO_BAIXO = 0.0105
BORLA_COMPRIMENTO = 0.052
FIOS = 5


def cor(hexa):
    hexa = hexa.lstrip("#")
    return tuple(int(hexa[i:i + 2], 16) / 255 for i in (0, 2, 4)) + (1.0,)


def material(nome, cor_base, rugosidade=0.6, metalico=0.0):
    mat = bpy.data.materials.new(nome)
    mat.use_nodes = True
    no = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    no.inputs["Base Color"].default_value = cor(cor_base)
    no.inputs["Roughness"].default_value = rugosidade
    no.inputs["Metallic"].default_value = metalico
    return mat


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


def pontas():
    angulos = [math.radians(30 + 120 * k) for k in range(3)]
    return [(RAIO_PONTA * math.cos(a), RAIO_PONTA * math.sin(a)) for a in angulos]


def placa(mat):
    malha = bpy.data.meshes.new("PlacaMalha")
    objeto = bpy.data.objects.new("Placa", malha)
    bpy.context.collection.objects.link(objeto)
    bm = bmesh.new()
    cantos = pontas()
    embaixo = [bm.verts.new((x, y, 0.0)) for x, y in cantos]
    em_cima = [bm.verts.new((x, y, PLACA_ESPESSURA)) for x, y in cantos]
    bm.faces.new(embaixo[::-1])
    bm.faces.new(em_cima)
    for i in range(3):
        j = (i + 1) % 3
        bm.faces.new((embaixo[i], embaixo[j], em_cima[j], em_cima[i]))
    bm.normal_update()
    bm.to_mesh(malha)
    bm.free()
    objeto.data.materials.append(mat)
    return objeto


def perfil_da_aba():
    """O contorno de uma aba vista de frente (x ao longo da borda, z para
    cima): mais alta no meio e baixa nas pontas, como as abas de um tricórnio."""
    metade = LADO_DO_TRIANGULO / 2
    return [(-metade, 0.0), (metade, 0.0), (metade, ABA_ALTURA_NA_PONTA),
            (metade * ABA_TOPO_RETO, ABA_ALTURA), (-metade * ABA_TOPO_RETO, ABA_ALTURA),
            (-metade, ABA_ALTURA_NA_PONTA)]


def prisma(nome, pontos, espessura, mat):
    """Extrude o contorno (x, z) por 'espessura' em y, centrado em y = 0."""
    malha = bpy.data.meshes.new(nome + "Malha")
    objeto = bpy.data.objects.new(nome, malha)
    bpy.context.collection.objects.link(objeto)
    bm = bmesh.new()
    frente = [bm.verts.new((x, -espessura / 2, z)) for x, z in pontos]
    fundo = [bm.verts.new((x, espessura / 2, z)) for x, z in pontos]
    bm.faces.new(frente[::-1])
    bm.faces.new(fundo)
    n = len(pontos)
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new((frente[i], frente[j], fundo[j], fundo[i]))
    bm.normal_update()
    bm.to_mesh(malha)
    bm.free()
    objeto.data.materials.append(mat)
    return objeto


def levantar(objeto, direcao_graus, afastamento, z_base):
    """Põe um prisma de pé a 'afastamento' do centro, na direção dada, inclinado
    ABA_INCLINACAO graus para fora (a origem do prisma é o meio da base)."""
    direcao = math.radians(direcao_graus)
    objeto.rotation_euler = (-math.radians(ABA_INCLINACAO), 0.0, direcao - math.pi / 2)
    objeto.location = (math.cos(direcao) * afastamento, math.sin(direcao) * afastamento, z_base)


def abas(feltro, galao):
    contorno = perfil_da_aba()
    borda = contorno[2:6]
    faixa = [(x, z) for x, z in borda] + [(x, z - GALAO_ALTURA) for x, z in reversed(borda)]
    pecas = []
    for k in range(3):
        direcao = 90 + 120 * k
        aba = prisma("Aba%d" % k, contorno, ABA_ESPESSURA, feltro)
        levantar(aba, direcao, APOTEMA, PLACA_ESPESSURA * 0.5)
        fita = prisma("Galao%d" % k, faixa, ABA_ESPESSURA + GALAO_EXCESSO, galao)
        levantar(fita, direcao, APOTEMA, PLACA_ESPESSURA * 0.5)
        pecas += [aba, fita]
    return pecas


def copa(feltro, faixa):
    bpy.ops.mesh.primitive_cone_add(
        vertices=24, radius1=COPA_RAIO_BAIXO, radius2=COPA_RAIO_TOPO, depth=COPA_ALTURA,
        location=(0, 0, PLACA_ESPESSURA + COPA_ALTURA / 2))
    objeto = bpy.context.active_object
    objeto.name = "Copa"
    objeto.data.materials.append(feltro)
    bpy.ops.mesh.primitive_cone_add(
        vertices=24, radius1=COPA_RAIO_BAIXO * 1.02, radius2=COPA_RAIO_BAIXO * 0.99, depth=FAIXA_ALTURA,
        location=(0, 0, PLACA_ESPESSURA + FAIXA_ALTURA / 2 + 0.004))
    fita = bpy.context.active_object
    fita.name = "FaixaDaCopa"
    fita.data.materials.append(faixa)
    return [objeto, fita]


def peca_deitada(nome, centro, raio_a, raio_b, comprimento, angulo, mat, lados=10):
    bpy.ops.mesh.primitive_cone_add(vertices=lados, radius1=raio_a, radius2=raio_b, depth=comprimento, location=centro)
    obj = bpy.context.active_object
    obj.name = nome
    obj.rotation_euler = (0.0, math.pi / 2, angulo)
    obj.data.materials.append(mat)
    return obj


def pingente(indice, ponta, latao, vinho):
    """Argola em pé na ponta do triângulo e, para fora, o colarinho, a borla e
    a franja, tudo deitado sobre a superfície."""
    x, y = ponta
    angulo = math.atan2(y, x)
    ux, uy = math.cos(angulo), math.sin(angulo)
    altura_do_eixo = BORLA_RAIO_BAIXO
    bpy.ops.mesh.primitive_torus_add(
        major_radius=ARGOLA_RAIO, minor_radius=ARGOLA_FIO, major_segments=16, minor_segments=6,
        location=(x, y, ARGOLA_RAIO + ARGOLA_FIO), rotation=(math.pi / 2, 0.0, angulo + math.pi / 2))
    argola = bpy.context.active_object
    argola.name = "Argola%d" % indice
    argola.data.materials.append(latao)
    pecas = [argola]

    inicio = ARGOLA_RAIO + 0.0045
    meio_do_colarinho = inicio + COLARINHO_ALTURA / 2
    pecas.append(peca_deitada(
        "Colarinho%d" % indice, (x + ux * meio_do_colarinho, y + uy * meio_do_colarinho, altura_do_eixo),
        COLARINHO_RAIO, COLARINHO_RAIO * 0.85, COLARINHO_ALTURA, angulo, latao))
    meio_da_borla = inicio + COLARINHO_ALTURA + BORLA_COMPRIMENTO / 2
    pecas.append(peca_deitada(
        "Borla%d" % indice, (x + ux * meio_da_borla, y + uy * meio_da_borla, altura_do_eixo),
        BORLA_RAIO_TOPO, BORLA_RAIO_BAIXO, BORLA_COMPRIMENTO, angulo, vinho))
    fim_da_borla = inicio + COLARINHO_ALTURA + BORLA_COMPRIMENTO
    for f in range(FIOS):
        lateral = (f - (FIOS - 1) / 2) * (BORLA_RAIO_BAIXO * 1.5 / FIOS)
        ao_longo = fim_da_borla + 0.004
        pecas.append(peca_deitada(
            "Fio%d_%d" % (indice, f),
            (x + ux * ao_longo - uy * lateral, y + uy * ao_longo + ux * lateral, altura_do_eixo * 0.8),
            0.0017, 0.0004, 0.012, angulo, vinho, lados=5))
    return pecas


def main():
    limpar_cena()
    feltro = material("Feltro", "#2e2420", rugosidade=0.95)
    feltro_gasto = material("FeltroGasto", "#3a2e28", rugosidade=0.95)
    latao = material("Latao", "#c07a22", rugosidade=0.4, metalico=0.6)
    vinho = material("Vinho", "#8f2434", rugosidade=0.9)

    juntar("Chapeu", [placa(feltro)] + abas(feltro_gasto, latao) + copa(feltro, latao))
    for i, ponta in enumerate(pontas()):
        juntar("Pingente%d" % i, pingente(i, ponta, latao, vinho))

    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=SAIDA, export_format="GLB", export_apply=True)
    print("Modelo salvo em", SAIDA)


main()

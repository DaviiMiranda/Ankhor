"""Acrescenta animacoes discretas ao .blend editado e atualiza o GLB do menu.

Execute com Blender em segundo plano, passando este arquivo para --python.
O script parte do .blend existente para preservar os ajustes feitos a mao.
"""

import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector


PASTA = Path(__file__).resolve().parent
RAIZ = PASTA.parents[2]
ARQUIVO_BLEND = PASTA / "menu_notebook.blend"
ARQUIVO_GLB = RAIZ / "assets/modelos/menu_notebook.glb"
TEXTURA_FUMACA = RAIZ / "assets/sprites/menu/notebook/fumaca.png"


def limpar_animacao_anterior():
    for nome in ("VaporDaCaneca",):
        objeto = bpy.data.objects.get(nome)
        if objeto:
            bpy.data.objects.remove(objeto, do_unlink=True)
    cortina = bpy.data.objects["Cortina"]
    if cortina.data.shape_keys:
        for chave in list(cortina.data.shape_keys.key_blocks)[::-1]:
            cortina.shape_key_remove(chave)
    for nome in ("CortinaBrisa", "FumacaCaneca"):
        acao = bpy.data.actions.get(nome)
        if acao:
            bpy.data.actions.remove(acao)


def animar_chave(chave, valores):
    chave.slider_min = -1.0
    chave.slider_max = 1.0
    for quadro, valor in valores:
        chave.value = valor
        chave.keyframe_insert(data_path="value", frame=quadro)
    chave.value = 0.0


def animar_cortina():
    cortina = bpy.data.objects["Cortina"]
    cortina.shape_key_add(name="Base", from_mix=False)
    brisa = cortina.shape_key_add(name="BrisaLeve", from_mix=False)
    pontos = [cortina.matrix_world @ vertice.co for vertice in cortina.data.vertices]
    base = min(ponto.z for ponto in pontos)
    topo = max(ponto.z for ponto in pontos)
    inversa = cortina.matrix_world.inverted()
    for i, ponto in enumerate(pontos):
        altura = max(0.0, min(1.0, (topo - ponto.z) / (topo - base)))
        peso = altura * altura
        deslocamento = Vector((
            0.007 * peso * math.sin(ponto.y * 14.0 + altura * 3.0),
            0.014 * peso * (0.72 + 0.28 * math.cos(ponto.y * 17.0 + altura * 4.0)),
            0.0,
        ))
        brisa.data[i].co = inversa @ (ponto + deslocamento)
    animar_chave(brisa, [(1, 0.0), (49, 1.0), (97, 0.0), (145, -1.0), (193, 0.0)])
    cortina.data.shape_keys.animation_data.action.name = "CortinaBrisa"


def criar_textura_fumaca():
    largura, altura = 64, 128
    imagem = bpy.data.images.get("FumacaDiscreta")
    if imagem:
        bpy.data.images.remove(imagem)
    imagem = bpy.data.images.new("FumacaDiscreta", width=largura, height=altura, alpha=True)
    pixels = []
    for y in range(altura):
        v = y / (altura - 1)
        fade = max(0.0, math.sin(math.pi * v)) ** 1.6
        for x in range(largura):
            u = x / (largura - 1)
            borda = math.exp(-((u - 0.5) / 0.25) ** 2)
            pixels.extend((0.72, 0.79, 0.84, 0.30 * fade * borda))
    imagem.pixels.foreach_set(pixels)
    imagem.filepath_raw = str(TEXTURA_FUMACA)
    imagem.file_format = "PNG"
    imagem.save()
    imagem.pack()
    return imagem


def criar_material_fumaca(imagem):
    material = bpy.data.materials.get("FumacaDiscreta") or bpy.data.materials.new("FumacaDiscreta")
    material.use_nodes = True
    material.diffuse_color = (0.72, 0.79, 0.84, 0.30)
    material.use_backface_culling = False
    if hasattr(material, "surface_render_method"):
        material.surface_render_method = "BLENDED"
    nos = material.node_tree.nodes
    nos.clear()
    textura = nos.new("ShaderNodeTexImage")
    textura.image = imagem
    textura.interpolation = "Linear"
    shader = nos.new("ShaderNodeBsdfPrincipled")
    shader.inputs["Roughness"].default_value = 1.0
    if "Emission Color" in shader.inputs:
        shader.inputs["Emission Color"].default_value = (0.45, 0.50, 0.54, 1.0)
        shader.inputs["Emission Strength"].default_value = 0.25
    saida = nos.new("ShaderNodeOutputMaterial")
    ligacoes = material.node_tree.links
    ligacoes.new(textura.outputs["Color"], shader.inputs["Base Color"])
    ligacoes.new(textura.outputs["Alpha"], shader.inputs["Alpha"])
    ligacoes.new(shader.outputs["BSDF"], saida.inputs["Surface"])
    return material


def centro_do_cafe():
    cafe = bpy.data.objects["Cafe"]
    pontos = [cafe.matrix_world @ vertice.co for vertice in cafe.data.vertices]
    return Vector((
        (min(ponto.x for ponto in pontos) + max(ponto.x for ponto in pontos)) / 2,
        (min(ponto.y for ponto in pontos) + max(ponto.y for ponto in pontos)) / 2,
        max(ponto.z for ponto in pontos),
    ))


def criar_vapor(material):
    centro = centro_do_cafe()
    vertices, faces, uvs = [], [], []
    for faixa in range(3):
        inicio = len(vertices)
        for passo in range(13):
            v = passo / 12
            altura = 0.008 + v * (0.12 + faixa * 0.012)
            lateral = (faixa - 1) * 0.014 + 0.008 * math.sin(v * 5.3 + faixa * 1.8)
            profundidade = 0.004 * math.cos(v * 4.0 + faixa)
            largura = (0.007 + 0.004 * v) * math.sin(math.pi * (0.07 + 0.86 * v))
            for lado, u in ((-1, 0.0), (1, 1.0)):
                vertices.append((centro.x + 0.004 + profundidade, centro.y + lateral + lado * largura, centro.z + altura))
                uvs.append((u, v))
        for passo in range(12):
            a = inicio + 2 * passo
            faces.append((a, a + 1, a + 3, a + 2))
    malha = bpy.data.meshes.new("MalhaDoVapor")
    malha.from_pydata(vertices, [], faces)
    malha.materials.append(material)
    malha.update()
    malha.uv_layers.new(name="UVMap")
    for poligono in malha.polygons:
        for indice in poligono.loop_indices:
            malha.uv_layers.active.data[indice].uv = uvs[malha.loops[indice].vertex_index]
    objeto = bpy.data.objects.new("VaporDaCaneca", malha)
    bpy.context.collection.objects.link(objeto)
    objeto.shape_key_add(name="Base", from_mix=False)
    ondulacao = objeto.shape_key_add(name="OndulacaoDoVapor", from_mix=False)
    for i, ponto in enumerate(vertices):
        v = uvs[i][1]
        ondulacao.data[i].co = (
            ponto[0] + 0.005 * v * math.sin(v * 7.0 + i * 0.22),
            ponto[1] + 0.006 * v * math.cos(v * 6.0 + i * 0.16),
            ponto[2],
        )
    animar_chave(ondulacao, [(1, 0.0), (25, 1.0), (49, 0.0), (73, -1.0), (97, 0.0),
                            (121, 1.0), (145, 0.0), (169, -1.0), (193, 0.0)])
    objeto.data.shape_keys.animation_data.action.name = "FumacaCaneca"


def exportar_modelo():
    bpy.ops.object.select_all(action="DESELECT")
    for objeto in bpy.context.scene.objects:
        if objeto.type == "MESH" and not objeto.name.startswith("Previa_"):
            objeto.select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects["Cortina"]
    bpy.ops.export_scene.gltf(
        filepath=str(ARQUIVO_GLB), export_format="GLB", use_selection=True,
        export_animations=True, export_morph=True, export_morph_animation=True,
    )
    bpy.ops.object.select_all(action="DESELECT")


def main():
    if Path(bpy.data.filepath).resolve() != ARQUIVO_BLEND.resolve():
        raise RuntimeError("Abra o menu_notebook.blend antes de executar este script")
    if "--apenas-exportar" in sys.argv:
        exportar_modelo()
        print("Ajustes atuais exportados para", ARQUIVO_GLB)
        return
    limpar_animacao_anterior()
    animar_cortina()
    criar_vapor(criar_material_fumaca(criar_textura_fumaca()))
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = 193
    bpy.context.scene.render.fps = 24
    bpy.context.scene.frame_set(1)
    exportar_modelo()
    bpy.ops.file.pack_all()
    bpy.ops.wm.save_as_mainfile(filepath=str(ARQUIVO_BLEND))
    print("Animacoes salvas em", ARQUIVO_BLEND)
    print("Modelo animado exportado para", ARQUIVO_GLB)


if __name__ == "__main__":
    main()

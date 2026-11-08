"""Monta o menu no Blender a partir da escrivaninha original do quarto VR.

Uso: blender -b --factory-startup --python assets/modelagem/menu/gerar_menu_notebook.py
Gera um GLB independente, um .blend editável e uma prévia iluminada.
"""

import ast
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector


RAIZ = Path(__file__).resolve().parents[3]
PASTA = Path(__file__).resolve().parent
TEXTURAS = RAIZ / "assets/sprites/cenario/visor"
MODELO = RAIZ / "assets/modelos/menu_notebook.glb"
CAMERA = (-1.429099, 1.23, -0.2)
ALVO = (-2.403885, 1.006857, -0.2)
FOV_VERTICAL = 40.0

sys.path.insert(0, str(PASTA))
from detalhar_menu_notebook import detalhar
from texturizar_menu_notebook import aplicar_materiais, gerar_texturas


def carregar_oficina():
    # Carrega apenas as definições: nunca executa o main nem regrava o quarto VR.
    caminho = RAIZ / "assets/modelagem/cenario/gerar_sala_visor.py"
    arvore = ast.parse(caminho.read_text(encoding="utf-8-sig"))
    principal = next(no for no in arvore.body if isinstance(no, ast.FunctionDef) and no.name == "main")
    arvore.body = [no for no in arvore.body if not isinstance(no, ast.Expr)]
    oficina = {"__file__": str(caminho), "__name__": "oficina_do_menu"}
    exec(compile(arvore, str(caminho), "exec"), oficina)
    oficina["limpar_cena"]()
    materiais = next(no for no in principal.body if isinstance(no, ast.Assign))
    exec(compile(ast.Module(body=[materiais], type_ignores=[]), str(caminho), "exec"), oficina)
    return oficina


def deslocar(objeto, deslocamento):
    objeto.location += Vector((deslocamento[0], -deslocamento[2], deslocamento[1]))


def montar_geometria(oficina):
    materiais = oficina["m"]
    for nome in ("escrivaninha", "notebook", "janela"):
        oficina[nome](materiais)

    # Escala uniforme em torno da base: a tela ganha espaço sem deformar o aparelho.
    origem = Vector(oficina["para_blender"](-2.29, 0.76, 0.28))
    translacao = Vector(oficina["para_blender"](0.22, 0.0, -0.48))
    for nome in ("Notebook", "TampaNotebook", "TelaNotebook"):
        objeto = bpy.data.objects[nome]
        for vertice in objeto.data.vertices:
            mundo = objeto.matrix_world @ vertice.co
            mundo = origem + (mundo - origem) * 1.6 + translacao
            vertice.co = objeto.matrix_world.inverted() @ mundo

    for nome in ("Luminaria", "Lampada"):
        deslocar(bpy.data.objects[nome], (0.0, 0.0, 0.4))
    deslocar(bpy.data.objects["Caneca"], (0.16, 0.0, 0.61))

    caixa = oficina["caixa"]
    caixa("ParedeDoMenu", (-2.56, 1.45, -0.2), (0.1, 2.9, 3.4), materiais["parede"])
    caixa("PisoDoMenu", (-1.85, -0.04, -0.2), (1.5, 0.08, 3.4), materiais["chao"])

    # A janela recebe o céu noturno próprio do menu; o quarto VR conserva sua paisagem.
    janela = oficina["material"]("PaisagemDaJanela", "#ffffff", brilho="#ffffff", forca_brilho=0.8)
    oficina["quad"]("PaisagemDaJanela", (-2.475, 1.102, 0.304), (-2.475, 1.102, -0.704),
                    (-2.475, 2.098, -0.704), (-2.475, 2.098, 0.304), janela)

    detalhar(oficina)

    # O GLB leva somente a geometria. A tela recebe o menu vivo no Godot.
    MODELO.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=str(MODELO), export_format="GLB", export_apply=True)
    triangulos = 0
    for objeto in bpy.context.scene.objects:
        if objeto.type == "MESH":
            objeto.data.calc_loop_triangles()
            triangulos += len(objeto.data.loop_triangles)
    print("Triangulos do cenario:", triangulos)


def aplicar_texturas_de_previa():
    texturas = {
        "Tampo": ("tampo_mesa", 0.7), "Madeira": ("madeira", 0.4),
        "MadeiraEscura": ("madeira_escura", 0.4), "Parede": ("parede", 1.0),
        "Chao": ("piso_madeira", 0.8), "Cortina": ("cortina", 0.25),
        "Paginas": ("paginas", 0.05), "Teclado": ("teclado_notebook", None),
    }
    for nome, (arquivo, metros) in texturas.items():
        material = bpy.data.materials.get(nome)
        if material is None:
            continue
        nos = material.node_tree.nodes
        ligacoes = material.node_tree.links
        imagem = nos.new("ShaderNodeTexImage")
        imagem.image = bpy.data.images.load(str(TEXTURAS / (arquivo + ".png")))
        imagem.interpolation = "Closest"
        if metros:
            coordenadas = nos.new("ShaderNodeNewGeometry")
            escala = nos.new("ShaderNodeVectorMath")
            escala.operation = "SCALE"
            escala.inputs[3].default_value = 1.0 / metros
            ligacoes.new(coordenadas.outputs["Position"], escala.inputs[0])
            ligacoes.new(escala.outputs["Vector"], imagem.inputs["Vector"])
            imagem.projection = "BOX"
        ligacoes.new(imagem.outputs["Color"], nos.get("Principled BSDF").inputs["Base Color"])
    janela = bpy.data.materials["PaisagemDaJanela"]
    nos, ligacoes = janela.node_tree.nodes, janela.node_tree.links
    nos.clear()
    textura = nos.new("ShaderNodeTexImage")
    textura.image = bpy.data.images.load(str(RAIZ / "assets/sprites/menu/notebook/ceu_noturno.png"))
    textura.interpolation = "Closest"
    emissao = nos.new("ShaderNodeEmission")
    emissao.inputs["Strength"].default_value = 0.3
    saida = nos.new("ShaderNodeOutputMaterial")
    ligacoes.new(textura.outputs["Color"], emissao.inputs["Color"])
    ligacoes.new(emissao.outputs[0], saida.inputs["Surface"])
    paisagem = bpy.data.objects["PaisagemDaJanela"]
    paisagem.visible_diffuse = False
    paisagem.visible_glossy = False


def criar_luz(nome, posicao, energia, cor, tamanho, alvo):
    dados = bpy.data.lights.new(nome, "AREA")
    dados.energy = energia
    dados.color = cor
    dados.shape = "DISK"
    dados.size = tamanho
    objeto = bpy.data.objects.new(nome, dados)
    bpy.context.collection.objects.link(objeto)
    objeto.location = Vector((posicao[0], -posicao[2], posicao[1]))
    destino = Vector((alvo[0], -alvo[2], alvo[1]))
    objeto.rotation_euler = (destino - objeto.location).to_track_quat("-Z", "Y").to_euler()


def escrever_previa(oficina):
    # Os textos são só uma prévia editável no Blender; não entram no GLB.
    tela = bpy.data.objects["TelaNotebook"]
    pontos = [tela.matrix_world @ vertice.co for vertice in tela.data.vertices]
    esquerda_baixo, direita_baixo, direita_cima, esquerda_cima = pontos
    direita = (direita_baixo - esquerda_baixo).normalized()
    cima = (esquerda_cima - esquerda_baixo).normalized()
    normal = direita.cross(cima).normalized()
    from mathutils import Matrix
    orientacao = Matrix((direita, cima, normal)).transposed().to_quaternion()
    material = oficina["material"]("TextoDaPrevia", "#abcad9", brilho="#abcad9", forca_brilho=0.6)
    fonte = bpy.data.fonts.load(str(RAIZ / "assets/fontes/galmuri_7.ttf"))
    for i, texto in enumerate(("ANKHOR", "Novo jogo", "Continuar", "Fases", "Opções", "Créditos       Sair")):
        dados = bpy.data.curves.new("TextoDoMenu", "FONT")
        dados.body = texto
        dados.font = fonte
        dados.size = 0.046 if i == 0 else 0.025
        objeto = bpy.data.objects.new("Previa_" + str(i), dados)
        bpy.context.collection.objects.link(objeto)
        objeto.location = esquerda_cima + direita * 0.035 - cima * (0.065 + i * 0.038) + normal * 0.001
        objeto.rotation_mode = "QUATERNION"
        objeto.rotation_quaternion = orientacao
        dados.materials.append(material)


def preparar_camera_e_luzes():
    cena = bpy.context.scene
    cena.render.engine = "CYCLES"
    cena.cycles.samples = 48
    cena.cycles.use_denoising = True
    cena.render.resolution_x = 1600
    cena.render.resolution_y = 900
    cena.render.resolution_percentage = 100
    cena.view_settings.view_transform = "AgX"
    cena.world.use_nodes = True
    cena.world.node_tree.nodes.get("Background").inputs["Strength"].default_value = 0.0
    criar_luz("LuzDaLuminaria", (-2.246035, 1.101134, 0.320129), 12,
              (1.0, 0.77, 0.48), 0.1287, (-2.135715, 0.813746, -0.631311))
    dados = bpy.data.cameras.new("CameraDoMenu")
    dados.sensor_fit = "VERTICAL"
    dados.lens = dados.sensor_height / (2.0 * math.tan(math.radians(FOV_VERTICAL) / 2.0))
    camera = bpy.data.objects.new("CameraDoMenu", dados)
    bpy.context.collection.objects.link(camera)
    camera.location = Vector((CAMERA[0], -CAMERA[2], CAMERA[1]))
    alvo = Vector((ALVO[0], -ALVO[2], ALVO[1]))
    camera.rotation_euler = (alvo - camera.location).to_track_quat("-Z", "Y").to_euler()
    cena.camera = camera
    # Abre diretamente na composição final quando o arquivo é aberto no Blender.
    for area in bpy.context.screen.areas:
        if area.type == "VIEW_3D":
            area.spaces.active.region_3d.view_perspective = "CAMERA"
    cena.render.image_settings.file_format = "PNG"
    cena.render.filepath = str(PASTA / "menu_notebook_previa.png")


def main():
    oficina = carregar_oficina()
    gerar_texturas()
    montar_geometria(oficina)
    aplicar_texturas_de_previa()
    aplicar_materiais()
    escrever_previa(oficina)
    preparar_camera_e_luzes()
    bpy.ops.file.pack_all()
    bpy.ops.wm.save_as_mainfile(filepath=str(PASTA / "menu_notebook.blend"))
    if "--sem-render" not in sys.argv:
        bpy.ops.render.render(write_still=True)
    print("Menu exportado:", MODELO)


if __name__ == "__main__":
    main()

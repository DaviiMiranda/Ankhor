# comum.py — peças que os scripts dos personagens usam em comum.
#
# Não roda sozinho: gerar_gabriel.py e gerar_vigia.py importam este arquivo.
#
# O que tem aqui:
#   1. Pastas e unidades (1 unidade do Blender = 1 metro).
#   2. Materiais com uma "cor de identificação" escondida (ver item 5).
#   3. Primitivas low poly (caixa, cilindro/cone, esfera) e "pivôs" (juntas).
#   4. Câmera ortográfica, luzes e configuração do Cycles.
#   5. O truque do pixel art: cada vista é renderizada DUAS vezes.
#        a) Passe de LUZ: todo mundo de argila branca. O resultado diz só
#           quanto de luz chega em cada pixel (0 = escuro, 1 = claro).
#        b) Passe de ID: cada material vira uma cor chapada única. O
#           resultado diz QUAL material está em cada pixel.
#      Juntando os dois: pixel = rampa[material][degrau de luz]. A luz é
#      "cortada" em 4 degraus (sombra funda, sombra, luz, brilho), como o
#      sombreamento em faixas da pixel art feita à mão. Assim a pele nunca
#      vira marrom da calça numa sombra, e a paleta é fixa e pequena.
#   6. Contorno seletivo de 1 px, folha de referência e gravação do PNG.
#   7. Personagem em pé: caminhada, respiração e retrato, com as mesmas
#      vistas e tamanhos para todos (Gabriel, Clarice, Zane).
#
# Mesmas técnicas do menu (assets/modelagem/menu/gerar_menu.py): Cycles na
# CPU sem janela, filtro de pixel mínimo (sem antialiasing), sem denoise,
# transformação de cor "Standard" e alfa cortado em 0 ou 1.

import math
import os
import shutil
import tempfile

import bmesh
import bpy
import numpy as np
from mathutils import Matrix, Vector

# ---------------------------------------------------------------------------
# 1. Pastas e escala
# ---------------------------------------------------------------------------

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
PASTA_SPRITES = os.path.join(PASTA_PROJETO, "assets", "sprites", "personagens")

# Escala do sprite de JOGO. Gabriel tem 1,75 m e deve ocupar 48 px dos
# 180 px de altura da tela (pouco mais de 1/4 da tela). Por que 48?
#   - Sobra 3/4 da tela para o cenário 2.5D: teto desabado, estantes,
#     plataformas acima e abaixo — o jogo é de exploração, o lugar importa.
#   - 48 = 3 tiles de 16 px: portas, estantes e degraus casam com a grade.
#   - A cabeça fica com ~7 px: dá para ler olho, cabelo e boné.
#     Com 32 px a cabeça teria 4–5 px e o Vigia viraria um borrão.
#   - É a proporção dos personagens de FNAF: Into the Pit (≈1/4 da tela).
# TODOS os personagens usam a mesma escala (px por metro), então um
# personagem mais alto ou mais curvado aparece maior ou menor de verdade.
ALTURA_GABRIEL_M = 1.75
PX_POR_M_JOGO = 48 / ALTURA_GABRIEL_M          # ≈ 27,4 px por metro (1 px ≈ 3,6 cm)
PX_POR_M_REF = 128 / ALTURA_GABRIEL_M          # folha de referência: 128 px de altura

# Tela (quadro) de cada sprite, em pixels. O pé fica sempre na mesma
# linha, então no Godot basta alinhar a base do sprite com o chão.
QUADRO_JOGO = (48, 56)      # largura, altura
PE_JOGO_PX = 3              # linhas livres abaixo do pé (cabe o contorno)
QUADRO_REF = (104, 148)
PE_REF_PX = 6

# ---------------------------------------------------------------------------
# 2. Cores e materiais
# ---------------------------------------------------------------------------


def hex_para_rgb(hexa):
    """'#rrggbb' -> (r, g, b) de 0 a 1, em sRGB (como no editor de imagem)."""
    hexa = hexa.lstrip("#")
    return np.array([int(hexa[i:i + 2], 16) / 255 for i in (0, 2, 4)], dtype=np.float64)


def srgb_para_linear(c):
    """sRGB -> RGB linear, o espaço em que o Blender faz as contas de luz."""
    c = np.asarray(c, dtype=np.float64)
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def rgb_para_hex(c):
    c = np.clip(np.round(np.asarray(c) * 255), 0, 255).astype(int)
    return "#%02x%02x%02x" % tuple(c)


# Cores para onde a rampa "puxa" as sombras e os brilhos. Sombra puxada
# para um azul-violeta escuro e brilho para um branco levemente frio: é o
# "hue shifting" da pixel art, e dá o clima neutro-frio do jogo sem
# depender da cor da luz. A sombra NUNCA chega ao preto puro.
COR_SOMBRA = hex_para_rgb("#232840")
COR_BRILHO = hex_para_rgb("#eef3ff")


def rampa(hexa):
    """A partir da cor base (o tom "iluminado"), gera 4 tons:
    0 = sombra funda, 1 = sombra, 2 = luz (a própria cor), 3 = brilho.

    A conta é uma mistura linear: tom = cor*(1-t) + alvo*t, e a cor
    também é escurecida por multiplicação nas sombras."""
    base = hex_para_rgb(hexa)
    t0 = base * 0.50 * 0.65 + COR_SOMBRA * 0.35
    t1 = base * 0.74 * 0.82 + COR_SOMBRA * 0.18
    t2 = base
    t3 = base * 0.78 + COR_BRILHO * 0.22
    return [np.clip(t, 0, 1) for t in (t0, t1, t2, t3)]


class Materiais:
    """Guarda todos os materiais do personagem, na ordem em que são criados.

    Cada material tem:
      - a cor base (hex) — o tom "iluminado" da rampa;
      - um modo: 'normal' (sombreado em 4 degraus), 'plano' (sempre a cor
        base, bom para detalhes de 1 px como olhos e distintivos) ou
        'brilho' (emite luz; também sempre a cor base);
      - uma cor de ID única, usada no passe de ID (ver o topo do arquivo).
    """

    def __init__(self):
        self.lista = []            # (nome, hex, modo, material do Blender)

    def novo(self, nome, hexa, modo="normal", aspereza=0.8):
        indice = len(self.lista)
        mat = bpy.data.materials.new(nome)
        try:
            mat.use_nodes = True   # no Blender 5 já vem ligado; em versões antigas precisa
        except Exception:
            pass
        nos = mat.node_tree.nodes
        bsdf = nos.get("Principled BSDF")
        bsdf.inputs["Base Color"].default_value = (*srgb_para_linear(hex_para_rgb(hexa)), 1)
        bsdf.inputs["Roughness"].default_value = aspereza
        if modo == "brilho":
            bsdf.inputs["Emission Color"].default_value = (*srgb_para_linear(hex_para_rgb(hexa)), 1)
            bsdf.inputs["Emission Strength"].default_value = 2.0
        # Nó de emissão com a cor de ID. O índice é guardado nos canais
        # vermelho e verde, de 8 em 8 níveis (de 0 a 255 cabem 31 valores
        # por canal): fácil de decodificar e sem risco de arredondamento.
        emissao = nos.new("ShaderNodeEmission")
        emissao.name = "ID"
        r = ((indice % 31) + 1) * 8 / 255
        g = ((indice // 31) + 1) * 8 / 255
        emissao.inputs["Color"].default_value = (*srgb_para_linear([r, g, 0.0]), 1)
        emissao.inputs["Strength"].default_value = 1.0
        self.lista.append((nome, hexa, modo, mat))
        return mat

    def modo_id(self, ligado):
        """Liga cada material à saída pela emissão de ID (ligado=True) ou
        pelo Principled BSDF normal (ligado=False)."""
        for _, _, _, mat in self.lista:
            arvore = mat.node_tree
            saida = arvore.nodes.get("Material Output")
            origem = arvore.nodes.get("ID") if ligado else arvore.nodes.get("Principled BSDF")
            arvore.links.new(origem.outputs[0], saida.inputs["Surface"])

    def rampas(self):
        """Lista de rampas (4 tons cada), na ordem dos índices."""
        saida = []
        for _, hexa, modo, _ in self.lista:
            if modo == "normal":
                saida.append(rampa(hexa))
            else:
                c = hex_para_rgb(hexa)
                saida.append([c, c, c, c])
        return saida


# ---------------------------------------------------------------------------
# 3. Primitivas e pivôs
# ---------------------------------------------------------------------------
# Um personagem é uma árvore de "pivôs" (objetos vazios, as juntas): raiz
# -> quadril -> tronco -> ombro -> cotovelo... Cada peça é filha de um
# pivô, e a posição dela é contada a partir dele. Girar o pivô do tronco
# curva o corpo inteiro de cima; girar o ombro levanta o braço todo.
#
# Eixos (personagem olhando para a câmera, "de frente"):
#   +X = esquerda da imagem para a direita, -Y = para a frente (para a
#   câmera), +Z = para cima. O chão é z = 0.
# Rotação em X positiva inclina para a FRENTE uma peça que aponta para
# cima (tronco, cabeça) e para TRÁS uma peça que pende para baixo
# (braço, perna).

COLECAO_ATUAL = None

# Nível de detalhe das primitivas. Cada script de personagem pode mudar
# antes de montar o modelo (os robôs e o Vigia ficam no padrão):
#   DETALHE  multiplica os gomos de cones e esferas (um cone de 6 lados vira
#            6·DETALHE lados) e dá DETALHE segmentos ao bisel das caixas: com
#            1 a quina é chanfrada; com 2 ou mais ela fica arredondada.
#   SUAVE    sombreamento suave nas curvas: a normal de cada ponto é a média
#            das faces em volta, então a luz desliza pela superfície em vez
#            de mudar de face em face. Quinas com mais de ANGULO_QUINA graus
#            continuam marcadas (senão a caixa viraria um sabonete).
# Com mais gomos e luz suave, a silhueta fica mais redonda e os degraus de
# luz (sombra funda, sombra, luz, brilho) viram faixas que seguem a forma,
# em vez de um mosaico de facetas: é isso que dá mais definição ao sprite.
DETALHE = 1
SUAVE = False
ANGULO_QUINA = 50


def usar_colecao(nome):
    """Cria uma coleção e passa a pôr nela tudo o que for criado."""
    global COLECAO_ATUAL
    col = bpy.data.collections.new(nome)
    bpy.context.scene.collection.children.link(col)
    COLECAO_ATUAL = col
    return col


def _ligar(obj, pai, pos, rot):
    COLECAO_ATUAL.objects.link(obj)
    if pai is not None:
        obj.parent = pai              # sem matriz inversa: pos é relativa ao pai
    obj.location = pos
    obj.rotation_euler = [math.radians(a) for a in rot]
    return obj


def pivo(nome, pos=(0, 0, 0), pai=None, rot=(0, 0, 0)):
    """Uma junta: objeto vazio que não aparece no render."""
    obj = bpy.data.objects.new(nome, None)
    obj.empty_display_size = 0.05
    return _ligar(obj, pai, pos, rot)


def _objeto(nome, bm, mat):
    malha = bpy.data.meshes.new(nome)
    bm.to_mesh(malha)
    bm.free()
    if SUAVE:
        malha.shade_smooth()
        malha.set_sharp_from_angle(angle=math.radians(ANGULO_QUINA))
    obj = bpy.data.objects.new(nome, malha)
    obj.data.materials.append(mat)
    return obj


def _bisel(obj, largura):
    if largura > 0:
        mod = obj.modifiers.new("Bisel", 'BEVEL')
        mod.width = largura
        mod.segments = DETALHE         # 1 segmento = quina chanfrada; 2 ou mais = arredondada
        mod.limit_method = 'NONE'
        if SUAVE:
            mod.harden_normals = True  # faces retas continuam retas perto da quina redonda


def caixa(nome, tam, pos, mat, pai=None, rot=(0, 0, 0), bisel=0.0, desloc=(0, 0, 0)):
    """Caixa de tamanho tam=(x, y, z) metros. 'desloc' move a malha dentro
    do objeto: com desloc=(0, 0, -L/2) a caixa "pende" do pivô, como um
    braço pendurado no ombro."""
    bm = bmesh.new()
    m = Matrix.Translation(desloc) @ Matrix.Diagonal((*tam, 1))
    bmesh.ops.create_cube(bm, size=1.0, matrix=m)
    obj = _objeto(nome, bm, mat)
    _bisel(obj, bisel)
    return _ligar(obj, pai, pos, rot)


def cone(nome, raio_baixo, raio_cima, altura, pos, mat, pai=None, rot=(0, 0, 0),
         lados=8, achatar=1.0, desloc=(0, 0, 0)):
    """Cilindro (ou tronco de cone) em pé, centrado no objeto.
    achatar < 1 deixa a seção oval (mais fina na profundidade Y)."""
    bm = bmesh.new()
    m = Matrix.Translation(desloc) @ Matrix.Diagonal((1, achatar, 1, 1))
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=lados * DETALHE,
                          radius1=raio_baixo, radius2=raio_cima, depth=altura, matrix=m)
    obj = _objeto(nome, bm, mat)
    return _ligar(obj, pai, pos, rot)


def membro(nome, raio_cima, raio_baixo, comprimento, mat, pai, lados=6, achatar=1.0):
    """Segmento de braço ou perna pendurado no pivô (vai de z=0 a z=-comprimento)."""
    return cone(nome, raio_baixo, raio_cima, comprimento, (0, 0, 0), mat, pai,
                lados=lados, achatar=achatar, desloc=(0, 0, -comprimento / 2))


def esfera(nome, raio, pos, mat, pai=None, rot=(0, 0, 0), escala=(1, 1, 1), seg=8, aneis=5):
    """Esfera low poly (poucos gomos: fica facetada, como o resto)."""
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=seg * DETALHE, v_segments=aneis * DETALHE, radius=raio,
                              matrix=Matrix.Diagonal((*escala, 1)))
    obj = _objeto(nome, bm, mat)
    return _ligar(obj, pai, pos, rot)


def achatar_sombra(nome):
    """Volta uma peça para o sombreamento facetado com quina só chanfrada.
    Serve para o rosto: com a luz suave, a parte de baixo arredondada da
    caixa escurece aos poucos e parece barba. Chapado, o rosto fica limpo."""
    obj = bpy.data.objects[nome]
    obj.data.shade_flat()
    bisel = obj.modifiers.get("Bisel")
    if bisel:
        bisel.segments = 1
        bisel.harden_normals = False


def pedra(nome, raio, pos, mat, pai=None, rot=(0, 0, 0)):
    """Icosfera de 1 subdivisão: um caco de pedra anguloso."""
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=1, radius=raio,
                               matrix=Matrix.Diagonal((1.0, 0.7, 1.4, 1)))
    obj = _objeto(nome, bm, mat)
    return _ligar(obj, pai, pos, rot)


# ---------------------------------------------------------------------------
# 4. Câmera, luzes e render
# ---------------------------------------------------------------------------

def cena_vazia():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    cena = bpy.context.scene
    cena.render.engine = 'CYCLES'
    cena.cycles.device = 'CPU'
    cena.cycles.use_denoising = False       # o denoiser borra; pixel art não pode borrar
    cena.cycles.use_adaptive_sampling = False
    cena.cycles.max_bounces = 3
    # Filtro de pixel quase zero = sem antialiasing: cada pixel "vê" um
    # único ponto da cena, então a borda da silhueta sai dura.
    cena.cycles.filter_width = 0.01
    cena.render.film_transparent = True
    cena.render.resolution_percentage = 100
    cena.render.dither_intensity = 0.0      # sem pontilhado: o passe de ID precisa das cores exatas
    cena.render.image_settings.file_format = 'PNG'
    cena.render.image_settings.color_mode = 'RGBA'
    cena.render.image_settings.color_depth = '8'
    cena.view_settings.view_transform = 'Standard'
    cena.view_settings.look = 'None'
    return cena


def criar_camera():
    """Câmera ORTOGRÁFICA olhando reto para +Y, na altura do personagem.

    Por que ortográfica? O jogo é de vista lateral: o sprite vai ser
    desenhado chapado na tela. Em perspectiva o pé (mais longe do olho
    que a cabeça, ou vice-versa) sairia com outra escala, e cada
    personagem teria um tamanho diferente conforme a distância. Na
    ortográfica 1 metro vale sempre o mesmo número de pixels."""
    dados = bpy.data.cameras.new("Camera")
    dados.type = 'ORTHO'
    dados.sensor_fit = 'HORIZONTAL'
    dados.clip_start = 0.1
    dados.clip_end = 100.0
    cam = bpy.data.objects.new("Camera", dados)
    cam.rotation_euler = (math.radians(90), 0, 0)
    bpy.context.scene.collection.objects.link(cam)
    bpy.context.scene.camera = cam
    return cam


def enquadrar(cam, largura_px, altura_px, px_por_m, pe_px):
    """Ajusta a câmera para que 1 m = px_por_m pixels e o chão (z = 0)
    caia exatamente 'pe_px' pixels acima da borda de baixo."""
    cena = bpy.context.scene
    cena.render.resolution_x = largura_px
    cena.render.resolution_y = altura_px
    cam.data.ortho_scale = largura_px / px_por_m            # largura visível, em metros
    centro_z = (altura_px / 2 - pe_px) / px_por_m           # meio do quadro, em metros
    cam.location = (0.0, -20.0, centro_z)


def criar_luzes():
    """Três sóis (luz direcional, igual em qualquer ponto), presos à
    câmera — o personagem gira e a luz fica parada, então todas as vistas
    têm o mesmo sombreamento. Iluminação de estúdio, só para ler a forma:
    no jogo quem ilumina é a PointLight2D do Godot."""
    def sol(nome, energia, rot_graus, angulo=8.0):
        dados = bpy.data.lights.new(nome, 'SUN')
        dados.energy = energia
        dados.angle = math.radians(angulo)   # sombra um pouco macia
        obj = bpy.data.objects.new(nome, dados)
        obj.rotation_euler = [math.radians(a) for a in rot_graus]
        bpy.context.scene.collection.objects.link(obj)

    # Principal: do alto, da frente e da esquerda (sombra cai à direita).
    sol("LuzPrincipal", 1.5, (50, 0, -55))
    # Preenchimento fraco da direita, para a sombra não virar mancha.
    sol("LuzPreenchimento", 0.3, (75, 0, 60), 20)
    # Contraluz: de trás e de cima, desenha a borda da silhueta.
    sol("LuzContra", 0.9, (-55, 0, 150))

    mundo = bpy.data.worlds.new("Estudio")
    try:
        mundo.use_nodes = True
    except Exception:
        pass
    fundo = mundo.node_tree.nodes.get("Background")
    fundo.inputs["Color"].default_value = (0.5, 0.5, 0.5, 1)
    fundo.inputs["Strength"].default_value = 0.25
    bpy.context.scene.world = mundo


def _ler_png(caminho):
    """Lê um PNG como array numpy (altura, largura, 4), de CIMA para BAIXO
    (o Blender guarda as linhas de baixo para cima; aqui invertemos)."""
    img = bpy.data.images.load(caminho)
    img.colorspace_settings.name = 'Non-Color'   # os bytes como estão, sem conversão
    w, h = img.size
    px = np.array(img.pixels[:], dtype=np.float32).reshape(h, w, 4)[::-1]
    bpy.data.images.remove(img)
    return px


def salvar_png(arr, caminho):
    """Grava um array (altura, largura, 4), de cima para baixo, como PNG."""
    h, w, _ = arr.shape
    img = bpy.data.images.new(os.path.basename(caminho), w, h, alpha=True)
    img.colorspace_settings.name = 'Non-Color'
    img.pixels[:] = np.ascontiguousarray(arr[::-1], dtype=np.float32).ravel()
    img.filepath_raw = caminho
    img.file_format = 'PNG'
    img.save()
    bpy.data.images.remove(img)


# Degraus de luz: a luminância do passe de argila (0 a 1) vira um dos
# 4 tons da rampa. Abaixo de 0,30 = sombra funda; até 0,60 = sombra;
# até 0,80 = luz; acima = brilho. Os limites foram escolhidos olhando o
# histograma da luz (rode com a variável DEBUG_LUZ=1): com estas luzes as
# faces viradas para a luz ficam entre 0,65 e 0,8 e as do lado da sombra
# entre 0,4 e 0,6. Pôr o corte no "vale" entre os dois grupos evita que
# o ruído do render faça pixels pularem de um tom para outro (sujeira).
DEGRAUS_LUZ = (0.30, 0.60, 0.80)


def renderizar_vista(cam, raiz, materiais, angulo, quadro, px_por_m, pe_px, amostras=256):
    """Renderiza o personagem girado 'angulo' graus em torno do eixo Z
    (0 = de frente, 90 = de lado olhando para a direita, 180 = de costas).
    Devolve um array RGBA já em pixel art (cores da paleta, alfa 0/1)."""
    cena = bpy.context.scene
    raiz.rotation_euler = (0, 0, math.radians(angulo))
    enquadrar(cam, quadro[0], quadro[1], px_por_m, pe_px)
    tmp = tempfile.mkdtemp()

    # a) Passe de LUZ: tudo de argila branca.
    argila = bpy.data.materials.get("argila_passe_luz")
    if argila is None:
        argila = bpy.data.materials.new("argila_passe_luz")
        try:
            argila.use_nodes = True
        except Exception:
            pass
        argila.node_tree.nodes.get("Principled BSDF").inputs["Base Color"].default_value = (0.8, 0.8, 0.8, 1)
    bpy.context.view_layer.material_override = argila
    cena.cycles.samples = amostras
    cena.render.filepath = os.path.join(tmp, "luz.png")
    bpy.ops.render.render(write_still=True)
    luz = _ler_png(cena.render.filepath)

    # b) Passe de ID: cada material vira sua cor chapada.
    bpy.context.view_layer.material_override = None
    materiais.modo_id(True)
    cena.cycles.samples = 1     # emissão chapada não tem ruído: 1 amostra basta
    cena.render.filepath = os.path.join(tmp, "id.png")
    bpy.ops.render.render(write_still=True)
    ids = _ler_png(cena.render.filepath)
    materiais.modo_id(False)
    shutil.rmtree(tmp, ignore_errors=True)   # apaga os PNGs intermediários

    # c) Junta os dois.
    alfa = ids[..., 3] >= 0.5
    r = np.round(ids[..., 0] * 255 / 8).astype(int) - 1
    g = np.round(ids[..., 1] * 255 / 8).astype(int) - 1
    indice = np.clip(g * 31 + r, 0, len(materiais.lista) - 1)
    # Luminância (quanto de luz): média ponderada do RGB, como o olho vê.
    lum = luz[..., 0] * 0.2126 + luz[..., 1] * 0.7152 + luz[..., 2] * 0.0722
    degrau = np.digitize(lum, DEGRAUS_LUZ)          # 0, 1, 2 ou 3
    if os.environ.get("DEBUG_LUZ"):
        hist, _ = np.histogram(lum[alfa], bins=20, range=(0, 1))
        print("[luz]", angulo, " ".join(str(v) for v in hist))
    rampas = np.array(materiais.rampas())           # (materiais, 4 tons, 3)
    saida = np.zeros(ids.shape, dtype=np.float32)
    saida[..., :3] = rampas[indice, degrau]
    saida[..., 3] = alfa
    saida[~alfa] = 0
    # Guardamos também o índice do material e o degrau, para o contorno.
    return saida, np.where(alfa, indice, -1), degrau


def contorno(arr, indice, materiais, escurecer=0.55):
    """Contorno seletivo de 1 px por FORA da silhueta.

    Em vez de preto, cada pixel do contorno pega a sombra funda do
    material vizinho, ainda mais escura. Assim a borda do casaco é um
    azul-marinho escuro e a borda da mão é um marrom escuro: a silhueta
    fica recortada contra o fundo sem virar um bloco preto."""
    h, w, _ = arr.shape
    alfa = arr[..., 3] > 0
    rampas = materiais.rampas()
    saida = arr.copy()
    for y in range(h):
        for x in range(w):
            if alfa[y, x]:
                continue
            viz = []
            for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                yy, xx = y + dy, x + dx
                if 0 <= yy < h and 0 <= xx < w and alfa[yy, xx]:
                    viz.append(indice[yy, xx])
            if viz:
                m = max(set(viz), key=viz.count)
                saida[y, x, :3] = cor_contorno(rampas[m][0], escurecer)
                saida[y, x, 3] = 1.0
    return saida


def cor_contorno(sombra_funda, escurecer=0.55):
    """Cor do contorno a partir da sombra funda do material."""
    return np.clip(np.asarray(sombra_funda) * escurecer + COR_SOMBRA * 0.25, 0, 1)


def srgb_para_lab(rgb):
    """RGB sRGB (0–1) -> CIELAB (o mesmo do menu). No Lab, a distância entre
    duas cores é parecida com a diferença que o olho percebe."""
    rgb = np.asarray(rgb, dtype=np.float64)
    lin = srgb_para_linear(rgb)
    m = np.array([[0.4124, 0.3576, 0.1805],
                  [0.2126, 0.7152, 0.0722],
                  [0.0193, 0.1192, 0.9505]])
    xyz = lin @ m.T / np.array([0.9505, 1.0, 1.089])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]),
                     200 * (f[..., 1] - f[..., 2])], axis=-1)


def unificar_paleta(imagens, materiais, max_cores):
    """Reduz TODAS as imagens de um personagem a UMA paleta fixa de no
    máximo 'max_cores' cores.

    As rampas geram 4 tons por material, e muitos tons escuros de
    materiais diferentes ficam quase iguais (a sombra da calça azul-marinho
    e a do quepe, por exemplo). A ideia é juntar cores quase iguais:
      1. conta quantos pixels usam cada cor;
      2. percorre as cores da mais usada para a menos usada; cada uma
         entra na paleta, a não ser que já exista uma cor da paleta a
         menos de 'limite' de distância no Lab — aí ela vira essa cor;
      3. se ainda sobrar cor demais, aumenta o limite e repete.
    As cores de detalhe (modo 'plano' e 'brilho': olhos, distintivo,
    lente) entram primeiro e nunca são trocadas.
    Devolve as imagens convertidas e a paleta (lista de cores 0–255)."""
    protegidas = [tuple(np.round(hex_para_rgb(hx) * 255).astype(int))
                  for _, hx, modo, _ in materiais.lista if modo != "normal"]
    contagem = {}
    for arr in imagens:
        for cor in map(tuple, np.round(arr[arr[..., 3] > 0][:, :3] * 255).astype(int)):
            contagem[cor] = contagem.get(cor, 0) + 1
    ordem = [cor for cor in protegidas if cor in contagem]
    ordem += sorted((cor for cor in contagem if cor not in ordem), key=lambda cor: -contagem[cor])
    lab = {cor: srgb_para_lab(np.array(cor) / 255) for cor in ordem}
    limite = 0.0
    while True:
        paleta = []
        for cor in ordem:
            if cor in protegidas or all(np.linalg.norm(lab[cor] - lab[p]) > limite for p in paleta):
                paleta.append(cor)
        if len(paleta) <= max_cores:
            break
        limite += 0.5
    print(f"[paleta] {len(contagem)} cores -> {len(paleta)} (juntando cores a menos de {limite:.1f} no Lab)")
    return aplicar_paleta(imagens, paleta), paleta


def aplicar_paleta(imagens, paleta):
    """Leva cada pixel das imagens para a cor mais próxima (no Lab) de uma
    paleta que já existe. Serve para desenhar um sprite novo com a mesma
    paleta dos antigos, sem mudar as cores deles."""
    pal = np.array(paleta, dtype=np.float64) / 255
    pal_lab = srgb_para_lab(pal)
    saida = []
    for arr in imagens:
        novo = arr.copy()
        opaco = arr[..., 3] > 0
        px_lab = srgb_para_lab(arr[opaco][:, :3])
        dist = ((px_lab[:, None, :] - pal_lab[None, :, :]) ** 2).sum(axis=2)
        novo[opaco, :3] = pal[dist.argmin(axis=1)]
        saida.append(novo)
    return saida


def paleta_usada(*imagens):
    """Lista (ordenada por brilho) das cores que aparecem nas imagens."""
    cores = set()
    for arr in imagens:
        opaco = arr[arr[..., 3] > 0][:, :3]
        for c in np.round(opaco * 255).astype(int):
            cores.add(tuple(c))
    return sorted(cores, key=lambda c: 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2])


def montar_folha(linhas, espaco=8, amostra=6):
    """Junta vistas lado a lado numa folha de referência.
    linhas = lista de listas de imagens (cada lista vira uma linha).
    Embaixo, uma faixa com a paleta usada (quadradinhos de 'amostra' px)."""
    alt_linha = max(im.shape[0] for linha in linhas for im in linha)
    larg = max(sum(im.shape[1] for im in linha) + espaco * (len(linha) + 1) for linha in linhas)
    cores = paleta_usada(*[im for linha in linhas for im in linha])
    por_linha = max(1, (larg - espaco) // (amostra + 1))
    linhas_paleta = math.ceil(len(cores) / por_linha)
    alt = espaco + len(linhas) * (alt_linha + espaco) + linhas_paleta * (amostra + 1) + espaco
    folha = np.zeros((alt, larg, 4), dtype=np.float32)
    y = espaco
    for linha in linhas:
        x = espaco
        for im in linha:
            h, w, _ = im.shape
            folha[y + alt_linha - h:y + alt_linha, x:x + w] = im
            x += w + espaco
        y += alt_linha + espaco
    for i, c in enumerate(cores):
        yy = y + (i // por_linha) * (amostra + 1)
        xx = espaco + (i % por_linha) * (amostra + 1)
        folha[yy:yy + amostra, xx:xx + amostra, :3] = np.array(c) / 255
        folha[yy:yy + amostra, xx:xx + amostra, 3] = 1
    return folha


def salvar_blend(caminho, raiz, angulo=35):
    """Salva a cena montada (sem backup .blend1), com o personagem em 3/4."""
    raiz.rotation_euler = (0, 0, math.radians(angulo))
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=caminho)


# ---------------------------------------------------------------------------
# 7. Personagem em pé: caminhada, respiração e retrato
# ---------------------------------------------------------------------------
#
# Gabriel, Clarice e Zane têm o mesmo conjunto de sprites de jogo, com o
# mesmo tamanho: cinco vistas, a caminhada e a respiração em cada uma, e os
# retratos da caixa de diálogo. Para isso, o esqueleto dos três tem as
# mesmas juntas, com os mesmos nomes: Quadril, Tronco, Cabeca e, de cada
# lado (Dir/Esq), PernaXQuadril, PernaXJoelho, PernaXTornozelo, BracoXOmbro
# e BracoXCotovelo.

# Resolução dobrada (docs/decisoes.md): os sprites de jogo saem com o dobro
# de pixels (96 x 112, 2 x 27,4 px por metro) e o Godot mostra com escala
# 0,5. O jogo desenha na resolução da janela (stretch "canvas_items"), então
# o personagem ocupa o mesmo espaço na tela, mas com o dobro de detalhe.
RESOLUCAO_2X = 2
QUADRO_JOGO_2X = (QUADRO_JOGO[0] * RESOLUCAO_2X, QUADRO_JOGO[1] * RESOLUCAO_2X)
PX_POR_M_JOGO_2X = PX_POR_M_JOGO * RESOLUCAO_2X
PE_JOGO_2X = PE_JOGO_PX * RESOLUCAO_2X

# Vistas dos sprites de jogo: (nome, giro do modelo em graus). 0 = de
# frente, 90 = de lado olhando para a direita, 180 = de costas; para a
# esquerda, o Godot espelha o sprite. 3/4 de costas (145°) é o espelho do
# 3/4 de frente (35°) em relação ao lado (90°): 90 - 55 e 90 + 55.
VISTAS_JOGO = (("lado", 90), ("frente", 0), ("tres_quartos", 35), ("costas", 180),
               ("tres_quartos_costas", 145))
QUADROS_ANDAR = 12   # quadros do ciclo de caminhada (dois passos)
QUADROS_PARADO = 8   # quadros do ciclo de respiração

# Retrato da caixa de diálogo: 80 x 80 px (mostrado em 40 x 40), câmera
# reta na altura do rosto, 176 px por metro (o rosto ocupa quase o retrato
# inteiro), virado 24 graus para a direita (para o texto da caixa).
QUADRO_RETRATO = (80, 80)
PX_POR_M_RETRATO = 176
GIRO_RETRATO = 24


def guardar_pose():
    """Guarda a rotação e a posição de todas as juntas, para voltar à pose
    parada depois de renderizar uma animação."""
    return {o.name: (tuple(o.rotation_euler), tuple(o.location))
            for o in bpy.data.objects if o.type == 'EMPTY'}


def restaurar_pose(pose):
    for nome, (rot, pos) in pose.items():
        obj = bpy.data.objects[nome]
        obj.rotation_euler = rot
        obj.location = pos


# Caminhada
# ---------
# Um ciclo de caminhada são DOIS passos: a perna direita vai à frente, depois
# a esquerda. Chamamos de fase (φ) o ponto do ciclo, de 0 a 360 graus, e
# cada junta segue uma onda seno dessa fase:
#
#   coxa   = -coxa · sen(φ)              a perna balança para a frente e
#                                        para trás (ângulo negativo = frente);
#                                        a outra perna usa φ + 180°, o oposto
#   joelho = dobra só enquanto a perna vem para a frente no ar, que é
#            quando cos(φ) > 0 (a coxa está indo para a frente)
#   ombro  = o braço balança ao contrário da perna do mesmo lado
#   quadril desce um pouco quando as pernas estão abertas (sen² φ = 1):
#            é o "sobe e desce" que dá peso ao andar
#
# Com 12 quadros, cada quadro avança 30° na fase. Os valores padrão são os
# do Gabriel; cada personagem pode passar os seus (o jeito de andar dele).

def pose_andar(parado, fase, coxa=22, joelho=55, braco=16, descida=0.037):
    """Coloca o personagem na pose da caminhada para a fase dada (em graus).
    Os ângulos somam por cima da pose parada (a postura de cada um).
    coxa, joelho e braco são as amplitudes em graus; descida é quanto o
    quadril desce, em metros (0,037 m = 1 px no sprite de 48 px)."""
    def girar(nome, graus_x):
        rot, _ = parado[nome]
        bpy.data.objects[nome].rotation_euler = (rot[0] + math.radians(graus_x), rot[1], rot[2])

    for perna, desloc in (("PernaDir", 0), ("PernaEsq", 180)):
        phi = math.radians(fase + desloc)
        giro_coxa = -coxa * math.sin(phi)
        giro_joelho = joelho * max(0.0, math.cos(phi)) ** 1.5
        girar(f"{perna}Quadril", giro_coxa)
        girar(f"{perna}Joelho", giro_joelho)
        # O tornozelo desfaz o giro da coxa e do joelho: o pé fica reto.
        girar(f"{perna}Tornozelo", -giro_coxa - giro_joelho)
    for lado, desloc in (("BracoDir", 0), ("BracoEsq", 180)):
        phi = math.radians(fase + desloc)
        girar(f"{lado}Ombro", braco * math.sin(phi))
        girar(f"{lado}Cotovelo", -10 * max(0.0, -math.sin(phi)))
    _, pos = parado["Quadril"]
    subida = descida * math.sin(math.radians(fase)) ** 2
    bpy.data.objects["Quadril"].location = (pos[0], pos[1], pos[2] - subida)


# Parado (respirando)
# -------------------
# Num sprite de 48 px, o menor movimento visível é 1 pixel, então a
# respiração é o tronco inteiro (com a cabeça e os braços) subindo 1 px ao
# puxar o ar, com as pernas paradas no chão. A cabeça pende um pouco e
# volta, atrasada em relação ao peito.
#
#   subida = SUBIDA · (1 - cos φ) / 2     vai de 0 (fase 0) a 1 px (180°)
#
# Na fase 0 a subida é zero: o primeiro quadro é igual ao sprite parado.

def pose_parado(parado, fase, subida=0.037, balanco_cabeca=3):
    """Pose da respiração para a fase dada (em graus)."""
    phi = math.radians(fase)
    _, pos = parado["Tronco"]
    sobe = subida * (1 - math.cos(phi)) / 2
    bpy.data.objects["Tronco"].location = (pos[0], pos[1], pos[2] + sobe)
    rot, _ = parado["Cabeca"]
    # Atrasada 60° em relação ao peito: primeiro o peito sobe, depois a
    # cabeça acompanha. É esse atraso que faz parecer um corpo, não um bloco.
    pende = balanco_cabeca * (1 - math.cos(phi - math.radians(60))) / 2
    bpy.data.objects["Cabeca"].rotation_euler = (rot[0] + math.radians(pende), rot[1], rot[2])


def renderizar_vistas_jogo(cam, raiz, materiais, rotulo=""):
    """As cinco vistas de jogo na pose atual: {nome: imagem com contorno}."""
    saida = {}
    for nome, angulo in VISTAS_JOGO:
        img, ind, _ = renderizar_vista(cam, raiz, materiais, angulo, QUADRO_JOGO_2X, PX_POR_M_JOGO_2X, PE_JOGO_2X)
        if rotulo:
            linhas = img[..., 3].any(axis=1).nonzero()[0]
            print(f"[{rotulo}] {nome}: altura do corpo no sprite: {linhas[-1] - linhas[0] + 1} px (resolução {RESOLUCAO_2X}x)")
        saida[nome] = contorno(img, ind, materiais)
    return saida


def renderizar_ciclo(cam, raiz, materiais, pose, quadros, rotulo):
    """Uma animação em todas as vistas: chama pose(fase) para cada quadro
    (fase de 0 a 360 graus) e devolve {vista: [quadros]}."""
    saida = {nome: [] for nome, _ in VISTAS_JOGO}
    for q in range(quadros):
        pose(360 * q / quadros)
        for nome, img in renderizar_vistas_jogo(cam, raiz, materiais).items():
            saida[nome].append(img)
        print(f"[{rotulo}] quadro {q + 1}/{quadros}")
    return saida


def renderizar_retrato(cam, raiz, materiais):
    """Rosto e ombros na pose e na expressão atuais, com a câmera na altura
    do objeto "Rosto"."""
    altura_rosto = bpy.data.objects["Rosto"].matrix_world.translation.z

    def enquadrar_retrato(cam, largura_px, altura_px, px_por_m, pe_px):
        cena = bpy.context.scene
        cena.render.resolution_x = largura_px
        cena.render.resolution_y = altura_px
        cam.data.ortho_scale = largura_px / px_por_m
        cam.location = (0.0, -20.0, altura_rosto - 0.02)

    global enquadrar
    original = enquadrar
    enquadrar = enquadrar_retrato
    try:
        img, ind, _ = renderizar_vista(cam, raiz, materiais, GIRO_RETRATO, QUADRO_RETRATO, PX_POR_M_RETRATO, 0)
    finally:
        enquadrar = original
    return contorno(img, ind, materiais)


def salvar_sprites_jogo(pasta, nome, paleta, jogo, andar, parado):
    """Grava as vistas, as tiras de caminhada e as de respiração, já na
    paleta do personagem: <nome>_<vista>.png, <nome>_andar_<vista>.png e
    <nome>_parado_<vista>.png."""
    vistas = [n for n, _ in VISTAS_JOGO]
    for vista, img in zip(vistas, aplicar_paleta([jogo[v] for v in vistas], paleta)):
        salvar_png(img, os.path.join(pasta, f"{nome}_{vista}.png"))
    for prefixo, ciclo in (("andar", andar), ("parado", parado)):
        for vista, quadros in ciclo.items():
            tira = np.concatenate(aplicar_paleta(quadros, paleta), axis=1)
            salvar_png(tira, os.path.join(pasta, f"{nome}_{prefixo}_{vista}.png"))


def gerar_em_pe(nome, raiz, materiais, max_cores, expressoes, expressao, esconder_boca,
                passo=None, respirar=None):
    """O roteiro inteiro de um personagem em pé, depois de montado (com o
    "Rosto" já achatado): renderiza as vistas de jogo, a caminhada, a
    respiração, a folha de referência e os retratos, junta tudo numa paleta
    só e grava os PNGs em assets/sprites/personagens/<nome>/ e o modelo em
    <nome>.blend.

    expressoes é a lista de nomes dos retratos (a primeira é a de sempre);
    expressao(qual) arma o rosto e esconder_boca() tira a boca dos sprites
    de jogo (no sprite de 48 px ela vira um risco no queixo). passo e
    respirar são as amplitudes próprias do personagem para pose_andar e
    pose_parado."""
    pasta = os.path.join(PASTA_SPRITES, nome)
    expressao(expressoes[0])
    esconder_boca()
    cam = criar_camera()
    criar_luzes()
    os.makedirs(pasta, exist_ok=True)

    # Sprites de jogo: as cinco vistas, a caminhada e a respiração.
    jogo = renderizar_vistas_jogo(cam, raiz, materiais, nome)
    parado = guardar_pose()
    andar = renderizar_ciclo(cam, raiz, materiais, lambda fase: pose_andar(parado, fase, **(passo or {})),
                             QUADROS_ANDAR, f"{nome} andar")
    restaurar_pose(parado)
    respiracao = renderizar_ciclo(cam, raiz, materiais, lambda fase: pose_parado(parado, fase, **(respirar or {})),
                                  QUADROS_PARADO, f"{nome} parado")
    restaurar_pose(parado)

    # Folha de referência: frente, 3/4, lado e costas, em 128 px.
    vistas = []
    for angulo in (0, 35, 90, 180):
        img, ind, _ = renderizar_vista(cam, raiz, materiais, angulo, QUADRO_REF, PX_POR_M_REF, PE_REF_PX)
        vistas.append(contorno(img, ind, materiais))
    retratos = {}
    for qual in expressoes:
        expressao(qual)
        retratos[qual] = renderizar_retrato(cam, raiz, materiais)
    expressao(expressoes[0])
    esconder_boca()

    # Uma paleta só para tudo, calculada com o sprite de lado, a referência
    # e os retratos; as animações só usam essa paleta.
    todas = [jogo["lado"]] + vistas + list(retratos.values())
    convertidas, paleta = unificar_paleta(todas, materiais, max_cores)
    vistas = convertidas[1:5]
    retratos = dict(zip(retratos.keys(), convertidas[5:]))
    salvar_sprites_jogo(pasta, nome, paleta, jogo, andar, respiracao)
    for qual, img in retratos.items():
        salvar_png(img, os.path.join(pasta, f"{nome}_retrato_{qual}.png"))
    salvar_png(montar_folha([vistas, list(retratos.values())]), os.path.join(pasta, f"{nome}_referencia.png"))
    print(f"[{nome}] paleta:", " ".join(rgb_para_hex(np.array(cor) / 255) for cor in paleta))
    salvar_blend(os.path.join(PASTA_SCRIPT, f"{nome}.blend"), raiz)
    print(f"[{nome}] pronto")

"""Geometria de perto: curvas, peças montadas e teclado físico do notebook."""

import math

import bpy


def arredondar(objeto, raio=0.001, segmentos=4):
    bpy.context.view_layer.objects.active = objeto
    bisel = objeto.modifiers.new("BordasUsinadas", "BEVEL")
    bisel.width = raio
    bisel.segments = segmentos
    bisel.limit_method = "ANGLE"
    bisel.angle_limit = 0.6
    bisel.harden_normals = True
    bpy.ops.object.modifier_apply(modifier=bisel.name)
    for face in objeto.data.polygons:
        face.use_smooth = True
    normal = objeto.modifiers.new("NormaisDasFaces", "WEIGHTED_NORMAL")
    normal.keep_sharp = True
    normal.weight = 50
    bpy.ops.object.modifier_apply(modifier=normal.name)
    return objeto


class Modelador:
    def __init__(self, oficina):
        self.oficina = oficina
        self.m = oficina["m"]
        criar = oficina["material"]
        self.metal = criar("MetalNotebook", "#3c4550", rugosidade=0.4)
        self.metal.node_tree.nodes.get("Principled BSDF").inputs["Metallic"].default_value = 0.65
        self.plastico = criar("PlasticoNotebook", "#141a22", rugosidade=0.58)
        self.teclas = criar("TeclasNotebook", "#1a2029", rugosidade=0.5)
        self.borracha = criar("BorrachaNotebook", "#070a0e", rugosidade=0.85)
        self.legendas = criar("LegendaTeclas", "#abb7c4", rugosidade=0.65)
        self.ceramica = criar("CeramicaCaneca", "#b7b3a6", rugosidade=0.24)
        self.fonte = bpy.data.fonts.load(str(oficina["PASTA_PROJETO"] + "/assets/fontes/galmuri_7.ttf"))

    def caixa(self, nome, centro, tamanho, material, raio=0.001, giro=(0, 0)):
        objeto = self.oficina["caixa"](nome, centro, tamanho, material, inclinar=giro)
        segmentos = 2 if raio < 0.001 else (4 if raio <= 0.002 else 6)
        return arredondar(objeto, raio, segmentos)

    def cilindro(self, nome, centro, raio, altura, material, giro=(0, 0), lados=48):
        objeto = self.oficina["cilindro"](nome, centro, raio, altura, material, lados=lados, inclinar=giro)
        return arredondar(objeto, min(raio * 0.18, altura * 0.15), 3)

    def ponto(self, lateral, fundo, altura):
        return (-2.07 + fundo, 0.76 + altura, -0.2 - lateral)

    def ponto_tela(self, lateral, subida, espessura=0.0):
        angulo = math.radians(15)
        return self.ponto(lateral, -0.178 - math.sin(angulo) * subida + math.cos(angulo) * espessura,
                          0.026 + math.cos(angulo) * subida + math.sin(angulo) * espessura)

    def escrever_tecla(self, texto, lateral, fundo, altura):
        dados = bpy.data.curves.new("GravacaoDaTecla", "FONT")
        dados.body = texto
        dados.font = self.fonte
        dados.size = 0.006
        dados.align_x = "CENTER"
        dados.align_y = "CENTER"
        objeto = bpy.data.objects.new("Legenda_" + texto, dados)
        bpy.context.collection.objects.link(objeto)
        objeto.location = self.oficina["para_blender"](*self.ponto(lateral, fundo, altura))
        objeto.rotation_euler.z = math.pi / 2
        dados.materials.append(self.legendas)
        bpy.ops.object.select_all(action="DESELECT")
        objeto.select_set(True)
        bpy.context.view_layer.objects.active = objeto
        bpy.ops.object.convert(target="MESH")
        return bpy.context.object

    def notebook(self):
        for nome in ("Notebook", "TampaNotebook", "TelaNotebook"):
            bpy.data.objects.remove(bpy.data.objects[nome], do_unlink=True)
        partes = [
            self.caixa("CarcacaInferior", self.ponto(0, 0, 0.010), (0.39, 0.020, 0.558), self.plastico, 0.007),
            self.caixa("JuntaDaCarcaca", self.ponto(0, 0, 0.020), (0.387, 0.002, 0.554), self.borracha, 0.0008),
            self.caixa("DeckDeAluminio", self.ponto(0, 0, 0.023), (0.386, 0.006, 0.554), self.metal, 0.0025),
            self.caixa("RebaixoDoTeclado", self.ponto(0, -0.064, 0.0263), (0.207, 0.0015, 0.501), self.borracha, 0.0006),
            self.caixa("ContornoDoTrackpad", self.ponto(0, 0.115, 0.0265), (0.089, 0.0015, 0.18), self.borracha, 0.0006),
            self.caixa("TrackpadDeVidro", self.ponto(0, 0.115, 0.0273), (0.086, 0.001, 0.177), self.metal, 0.0004),
        ]
        for lado in (-1, 1):
            partes.append(self.cilindro("DobradicaMetalica", self.ponto(lado * 0.207, -0.179, 0.026),
                                          0.009, 0.079, self.metal, (90, 0), 64))
            partes.append(self.cilindro("TampaDaDobradica", self.ponto(lado * 0.249, -0.179, 0.026),
                                          0.0092, 0.003, self.plastico, (90, 0), 48))
        self.oficina["juntar"]("Notebook", partes)

        linhas = [
            "ESC F1 F2 F3 F4 F5 F6 F7 F8 F9 F10 F11 F12 DEL".split(),
            "` 1 2 3 4 5 6 7 8 9 0 - BK".split(),
            "TAB Q W E R T Y U I O P [ ] \\".split(),
            "CAP A S D F G H J K L ; ' ENT".split(),
            "SH Z X C V B N M , . / UP SH".split(),
        ]
        teclas, letras = [], []
        for linha, titulos in enumerate(linhas):
            fundo = -0.147 + linha * 0.034
            passo = 0.476 / len(titulos)
            for coluna, titulo in enumerate(titulos):
                lateral = -0.238 + passo * (coluna + 0.5)
                teclas.append(self.caixa("Tecla", self.ponto(lateral, fundo, 0.0307),
                                         (0.026, 0.007, passo - 0.004), self.teclas, 0.002))
                letras.append(self.escrever_tecla(titulo, lateral, fundo - 0.001, 0.03425))
        for titulo, lateral, largura in (("CTRL", -0.216, 0.038), ("FN", -0.174, 0.034),
                                         ("ALT", -0.135, 0.036), ("", -0.007, 0.207),
                                         ("ALT", 0.124, 0.034), ("<", 0.164, 0.032),
                                         ("V", 0.201, 0.032), (">", 0.238, 0.032)):
            teclas.append(self.caixa("TeclaInferior", self.ponto(lateral, 0.023, 0.0307),
                                     (0.024, 0.007, largura), self.teclas, 0.002))
            if titulo:
                letras.append(self.escrever_tecla(titulo, lateral, 0.023, 0.03425))
        self.oficina["juntar"]("TeclasIndividuais", teclas)
        self.oficina["juntar"]("LegendasDoTeclado", letras)

        pequenos = []
        for lado in (-1, 1):
            for i in range(21):
                pequenos.append(self.caixa("SaidaDeAr", self.ponto(lado * 0.279, -0.138 + i * 0.009, 0.011),
                                           (0.004, 0.006, 0.001), self.borracha, 0.0004))
            for fundo in (0.075, 0.123):
                pequenos.append(self.caixa("PortaUsb", self.ponto(lado * 0.280, fundo, 0.013),
                                           (0.025, 0.008, 0.0015), self.borracha, 0.0006))
                pequenos.append(self.caixa("ContatoUsb", self.ponto(lado * 0.281, fundo, 0.013),
                                           (0.018, 0.002, 0.001), self.metal, 0.0003))
            for i in range(12):
                pequenos.append(self.cilindro("FuroDoAltoFalante", self.ponto(lado * 0.26, -0.13 + i * 0.013, 0.0265),
                                               0.0011, 0.0006, self.borracha, lados=12))
        pequenos.append(self.caixa("LedDeEnergia", self.ponto(0.225, 0.1948, 0.012),
                                   (0.0008, 0.0015, 0.007), self.m["ciano"], 0.0003))
        self.oficina["juntar"]("ConectoresEVentilacao", pequenos)

        self.caixa("TampaNotebook", self.ponto_tela(0, 0.177), (0.012, 0.354, 0.55),
                   self.plastico, 0.005, (0, 15))
        self.caixa("MolduraInterna", self.ponto_tela(0, 0.177, 0.0065), (0.002, 0.331, 0.524),
                   self.borracha, 0.0008, (0, 15))
        self.oficina["quad"]("TelaNotebook", self.ponto_tela(-0.24, 0.027, 0.008),
                             self.ponto_tela(0.24, 0.027, 0.008), self.ponto_tela(0.24, 0.327, 0.008),
                             self.ponto_tela(-0.24, 0.327, 0.008), self.m["tela_notebook"])
        for lateral, raio, material in ((0, 0.0023, self.m["metal"]), (0, 0.0015, self.borracha),
                                        (0.011, 0.00065, self.legendas)):
            posicao = self.ponto_tela(lateral, 0.341, 0.0089 if material != self.borracha else 0.010)
            objeto = self.oficina["esfera"]("Webcam", posicao, raio, material)
            for face in objeto.data.polygons:
                face.use_smooth = True

    def torneado(self, nome, centro, perfil, material, lados=72):
        # Superfície de revolução: (r,h) -> (r cos a, h, r sin a), com costura fechada.
        vertices, faces = [], []
        for raio, altura in perfil:
            for i in range(lados):
                angulo = i * math.tau / lados
                vertices.append(self.oficina["para_blender"](centro[0] + raio * math.cos(angulo),
                                 centro[1] + altura, centro[2] + raio * math.sin(angulo)))
        for linha in range(len(perfil) - 1):
            for i in range(lados):
                a, b = linha * lados + i, linha * lados + (i + 1) % lados
                faces.append((a, a + lados, b + lados, b))
        malha = bpy.data.meshes.new(nome)
        malha.from_pydata(vertices, [], faces)
        malha.materials.append(material)
        objeto = bpy.data.objects.new(nome, malha)
        bpy.context.collection.objects.link(objeto)
        for face in malha.polygons:
            face.use_smooth = True
        return objeto

    def caneca(self):
        bpy.data.objects.remove(bpy.data.objects["Caneca"], do_unlink=True)
        centro = (-2.16, 0.76, 0.32)
        perfil = [(0.001, 0.002), (0.028, 0.002), (0.034, 0.004), (0.036, 0.009),
                  (0.039, 0.085), (0.040, 0.096), (0.0398, 0.099), (0.0385, 0.100),
                  (0.037, 0.099), (0.036, 0.096), (0.035, 0.018), (0.031, 0.013), (0.001, 0.013)]
        self.torneado("CanecaCeramica", centro, perfil, self.ceramica)
        self.cilindro("Cafe", (centro[0], 0.851, centro[2]), 0.035, 0.001, self.m["cafe"], lados=72)
        vertices, faces = [], []
        # Alça tubular elíptica: anel de 64 seções, cada uma com 12 lados.
        for i in range(64):
            a = i * math.tau / 64
            for j in range(12):
                b = j * math.tau / 12
                vertices.append(self.oficina["para_blender"](centro[0] + 0.005 * math.sin(b),
                    0.811 + (0.030 + 0.005 * math.cos(b)) * math.sin(a),
                    centro[2] + 0.043 + (0.024 + 0.005 * math.cos(b)) * math.cos(a)))
        for i in range(64):
            for j in range(12):
                faces.append((i * 12 + j, i * 12 + (j + 1) % 12,
                              ((i + 1) % 64) * 12 + (j + 1) % 12, ((i + 1) % 64) * 12 + j))
        malha = bpy.data.meshes.new("AlcaDaCaneca")
        malha.from_pydata(vertices, [], faces)
        malha.materials.append(self.ceramica)
        objeto = bpy.data.objects.new("AlcaDaCaneca", malha)
        bpy.context.collection.objects.link(objeto)
        for face in malha.polygons:
            face.use_smooth = True

    def cacto(self):
        bpy.data.objects.remove(bpy.data.objects["Cacto"], do_unlink=True)
        centro = (-2.42, 1.045, -0.58)
        perfil = [(0.026, 0), (0.029, 0.004), (0.04, 0.058), (0.044, 0.062),
                  (0.044, 0.069), (0.041, 0.072), (0.037, 0.072), (0.037, 0.061), (0.027, 0.01)]
        self.torneado("VasoDeTerracota", centro, perfil, self.m["vaso"])
        self.cilindro("TerraDoCacto", (centro[0], centro[1] + 0.062, centro[2]),
                       0.036, 0.002, self.m["terra"], lados=64)
        vertices, faces = [], []
        lados, aneis = 64, 25
        for j in range(aneis):
            h = j / (aneis - 1)
            tampa = math.sqrt(max(0.002, 1 - max(0, (h - 0.78) / 0.22) ** 2))
            for i in range(lados):
                a = i * math.tau / lados
                r = 0.027 * tampa * (1 + 0.055 * math.cos(a * 9))
                vertices.append(self.oficina["para_blender"](centro[0] + r * math.cos(a),
                    centro[1] + 0.06 + h * 0.16, centro[2] + r * math.sin(a)))
        for j in range(aneis - 1):
            for i in range(lados):
                a, b = j * lados + i, j * lados + (i + 1) % lados
                faces.append((a, a + lados, b + lados, b))
        malha = bpy.data.meshes.new("CactoComGomos")
        malha.from_pydata(vertices, [], faces)
        malha.materials.append(self.m["folha"])
        objeto = bpy.data.objects.new("CactoComGomos", malha)
        bpy.context.collection.objects.link(objeto)
        for face in malha.polygons:
            face.use_smooth = True
        for lado in (-1, 1):
            curva = bpy.data.curves.new("BracoDoCacto", "CURVE")
            curva.dimensions = "3D"
            curva.bevel_depth = 0.010
            curva.bevel_resolution = 5
            curva.resolution_u = 12
            caminho = curva.splines.new("BEZIER")
            caminho.bezier_points.add(2)
            for ponto, (dz, h) in zip(caminho.bezier_points, ((0.018, 0.12), (0.047, 0.135), (0.05, 0.16))):
                ponto.co = self.oficina["para_blender"](centro[0], centro[1] + h, centro[2] + lado * dz)
                ponto.handle_left_type = "AUTO"
                ponto.handle_right_type = "AUTO"
            curva.use_fill_caps = True
            curva.materials.append(self.m["folha"])
            objeto = bpy.data.objects.new("BracoDoCacto", curva)
            bpy.context.collection.objects.link(objeto)
            bpy.ops.object.select_all(action="DESELECT")
            objeto.select_set(True)
            bpy.context.view_layer.objects.active = objeto
            bpy.ops.object.convert(target="MESH")


def detalhar(oficina):
    for nome in ("Escrivaninha", "LivrosDaMesa", "Luminaria", "Janela", "Cortina", "PoteDeLapis"):
        arredondar(bpy.data.objects[nome], 0.0012, 4)
    modelador = Modelador(oficina)
    modelador.notebook()
    modelador.caneca()
    modelador.cacto()
    for nome in ("Luminaria", "PoteDeLapis"):
        objeto = bpy.data.objects[nome]
        for i, material in enumerate(objeto.data.materials):
            if material and material.name in ("Notebook", "Metal"):
                objeto.data.materials[i] = modelador.metal

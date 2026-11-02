class_name KitDaNave
extends Node3D

const PASTA := "res://assets/sprites/cenario/hora_morta/%s.png"
const COR_FRIA := Color(0.55, 0.78, 1.0)
const COR_QUENTE := Color(1.0, 0.72, 0.42)
const COR_DAS_FAIXAS := Color(1.0, 0.68, 0.32)
const BRILHO_DAS_FAIXAS := 1.3
const LARGURA_DA_PORTA := 1.5
const ALTURA_DA_PORTA := 2.1
const ESPESSURA_DA_COLISAO := 0.2
const MEIA_LARGURA_DA_JANELA := 1.3
const MEIA_ALTURA_DA_JANELA := 0.725
const CENTRO_DA_JANELA_Y := 1.325
const RAIO_DA_JANELA := 0.38
const JANELA_PADRAO := Vector4(MEIA_LARGURA_DA_JANELA, MEIA_ALTURA_DA_JANELA, CENTRO_DA_JANELA_Y, RAIO_DA_JANELA)
const LARGURA_DA_MOLDURA := 0.1
const SALIENCIA_DA_MOLDURA := 0.07
const FUNDO_DA_JANELA := 0.26
const PONTOS_POR_CANTO := 13

static var _materiais: Dictionary = {}

@export var segura := false
@export var tem_janelas := false
@export var acende_com_a_energia := false

var lampadas: Array[LampadaDaNave] = []
var limites := AABB()
var corpo: StaticBody3D
var material_das_faixas: StandardMaterial3D


func _ready() -> void:
	material_das_faixas = cor_acesa(COR_DAS_FAIXAS, BRILHO_DAS_FAIXAS)
	corpo = StaticBody3D.new()
	add_child(corpo)
	_montar()


func _montar() -> void:
	pass


func contem(lugar: Vector3) -> bool:
	return limites.has_point(to_local(lugar))


func cortar_energia() -> void:
	material_das_faixas.emission_energy_multiplier = 0.0
	for lampada in lampadas:
		lampada.cortar_energia()


func religar() -> void:
	material_das_faixas.emission_energy_multiplier = BRILHO_DAS_FAIXAS
	for lampada in lampadas:
		lampada.religar()


func receber_energia() -> void:
	if not acende_com_a_energia:
		return
	for lampada in lampadas:
		lampada.acender_de_vez()


func definir_alarme(ligado: bool) -> void:
	for lampada in lampadas:
		lampada.definir_alarme(ligado)


func material(nome: String) -> Material:
	if _materiais.is_empty():
		_criar_materiais()
	return _materiais[nome]


func _criar_materiais() -> void:
	_materiais["parede"] = metal("painel_nave", 1.3)
	_materiais["parede_escura"] = metal("painel_nave", 1.0, Color(0.6, 0.64, 0.66))
	_materiais["chapa"] = metal("chao_chapa", 1.2)
	_materiais["grade"] = metal("chao_grade", 0.8)
	_materiais["forro"] = metal("teto_dutos", 1.2)
	_materiais["costela"] = metal("painel_nave", 0.55, Color(0.62, 0.66, 0.68), 0.55, 0.3)
	_materiais["perigo"] = metal("faixa_perigo", 0.5)
	_materiais["moldura"] = cor_lisa(Color(0.3, 0.33, 0.35), 0.45)
	_materiais["reflexo"] = cor_lisa(Color(0.42, 0.46, 0.5), 0.3)
	_materiais["borracha"] = cor_lisa(Color(0.04, 0.04, 0.05), 0.8)
	_materiais["veludo"] = cor_lisa(Color(0.22, 0.06, 0.08), 0.95)
	_materiais["cabo_preto"] = cor_lisa(Color(0.08, 0.08, 0.09), 0.55)
	_materiais["cabo_azul"] = cor_lisa(Color(0.1, 0.16, 0.28), 0.55)
	_materiais["cabo_vermelho"] = cor_lisa(Color(0.42, 0.14, 0.06), 0.55)
	_materiais["cano"] = cor_lisa(Color(0.42, 0.45, 0.47), 0.5)
	var corrimao := cor_lisa(Color(0.46, 0.32, 0.14), 0.4)
	corrimao.metallic = 0.7
	_materiais["corrimao"] = corrimao
	var vidro := StandardMaterial3D.new()
	vidro.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	vidro.albedo_color = Color(0.5, 0.65, 0.85, 0.05)
	vidro.roughness = 0.05
	vidro.cull_mode = BaseMaterial3D.CULL_DISABLED
	_materiais["vidro"] = vidro


func metal(nome: String, metros: float, tinta: Color = Color.WHITE, rugosidade: float = 0.62, metalico: float = 0.35) -> StandardMaterial3D:
	var novo := StandardMaterial3D.new()
	novo.albedo_texture = load(PASTA % nome)
	novo.albedo_color = tinta
	novo.texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS_ANISOTROPIC
	novo.uv1_triplanar = true
	novo.uv1_world_triplanar = true
	novo.uv1_scale = Vector3.ONE / metros
	novo.roughness = rugosidade
	novo.metallic = metalico
	novo.cull_mode = BaseMaterial3D.CULL_DISABLED
	var caminho_normal := PASTA % (nome + "_n")
	if ResourceLoader.exists(caminho_normal):
		novo.normal_enabled = true
		novo.normal_texture = load(caminho_normal)
		novo.normal_scale = 0.9
	return novo


func cor_lisa(cor: Color, rugosidade: float) -> StandardMaterial3D:
	var novo := StandardMaterial3D.new()
	novo.albedo_color = cor
	novo.roughness = rugosidade
	novo.cull_mode = BaseMaterial3D.CULL_DISABLED
	return novo


func cor_acesa(cor: Color, brilho: float) -> StandardMaterial3D:
	var novo := cor_lisa(cor * 0.4, 0.5)
	novo.emission_enabled = true
	novo.emission = cor
	novo.emission_energy_multiplier = brilho
	return novo


func parede(inicio: Vector3, fim: Vector3, altura: float, portas: PackedFloat32Array, acabamento: Material) -> void:
	var direcao := (fim - inicio).normalized()
	var comprimento := inicio.distance_to(fim)
	var ordenadas := portas.duplicate()
	ordenadas.sort()
	var cursor := 0.0
	for deslocamento in ordenadas:
		var centro := comprimento / 2.0 + deslocamento
		_trecho(inicio, direcao, cursor, centro - LARGURA_DA_PORTA / 2.0, 0.0, altura, acabamento)
		_trecho(inicio, direcao, centro - LARGURA_DA_PORTA / 2.0, centro + LARGURA_DA_PORTA / 2.0, ALTURA_DA_PORTA, altura, acabamento)
		cursor = centro + LARGURA_DA_PORTA / 2.0
	_trecho(inicio, direcao, cursor, comprimento, 0.0, altura, acabamento)


func _trecho(inicio: Vector3, direcao: Vector3, de: float, ate: float, y0: float, y1: float, acabamento: Material) -> void:
	if ate - de <= 0.001:
		return
	var a := inicio + direcao * de
	var b := inicio + direcao * ate
	quadrilatero(a + Vector3.UP * y0, b + Vector3.UP * y0, b + Vector3.UP * y1, a + Vector3.UP * y1, acabamento)
	var eixo := Vector3(absf(direcao.x), 0.0, absf(direcao.z))
	var espessura := Vector3.ONE - eixo - Vector3.UP
	var tamanho := eixo * (ate - de) + espessura * ESPESSURA_DA_COLISAO + Vector3.UP * (y1 - y0)
	forma(tamanho, (a + b) / 2.0 + Vector3.UP * (y0 + y1) / 2.0)


func janela_em_x(x: float, z: float, comprimento_do_vao: float, y_base: float, y_topo: float, medidas: Vector4 = JANELA_PADRAO) -> void:
	var centro_y := medidas.z
	var furo := _contorno_da_janela(0.0, medidas)
	var borda := _borda_em_volta(comprimento_do_vao / 2.0, y_topo - centro_y, centro_y - y_base, medidas)
	faixa(_na_parede(borda, x, z, centro_y), _na_parede(furo, x, z, centro_y), material("parede"))
	var moldura := _contorno_da_janela(LARGURA_DA_MOLDURA, medidas)
	var x_da_frente := x - SALIENCIA_DA_MOLDURA
	var x_do_fundo := x + FUNDO_DA_JANELA
	faixa(_na_parede(moldura, x, z, centro_y), _na_parede(moldura, x_da_frente, z, centro_y), material("moldura"))
	faixa(_na_parede(moldura, x_da_frente, z, centro_y), _na_parede(furo, x_da_frente, z, centro_y), material("moldura"))
	faixa(_na_parede(furo, x_da_frente, z, centro_y), _na_parede(furo, x_do_fundo, z, centro_y), material("reflexo"))
	poligono(_na_parede(furo, x_do_fundo, z, centro_y), material("vidro"), false)
	if medidas == JANELA_PADRAO:
		_ferragens_da_janela(x, z)
	forma(Vector3(ESPESSURA_DA_COLISAO, y_topo - y_base, comprimento_do_vao), Vector3(x, (y_base + y_topo) / 2.0, z))


func _ferragens_da_janela(x: float, z: float) -> void:
	var dentro := x - 0.1
	tubo(0.016, 1.0, Vector3(dentro, CENTRO_DA_JANELA_Y, z + MEIA_LARGURA_DA_JANELA + 0.28), material("corrimao"), Vector3.UP)
	for y: float in [0.5, -0.5]:
		bloco(Vector3(0.1, 0.03, 0.03), Vector3(dentro + 0.05, CENTRO_DA_JANELA_Y + y, z + MEIA_LARGURA_DA_JANELA + 0.28), material("costela"))
	var alto := CENTRO_DA_JANELA_Y + MEIA_ALTURA_DA_JANELA + 0.06
	bloco(Vector3(0.02, 0.05, 0.7), Vector3(x - 0.01, alto, z - 0.3), material("perigo"))
	bloco(Vector3(0.05, 0.04, 0.42), Vector3(x - 0.03, 0.42, z + 0.2), material("costela"))
	bloco(Vector3(0.09, 0.022, 0.28), Vector3(x - 0.05, 0.42, z + 0.2), material("corrimao"))


func _contorno_da_janela(folga: float, medidas: Vector4) -> PackedVector2Array:
	var mz := medidas.x + folga
	var my := medidas.y + folga
	var raio := medidas.w + folga
	var pontos := PackedVector2Array()
	var centros: Array[Vector2] = [Vector2(mz - raio, my - raio), Vector2(-mz + raio, my - raio), Vector2(-mz + raio, -my + raio), Vector2(mz - raio, -my + raio)]
	for canto in 4:
		for passo in PONTOS_POR_CANTO:
			var angulo := PI / 2.0 * (float(canto) + float(passo) / float(PONTOS_POR_CANTO - 1))
			pontos.append(centros[canto] + Vector2(cos(angulo), sin(angulo)) * raio)
	return pontos


func _borda_em_volta(mz: float, cima: float, baixo: float, medidas: Vector4) -> PackedVector2Array:
	var reta_z := medidas.x - medidas.w
	var reta_y := medidas.y - medidas.w
	var cantos: Array = [
		[Vector2(mz, reta_y), Vector2(mz, cima), Vector2(reta_z, cima)],
		[Vector2(-reta_z, cima), Vector2(-mz, cima), Vector2(-mz, reta_y)],
		[Vector2(-mz, -reta_y), Vector2(-mz, -baixo), Vector2(-reta_z, -baixo)],
		[Vector2(reta_z, -baixo), Vector2(mz, -baixo), Vector2(mz, -reta_y)],
	]
	var pontos := PackedVector2Array()
	var metade := (PONTOS_POR_CANTO - 1) / 2
	for canto: Array in cantos:
		for passo in PONTOS_POR_CANTO:
			if passo <= metade:
				pontos.append((canto[0] as Vector2).lerp(canto[1], float(passo) / float(metade)))
			else:
				pontos.append((canto[1] as Vector2).lerp(canto[2], float(passo - metade) / float(metade)))
	return pontos


func _na_parede(contorno: PackedVector2Array, x: float, z: float, centro_y: float) -> PackedVector3Array:
	var pontos := PackedVector3Array()
	for ponto in contorno:
		pontos.append(Vector3(x, centro_y + ponto.y, z + ponto.x))
	return pontos


func lampada_de_teto(lugar: Vector3, estado: int, alcance: float, cor: Color = COR_FRIA, comprimento: float = 1.5) -> LampadaDaNave:
	var vidro := cor_acesa(cor, 0.0)
	bloco(Vector3(0.42, 0.05, comprimento), lugar, material("costela"))
	var luz := bloco(Vector3(0.28, 0.02, comprimento - 0.16), lugar - Vector3(0.0, 0.03, 0.0), vidro)
	luz.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	var lampada := LampadaDaNave.new()
	lampada.estado = estado as LampadaDaNave.Estado
	lampada.materiais_do_vidro = [vidro]
	lampada.alcance = alcance
	lampada.position = lugar - Vector3(0.0, 0.3, 0.0)
	lampada.light_color = cor
	lampada.light_energy = 1.7
	lampada.omni_range = alcance * 2.4
	lampada.omni_attenuation = 1.2
	add_child(lampada)
	lampadas.append(lampada)
	return lampada


func placa(texto: String, lugar: Vector3, giro_y: float, tamanho: float = 0.018, cor: Color = Color(0.46, 0.16, 0.12, 0.95)) -> void:
	var nova := Label3D.new()
	nova.text = texto
	nova.font = load("res://cenas/interface/fonte_jogo.tres")
	nova.font_size = 16
	nova.outline_size = 0
	nova.pixel_size = tamanho
	nova.shaded = true
	nova.modulate = cor
	nova.position = lugar
	nova.rotation.y = giro_y
	add_child(nova)


func quadrilatero(a: Vector3, b: Vector3, c: Vector3, d: Vector3, acabamento: Material) -> void:
	faixa(PackedVector3Array([a, b]), PackedVector3Array([d, c]), acabamento, false)


func faixa(a: PackedVector3Array, b: PackedVector3Array, acabamento: Material, fechar: bool = true) -> void:
	var montador := SurfaceTool.new()
	montador.begin(Mesh.PRIMITIVE_TRIANGLES)
	var total := a.size() if fechar else a.size() - 1
	for i in total:
		var j := (i + 1) % a.size()
		for vertice: Vector3 in [a[i], b[i], a[j], a[j], b[i], b[j]]:
			montador.add_vertex(vertice)
	_adicionar_malha(montador, acabamento)


func poligono(pontos: PackedVector3Array, acabamento: Material, projeta_sombra: bool) -> void:
	var centro := Vector3.ZERO
	for ponto in pontos:
		centro += ponto
	centro /= float(pontos.size())
	var montador := SurfaceTool.new()
	montador.begin(Mesh.PRIMITIVE_TRIANGLES)
	for i in pontos.size():
		for vertice: Vector3 in [centro, pontos[i], pontos[(i + 1) % pontos.size()]]:
			montador.add_vertex(vertice)
	var instancia := _adicionar_malha(montador, acabamento)
	if not projeta_sombra:
		instancia.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF


func _adicionar_malha(montador: SurfaceTool, acabamento: Material) -> MeshInstance3D:
	montador.generate_normals()
	var instancia := MeshInstance3D.new()
	instancia.mesh = montador.commit()
	instancia.material_override = acabamento
	instancia.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_DOUBLE_SIDED
	add_child(instancia)
	return instancia


func bloco(tamanho: Vector3, lugar: Vector3, acabamento: Material) -> MeshInstance3D:
	var malha := BoxMesh.new()
	malha.size = tamanho
	var novo := MeshInstance3D.new()
	novo.mesh = malha
	novo.material_override = acabamento
	novo.position = lugar
	add_child(novo)
	return novo


func bloco_solido(tamanho: Vector3, lugar: Vector3, acabamento: Material) -> MeshInstance3D:
	forma(tamanho, lugar)
	return bloco(tamanho, lugar, acabamento)


func tubo(raio: float, comprimento: float, lugar: Vector3, acabamento: Material, eixo: Vector3, segmentos: int = 8) -> void:
	var malha := CylinderMesh.new()
	malha.top_radius = raio
	malha.bottom_radius = raio
	malha.height = comprimento
	malha.radial_segments = segmentos
	malha.rings = 1
	var novo := MeshInstance3D.new()
	novo.mesh = malha
	novo.material_override = acabamento
	novo.position = lugar
	if eixo == Vector3.BACK:
		novo.rotation.x = PI / 2.0
	elif eixo == Vector3.RIGHT:
		novo.rotation.z = PI / 2.0
	add_child(novo)


func forma(tamanho: Vector3, lugar: Vector3) -> void:
	var caixa := BoxShape3D.new()
	caixa.size = tamanho
	var nova := CollisionShape3D.new()
	nova.shape = caixa
	nova.position = lugar
	corpo.add_child(nova)

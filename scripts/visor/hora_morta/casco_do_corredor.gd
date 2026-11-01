class_name CascoDoCorredor
extends Node3D

const PASTA := "res://assets/sprites/cenario/hora_morta/%s.png"
const VAOS := 6
const COMPRIMENTO_DO_VAO := 4.0
const MEIA_LARGURA := 1.15
const ALTURA := 2.7
const CHANFRO_DO_TETO := 0.5
const CHANFRO_DO_CHAO := 0.25
const FORRO_RECUADO := 0.22
const MEIA_LARGURA_DA_JANELA := 1.3
const MEIA_ALTURA_DA_JANELA := 0.725
const CENTRO_DA_JANELA_Y := 1.325
const RAIO_DA_JANELA := 0.38
const LARGURA_DA_MOLDURA := 0.1
const SALIENCIA_DA_MOLDURA := 0.07
const FUNDO_DA_JANELA := 0.26
const PONTOS_POR_CANTO := 13
const RECUO_DA_COSTELA := 0.11
const ESPESSURA_DA_COSTELA := 0.26
const FOLGA_DA_PAREDE := 0.1
const COR_FRIA := Color(0.55, 0.78, 1.0)
const COR_QUENTE := Color(1.0, 0.72, 0.42)
const COR_DAS_FAIXAS := Color(1.0, 0.68, 0.32)
const BRILHO_DAS_FAIXAS := 1.3
const POSICOES_DAS_LAMPADAS: Array[float] = [10.0, 6.0, 2.0, -2.0, -6.0, -10.0]
const ESTADOS_DAS_LAMPADAS: Array[int] = [
	LampadaDaNave.Estado.ACESA,
	LampadaDaNave.Estado.QUEBRADA,
	LampadaDaNave.Estado.ACESA,
	LampadaDaNave.Estado.MORTA,
	LampadaDaNave.Estado.ACESA,
	LampadaDaNave.Estado.QUEBRADA,
]
const ARMARIOS: Array[Dictionary] = [
	{"lugar": Vector3(-0.92, 0.75, 7.0), "tamanho": Vector3(0.36, 1.5, 1.1)},
	{"lugar": Vector3(-0.94, 0.65, 3.2), "tamanho": Vector3(0.32, 1.3, 0.8)},
	{"lugar": Vector3(-0.92, 0.75, -3.4), "tamanho": Vector3(0.36, 1.5, 1.3)},
	{"lugar": Vector3(-0.94, 0.65, -7.6), "tamanho": Vector3(0.32, 1.3, 0.9)},
]
const TUBOS_DA_PAREDE: Array[Dictionary] = [
	{"y": 0.42, "raio": 0.035, "cor": Color(0.08, 0.08, 0.09), "afastado": 0.05},
	{"y": 0.5, "raio": 0.03, "cor": Color(0.1, 0.16, 0.28), "afastado": 0.09},
	{"y": 0.57, "raio": 0.028, "cor": Color(0.42, 0.14, 0.06), "afastado": 0.05},
	{"y": 0.63, "raio": 0.03, "cor": Color(0.07, 0.07, 0.08), "afastado": 0.1},
	{"y": 1.98, "raio": 0.05, "cor": Color(0.42, 0.45, 0.47), "afastado": 0.08},
	{"y": 2.08, "raio": 0.035, "cor": Color(0.34, 0.37, 0.4), "afastado": 0.1},
]
const TUBOS_DO_TETO: Array[Dictionary] = [
	{"x": -0.42, "raio": 0.05},
	{"x": -0.22, "raio": 0.035},
	{"x": 0.05, "raio": 0.06},
	{"x": 0.3, "raio": 0.04},
	{"x": 0.46, "raio": 0.03},
]

var lampadas: Array[LampadaDaNave] = []
var _material_das_faixas: StandardMaterial3D
var _material_da_tela: StandardMaterial3D
var _parede: StandardMaterial3D
var _parede_escura: StandardMaterial3D
var _chapa: StandardMaterial3D
var _grade: StandardMaterial3D
var _forro: StandardMaterial3D
var _moldura: StandardMaterial3D
var _reflexo_da_janela: StandardMaterial3D
var _costela: StandardMaterial3D
var _perigo: StandardMaterial3D
var _vidro: StandardMaterial3D
var _borracha: StandardMaterial3D
var _corrimao: StandardMaterial3D


func _ready() -> void:
	_criar_materiais()
	for vao in VAOS:
		_montar_vao(vao)
	for indice in VAOS + 1:
		_montar_costela(_z_da_costela(indice))
	_montar_tampas_e_portas()
	_montar_armarios()
	_montar_placas()
	_montar_colisao()


func cortar_energia() -> void:
	_material_das_faixas.emission_energy_multiplier = 0.0
	for lampada in lampadas:
		lampada.cortar_energia()


func religar() -> void:
	_material_das_faixas.emission_energy_multiplier = BRILHO_DAS_FAIXAS
	for lampada in lampadas:
		lampada.religar()


func _criar_materiais() -> void:
	_parede = _metal("painel_nave", 1.3)
	_parede_escura = _metal("painel_nave", 1.0, Color(0.6, 0.64, 0.66))
	_chapa = _metal("chao_chapa", 1.2)
	_grade = _metal("chao_grade", 0.8)
	_forro = _metal("teto_dutos", 1.2)
	_moldura = _cor_lisa(Color(0.3, 0.33, 0.35), 0.45)
	_reflexo_da_janela = _cor_lisa(Color(0.42, 0.46, 0.5), 0.3)
	_costela = _metal("painel_nave", 0.55, Color(0.62, 0.66, 0.68), 0.55, 0.3)
	_perigo = _metal("faixa_perigo", 0.5)
	_borracha = _cor_lisa(Color(0.04, 0.04, 0.05), 0.8)
	_corrimao = _cor_lisa(Color(0.46, 0.32, 0.14), 0.4)
	_corrimao.metallic = 0.7
	_material_das_faixas = _cor_acesa(COR_DAS_FAIXAS, BRILHO_DAS_FAIXAS)
	_material_da_tela = _cor_acesa(Color(0.2, 0.85, 1.0), 1.6)
	_vidro = StandardMaterial3D.new()
	_vidro.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	_vidro.albedo_color = Color(0.5, 0.65, 0.85, 0.05)
	_vidro.roughness = 0.05
	_vidro.cull_mode = BaseMaterial3D.CULL_DISABLED


func _metal(nome: String, metros: float, tinta: Color = Color.WHITE, rugosidade: float = 0.62, metalico: float = 0.35) -> StandardMaterial3D:
	var material := StandardMaterial3D.new()
	material.albedo_texture = load(PASTA % nome)
	material.albedo_color = tinta
	material.texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS_ANISOTROPIC
	material.uv1_triplanar = true
	material.uv1_world_triplanar = true
	material.uv1_scale = Vector3.ONE / metros
	material.roughness = rugosidade
	material.metallic = metalico
	material.cull_mode = BaseMaterial3D.CULL_DISABLED
	var caminho_normal := PASTA % (nome + "_n")
	if ResourceLoader.exists(caminho_normal):
		material.normal_enabled = true
		material.normal_texture = load(caminho_normal)
		material.normal_scale = 0.9
	return material


func _cor_lisa(cor: Color, rugosidade: float) -> StandardMaterial3D:
	var material := StandardMaterial3D.new()
	material.albedo_color = cor
	material.roughness = rugosidade
	material.cull_mode = BaseMaterial3D.CULL_DISABLED
	return material


func _cor_acesa(cor: Color, brilho: float) -> StandardMaterial3D:
	var material := _cor_lisa(cor * 0.4, 0.5)
	material.emission_enabled = true
	material.emission = cor
	material.emission_energy_multiplier = brilho
	return material


func _montar_vao(vao: int) -> void:
	var z := _centro_do_vao(vao)
	_montar_chao(z)
	_montar_paredes_lisas(z)
	_montar_janela(z)
	_montar_teto(z)
	_montar_cabos(z)
	_montar_faixas_do_chao(z)
	lampadas.append(_nova_lampada(z, ESTADOS_DAS_LAMPADAS[vao]))


func _montar_chao(z: float) -> void:
	var meio := COMPRIMENTO_DO_VAO / 2.0
	var borda := MEIA_LARGURA - CHANFRO_DO_CHAO
	_chapa_do_chao(-borda, -0.52, z, meio, _grade)
	_chapa_do_chao(-0.52, 0.52, z, meio, _chapa)
	_chapa_do_chao(0.52, borda, z, meio, _grade)
	for x: float in [-0.52, 0.52]:
		_bloco(Vector3(0.05, 0.012, COMPRIMENTO_DO_VAO), Vector3(x, 0.006, z), _costela)


func _chapa_do_chao(x0: float, x1: float, z: float, meio: float, material: Material) -> void:
	_quadrilatero(Vector3(x0, 0.0, z - meio), Vector3(x1, 0.0, z - meio), Vector3(x1, 0.0, z + meio), Vector3(x0, 0.0, z + meio), material)


func _montar_paredes_lisas(z: float) -> void:
	var perfil := _perfil_da_secao(0.0)
	var meio := COMPRIMENTO_DO_VAO / 2.0
	for indice in perfil.size() - 1:
		if _segmento_tem_janela(indice):
			continue
		var a := perfil[indice]
		var b := perfil[indice + 1]
		_quadrilatero(Vector3(a.x, a.y, z - meio), Vector3(b.x, b.y, z - meio), Vector3(b.x, b.y, z + meio), Vector3(a.x, a.y, z + meio), _material_do_segmento(indice))


func _perfil_da_secao(recuo: float) -> PackedVector2Array:
	var l := MEIA_LARGURA - recuo
	var a := ALTURA - recuo
	return PackedVector2Array([
		Vector2(-l + CHANFRO_DO_CHAO, 0.0),
		Vector2(-l, CHANFRO_DO_CHAO),
		Vector2(-l, a - CHANFRO_DO_TETO),
		Vector2(-l + CHANFRO_DO_TETO, a),
		Vector2(l - CHANFRO_DO_TETO, a),
		Vector2(l, a - CHANFRO_DO_TETO),
		Vector2(l, CHANFRO_DO_CHAO),
		Vector2(l - CHANFRO_DO_CHAO, 0.0),
	])


func _segmento_tem_janela(indice: int) -> bool:
	return indice == 5 or indice == 3


func _material_do_segmento(indice: int) -> Material:
	return _parede_escura if indice == 0 or indice == 6 else _parede


func _montar_janela(z: float) -> void:
	var furo := _contorno_da_janela(0.0)
	var borda := _borda_da_parede_em_volta()
	_faixa(_na_parede(borda, MEIA_LARGURA, z), _na_parede(furo, MEIA_LARGURA, z), _parede)
	var moldura := _contorno_da_janela(LARGURA_DA_MOLDURA)
	var x_da_frente := MEIA_LARGURA - SALIENCIA_DA_MOLDURA
	var x_do_fundo := MEIA_LARGURA + FUNDO_DA_JANELA
	_faixa(_na_parede(moldura, MEIA_LARGURA, z), _na_parede(moldura, x_da_frente, z), _moldura)
	_faixa(_na_parede(moldura, x_da_frente, z), _na_parede(furo, x_da_frente, z), _moldura)
	_faixa(_na_parede(furo, x_da_frente, z), _na_parede(furo, x_do_fundo, z), _reflexo_da_janela)
	_poligono(_na_parede(furo, x_do_fundo, z), _vidro, false)
	_montar_ferragens_da_janela(z)


func _contorno_da_janela(folga: float) -> PackedVector2Array:
	var mz := MEIA_LARGURA_DA_JANELA + folga
	var my := MEIA_ALTURA_DA_JANELA + folga
	var raio := RAIO_DA_JANELA + folga
	var pontos := PackedVector2Array()
	var centros: Array[Vector2] = [Vector2(mz - raio, my - raio), Vector2(-mz + raio, my - raio), Vector2(-mz + raio, -my + raio), Vector2(mz - raio, -my + raio)]
	for canto in 4:
		for passo in PONTOS_POR_CANTO:
			var angulo := PI / 2.0 * (float(canto) + float(passo) / float(PONTOS_POR_CANTO - 1))
			pontos.append(centros[canto] + Vector2(cos(angulo), sin(angulo)) * raio)
	return pontos


func _borda_da_parede_em_volta() -> PackedVector2Array:
	var mz := COMPRIMENTO_DO_VAO / 2.0
	var cima := ALTURA - CHANFRO_DO_TETO - CENTRO_DA_JANELA_Y
	var baixo := -(CENTRO_DA_JANELA_Y - CHANFRO_DO_CHAO)
	var reta_z := MEIA_LARGURA_DA_JANELA - RAIO_DA_JANELA
	var reta_y := MEIA_ALTURA_DA_JANELA - RAIO_DA_JANELA
	var cantos: Array = [
		[Vector2(mz, reta_y), Vector2(mz, cima), Vector2(reta_z, cima)],
		[Vector2(-reta_z, cima), Vector2(-mz, cima), Vector2(-mz, reta_y)],
		[Vector2(-mz, -reta_y), Vector2(-mz, baixo), Vector2(-reta_z, baixo)],
		[Vector2(reta_z, baixo), Vector2(mz, baixo), Vector2(mz, -reta_y)],
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


func _na_parede(contorno: PackedVector2Array, x: float, z: float) -> PackedVector3Array:
	var pontos := PackedVector3Array()
	for ponto in contorno:
		pontos.append(Vector3(x, CENTRO_DA_JANELA_Y + ponto.y, z + ponto.x))
	return pontos


func _montar_ferragens_da_janela(z: float) -> void:
	var x := MEIA_LARGURA - 0.1
	_tubo(0.016, 1.0, Vector3(x, CENTRO_DA_JANELA_Y, z + MEIA_LARGURA_DA_JANELA + 0.28), _corrimao, Vector3.UP)
	for y: float in [0.5, -0.5]:
		_bloco(Vector3(0.1, 0.03, 0.03), Vector3(x + 0.05, CENTRO_DA_JANELA_Y + y, z + MEIA_LARGURA_DA_JANELA + 0.28), _costela)
	var alto := CENTRO_DA_JANELA_Y + MEIA_ALTURA_DA_JANELA + 0.04
	_bloco(Vector3(0.02, 0.05, 0.7), Vector3(MEIA_LARGURA - 0.01, alto + 0.02, z - 0.3), _perigo)
	_bloco(Vector3(0.05, 0.04, 0.42), Vector3(MEIA_LARGURA - 0.03, 0.42, z + 0.2), _costela)
	_bloco(Vector3(0.09, 0.022, 0.28), Vector3(MEIA_LARGURA - 0.05, 0.42, z + 0.2), _corrimao)


func _montar_teto(z: float) -> void:
	var meio := COMPRIMENTO_DO_VAO / 2.0
	var largura := MEIA_LARGURA - CHANFRO_DO_TETO
	var fundo := ALTURA + FORRO_RECUADO
	_quadrilatero(Vector3(-largura, fundo, z - meio), Vector3(largura, fundo, z - meio), Vector3(largura, fundo, z + meio), Vector3(-largura, fundo, z + meio), _forro)
	for lado: float in [-1.0, 1.0]:
		_quadrilatero(Vector3(lado * largura, ALTURA, z - meio), Vector3(lado * largura, fundo, z - meio), Vector3(lado * largura, fundo, z + meio), Vector3(lado * largura, ALTURA, z + meio), _costela)
	for tubo in TUBOS_DO_TETO:
		_tubo(tubo["raio"], COMPRIMENTO_DO_VAO, Vector3(tubo["x"], fundo - 0.08, z), _costela, Vector3.BACK)
	for deslocamento: float in [-1.2, -0.4, 0.4, 1.2]:
		_bloco(Vector3(largura * 2.0, 0.09, 0.09), Vector3(0.0, fundo - 0.15, z + deslocamento), _parede_escura)


func _montar_cabos(z: float) -> void:
	var x := -MEIA_LARGURA
	for tubo in TUBOS_DA_PAREDE:
		var material := _cor_lisa(tubo["cor"], 0.55)
		_tubo(tubo["raio"], COMPRIMENTO_DO_VAO, Vector3(x + tubo["afastado"], tubo["y"], z), material, Vector3.BACK)
	for deslocamento: float in [-1.1, 0.9]:
		_bloco(Vector3(0.08, 0.34, 0.05), Vector3(x + 0.06, 0.52, z + deslocamento), _costela)
		_tubo(0.018, 1.3, Vector3(x + 0.05, 1.3, z + deslocamento + 0.5), _corrimao, Vector3.UP)


func _montar_faixas_do_chao(z: float) -> void:
	var x := MEIA_LARGURA - CHANFRO_DO_CHAO / 2.0 - 0.015
	for lado: float in [-1.0, 1.0]:
		var faixa := _bloco(Vector3(0.05, 0.022, COMPRIMENTO_DO_VAO - ESPESSURA_DA_COSTELA), Vector3(lado * x, CHANFRO_DO_CHAO / 2.0 + 0.015, z), _material_das_faixas)
		faixa.rotation.z = lado * PI / 4.0
		faixa.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF


func _nova_lampada(z: float, estado: int) -> LampadaDaNave:
	var fria := _cor_acesa(COR_FRIA, 0.0)
	var quente := _cor_acesa(COR_QUENTE, 0.0)
	_luminaria(-1.0, z, fria)
	_luminaria(1.0, z, quente)
	var lampada := LampadaDaNave.new()
	lampada.estado = estado as LampadaDaNave.Estado
	lampada.materiais_do_vidro = [fria, quente]
	lampada.position = Vector3(-0.55, ALTURA - 0.35, z)
	lampada.light_color = COR_FRIA
	lampada.light_energy = 1.5
	lampada.omni_range = 4.6
	lampada.omni_attenuation = 1.3
	var gemea := OmniLight3D.new()
	gemea.position = Vector3(1.1, 0.0, 0.0)
	gemea.light_color = COR_QUENTE
	gemea.light_energy = 1.5
	gemea.omni_range = 4.6
	gemea.omni_attenuation = 1.3
	lampada.add_child(gemea)
	add_child(lampada)
	return lampada


func _luminaria(lado: float, z: float, vidro: Material) -> void:
	var x := lado * (MEIA_LARGURA - CHANFRO_DO_TETO / 2.0)
	var y := ALTURA - CHANFRO_DO_TETO / 2.0
	var inclinacao := -lado * PI / 4.0
	var caixa := _bloco(Vector3(0.3, 0.05, 1.5), Vector3(x, y, z), _costela)
	caixa.rotation.z = inclinacao
	var luz := _bloco(Vector3(0.16, 0.02, 1.34), Vector3(x - lado * 0.022, y - 0.022, z), vidro)
	luz.rotation.z = inclinacao
	luz.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF


func _montar_costela(z: float) -> void:
	var externo := _perfil_da_secao(0.0)
	var interno := _perfil_da_secao(RECUO_DA_COSTELA)
	interno[0].y = 0.0
	interno[interno.size() - 1].y = 0.0
	var frente := z + ESPESSURA_DA_COSTELA / 2.0
	var costas := z - ESPESSURA_DA_COSTELA / 2.0
	_faixa(_na_secao(externo, frente), _na_secao(interno, frente), _costela, false)
	_faixa(_na_secao(interno, frente), _na_secao(interno, costas), _costela, false)
	_faixa(_na_secao(interno, costas), _na_secao(externo, costas), _costela, false)
	_bloco(Vector3(MEIA_LARGURA * 2.0, 0.015, ESPESSURA_DA_COSTELA), Vector3(0.0, 0.008, z), _costela)
	_bloco(Vector3(MEIA_LARGURA * 2.0 - 0.8, 0.06, ESPESSURA_DA_COSTELA), Vector3(0.0, ALTURA - RECUO_DA_COSTELA - 0.03, z), _costela)


func _na_secao(perfil: PackedVector2Array, z: float) -> PackedVector3Array:
	var pontos := PackedVector3Array()
	for ponto in perfil:
		pontos.append(Vector3(ponto.x, ponto.y, z))
	return pontos


func _montar_tampas_e_portas() -> void:
	var fim := COMPRIMENTO_DO_VAO * VAOS / 2.0
	for lado: float in [-1.0, 1.0]:
		var z := lado * fim
		_poligono(_na_secao(_perfil_da_secao(0.0), z), _parede, true)
		_montar_porta(z, lado)


func _montar_porta(z: float, lado: float) -> void:
	var material := StandardMaterial3D.new()
	material.albedo_texture = load(PASTA % "porta_nave")
	material.normal_enabled = true
	material.normal_texture = load(PASTA % "porta_nave_n")
	material.texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS_ANISOTROPIC
	material.roughness = 0.55
	material.metallic = 0.35
	var malha := QuadMesh.new()
	malha.size = Vector2(1.5, 2.1)
	var porta := MeshInstance3D.new()
	porta.mesh = malha
	porta.material_override = material
	porta.position = Vector3(0.0, 1.05, z - lado * 0.02)
	porta.rotation.y = 0.0 if lado < 0.0 else PI
	add_child(porta)
	var x := -lado * 0.92
	var parede := z - lado * 0.03
	_bloco(Vector3(0.24, 0.34, 0.03), Vector3(x, 1.25, parede), _borracha)
	_bloco(Vector3(0.18, 0.15, 0.012), Vector3(x, 1.32, parede - lado * 0.018), _material_da_tela)
	var botao := _cor_acesa(Color(0.2, 1.0, 0.4), 2.4)
	_bloco(Vector3(0.05, 0.05, 0.015), Vector3(x, 1.0, parede), botao)


func _montar_armarios() -> void:
	for armario in ARMARIOS:
		var lugar: Vector3 = armario["lugar"]
		var tamanho: Vector3 = armario["tamanho"]
		_bloco(tamanho, lugar, _parede_escura)
		for y: float in [tamanho.y * 0.32, -tamanho.y * 0.08]:
			_bloco(Vector3(0.012, 0.022, tamanho.z * 0.8), lugar + Vector3(tamanho.x / 2.0 + 0.005, y, 0.0), _borracha)
		_bloco(Vector3(0.012, 0.11, tamanho.z * 0.72), lugar + Vector3(tamanho.x / 2.0 + 0.004, -tamanho.y / 2.0 + 0.11, 0.0), _perigo)
		_bloco(Vector3(0.04, 0.14, 0.03), lugar + Vector3(tamanho.x / 2.0 + 0.02, 0.1, tamanho.z * 0.38), _corrimao)


func _montar_placas() -> void:
	var fonte: Font = load("res://cenas/interface/fonte_jogo.tres")
	for z: float in [9.6, 1.2, -9.4]:
		var placa := Label3D.new()
		placa.text = "CONVÉS 3"
		placa.font = fonte
		placa.font_size = 16
		placa.outline_size = 0
		placa.pixel_size = 0.018
		placa.shaded = true
		placa.modulate = Color(0.46, 0.16, 0.12, 0.95)
		placa.position = Vector3(-MEIA_LARGURA + 0.012, 1.58, z)
		placa.rotation.y = PI / 2.0
		add_child(placa)


func _montar_colisao() -> void:
	var corpo := StaticBody3D.new()
	add_child(corpo)
	var comprimento := COMPRIMENTO_DO_VAO * VAOS
	var largura := MEIA_LARGURA * 2.0
	var espessura := 0.4
	_forma(corpo, Vector3(largura, espessura, comprimento + 2.0), Vector3(0.0, -espessura / 2.0, 0.0))
	_forma(corpo, Vector3(largura, espessura, comprimento + 2.0), Vector3(0.0, ALTURA + espessura / 2.0, 0.0))
	for lado: float in [-1.0, 1.0]:
		_forma(corpo, Vector3(espessura, ALTURA, comprimento), Vector3(lado * (MEIA_LARGURA - FOLGA_DA_PAREDE + espessura / 2.0), ALTURA / 2.0, 0.0))
		_forma(corpo, Vector3(largura, ALTURA, espessura), Vector3(0.0, ALTURA / 2.0, lado * (comprimento + espessura) / 2.0))
	for armario in ARMARIOS:
		_forma(corpo, armario["tamanho"], armario["lugar"])


func _forma(corpo: StaticBody3D, tamanho: Vector3, lugar: Vector3) -> void:
	var caixa := BoxShape3D.new()
	caixa.size = tamanho
	var forma := CollisionShape3D.new()
	forma.shape = caixa
	forma.position = lugar
	corpo.add_child(forma)


func _quadrilatero(a: Vector3, b: Vector3, c: Vector3, d: Vector3, material: Material) -> void:
	_faixa(PackedVector3Array([a, b]), PackedVector3Array([d, c]), material, false)


func _faixa(a: PackedVector3Array, b: PackedVector3Array, material: Material, fechar: bool = true) -> void:
	var montador := SurfaceTool.new()
	montador.begin(Mesh.PRIMITIVE_TRIANGLES)
	var total := a.size() if fechar else a.size() - 1
	for i in total:
		var j := (i + 1) % a.size()
		for vertice: Vector3 in [a[i], b[i], a[j], a[j], b[i], b[j]]:
			montador.add_vertex(vertice)
	_adicionar_malha(montador, material)


func _poligono(pontos: PackedVector3Array, material: Material, projeta_sombra: bool) -> void:
	var centro := Vector3.ZERO
	for ponto in pontos:
		centro += ponto
	centro /= float(pontos.size())
	var montador := SurfaceTool.new()
	montador.begin(Mesh.PRIMITIVE_TRIANGLES)
	for i in pontos.size():
		for vertice: Vector3 in [centro, pontos[i], pontos[(i + 1) % pontos.size()]]:
			montador.add_vertex(vertice)
	var instancia := _adicionar_malha(montador, material)
	if not projeta_sombra:
		instancia.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF


func _adicionar_malha(montador: SurfaceTool, material: Material) -> MeshInstance3D:
	montador.generate_normals()
	var instancia := MeshInstance3D.new()
	instancia.mesh = montador.commit()
	instancia.material_override = material
	instancia.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_DOUBLE_SIDED
	add_child(instancia)
	return instancia


func _bloco(tamanho: Vector3, lugar: Vector3, material: Material) -> MeshInstance3D:
	var malha := BoxMesh.new()
	malha.size = tamanho
	var bloco := MeshInstance3D.new()
	bloco.mesh = malha
	bloco.material_override = material
	bloco.position = lugar
	add_child(bloco)
	return bloco


func _tubo(raio: float, comprimento: float, lugar: Vector3, material: Material, eixo: Vector3) -> void:
	var malha := CylinderMesh.new()
	malha.top_radius = raio
	malha.bottom_radius = raio
	malha.height = comprimento
	malha.radial_segments = 8
	malha.rings = 1
	var tubo := MeshInstance3D.new()
	tubo.mesh = malha
	tubo.material_override = material
	tubo.position = lugar
	if eixo == Vector3.BACK:
		tubo.rotation.x = PI / 2.0
	add_child(tubo)


func _centro_do_vao(vao: int) -> float:
	return POSICOES_DAS_LAMPADAS[vao]


func _z_da_costela(indice: int) -> float:
	return COMPRIMENTO_DO_VAO * (float(indice) - float(VAOS) / 2.0)

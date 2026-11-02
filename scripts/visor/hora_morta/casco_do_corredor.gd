class_name CascoDoCorredor
extends KitDaNave

const COMPRIMENTO_DO_VAO := 4.0
const ALTURA := 2.7
const CHANFRO_DO_TETO := 0.5
const CHANFRO_DO_CHAO := 0.25
const FORRO_RECUADO := 0.22
const RECUO_DA_COSTELA := 0.11
const ESPESSURA_DA_COSTELA := 0.26
const FOLGA_DA_PAREDE := 0.1
const ALCANCE_DA_LAMPADA := 2.0
const TUBOS_DA_PAREDE: Array[Dictionary] = [
	{"y": 0.42, "raio": 0.035, "material": "cabo_preto", "afastado": 0.05},
	{"y": 0.5, "raio": 0.03, "material": "cabo_azul", "afastado": 0.09},
	{"y": 0.57, "raio": 0.028, "material": "cabo_vermelho", "afastado": 0.05},
	{"y": 0.63, "raio": 0.03, "material": "cabo_preto", "afastado": 0.1},
	{"y": 1.98, "raio": 0.05, "material": "cano", "afastado": 0.08},
	{"y": 2.08, "raio": 0.035, "material": "cano", "afastado": 0.1},
]
const TUBOS_DO_TETO: Array[Dictionary] = [
	{"x": -0.42, "raio": 0.05},
	{"x": -0.22, "raio": 0.035},
	{"x": 0.05, "raio": 0.06},
	{"x": 0.3, "raio": 0.04},
	{"x": 0.46, "raio": 0.03},
]

@export var vaos := 6
@export var meia_largura := 1.15
@export var estados: Array[int] = []
@export var armarios: Array[Vector4] = []
@export var texto_da_placa := "CONVÉS 3"


func _montar() -> void:
	var meio := COMPRIMENTO_DO_VAO * float(vaos) / 2.0
	limites = AABB(Vector3(-meia_largura, 0.0, -meio), Vector3(meia_largura * 2.0, ALTURA, meio * 2.0))
	for vao in vaos:
		_montar_vao(vao)
	for indice in vaos + 1:
		_montar_costela(COMPRIMENTO_DO_VAO * float(indice) - meio)
	for lado: float in [-1.0, 1.0]:
		parede(Vector3(-meia_largura, 0.0, lado * meio), Vector3(meia_largura, 0.0, lado * meio), ALTURA, PackedFloat32Array([0.0]), material("parede"))
	_montar_armarios()
	_montar_colisao(meio)
	placa(texto_da_placa, Vector3(-meia_largura + 0.012, 1.58, meio - 2.4), PI / 2.0)


func z_do_vao(vao: int) -> float:
	return COMPRIMENTO_DO_VAO * (float(vaos) / 2.0 - float(vao) - 0.5)


func _montar_vao(vao: int) -> void:
	var z := z_do_vao(vao)
	_montar_chao(z)
	_montar_lados(z)
	_montar_teto(z)
	_montar_cabos(z)
	_montar_faixas_do_chao(z)
	lampadas.append(_nova_lampada(z, estados[vao] if vao < estados.size() else LampadaDaNave.Estado.MORTA))


func _montar_chao(z: float) -> void:
	var meio := COMPRIMENTO_DO_VAO / 2.0
	var borda := meia_largura - CHANFRO_DO_CHAO
	var chapa := borda * 0.58
	_chapa_do_chao(-borda, -chapa, z, meio, "grade")
	_chapa_do_chao(-chapa, chapa, z, meio, "chapa")
	_chapa_do_chao(chapa, borda, z, meio, "grade")
	for x: float in [-chapa, chapa]:
		bloco(Vector3(0.05, 0.012, COMPRIMENTO_DO_VAO), Vector3(x, 0.006, z), material("costela"))


func _chapa_do_chao(x0: float, x1: float, z: float, meio: float, nome: String) -> void:
	quadrilatero(Vector3(x0, 0.0, z - meio), Vector3(x1, 0.0, z - meio), Vector3(x1, 0.0, z + meio), Vector3(x0, 0.0, z + meio), material(nome))


func _perfil_da_secao(recuo: float) -> PackedVector2Array:
	var l := meia_largura - recuo
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


func _montar_lados(z: float) -> void:
	var perfil := _perfil_da_secao(0.0)
	var meio := COMPRIMENTO_DO_VAO / 2.0
	for indice in perfil.size() - 1:
		if indice == 3 or (indice == 5 and tem_janelas):
			continue
		var a := perfil[indice]
		var b := perfil[indice + 1]
		var nome := "parede_escura" if indice == 0 or indice == 6 else "parede"
		quadrilatero(Vector3(a.x, a.y, z - meio), Vector3(b.x, b.y, z - meio), Vector3(b.x, b.y, z + meio), Vector3(a.x, a.y, z + meio), material(nome))
	if tem_janelas:
		janela_em_x(meia_largura, z, COMPRIMENTO_DO_VAO, CHANFRO_DO_CHAO, ALTURA - CHANFRO_DO_TETO)


func _montar_teto(z: float) -> void:
	var meio := COMPRIMENTO_DO_VAO / 2.0
	var largura := meia_largura - CHANFRO_DO_TETO
	var fundo := ALTURA + FORRO_RECUADO
	quadrilatero(Vector3(-largura, fundo, z - meio), Vector3(largura, fundo, z - meio), Vector3(largura, fundo, z + meio), Vector3(-largura, fundo, z + meio), material("forro"))
	for lado: float in [-1.0, 1.0]:
		quadrilatero(Vector3(lado * largura, ALTURA, z - meio), Vector3(lado * largura, fundo, z - meio), Vector3(lado * largura, fundo, z + meio), Vector3(lado * largura, ALTURA, z + meio), material("costela"))
	var escala := largura / 0.65
	for dados in TUBOS_DO_TETO:
		tubo(dados["raio"], COMPRIMENTO_DO_VAO, Vector3(dados["x"] * escala, fundo - 0.08, z), material("costela"), Vector3.BACK)
	for deslocamento: float in [-1.2, -0.4, 0.4, 1.2]:
		bloco(Vector3(largura * 2.0, 0.09, 0.09), Vector3(0.0, fundo - 0.15, z + deslocamento), material("parede_escura"))


func _montar_cabos(z: float) -> void:
	var x := -meia_largura
	for dados in TUBOS_DA_PAREDE:
		tubo(dados["raio"], COMPRIMENTO_DO_VAO, Vector3(x + dados["afastado"], dados["y"], z), material(dados["material"]), Vector3.BACK)
	for deslocamento: float in [-1.1, 0.9]:
		bloco(Vector3(0.08, 0.34, 0.05), Vector3(x + 0.06, 0.52, z + deslocamento), material("costela"))
		tubo(0.018, 1.3, Vector3(x + 0.05, 1.3, z + deslocamento + 0.5), material("corrimao"), Vector3.UP)
	if tem_janelas:
		return
	for dados in TUBOS_DA_PAREDE:
		tubo(dados["raio"], COMPRIMENTO_DO_VAO, Vector3(-x - dados["afastado"], dados["y"] + 0.1, z), material(dados["material"]), Vector3.BACK)


func _montar_faixas_do_chao(z: float) -> void:
	var x := meia_largura - CHANFRO_DO_CHAO / 2.0 - 0.015
	for lado: float in [-1.0, 1.0]:
		var nova := bloco(Vector3(0.05, 0.022, COMPRIMENTO_DO_VAO - ESPESSURA_DA_COSTELA), Vector3(lado * x, CHANFRO_DO_CHAO / 2.0 + 0.015, z), material_das_faixas)
		nova.rotation.z = lado * PI / 4.0
		nova.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF


func _nova_lampada(z: float, estado: int) -> LampadaDaNave:
	var fria := cor_acesa(COR_FRIA, 0.0)
	var quente := cor_acesa(COR_QUENTE, 0.0)
	_luminaria(-1.0, z, fria)
	_luminaria(1.0, z, quente)
	var distancia := minf(0.55, meia_largura - 0.5)
	var lampada := LampadaDaNave.new()
	lampada.estado = estado as LampadaDaNave.Estado
	lampada.materiais_do_vidro = [fria, quente]
	lampada.alcance = ALCANCE_DA_LAMPADA
	lampada.centro_local = Vector3(distancia, 0.0, 0.0)
	lampada.position = Vector3(-distancia, ALTURA - 0.35, z)
	lampada.light_color = COR_FRIA
	lampada.light_energy = 1.5
	lampada.omni_range = 4.6
	lampada.omni_attenuation = 1.3
	var gemea := OmniLight3D.new()
	gemea.position = Vector3(distancia * 2.0, 0.0, 0.0)
	gemea.light_color = COR_QUENTE
	gemea.light_energy = 1.5
	gemea.omni_range = 4.6
	gemea.omni_attenuation = 1.3
	lampada.add_child(gemea)
	add_child(lampada)
	return lampada


func _luminaria(lado: float, z: float, vidro: Material) -> void:
	var x := lado * (meia_largura - CHANFRO_DO_TETO / 2.0)
	var y := ALTURA - CHANFRO_DO_TETO / 2.0
	var inclinacao := -lado * PI / 4.0
	var caixa := bloco(Vector3(0.3, 0.05, 1.5), Vector3(x, y, z), material("costela"))
	caixa.rotation.z = inclinacao
	var luz := bloco(Vector3(0.16, 0.02, 1.34), Vector3(x - lado * 0.022, y - 0.022, z), vidro)
	luz.rotation.z = inclinacao
	luz.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF


func _montar_costela(z: float) -> void:
	var externo := _perfil_da_secao(0.0)
	var interno := _perfil_da_secao(RECUO_DA_COSTELA)
	interno[0].y = 0.0
	interno[interno.size() - 1].y = 0.0
	var frente := z + ESPESSURA_DA_COSTELA / 2.0
	var costas := z - ESPESSURA_DA_COSTELA / 2.0
	faixa(_na_secao(externo, frente), _na_secao(interno, frente), material("costela"), false)
	faixa(_na_secao(interno, frente), _na_secao(interno, costas), material("costela"), false)
	faixa(_na_secao(interno, costas), _na_secao(externo, costas), material("costela"), false)
	bloco(Vector3(meia_largura * 2.0, 0.015, ESPESSURA_DA_COSTELA), Vector3(0.0, 0.008, z), material("costela"))
	bloco(Vector3(meia_largura * 2.0 - 0.8, 0.06, ESPESSURA_DA_COSTELA), Vector3(0.0, ALTURA - RECUO_DA_COSTELA - 0.03, z), material("costela"))


func _na_secao(perfil: PackedVector2Array, z: float) -> PackedVector3Array:
	var pontos := PackedVector3Array()
	for ponto in perfil:
		pontos.append(Vector3(ponto.x, ponto.y, z))
	return pontos


func _montar_armarios() -> void:
	for dados in armarios:
		var tamanho := Vector3(0.34, dados.y, dados.z)
		var lugar := Vector3(dados.x * meia_largura, dados.y / 2.0, dados.w)
		var lado := signf(dados.x)
		bloco_solido(tamanho, lugar, material("parede_escura"))
		for y: float in [tamanho.y * 0.32, -tamanho.y * 0.08]:
			bloco(Vector3(0.012, 0.022, tamanho.z * 0.8), lugar - Vector3(lado * (tamanho.x / 2.0 + 0.005), -y, 0.0), material("borracha"))
		bloco(Vector3(0.012, 0.11, tamanho.z * 0.72), lugar - Vector3(lado * (tamanho.x / 2.0 + 0.004), tamanho.y / 2.0 - 0.11, 0.0), material("perigo"))
		bloco(Vector3(0.04, 0.14, 0.03), lugar - Vector3(lado * (tamanho.x / 2.0 + 0.02), -0.1, -tamanho.z * 0.38), material("corrimao"))


func _montar_colisao(meio: float) -> void:
	var espessura := 0.4
	var largura := meia_largura * 2.0
	forma(Vector3(largura, espessura, meio * 2.0 + 0.6), Vector3(0.0, -espessura / 2.0, 0.0))
	forma(Vector3(largura, espessura, meio * 2.0 + 0.6), Vector3(0.0, ALTURA + espessura / 2.0, 0.0))
	for lado: float in [-1.0, 1.0]:
		forma(Vector3(espessura, ALTURA, meio * 2.0), Vector3(lado * (meia_largura - FOLGA_DA_PAREDE + espessura / 2.0), ALTURA / 2.0, 0.0))

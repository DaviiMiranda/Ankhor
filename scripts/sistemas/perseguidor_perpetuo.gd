extends Node

const PREFIXO_DA_FASE := "res://cenas/salas/bunker/"
const CENA_DO_CIBORGUE := "res://cenas/personagens/ciborgue_do_carlos.tscn"
const AVISO_CHEGOU := "Passos pesados atrás da porta. É ele."
const SEGUNDOS_NA_CHEGADA_DA_FASE := 8.0
const SEGUNDOS_AO_RECOMECAR := 12.0
const SEGUNDOS_DEPOIS_DO_ABRIGO := 6.0
const SEGUNDOS_FORA := 5.0
const SEGUNDOS_MINIMOS := 1.5
const SEGUNDOS_MAXIMOS := 40.0
const DISTANCIA_DA_PORTA := 22.0
const DISTANCIA_IDEAL_DA_VOLTA := 260.0
const DISTANCIA_MINIMA_DO_GABRIEL := 90.0
const VELOCIDADE_DO_CIBORGUE := 40.0

var desligado := false

var _na_fase := false
var _cena: Node
var _segundos := -1.0
var _porta_de_chegada := ""
var _veio_pela_porta := false
var _trazendo := false
var _ciborgue: CiborgueDoCarlos


func segundos_ate_chegar() -> float:
	return _segundos


func ciborgue() -> CiborgueDoCarlos:
	return _ciborgue if is_instance_valid(_ciborgue) else null


func gabriel_saiu_pela(porta: Porta) -> void:
	if not _na_fase:
		return
	_veio_pela_porta = true
	var sala := get_tree().current_scene
	if _e_abrigo(sala):
		_agendar(maxf(_segundos, SEGUNDOS_DEPOIS_DO_ABRIGO), "")
	elif ciborgue() and _ciborgue.modo == CiborgueDoCarlos.Modo.INDO_EMBORA:
		_agendar(SEGUNDOS_FORA, "")
	elif ciborgue():
		_agendar(_ciborgue.global_position.distance_to(porta.global_position) / _ciborgue.velocidade_perseguicao, porta.porta_destino)
	elif _segundos >= 0.0:
		_agendar(_segundos + _travessia(sala, porta), porta.porta_destino)


func _process(delta: float) -> void:
	var cena := get_tree().current_scene
	if cena != _cena:
		_cena = cena
		_ao_trocar_de_sala(cena)
	if desligado or not _na_fase or _trazendo or ciborgue() or _segundos < 0.0 or _e_abrigo(cena):
		return
	_segundos -= delta
	if _segundos <= 0.0:
		_trazer(cena as Sala)


func _ao_trocar_de_sala(cena: Node) -> void:
	if cena == null:
		return
	_ciborgue = null
	if not cena.scene_file_path.begins_with(PREFIXO_DA_FASE):
		_na_fase = false
		_veio_pela_porta = false
		_segundos = -1.0
		return
	if not _na_fase:
		_na_fase = true
		_agendar(SEGUNDOS_NA_CHEGADA_DA_FASE, "")
	elif not _veio_pela_porta:
		_agendar(SEGUNDOS_AO_RECOMECAR, "")
	_veio_pela_porta = false


func _agendar(segundos: float, porta: String) -> void:
	_segundos = clampf(segundos, SEGUNDOS_MINIMOS, SEGUNDOS_MAXIMOS)
	_porta_de_chegada = porta


func _travessia(sala: Node, saida: Porta) -> float:
	var entrada := _porta_com_id(sala, _porta_de_chegada)
	if entrada == null:
		return 0.0
	return entrada.global_position.distance_to(saida.global_position) / VELOCIDADE_DO_CIBORGUE


func _e_abrigo(cena: Node) -> bool:
	return cena is SalaSegura or (cena != null and PerseguicaoEntreSalas.SALAS_PROTEGIDAS.has(cena.scene_file_path))


func _trazer(sala: Sala) -> void:
	_segundos = -1.0
	if sala == null or sala.get_node_or_null("Objetos") == null:
		return
	_trazendo = true
	var grade := PerseguicaoEntreSalas.grade_da_sala(sala)
	if grade == null:
		sala.add_child(RobosDaSala.new())
		await get_tree().process_frame
		await get_tree().process_frame
		if not is_instance_valid(sala) or get_tree().current_scene != sala:
			_trazendo = false
			return
		grade = PerseguicaoEntreSalas.grade_da_sala(sala)
	_trazendo = false
	if grade == null:
		return
	var porta := _porta_para_entrar(sala)
	var ponto := _ponto_de_entrada(sala, porta)
	_ciborgue = (load(CENA_DO_CIBORGUE) as PackedScene).instantiate() as CiborgueDoCarlos
	sala.get_node("Objetos").add_child(_ciborgue)
	_ciborgue.saiu_da_sala.connect(_ao_ciborgue_sair)
	_ciborgue.entrar(grade, grade.centro(grade.livre_mais_perto(grade.celula(ponto))))
	var musica := sala.get_node_or_null("MusicaPerseguicao") as MusicaPerseguicao
	if musica:
		musica.conectar_robos()
	if porta:
		porta.tocar_abertura()
	Inventario.aviso.emit(AVISO_CHEGOU)


func _ao_ciborgue_sair(_quem: CiborgueDoCarlos) -> void:
	_ciborgue = null
	_agendar(SEGUNDOS_FORA, "")


func _porta_para_entrar(sala: Node) -> Porta:
	var pela_id := _porta_com_id(sala, _porta_de_chegada)
	if pela_id:
		return pela_id
	var gabriel := get_tree().get_first_node_in_group("jogador") as Node2D
	var melhor: Porta = null
	var menor := INF
	for porta in _portas(sala):
		if gabriel == null:
			return porta
		var distancia := porta.global_position.distance_to(gabriel.global_position)
		var nota := absf(distancia - DISTANCIA_IDEAL_DA_VOLTA)
		if distancia < DISTANCIA_MINIMA_DO_GABRIEL:
			nota += 10000.0
		if nota < menor:
			menor = nota
			melhor = porta
	return melhor


func _ponto_de_entrada(sala: Sala, porta: Porta) -> Vector2:
	if porta:
		return porta.global_position - porta.direcao_entrar * DISTANCIA_DA_PORTA
	var gabriel := get_tree().get_first_node_in_group("jogador") as Node2D
	var x := float(sala.margem_lados + 20)
	if gabriel and gabriel.global_position.x < sala.largura / 2.0:
		x = sala.largura - sala.margem_lados - 20.0
	return Vector2(x, (sala.chao_fundo + sala.chao_frente) / 2.0)


func _porta_com_id(sala: Node, id: String) -> Porta:
	if id.is_empty():
		return null
	for porta in _portas(sala):
		if porta.id == id:
			return porta
	return null


func _portas(sala: Node) -> Array[Porta]:
	var lista: Array[Porta] = []
	if sala == null:
		return lista
	for no in get_tree().get_nodes_in_group("portas"):
		var porta := no as Porta
		if porta and sala.is_ancestor_of(porta):
			lista.append(porta)
	return lista

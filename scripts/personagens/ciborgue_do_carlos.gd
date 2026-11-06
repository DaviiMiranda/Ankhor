class_name CiborgueDoCarlos
extends Robo

signal saiu_da_sala(ciborgue: CiborgueDoCarlos)

enum Modo { CACANDO, ESPERANDO, INDO_EMBORA }

const CENA_RESPIRACAO := preload("res://cenas/sistemas/respiracao_contida.tscn")
const AVISO_IMUNE := "Não fez nada com ele."
const AVISO_OUVIU := "Ele ouviu você."
const AVISO_FOI_EMBORA := "Ele saiu. Mas vai voltar."
const DISTANCIA_DA_PORTA := 22.0
const DISTANCIA_MINIMA_DO_GABRIEL := 90.0

static var _avisou_imune := false

@export_group("Esconderijo")
@export var segundos_esperando_minimo: float = 7.0
@export var segundos_esperando_maximo: float = 11.0
@export var distancia_da_espera: float = 28.0
@export var distancia_da_respiracao: float = 56.0

var modo: Modo = Modo.CACANDO
var _segundos_esperando := 0.0
var _respiracao: RespiracaoContida
var _porta_da_saida: Porta
var _saindo := false


func entrar(nova_grade: GradeLabirinto, ponto: Vector2) -> void:
	grade = nova_grade
	_sorteio.randomize()
	global_position = ponto
	_cacar()


func esta_perseguindo() -> bool:
	return modo == Modo.CACANDO


func atordoar(_segundos: float) -> void:
	if not _avisou_imune:
		_avisou_imune = true
		Inventario.aviso.emit(AVISO_IMUNE)


func pode_ser_hackeado_de(_ponto: Vector2) -> bool:
	return false


func ouvir_barulho(_origem: Vector2, _alcance_base: float) -> void:
	pass


func distrair(_onde: Vector2, _segundos: float) -> void:
	pass


func denunciar() -> void:
	if grade != null and not _saindo:
		_cacar()


func _decidir(delta: float) -> void:
	if _gabriel == null or _saindo:
		return
	match modo:
		Modo.CACANDO:
			_decidir_cacando(delta)
		Modo.ESPERANDO:
			_decidir_esperando(delta)
		Modo.INDO_EMBORA:
			if _ve_o_jogador():
				_cacar()


func _decidir_cacando(delta: float) -> void:
	if estado == Estado.ATACOU:
		if _tempo_no_estado > segundos_depois_do_ataque:
			_perseguir()
		return
	if _gabriel.escondido:
		_esperar_do_lado_de_fora()
		return
	if estado != Estado.PERSEGUINDO:
		_perseguir()
	_ultima_vista = _gabriel.global_position
	_tempo_novo_caminho -= delta
	if _tempo_novo_caminho <= 0.0:
		_tempo_novo_caminho = INTERVALO_NOVO_CAMINHO
		_ir_para(_ultima_vista)


func _decidir_esperando(delta: float) -> void:
	if not _gabriel.escondido:
		_cacar()
		return
	if not _caminho.is_empty():
		return
	if _respiracao == null and global_position.distance_to(_gabriel.global_position) <= distancia_da_respiracao:
		_comecar_respiracao()
	_segundos_esperando -= delta
	if _segundos_esperando <= 0.0:
		_ir_embora()


func _cacar() -> void:
	modo = Modo.CACANDO
	_encerrar_respiracao()
	_perseguir()


func _esperar_do_lado_de_fora() -> void:
	modo = Modo.ESPERANDO
	_segundos_esperando = _sorteio.randf_range(segundos_esperando_minimo, segundos_esperando_maximo)
	_mudar_estado(Estado.INVESTIGANDO)
	_ir_para(_ponto_de_espera())


func _ponto_de_espera() -> Vector2:
	var lado := signf(global_position.x - _gabriel.global_position.x)
	var ponto := _gabriel.global_position + Vector2(lado * 10.0, distancia_da_espera)
	return grade.centro(grade.livre_mais_perto(grade.celula(ponto)))


func _comecar_respiracao() -> void:
	_respiracao = CENA_RESPIRACAO.instantiate() as RespiracaoContida
	_respiracao.acompanhar(_gabriel)
	_respiracao.falhou.connect(_ao_ouvir_a_respiracao)
	get_tree().current_scene.add_child(_respiracao)


func _encerrar_respiracao() -> void:
	if is_instance_valid(_respiracao):
		_respiracao.queue_free()
	_respiracao = null


func _ao_ouvir_a_respiracao() -> void:
	_respiracao = null
	Inventario.aviso.emit(AVISO_OUVIU)
	_gabriel.esconder(false)
	_cacar()


func _ir_embora() -> void:
	_encerrar_respiracao()
	modo = Modo.INDO_EMBORA
	_mudar_estado(Estado.PATRULHA)
	_porta_da_saida = _porta_para_sair()
	if _porta_da_saida:
		_ir_para(_porta_da_saida.global_position - _porta_da_saida.direcao_entrar * DISTANCIA_DA_PORTA)
	else:
		_ir_para(global_position + Vector2(signf(global_position.x - _gabriel.global_position.x) * 200.0, 0.0))


func _porta_para_sair() -> Porta:
	var melhor: Porta = null
	var menor := INF
	for no in get_tree().get_nodes_in_group("portas"):
		var porta := no as Porta
		if porta == null or not get_tree().current_scene.is_ancestor_of(porta):
			continue
		if porta.global_position.distance_to(_gabriel.global_position) < DISTANCIA_MINIMA_DO_GABRIEL:
			continue
		var distancia := global_position.distance_to(porta.global_position)
		if distancia < menor:
			menor = distancia
			melhor = porta
	return melhor


func _ao_chegar() -> void:
	if modo == Modo.INDO_EMBORA:
		_sair()


func _tentar_atacar() -> void:
	if _gabriel and _gabriel.escondido:
		return
	super()


func _sair() -> void:
	if _saindo:
		return
	_saindo = true
	remove_from_group("robos")
	velocity = Vector2.ZERO
	if is_instance_valid(_porta_da_saida):
		_porta_da_saida.tocar_abertura()
	Inventario.aviso.emit(AVISO_FOI_EMBORA)
	var sumir := create_tween()
	sumir.tween_property(self, "modulate:a", 0.0, 0.5)
	sumir.tween_callback(_terminar_saida)


func _terminar_saida() -> void:
	saiu_da_sala.emit(self)
	queue_free()


func _exit_tree() -> void:
	_encerrar_respiracao()

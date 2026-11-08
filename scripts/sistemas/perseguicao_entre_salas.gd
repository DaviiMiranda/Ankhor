class_name PerseguicaoEntreSalas
extends RefCounted

const SEGUNDOS_MINIMOS := 1.2
const SEGUNDOS_MAXIMOS := 9.0
const DISTANCIA_DA_PORTA := 22.0
const AVISO := "Algo atravessou a porta atrás de você."
const PREFIXOS_SEM_PERSEGUICAO := ["res://cenas/salas/dtec/"]
const SALAS_PROTEGIDAS := [
	"res://cenas/salas/bloco_de_salas/sala_103.tscn",
	"res://cenas/salas/centro_de_convivencia/loja_1.tscn",
	"res://cenas/salas/bunker/central_dados.tscn",
	"res://cenas/salas/bunker/fuga.tscn",
	"res://cenas/salas/labirinto/corredor_do_tempo.tscn",
]

static var _cena_do_robo := ""
static var _segundos := 0.0


static func anotar(arvore: SceneTree, porta: Porta) -> void:
	_cena_do_robo = ""
	if not porta.robo_atravessa:
		return
	var menor := SEGUNDOS_MAXIMOS
	for no in arvore.get_nodes_in_group("robos"):
		var robo := no as Robo
		if robo == null or robo is CiborgueDoCarlos or not robo.esta_perseguindo():
			continue
		var segundos := robo.global_position.distance_to(porta.global_position) / robo.velocidade_perseguicao
		if segundos <= menor:
			menor = segundos
			_cena_do_robo = robo.scene_file_path
	_segundos = maxf(menor, SEGUNDOS_MINIMOS)


static func chamar(porta: Porta) -> void:
	var cena := _cena_do_robo
	_cena_do_robo = ""
	if cena.is_empty():
		return
	var sala := porta.get_tree().current_scene as Sala
	if sala == null or not _aceita_perseguidor(sala):
		return
	await porta.get_tree().create_timer(_segundos, false).timeout
	if is_instance_valid(porta) and porta.is_inside_tree():
		await _chegar(sala, porta, cena)


static func grade_da_sala(sala: Sala) -> GradeLabirinto:
	if sala == null:
		return null
	var propria = sala.get("grade")
	if propria is GradeLabirinto:
		return propria
	for filho in sala.get_children():
		if filho is RobosDaSala:
			return (filho as RobosDaSala).grade
	return null


static func _aceita_perseguidor(sala: Sala) -> bool:
	if sala is SalaSegura or SALAS_PROTEGIDAS.has(sala.scene_file_path):
		return false
	for prefixo in PREFIXOS_SEM_PERSEGUICAO:
		if sala.scene_file_path.begins_with(prefixo):
			return false
	return sala.get_node_or_null("Objetos") != null


static func _chegar(sala: Sala, porta: Porta, cena: String) -> void:
	var grade := grade_da_sala(sala)
	if grade == null:
		sala.add_child(RobosDaSala.new())
		await porta.get_tree().process_frame
		await porta.get_tree().process_frame
		if not is_instance_valid(sala):
			return
		grade = grade_da_sala(sala)
	if grade == null:
		return
	var ponto := grade.centro(grade.livre_mais_perto(grade.celula(porta.global_position - porta.direcao_entrar * DISTANCIA_DA_PORTA)))
	var robo := _robo_igual_na_sala(porta.get_tree(), cena)
	if robo:
		robo.chegar_pela_porta(ponto)
	else:
		robo = (load(cena) as PackedScene).instantiate() as Robo
		sala.get_node("Objetos").add_child(robo)
		robo.global_position = ponto
		robo.chegar_de_fora(grade, ponto)
	var musica := sala.get_node_or_null("MusicaPerseguicao") as MusicaPerseguicao
	if musica:
		musica.conectar_robos()
	porta.tocar_abertura()
	Inventario.aviso.emit(AVISO)


static func _robo_igual_na_sala(arvore: SceneTree, cena: String) -> Robo:
	for no in arvore.get_nodes_in_group("robos"):
		var robo := no as Robo
		if robo and robo.scene_file_path == cena and robo.can_process():
			return robo
	return null

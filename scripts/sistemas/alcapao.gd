class_name Alcapao
extends Interagivel

const CENA_SAIDA := preload("res://cenas/sistemas/saida_fase.tscn")
const MARCA_REVELADO := "labirinto_alcapao_revelado"
const SEGUNDOS_DESCENDO := 0.7

@export_file("*.tscn") var cena_destino: String = ""
@export var titulo: String = "VOCÊ SAIU DO LABIRINTO"
@export var subtitulo: String = "Próxima fase: o Bunker"
@export var textura_escondido: Texture2D
@export var textura_aberto: Texture2D

var _descendo := false

@onready var sprite: Sprite2D = $Sprite2D
@onready var luz: PointLight2D = get_node_or_null("Luz")


func _ready() -> void:
	super()
	if Engine.is_editor_hint():
		return
	Progresso.mudou.connect(_ao_marcar)
	_atualizar()


func pode_interagir() -> bool:
	return Progresso.tem(MARCA_REVELADO) and not _descendo


func interagir() -> void:
	var gabriel := get_tree().get_first_node_in_group("jogador") as Gabriel
	if gabriel == null:
		return
	_descendo = true
	remove_from_group(GRUPO_PERTO)
	gabriel.andar_sozinho(Vector2.ZERO)
	var descida := create_tween()
	descida.tween_property(gabriel, "modulate", Color(0, 0, 0, 0), SEGUNDOS_DESCENDO)
	descida.tween_callback(_terminar_fase)


func _terminar_fase() -> void:
	var saida: SaidaFase = CENA_SAIDA.instantiate()
	saida.sair_ao_carregar = true
	if not cena_destino.is_empty():
		saida.cena_destino = cena_destino
	get_tree().current_scene.add_child(saida)
	(saida.get_node("Tela/Titulo") as Label).text = titulo
	(saida.get_node("Tela/Titulo/Subtitulo") as Label).text = subtitulo


func _ao_marcar(marca: String) -> void:
	if marca == MARCA_REVELADO:
		_atualizar()


func _atualizar() -> void:
	var revelado := Progresso.tem(MARCA_REVELADO)
	sprite.texture = textura_aberto if revelado else textura_escondido
	if luz:
		luz.visible = revelado

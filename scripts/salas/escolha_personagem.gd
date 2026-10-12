extends Node

const PERSONAGENS: Array[String] = ["gabriel", "clarice", "zane", "baltazar", "rafael", "henrique", "carlos"]
const NOMES := {
	"gabriel": "Gabriel",
	"clarice": "Clarice",
	"zane": "Zane",
	"baltazar": "Baltazar",
	"rafael": "Rafael",
	"henrique": "Henrique",
	"carlos": "Carlos",
}
const VISTAS: Array[String] = ["lado", "frente", "tres_quartos", "costas", "tres_quartos_costas"]
const TECLA_TROCAR := KEY_C

@export var personagem_inicial: String = "gabriel"

var _atual := 0


func _ready() -> void:
	_atual = maxi(PERSONAGENS.find(personagem_inicial), 0)
	_aplicar.call_deferred()


func _unhandled_key_input(evento: InputEvent) -> void:
	var tecla := evento as InputEventKey
	if tecla == null or not tecla.pressed or tecla.echo or tecla.physical_keycode != TECLA_TROCAR:
		return
	_atual = (_atual + 1) % PERSONAGENS.size()
	_aplicar()
	get_viewport().set_input_as_handled()


func _aplicar() -> void:
	var jogador := get_tree().get_first_node_in_group("jogador")
	if jogador == null:
		return
	var nome := PERSONAGENS[_atual]
	for vista in VISTAS:
		jogador.set("sprite_" + vista, _textura(nome, vista))
		jogador.set("andar_" + vista, _textura(nome, "andar_" + vista))
		jogador.set("parado_" + vista, _textura(nome, "parado_" + vista))
	Inventario.aviso.emit("Personagem: %s   [C] trocar" % NOMES[nome])


func _textura(nome: String, vista: String) -> Texture2D:
	return load("res://assets/sprites/personagens/%s/%s_%s.png" % [nome, nome, vista])

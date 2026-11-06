extends Sala

const VISTAS: Array[String] = ["lado", "frente", "tres_quartos", "costas", "tres_quartos_costas"]
const PASTA_ZANE := "res://assets/sprites/personagens/zane/zane_%s.png"


func _ready() -> void:
	super()
	if Engine.is_editor_hint():
		return
	_vestir_zane.call_deferred()


func _vestir_zane() -> void:
	var jogador := get_tree().get_first_node_in_group("jogador")
	if jogador == null:
		return
	for vista in VISTAS:
		var andando := _textura("andar_" + vista)
		jogador.set("sprite_" + vista, _textura(vista))
		jogador.set("andar_" + vista, andando)
		jogador.set("correr_" + vista, andando)
		jogador.set("parado_" + vista, _textura("parado_" + vista))


func _textura(nome: String) -> Texture2D:
	return load(PASTA_ZANE % nome) as Texture2D

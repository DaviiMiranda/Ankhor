class_name AtorDeCena
extends RefCounted

const QUADROS_ANDAR := 12
const PX_POR_QUADRO := 2.8


static func andar_ate(personagem: PersonagemParado, destino: Vector2, velocidade: float) -> Tween:
	var sprite := personagem.sprite
	var distancia := personagem.position.distance_to(destino)
	var duracao := maxf(distancia / velocidade, 0.01)
	var para_esquerda := destino.x < personagem.position.x
	personagem.set_process(false)
	sprite.texture = tira_de_andar(personagem)
	sprite.hframes = QUADROS_ANDAR
	sprite.flip_h = para_esquerda
	var mostrar_quadro := func(quadro: float) -> void: sprite.frame = int(quadro) % QUADROS_ANDAR
	var parar := func() -> void:
		personagem.virar("lado", para_esquerda)
		personagem.set_process(true)
	var tween := personagem.create_tween().set_parallel()
	tween.tween_property(personagem, "position", destino, duracao)
	tween.tween_method(mostrar_quadro, 0.0, distancia / PX_POR_QUADRO, duracao)
	tween.chain().tween_callback(parar)
	return tween


static func tira_de_andar(personagem: PersonagemParado) -> Texture2D:
	return load(personagem.parado_lado.resource_path.replace("_parado_", "_andar_"))

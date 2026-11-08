class_name AtorDeCena
extends RefCounted

const QUADROS_ANDAR := 12
const PX_POR_QUADRO_ANDANDO := 2.8
const LARGURA_DO_QUADRO := 96
const PX_POR_QUADRO_CORRENDO := {24: 5.0, 48: 5.6}


static func andar_ate(personagem: PersonagemParado, destino: Vector2, velocidade: float) -> Tween:
	return _ir_ate(personagem, destino, velocidade, false)


static func correr_ate(personagem: PersonagemParado, destino: Vector2, velocidade: float) -> Tween:
	return _ir_ate(personagem, destino, velocidade, true)


static func mostrar_corrida(personagem: PersonagemParado, andado: float, para_esquerda := false) -> void:
	var tira := tira_de_correr(personagem)
	var quadros := tira.get_width() / LARGURA_DO_QUADRO if tira else QUADROS_ANDAR
	var px_por_quadro: float = PX_POR_QUADRO_CORRENDO.get(quadros, 5.0) if tira else PX_POR_QUADRO_ANDANDO
	personagem.set_process(false)
	personagem.sprite.texture = tira if tira else tira_de_andar(personagem)
	personagem.sprite.hframes = quadros
	personagem.sprite.flip_h = para_esquerda
	personagem.sprite.frame = int(andado / px_por_quadro) % quadros


static func parar(personagem: PersonagemParado, para_esquerda := false) -> void:
	personagem.virar("lado", para_esquerda)
	personagem.set_process(true)


static func tira_de_andar(personagem: PersonagemParado) -> Texture2D:
	return load(personagem.parado_lado.resource_path.replace("_parado_", "_andar_"))


static func tira_de_correr(personagem: PersonagemParado) -> Texture2D:
	var caminho := personagem.parado_lado.resource_path.replace("_parado_", "_correr_")
	return load(caminho) if ResourceLoader.exists(caminho) else null


static func _ir_ate(personagem: PersonagemParado, destino: Vector2, velocidade: float, correndo: bool) -> Tween:
	var distancia := personagem.position.distance_to(destino)
	var duracao := maxf(distancia / velocidade, 0.01)
	var para_esquerda := destino.x < personagem.position.x
	var mostrar := func(andado: float) -> void:
		if correndo:
			mostrar_corrida(personagem, andado, para_esquerda)
		else:
			_mostrar_caminhada(personagem, andado, para_esquerda)
	var tween := personagem.create_tween().set_parallel()
	tween.tween_property(personagem, "position", destino, duracao)
	tween.tween_method(mostrar, 0.0, distancia, duracao)
	tween.chain().tween_callback(func() -> void: parar(personagem, para_esquerda))
	return tween


static func _mostrar_caminhada(personagem: PersonagemParado, andado: float, para_esquerda: bool) -> void:
	personagem.set_process(false)
	personagem.sprite.texture = tira_de_andar(personagem)
	personagem.sprite.hframes = QUADROS_ANDAR
	personagem.sprite.flip_h = para_esquerda
	personagem.sprite.frame = int(andado / PX_POR_QUADRO_ANDANDO) % QUADROS_ANDAR

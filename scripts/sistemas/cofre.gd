class_name Cofre
extends PainelCodigo

@export var quantidade: int = 1
@export var textura_aberto: Texture2D


func _ready() -> void:
	super()
	if Progresso.tem(marca):
		_soltar_recompensa.call_deferred()


func _ao_mudar() -> void:
	sprite.texture = textura_aberto if Progresso.tem(marca) else textura_apagado


func _confirmar() -> void:
	som_tecla.play()
	if _digitado() != codigo:
		som_erro.play()
		visor.text = "CÓDIGO INVÁLIDO"
		visor.add_theme_color_override("font_color", COR_ERRO)
		return
	visor.text = "COFRE ABERTO"
	visor.add_theme_color_override("font_color", COR_DIGITO)
	Progresso.marcar(marca)
	_soltar_recompensa()
	await get_tree().create_timer(0.8, true).timeout
	_fechar()
	Inventario.aviso.emit(aviso_aberto)


func _soltar_recompensa() -> void:
	Recompensa.soltar(self, item_ao_abrir, null, quantidade)

class_name Cofre
extends PainelCodigo

const CENA_ITEM := preload("res://cenas/itens/item_no_chao.tscn")

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
	if item_ao_abrir == null:
		return
	for i in quantidade:
		var recompensa := CENA_ITEM.instantiate() as ItemNoChao
		recompensa.name = "Recompensa%d" % (i + 1)
		recompensa.item = item_ao_abrir
		recompensa.position = position + Vector2(-8 + 16 * i - 8 * (quantidade - 1), 12)
		get_parent().add_child(recompensa)

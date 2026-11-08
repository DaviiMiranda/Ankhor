extends "res://scripts/menu_principal.gd"

signal transicao_novo_jogo_solicitada
signal transicao_novo_jogo_concluida

var _novo_jogo_iniciado := false


func _ready() -> void:
	super._ready()
	luz.enabled = false
	efeito_crt_rect.hide()
	for painel: Control in [menu, lista_fases, painel_carregar, painel_opcoes, painel_controles, painel_creditos]:
		painel.position = Vector2(12, 8)
		painel.size = Vector2(232, 144)
	var titulo: Label = $Monitor/Menu/Titulo
	titulo.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	menu.add_theme_constant_override("separation", 5)


func _process(_delta: float) -> void:
	pass


func _ao_apertar_novo_jogo() -> void:
	if _novo_jogo_iniciado:
		return
	_novo_jogo_iniciado = true
	novo_jogo_pedido.emit()
	transicao_novo_jogo_solicitada.emit()
	await transicao_novo_jogo_concluida
	_comecar_do_zero()
	if cena_novo_jogo:
		get_tree().change_scene_to_packed(cena_novo_jogo)
	else:
		print("Menu: ainda não há cena de novo jogo configurada.")


func _ao_mudar_configuracoes() -> void:
	efeito_crt_rect.hide()
	_atualizar_textos_opcoes()

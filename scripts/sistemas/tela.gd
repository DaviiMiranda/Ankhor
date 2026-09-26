extends Node
## Tela cheia e janela: a tecla F11 (ação "tela_cheia") alterna entre as duas.
##
## É um autoload (como o Inventario): funciona em qualquer cena, até no menu
## e com o jogo pausado.
##
## Por que o jogo continua nítido em qualquer tamanho: ele é desenhado em
## 320 x 180 e depois AMPLIADO por um número inteiro (Configurações do
## Projeto > Exibição > Janela > Stretch: mode "viewport", scale "integer").
## Em Full HD (1920 x 1080) a ampliação é exatamente 6: cada pixel da arte
## vira um quadrado de 6 x 6 pixels do monitor. Na janela (1280 x 720), 4.
## Com número inteiro, nenhum pixel fica maior que o vizinho e nada borra.
##
## O jogo abre em tela cheia (Exibição > Janela > Modo: Fullscreen).


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS


func _unhandled_input(evento: InputEvent) -> void:
	if evento.is_action_pressed("tela_cheia"):
		alternar()
		get_viewport().set_input_as_handled()


## Tela cheia <-> janela.
func alternar() -> void:
	if DisplayServer.window_get_mode() == DisplayServer.WINDOW_MODE_FULLSCREEN:
		DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
		# Volta ao tamanho da janela (4 x 320 x 180) e centraliza na tela.
		var tamanho := Vector2i(1280, 720)
		DisplayServer.window_set_size(tamanho)
		var area := DisplayServer.screen_get_usable_rect(DisplayServer.window_get_current_screen())
		DisplayServer.window_set_position(area.position + (area.size - tamanho) / 2)
	else:
		DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_FULLSCREEN)

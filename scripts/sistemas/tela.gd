extends Node


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS


func _unhandled_input(evento: InputEvent) -> void:
	if evento.is_action_pressed("tela_cheia"):
		alternar()
		get_viewport().set_input_as_handled()


func alternar() -> void:
	if DisplayServer.window_get_mode() == DisplayServer.WINDOW_MODE_FULLSCREEN:
		DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
		var tamanho := Vector2i(1280, 720)
		DisplayServer.window_set_size(tamanho)
		var area := DisplayServer.screen_get_usable_rect(DisplayServer.window_get_current_screen())
		DisplayServer.window_set_position(area.position + (area.size - tamanho) / 2)
	else:
		DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_FULLSCREEN)

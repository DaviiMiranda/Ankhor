extends Cutscene


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	animacao.process_mode = Node.PROCESS_MODE_PAUSABLE
	super()


func pensar(caminho_dialogo: String) -> void:
	Dialogos.iniciar(caminho_dialogo)


func _terminar() -> void:
	while Dialogos.ativo and not Dialogos.esperando_escolha():
		Dialogos.avancar()
	super()

extends MecanismoDoTempo

const COMANDOS: Array[String] = ["LOAD ANCORA", "LIST", "RUN"]
const RESPOSTAS: Array[String] = ["SEARCHING FOR ANCORA|LOADING|READY.", "10 REM CALIBRAR ANCORA|20 GOTO 1985|READY.", "CALIBRANDO..."]
const ERRO := "?SYNTAX ERROR"
const MAXIMO_DE_LETRAS := 22
const LINHAS_NA_TELA := 6
const ALTURA_LINHA := 14.0
const COR_FOSFORO := Color("6ae06e")
const COR_TELA := Color("06140a")

var _digitado := ""
var _historico: Array[String] = []
var _resposta_certa := false


func _preparar() -> void:
	_digitado = ""
	_historico.clear()
	_historico.append("ANCORA BASIC V1.0")
	_historico.append("READY.")
	_mostrar_dica()


func _input(evento: InputEvent) -> void:
	if not _aberto or _travado or not evento is InputEventKey:
		return
	var tecla := evento as InputEventKey
	if tecla.pressed:
		_digitar(tecla)
	get_viewport().set_input_as_handled()


func _digitar(tecla: InputEventKey) -> void:
	if tecla.is_action_pressed("ui_cancel"):
		_fechar()
	elif tecla.keycode == KEY_ENTER or tecla.keycode == KEY_KP_ENTER:
		_executar()
	elif tecla.keycode == KEY_BACKSPACE:
		_digitado = _digitado.left(-1)
	elif tecla.unicode >= 32 and _digitado.length() < MAXIMO_DE_LETRAS:
		_digitado += String.chr(tecla.unicode).to_upper()


func _executar() -> void:
	_historico.append(_digitado)
	_resposta_certa = _digitado.strip_edges() == COMANDOS[_acertos]
	_digitado = ""
	var respostas := RESPOSTAS[_acertos].split("|") if _resposta_certa else PackedStringArray([ERRO])
	for resposta in respostas:
		_historico.append(resposta)
	_tentar()


func _acertou() -> bool:
	return _resposta_certa


func _ao_acertar() -> void:
	_mostrar_dica()


func _erro_zera_acertos() -> bool:
	return false


func _mostrar_dica() -> void:
	dica.text = "Digite: %s     Enter: executar     Esc: sair" % COMANDOS[mini(_acertos, COMANDOS.size() - 1)]


func _desenhar(_centro: Vector2) -> void:
	desenho.draw_rect(Rect2(Vector2.ZERO, desenho.size), COR_TELA)
	for y in range(0, int(desenho.size.y), 2):
		desenho.draw_line(Vector2(0, y), Vector2(desenho.size.x, y), Color(0, 0, 0, 0.25), 1.0)
	var fonte := desenho.get_theme_default_font()
	var linhas := _historico.slice(maxi(_historico.size() - (LINHAS_NA_TELA - 1), 0))
	var cursor := "_" if fmod(_tempo, 0.8) < 0.4 else " "
	linhas.append("" if _travado else _digitado + cursor)
	for i in linhas.size():
		var cor := COR_ERRO if linhas[i] == ERRO else COR_FOSFORO
		desenho.draw_string(fonte, Vector2(4.0, 11.0 + i * ALTURA_LINHA), linhas[i], HORIZONTAL_ALIGNMENT_LEFT, desenho.size.x - 8.0, 8, cor)

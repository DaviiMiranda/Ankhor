extends Control

@export_range(0.5, 1.0) var resolucao_do_3d := 1.0
@export var alvo_da_camera := Vector3(-2.30, 1.04, -0.2)

@onready var imagem: SubViewportContainer = $Imagem
@onready var mundo: SubViewport = $Imagem/Mundo
@onready var camera: Camera3D = $Imagem/Mundo/Camera
@onready var modelo: Node3D = $Imagem/Mundo/Modelo
@onready var tela_menu: SubViewport = $TelaMenu

var _origem_tela := Vector3.ZERO
var _direita_tela := Vector3.ZERO
var _baixo_tela := Vector3.ZERO
var _plano_tela := Plane()
var _mouse_sobre_tela := false


func _ready() -> void:
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	camera.look_at(alvo_da_camera)
	_ajustar_resolucao()
	get_window().size_changed.connect(_ajustar_resolucao)
	var tela := modelo.find_child("TelaNotebook", true, false) as MeshInstance3D
	_preparar_superficie(tela)
	var material := StandardMaterial3D.new()
	material.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	material.texture_filter = BaseMaterial3D.TEXTURE_FILTER_NEAREST
	material.albedo_texture = tela_menu.get_texture()
	tela.material_override = material
	var paisagem := modelo.find_child("PaisagemDaJanela", true, false) as MeshInstance3D
	var material_janela := StandardMaterial3D.new()
	material_janela.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	material_janela.texture_filter = BaseMaterial3D.TEXTURE_FILTER_NEAREST
	material_janela.albedo_texture = preload("res://assets/sprites/cenario/visor/janela_prologo.png")
	paisagem.material_override = material_janela
	$Rodape/RotuloVersao.show()


func _ajustar_resolucao() -> void:
	var tamanho := get_viewport_rect().size
	var pixels := (Vector2(get_window().size) * resolucao_do_3d).round().max(tamanho)
	imagem.stretch = false
	imagem.set_anchors_and_offsets_preset(Control.PRESET_TOP_LEFT)
	mundo.size = Vector2i(pixels)
	imagem.size = pixels
	imagem.scale = tamanho / pixels


func _preparar_superficie(tela: MeshInstance3D) -> void:
	var dados := tela.mesh.surface_get_arrays(0)
	var vertices: PackedVector3Array = dados[Mesh.ARRAY_VERTEX]
	var coordenadas: PackedVector2Array = dados[Mesh.ARRAY_TEX_UV]
	var canto_direito := Vector3.ZERO
	var canto_inferior := Vector3.ZERO
	for i in vertices.size():
		var uv := coordenadas[i]
		var ponto := tela.to_global(vertices[i])
		if uv.x < 0.1 and uv.y < 0.1:
			_origem_tela = ponto
		elif uv.x > 0.9 and uv.y < 0.1:
			canto_direito = ponto
		elif uv.x < 0.1 and uv.y > 0.9:
			canto_inferior = ponto
	_direita_tela = canto_direito - _origem_tela
	_baixo_tela = canto_inferior - _origem_tela
	_plano_tela = Plane(_direita_tela.cross(_baixo_tela).normalized(), _origem_tela)


func _posicao_na_tela(posicao: Vector2) -> Vector2:
	var ponto_camera := posicao / imagem.scale
	var origem := camera.project_ray_origin(ponto_camera)
	var direcao := camera.project_ray_normal(ponto_camera)
	var encontro: Variant = _plano_tela.intersects_ray(origem, direcao)
	if encontro == null:
		return Vector2(-1, -1)
	var local: Vector3 = encontro - _origem_tela
	return Vector2(local.dot(_direita_tela) / _direita_tela.length_squared(), local.dot(_baixo_tela) / _baixo_tela.length_squared()) * Vector2(tela_menu.size)


func _input(evento: InputEvent) -> void:
	if not is_node_ready():
		return
	if evento is InputEventMouse:
		var no_notebook := evento.duplicate() as InputEventMouse
		no_notebook.position = _posicao_na_tela(evento.position)
		no_notebook.global_position = no_notebook.position
		var dentro := Rect2(Vector2.ZERO, Vector2(tela_menu.size)).has_point(no_notebook.position)
		if dentro != _mouse_sobre_tela:
			_mouse_sobre_tela = dentro
			if dentro:
				tela_menu.notify_mouse_entered()
			else:
				tela_menu.notify_mouse_exited()
		if no_notebook is InputEventMouseMotion:
			no_notebook.relative = no_notebook.position - _posicao_na_tela(evento.position - evento.relative)
		tela_menu.push_input(no_notebook, true)
		get_viewport().set_input_as_handled()
	elif evento is InputEventKey or evento is InputEventJoypadButton or evento is InputEventJoypadMotion:
		var encaminhado := _adaptar_tecla(evento)
		tela_menu.push_input(encaminhado, true)
		get_viewport().set_input_as_handled()


func _adaptar_tecla(evento: InputEvent) -> InputEvent:
	var acoes := {"mover_cima": "ui_up", "mover_baixo": "ui_down", "mover_esquerda": "ui_left", "mover_direita": "ui_right", "interagir": "ui_accept"}
	for acao: String in acoes:
		if evento.is_action(acao):
			var adaptado := InputEventAction.new()
			adaptado.action = acoes[acao]
			adaptado.pressed = evento.is_pressed()
			adaptado.strength = evento.get_action_strength(acao)
			return adaptado
	return evento

class_name PainelCriacao
extends Control

@onready var nome: Label = $Nome
@onready var descricao: Label = $Descricao
@onready var estoque: Label = $Estoque
@onready var situacao: Label = $Situacao


func _ready() -> void:
	nome.text = "BALA DE IMPULSO"
	descricao.text = "Carga da arma de impulso. Cada bala gasta %d pilhas." % Criacao.PILHAS_POR_BALA
	visibility_changed.connect(atualizar)


func atualizar() -> void:
	if not is_node_ready() or not is_visible_in_tree():
		return
	estoque.text = "Pilhas: %d/%d\nBalas da arma: %d/%d" % [Inventario.pilhas(), Inventario.MAXIMO_PILHAS,
			Criacao.balas(), Criacao.ARMA.maximo_unidades]
	var motivo := Criacao.motivo_de_nao_criar()
	situacao.text = "E: criar uma bala" if motivo.is_empty() else motivo

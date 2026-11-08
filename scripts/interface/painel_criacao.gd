class_name PainelCriacao
extends Control

enum Receita { BALA, FLASH }

var receita := Receita.BALA

@onready var icone: TextureRect = $Icone
@onready var nome: Label = $Nome
@onready var descricao: Label = $Descricao
@onready var estoque: Label = $Estoque
@onready var situacao: Label = $Situacao


func _ready() -> void:
	visibility_changed.connect(atualizar)


func trocar_receita() -> void:
	receita = Receita.FLASH if receita == Receita.BALA else Receita.BALA
	atualizar()


func criar() -> bool:
	return Criacao.criar_bala() if receita == Receita.BALA else Criacao.criar_flash()


func nome_da_receita() -> String:
	return "Bala de impulso" if receita == Receita.BALA else "Flash"


func atualizar() -> void:
	if not is_node_ready() or not is_visible_in_tree():
		return
	var bala := receita == Receita.BALA
	icone.texture = Criacao.ARMA.icone if bala else Criacao.FLASH.icone
	nome.text = "< BALA DE IMPULSO >" if bala else "< FLASH >"
	descricao.text = "1 chip + 3 pilhas" if bala else "1 chip + 1 pilha"
	var quantidade := Criacao.balas() if bala else Criacao.flashes()
	var limite := Criacao.ARMA.maximo_unidades if bala else Criacao.FLASH.maximo_unidades
	estoque.text = "Chips: %d/%d   Pilhas: %d/%d\n%s: %d/%d" % [Criacao.chips(), Criacao.CHIPS.maximo_unidades,
			Inventario.pilhas(), Inventario.MAXIMO_PILHAS, "Balas" if bala else "Flashes", quantidade, limite]
	var motivo := Criacao.motivo_de_nao_criar_bala() if bala else Criacao.motivo_de_nao_criar_flash()
	situacao.text = "E: criar" if motivo.is_empty() else motivo

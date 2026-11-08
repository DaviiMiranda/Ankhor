class_name PerfilZane
extends RefCounted

const MAOS := preload("res://scripts/personagens/maos_do_zane.gd")
const KIT: Array[Item] = [
	preload("res://dados/itens/clarao.tres"),
	preload("res://dados/itens/braco_hack.tres"),
]
const VISTAS: Array[String] = ["lado", "frente", "tres_quartos", "costas", "tres_quartos_costas"]
const PASTA_SPRITES := "res://assets/sprites/personagens/zane/zane_%s.png"
const TIRAS_DO_CASACO := {
	"lado": preload("res://assets/sprites/personagens/zane/zane_casaco_lado.png"),
	"frente": preload("res://assets/sprites/personagens/zane/zane_casaco_frente.png"),
	"tres_quartos": preload("res://assets/sprites/personagens/zane/zane_casaco_tres_quartos.png"),
	"costas": preload("res://assets/sprites/personagens/zane/zane_casaco_costas.png"),
	"tres_quartos_costas": preload("res://assets/sprites/personagens/zane/zane_casaco_tres_quartos_costas.png"),
}
const ESTAMINA_MAXIMA := 160.0
const QUADROS_CORRER := 48
const PX_POR_QUADRO_CORRENDO := 5.6


static func aplicar(jogador: Gabriel) -> void:
	for vista in VISTAS:
		jogador.set("sprite_" + vista, _textura(vista))
		jogador.set("andar_" + vista, _textura("andar_" + vista))
		jogador.set("correr_" + vista, _textura("correr_" + vista))
		jogador.set("parado_" + vista, _textura("parado_" + vista))
	jogador.quadros_correr = QUADROS_CORRER
	jogador.px_por_quadro_correndo = PX_POR_QUADRO_CORRENDO
	jogador.tabela_maos = MAOS.MAOS
	jogador.tabela_maos_correndo = MAOS.MAOS_CORRENDO
	jogador.tiras_do_gesto_da_mochila = TIRAS_DO_CASACO
	jogador.fadiga.estamina_maxima = ESTAMINA_MAXIMA
	jogador.fadiga.reiniciar()
	if not Inventario.com_kit_emprestado():
		Inventario.emprestar_kit(KIT)


static func devolver_inventario() -> void:
	Inventario.devolver_kit()


static func _textura(nome: String) -> Texture2D:
	return load(PASTA_SPRITES % nome) as Texture2D

# gerar_efeitos_inventario.py — compõe por código os sons de equipar e
# desequipar um gadget na tela do inventário.
#
# Como rodar (Python 3 + numpy):
#   python assets/modelagem/audio/gerar_efeitos_inventario.py
#
# Gera:
#   assets/audio/efeitos/interface/gadget_equipar.wav      ao pôr numa tecla (1-3)
#   assets/audio/efeitos/interface/gadget_desequipar.wav   ao tirar da tecla
#
# Os dois têm de ser sutis: quem organiza a mochila aperta essas teclas várias
# vezes seguidas. Cada um dura menos de 0,2 s e tem pico em -16 dB.
#
# O som é o de um objeto preso num mosquetão da mochila, em duas partes:
#   1. o pano mexendo: ruído em faixa média, com envelope exponencial curto;
#   2. o estalo do metal: duas frequências que não formam acorde (a razão
#      1 : 1,62 não é uma razão simples, e é isso que soa como metal, não como
#      nota), morrendo em poucos milissegundos.
#
# Equipar e desequipar são o mesmo gesto com a ordem e a altura trocadas. Ao
# equipar, o metal vem por último e mais agudo: soa como "travou". Ao desequipar,
# o metal vem primeiro e mais grave: soa como "soltou".
# As ferramentas (envelope, filtro, salvar) vêm do gerar_efeitos_gabriel.py.

import importlib.util
import os

import numpy as np

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
PASTA_INTERFACE = os.path.join(PASTA_PROJETO, "assets", "audio", "efeitos", "interface")

_spec = importlib.util.spec_from_file_location(
    "gerar_efeitos_gabriel", os.path.join(PASTA_SCRIPT, "gerar_efeitos_gabriel.py"))
ef = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ef)

tempo, envelope, filtrar, normalizar, salvar = ef.tempo, ef.envelope, ef.filtrar, ef.normalizar, ef.salvar
rng = np.random.default_rng(2026)
DURACAO = 0.18
PICO_DB = -16.0


def estalo_de_metal(t, inicio, frequencia):
    onda = np.sin(2 * np.pi * frequencia * t) + 0.6 * np.sin(2 * np.pi * frequencia * 1.62 * t)
    return onda * envelope(t, inicio, 0.007, ataque=0.0005)


def pano(t, inicio):
    ruido = filtrar(rng.standard_normal(len(t)), corte_baixo=500, corte_alto=3500)
    ruido /= np.max(np.abs(ruido))
    return ruido * envelope(t, inicio, 0.025, ataque=0.006)


def gadget_equipar():
    t = tempo(DURACAO)
    return normalizar(0.5 * pano(t, 0.0) + estalo_de_metal(t, 0.055, 2600), PICO_DB)


def gadget_desequipar():
    t = tempo(DURACAO)
    return normalizar(estalo_de_metal(t, 0.0, 1900) + 0.5 * pano(t, 0.035), PICO_DB)


def main():
    print("[efeitos do inventário]")
    salvar(os.path.join(PASTA_INTERFACE, "gadget_equipar.wav"), gadget_equipar())
    salvar(os.path.join(PASTA_INTERFACE, "gadget_desequipar.wav"), gadget_desequipar())


if __name__ == "__main__":
    main()

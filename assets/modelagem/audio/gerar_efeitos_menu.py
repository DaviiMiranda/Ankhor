# gerar_efeitos_menu.py — compõe por código os sons do menu principal.
#
# Como rodar (Python 3 + numpy):
#   python assets/modelagem/audio/gerar_efeitos_menu.py
#
# Gera:
#   assets/audio/efeitos/interface/menu_passar.wav   ao passar por uma opção
#   assets/audio/efeitos/interface/menu_clique.wav   ao escolher uma opção
#
# O menu é a tela de um computador velho (um monitor CRT na mesa). Os sons
# são os de um computador assim: um "bip" curto e baixo ao mover a seleção
# e, ao escolher, o clique do botão do mouse seguido de um bipe de
# confirmação subindo (quinta justa, 660 -> 990 Hz: soa como "ok").
#
# O bipe é uma onda QUADRADA suavizada: seno passado por tanh com ganho
# alto (tanh achata a onda, que vira quase quadrada; é o timbre dos alto-
# falantes de PC antigos) e depois um passa-baixa para não ficar estridente.
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

TAXA = ef.TAXA
tempo, envelope, filtrar, normalizar, salvar = ef.tempo, ef.envelope, ef.filtrar, ef.normalizar, ef.salvar
rng = np.random.default_rng(1994)


def bipe(t, inicio, f, duracao):
    """Onda quase quadrada (tanh de um seno) com envelope curto."""
    forma = envelope(t, inicio, duracao / 3, 0.002) * (t < inicio + duracao)
    return np.tanh(4 * np.sin(2 * np.pi * f * (t - inicio))) * forma


def menu_passar():
    """Bipe de 40 ms em 1320 Hz, baixinho: não pode cansar quem fica
    subindo e descendo pelas opções."""
    t = tempo(0.08)
    return normalizar(filtrar(bipe(t, 0.0, 1320, 0.04), corte_alto=3500), -20.0)


def menu_clique():
    """O clique do mouse (dois estalos: o botão descendo e subindo) e o
    bipe de confirmação em duas notas subindo."""
    t = tempo(0.25)
    n = len(t)
    clique = filtrar(rng.standard_normal(n), corte_baixo=1500, corte_alto=7000)
    clique *= envelope(t, 0.0, 0.002, 0.0002) + 0.5 * envelope(t, 0.035, 0.0015, 0.0002)
    clique /= np.max(np.abs(clique)) + 1e-9
    confirma = bipe(t, 0.05, 660, 0.05) + bipe(t, 0.1, 990, 0.08)
    return normalizar(0.8 * clique + 0.45 * filtrar(confirma, corte_alto=3500), -10.0)


def main():
    print("[efeitos do menu]")
    salvar(os.path.join(PASTA_INTERFACE, "menu_passar.wav"), menu_passar())
    salvar(os.path.join(PASTA_INTERFACE, "menu_clique.wav"), menu_clique())


if __name__ == "__main__":
    main()

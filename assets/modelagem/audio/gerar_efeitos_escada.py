# gerar_efeitos_escada.py — compõe por código o som de SUBIR (ou descer) a ESCADA
# de metal entre a praça de alimentação e o mezanino do Centro de Convivência
# (assets/modelagem/cenario/gerar_andar2.py).
#
# Como rodar (Python 3 + numpy):
#   python assets/modelagem/audio/gerar_efeitos_escada.py
#
# Gera:
#   assets/audio/efeitos/objetos/escada.wav   1,10 s
#
# Oito passos em degraus de grade de aço, cada um um pouco mais baixo que o
# anterior (a pessoa se afasta), com o eco do vão da escada por cima.
#
# Componentes sintetizados em cada passo:
#   1. Baque da sola: uma senoide grave (95 ou 105 Hz, alternando o pé) com
#      decaimento exponencial.
#   2. Clique da grade: um estalo de ruído filtrado entre 900 e 7000 Hz.
#   3. Ressonância do degrau: uma senoide de 1500 a 1660 Hz que morre rápido,
#      o "tinido" do metal.
# No fim, a mistura passa pela reverberação do vão (a função sala).

import importlib.util
import os

import numpy as np

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
PASTA_OBJETOS = os.path.join(PASTA_PROJETO, "assets", "audio", "efeitos", "objetos")

_spec = importlib.util.spec_from_file_location("gerar_efeitos_gabriel", os.path.join(PASTA_SCRIPT, "gerar_efeitos_gabriel.py"))
ef = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ef)

TAXA = ef.TAXA
tempo, envelope, filtrar, normalizar, salvar, sala = ef.tempo, ef.envelope, ef.filtrar, ef.normalizar, ef.salvar, ef.sala


def escada():
    rng = np.random.default_rng(3028)
    t = tempo(1.1)
    n = len(t)
    soma = np.zeros(n)
    for k in range(8):
        inicio = 0.04 + k * 0.12 + rng.uniform(-0.008, 0.008)
        forca = 1.0 - 0.07 * k
        grave = 95.0 + 10.0 * (k % 2)
        soma += np.sin(2 * np.pi * grave * (t - inicio)) * envelope(t, inicio, 0.05, ataque=0.002) * 0.7 * forca
        estalo = rng.standard_normal(n) * envelope(t, inicio, 0.012, ataque=0.0008)
        soma += filtrar(estalo, corte_baixo=900, corte_alto=7000) * 0.5 * forca
        soma += np.sin(2 * np.pi * (1500.0 + 80.0 * (k % 3)) * (t - inicio)) * envelope(t, inicio, 0.09, ataque=0.001) * 0.12 * forca
    return normalizar(sala(soma, mistura=0.28), -6.0)


def main():
    print("[efeito sonoro da escada do mezanino]")
    salvar(os.path.join(PASTA_OBJETOS, "escada.wav"), escada())


if __name__ == "__main__":
    main()

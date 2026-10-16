# gerar_efeitos_porta_restaurante.py — compõe por código o som da PORTA DE VIDRO
# dos restaurantes do Centro de Convivência (a porta automática de duas folhas
# que correm para os lados: assets/modelagem/cenario/gerar_porta_restaurante.py).
#
# Como rodar (Python 3 + numpy):
#   python assets/modelagem/audio/gerar_efeitos_porta_restaurante.py
#
# Gera:
#   assets/audio/efeitos/objetos/porta_restaurante.wav   0,95 s
#
# Diferente das portas de aço do Bloco de salas (trinco, rodízios, amortecedor),
# esta é leve e eletrônica: um sensor que apita duas notas, o motorzinho que
# sobe de tom e desce, o vidro deslizando no trilho e a batidinha de borracha
# no fim.
#
# Componentes sintetizados:
#   1. Sensor de presença: duas notas de sino (1175 Hz e 1760 Hz, um quinto
#      acima) em sequência, cada uma com decaimento exponencial.
#   2. Motor: uma senoide cuja frequência sobe de 230 para 430 Hz e volta,
#      seguindo a velocidade v(t) = sen(pi * x)^1,2 das folhas. A fase é a
#      INTEGRAL da frequência (soma acumulada), senão o tom daria saltos.
#   3. Vidro no trilho: ruído filtrado entre 1800 e 7000 Hz, modulado por v(t).
#   4. Ar do mecanismo: um sopro curto entre 3000 e 9000 Hz.
#   5. Parada: baque de borracha grave (90 Hz) e um estalo de plástico.

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


def porta_restaurante():
    rng = np.random.default_rng(3027)
    t = tempo(0.95)
    n = len(t)
    sino = np.zeros(n)
    for inicio, freq in ((0.0, 1175.0), (0.11, 1760.0)):
        sino += np.sin(2 * np.pi * freq * (t - inicio)) * envelope(t, inicio, 0.09, ataque=0.002) * 0.45
        sino += np.sin(2 * np.pi * freq * 2.01 * (t - inicio)) * envelope(t, inicio, 0.04, ataque=0.001) * 0.12
    x = np.clip((t - 0.12) / 0.6, 0.0, 1.0)
    v = np.sin(np.pi * x) ** 1.2
    frequencia = 230.0 + 200.0 * v
    fase = np.cumsum(frequencia) / TAXA
    motor = np.sin(2 * np.pi * fase) * v * 0.32
    motor += np.sin(4 * np.pi * fase) * v * 0.1
    vidro = filtrar(rng.standard_normal(n), corte_baixo=1800, corte_alto=7000) * v * 0.35
    ar = filtrar(rng.standard_normal(n), corte_baixo=3000, corte_alto=9000) * envelope(t, 0.12, 0.16, ataque=0.01) * 0.18
    t_fim = 0.74
    baque = np.sin(2 * np.pi * 90 * (t - t_fim)) * envelope(t, t_fim, 0.07, ataque=0.003) * 0.9
    baque += filtrar(rng.standard_normal(n) * envelope(t, t_fim, 0.02, ataque=0.001), corte_baixo=600, corte_alto=5000) * 0.35
    soma = sino + motor + vidro + ar + baque
    return normalizar(sala(soma, mistura=0.16), -5.0)


def main():
    print("[efeito sonoro da porta de vidro dos restaurantes]")
    salvar(os.path.join(PASTA_OBJETOS, "porta_restaurante.wav"), porta_restaurante())


if __name__ == "__main__":
    main()

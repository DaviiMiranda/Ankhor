# gerar_efeitos_porta_correr.py — compõe por código o som da porta de correr
# de madeira com batente de aço da Biblioteca.
#
# Como rodar (Python 3 + numpy):
#   python assets/modelagem/audio/gerar_efeitos_porta_correr.py
#
# Gera:
#   assets/audio/efeitos/objetos/porta_correr.wav   1,3 s: trinco, rodinhas no trilho,
#                                                   raspar da folha e a batida no batente
#
# O porta_abrir.wav (porta de dobradiça) não serve para a animação: aqui a
# folha desliza de lado, então o som é de movimento contínuo e não de rangido.
#
# Ferramentas (envelope, filtro pela FFT, reverberação, salvar) do
# gerar_efeitos_gabriel.py e o metal inarmônico do gerar_efeitos_labirinto.py.
#
# - PERFIL DE VELOCIDADE v(t): a folha acelera e freia, então a intensidade
#   de tudo segue uma meia-senoide, v = sen(pi·x)^1,2, com x indo de 0 a 1
#   durante o deslizamento. Quanto mais rápido, mais alto e mais agudo.
# - RODINHAS: ruído grave multiplicado por |sen(pi·fase)|^3. A fase é a
#   integral da frequência de giro (np.cumsum(f) / TAXA), por isso o ritmo
#   do "tru-tru-tru" acelera e desacelera junto com a folha.
# - RASPAR: ruído agudo em estalos esparsos (pontos sorteados com chance
#   proporcional a v): é a folha roçando areia e poeira no trilho.
# - BATIDA: um baque grave de 62 Hz, ruído abafado e uma madeira curta que
#   rebate uma segunda vez, mais fraca, como a folha quicando no batente.

import importlib.util
import os

import numpy as np

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
PASTA_OBJETOS = os.path.join(PASTA_PROJETO, "assets", "audio", "efeitos", "objetos")

_spec = importlib.util.spec_from_file_location(
    "gerar_efeitos_labirinto", os.path.join(PASTA_SCRIPT, "gerar_efeitos_labirinto.py"))
lab = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lab)

ef = lab.ef
TAXA = ef.TAXA
tempo, envelope, filtrar, normalizar, salvar, sala = ef.tempo, ef.envelope, ef.filtrar, ef.normalizar, ef.salvar, ef.sala
metal = lab.metal

INICIO_DESLIZE = 0.06
FIM_DESLIZE = 0.88


def porta_correr():
    g = np.random.default_rng(1986)
    t = tempo(1.3)
    n = len(t)

    x = np.clip((t - INICIO_DESLIZE) / (FIM_DESLIZE - INICIO_DESLIZE), 0.0, 1.0)
    v = np.sin(np.pi * x) ** 1.2

    trinco = metal(t, 900, 0.0, ((1.0, 1.0, 0.02), (2.4, 0.5, 0.012)), 0.5)
    trinco += np.sin(2 * np.pi * 140 * t) * envelope(t, 0.0, 0.03) * 0.5

    giro = 6.0 + 16.0 * v
    fase = np.cumsum(giro) / TAXA
    pulso = np.abs(np.sin(np.pi * fase)) ** 3
    rodinhas = filtrar(g.standard_normal(n), corte_baixo=80, corte_alto=700) * (0.35 + 0.65 * pulso) * v * 1.6

    chance = 0.012 + 0.05 * v
    estalos = (g.random(n) < chance).astype(float) * g.standard_normal(n)
    raspar = filtrar(estalos, corte_baixo=1200, corte_alto=7000) * 3.0 * v
    raspar += filtrar(g.standard_normal(n), corte_baixo=1800, corte_alto=5000) * 0.12 * v ** 2

    f = 180 + 120 * v
    trilho = np.sin(2 * np.pi * np.cumsum(f) / TAXA) * v ** 2 * 0.07

    t_batida = FIM_DESLIZE + 0.02
    baque = np.sin(2 * np.pi * 62 * (t - t_batida)) * envelope(t, t_batida, 0.07)
    baque += filtrar(g.standard_normal(n), corte_alto=500) * envelope(t, t_batida, 0.04) * 0.9
    madeira = metal(t, 260, t_batida, ((1.0, 1.0, 0.06), (2.1, 0.5, 0.04)), 0.35)
    rebate = np.sin(2 * np.pi * 70 * (t - t_batida - 0.07)) * envelope(t, t_batida + 0.07, 0.04) * 0.4
    rebate += metal(t, 300, t_batida + 0.07, ((1.0, 1.0, 0.03),), 0.12)

    movimento = np.tanh(1.5 * (rodinhas + raspar + trilho)) / 1.5
    batida = 2.6 * (baque + madeira + rebate)
    som = trinco + movimento + batida
    return normalizar(sala(som, mistura=0.2), -5.0)


def main():
    print("[efeito da porta de correr]")
    salvar(os.path.join(PASTA_OBJETOS, "porta_correr.wav"), porta_correr())


if __name__ == "__main__":
    main()

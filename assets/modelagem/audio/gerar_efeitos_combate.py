# gerar_efeitos_combate.py — compõe por código os sons do combate do Centro
# de Convivência (docs/mecanicas/combate.md): a arma de impulso, o robô
# atirador (a carga do raio e o disparo).
#
# Como rodar (Python 3 + numpy):
#   python assets/modelagem/audio/gerar_efeitos_combate.py
#
# Gera:
#   assets/audio/efeitos/objetos/impulso_disparo.wav   o estouro grave da arma
#   assets/audio/efeitos/robos/raio_carga.wav          1,1 s de tom subindo
#   assets/audio/efeitos/robos/raio_disparo.wav        o estalo elétrico do raio
#
# As ferramentas (envelope, filtro pela FFT, normalizar, salvar) vêm do
# gerar_efeitos_gabriel.py, importado como módulo. A matemática delas está
# explicada lá.

import importlib.util
import os

import numpy as np

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
PASTA_EFEITOS = os.path.join(PASTA_PROJETO, "assets", "audio", "efeitos")

_spec = importlib.util.spec_from_file_location(
    "gerar_efeitos_gabriel", os.path.join(PASTA_SCRIPT, "gerar_efeitos_gabriel.py"))
ef = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ef)

TAXA = ef.TAXA
tempo, envelope, filtrar, normalizar, salvar = ef.tempo, ef.envelope, ef.filtrar, ef.normalizar, ef.salvar
rng = np.random.default_rng(2026)


def varredura(t, freq_inicial, freq_final, duracao):
    """Seno cuja frequência vai de freq_inicial a freq_final em "duracao" s.

    Uma frequência que muda no tempo não é sen(2*pi*f(t)*t): o que importa
    é a fase, que é a integral da frequência. Com f(t) linear de f0 a f1, a
    fase é 2*pi*(f0*t + (f1-f0)*t²/(2*duracao)), e é isso que entra no seno."""
    k = (freq_final - freq_inicial) / duracao
    return np.sin(2 * np.pi * (freq_inicial * t + 0.5 * k * t * t))


def impulso_disparo():
    """O estouro da arma de impulso: um golpe de ar (ruído grave com queda
    rápida) e, por baixo, um seno que cai de 170 Hz para 38 Hz em 0,35 s
    (o corpo da onda de choque), mais um "tchi" agudo no ataque."""
    t = tempo(0.5)
    golpe = rng.standard_normal(len(t)) * envelope(t, 0.0, 0.09, ataque=0.002)
    golpe = filtrar(golpe, corte_baixo=40, corte_alto=900, ordem=2)
    corpo = varredura(t, 170, 38, 0.35) * envelope(t, 0.0, 0.14, ataque=0.002)
    estalo = rng.standard_normal(len(t)) * envelope(t, 0.0, 0.015, ataque=0.0008)
    som = 1.2 * golpe + 1.6 * corpo + 0.5 * filtrar(estalo, corte_baixo=2500)
    return normalizar(som, -3)


def raio_carga():
    """A carga do raio do robô atirador, 1,1 s (o tempo da mira): um tom que
    sobe de 260 Hz a 1500 Hz com um tremido de 14 Hz no volume que acelera
    (o capacitor enchendo), e o volume cresce até o fim."""
    duracao = 1.1
    t = tempo(duracao)
    tom = varredura(t, 260, 1500, duracao)
    tremido = 0.65 + 0.35 * np.sin(2 * np.pi * (14 * t + 10 * t * t))
    subida = np.clip(t / duracao, 0, 1) ** 1.5
    zumbido = np.sin(2 * np.pi * 60 * t) * 0.3
    som = (tom * tremido + zumbido) * (0.15 + 0.85 * subida)
    som = filtrar(som, corte_baixo=80, corte_alto=5000, ordem=2)
    return normalizar(som, -9)


def raio_disparo():
    """O estalo do raio: ruído agudo muito curto (a faísca), um seno que cai
    de 2400 Hz para 220 Hz em 0,22 s (o "piu" do tiro de energia) e um
    zumbido grave que some logo depois."""
    t = tempo(0.45)
    faisca = rng.standard_normal(len(t)) * envelope(t, 0.0, 0.03, ataque=0.0006)
    faisca = filtrar(faisca, corte_baixo=1800)
    piu = varredura(t, 2400, 220, 0.22) * envelope(t, 0.0, 0.1, ataque=0.001)
    zumbido = np.sin(2 * np.pi * 110 * t) * envelope(t, 0.0, 0.12, ataque=0.003)
    som = 0.9 * faisca + 1.2 * piu + 0.5 * zumbido
    return normalizar(som, -4)


if __name__ == "__main__":
    print("Gerando os sons do combate:")
    salvar(os.path.join(PASTA_EFEITOS, "objetos", "impulso_disparo.wav"), impulso_disparo())
    salvar(os.path.join(PASTA_EFEITOS, "robos", "raio_carga.wav"), raio_carga())
    salvar(os.path.join(PASTA_EFEITOS, "robos", "raio_disparo.wav"), raio_disparo())

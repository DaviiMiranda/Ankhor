# gerar_efeitos_registros.py — compõe por código os sons dos REGISTROS dos
# antecessores: o rádio do Rafael e o papel dos bilhetes e do caderno.
#
# Como rodar (Python 3 + numpy):
#   python assets/modelagem/audio/gerar_efeitos_registros.py
#
# Gera:
#   assets/audio/efeitos/objetos/radio_chiado.wav     2 s em loop: a estática
#                                                     por baixo da voz do Rafael
#   assets/audio/efeitos/objetos/radio_clique.wav     o "clec" do botão de falar
#                                                     e o chiado curto de quando
#                                                     a transmissão abre e fecha
#   assets/audio/efeitos/interface/papel_folhear.wav  uma folha virando
#
# As ferramentas (envelope, filtro pela FFT, ruído, salvar) vêm do
# gerar_efeitos_gabriel.py, importado como módulo. A matemática delas está
# explicada lá.
#
# Um truque novo aqui: o LOOP SEM EMENDA do chiado. O filtro pela FFT trata
# o som como se ele desse a volta (a última amostra é vizinha da primeira),
# porque a Transformada de Fourier supõe um sinal periódico. Então ruído
# filtrado pela FFT já sai "circular": o fim encaixa no começo sem estalo.
# A oscilação de volume (o sinal do rádio indo e voltando) também usa
# frequências que cabem um número inteiro de vezes nos 2 s, pelo mesmo
# motivo. No Godot, o .import do arquivo está com loop ligado (Forward).

import importlib.util
import os

import numpy as np

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
PASTA_OBJETOS = os.path.join(PASTA_PROJETO, "assets", "audio", "efeitos", "objetos")
PASTA_INTERFACE = os.path.join(PASTA_PROJETO, "assets", "audio", "efeitos", "interface")

_spec = importlib.util.spec_from_file_location(
    "gerar_efeitos_gabriel", os.path.join(PASTA_SCRIPT, "gerar_efeitos_gabriel.py"))
ef = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ef)

TAXA = ef.TAXA
tempo, envelope, filtrar, normalizar, salvar = ef.tempo, ef.envelope, ef.filtrar, ef.normalizar, ef.salvar
rng = np.random.default_rng(2008)   # sorteios fixos: o ano do Rafael


def ruido(n):
    return rng.standard_normal(n)


def radio_chiado():
    """Estática de rádio: ruído na faixa de um alto-falante pequeno (de 400
    a 3500 Hz; rádio portátil não tem grave nem agudo), com o volume indo e
    voltando devagar, como sinal fraco. Por cima, estalos soltos (poeira na
    antena): pulsos curtíssimos em instantes sorteados."""
    duracao = 2.0
    t = tempo(duracao)
    n = len(t)
    estatica = filtrar(ruido(n), corte_baixo=400, corte_alto=3500, ordem=3)
    estatica /= np.max(np.abs(estatica))
    # 1 e 3 ciclos em 2 s: números inteiros de voltas, então o loop fecha.
    onda = 0.75 + 0.15 * np.sin(2 * np.pi * 0.5 * t) + 0.1 * np.sin(2 * np.pi * 1.5 * t + 1.0)
    estalos = np.zeros(n)
    for i in rng.integers(0, n, 14):
        estalos[i] = rng.uniform(-1, 1)
    estalos = filtrar(estalos, corte_baixo=1500)
    estalos /= np.max(np.abs(estalos)) + 1e-9
    return normalizar(estatica * onda + 0.5 * estalos, -9.0)


def radio_clique():
    """O botão de falar (PTT) de um rádio: um "clec" de plástico (dois
    estalos seguidos, de 2 e 1 ms) e logo depois o "chhht" do squelch, a
    estática que passa enquanto o rádio abre o canal, subindo e sumindo em
    menos de 0,2 s."""
    duracao = 0.3
    t = tempo(duracao)
    n = len(t)
    clec = filtrar(ruido(n), corte_baixo=2000, corte_alto=6000)
    clec *= envelope(t, 0.0, 0.002, ataque=0.0003) + 0.6 * envelope(t, 0.012, 0.001, ataque=0.0003)
    clec /= np.max(np.abs(clec)) + 1e-9
    squelch = filtrar(ruido(n), corte_baixo=500, corte_alto=4000, ordem=3)
    squelch /= np.max(np.abs(squelch))
    squelch *= np.sin(np.pi * np.clip((t - 0.03) / 0.2, 0, 1)) ** 2
    som = clec + 0.5 * squelch
    som *= np.clip((duracao - t) / 0.02, 0, 1)
    return normalizar(som, -8.0)


def papel_folhear():
    """Uma folha virando: o papel raspa (ruído agudo, 2 a 8 kHz) em três
    "ondas" curtas, porque a folha dobra, desliza e assenta. No fim, um
    baque bem leve e abafado: a folha deitando na outra."""
    duracao = 0.35
    t = tempo(duracao)
    n = len(t)
    raspa = filtrar(ruido(n), corte_baixo=2000, corte_alto=8000)
    raspa /= np.max(np.abs(raspa))
    forma = (0.6 * np.exp(-((t - 0.05) / 0.025) ** 2) + np.exp(-((t - 0.13) / 0.04) ** 2)
             + 0.4 * np.exp(-((t - 0.22) / 0.03) ** 2))
    assenta = filtrar(ruido(n), corte_alto=700) * envelope(t, 0.24, 0.03)
    assenta /= np.max(np.abs(assenta)) + 1e-9
    som = raspa * forma + 0.3 * assenta
    som *= np.clip((duracao - t) / 0.03, 0, 1)
    return normalizar(som, -10.0)


def main():
    print("[efeitos dos registros]")
    salvar(os.path.join(PASTA_OBJETOS, "radio_chiado.wav"), radio_chiado())
    salvar(os.path.join(PASTA_OBJETOS, "radio_clique.wav"), radio_clique())
    salvar(os.path.join(PASTA_INTERFACE, "papel_folhear.wav"), papel_folhear())


if __name__ == "__main__":
    main()

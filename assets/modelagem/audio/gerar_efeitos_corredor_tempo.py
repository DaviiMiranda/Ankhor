# gerar_efeitos_corredor_tempo.py — compõe por código os sons do Corredor do
# Tempo do Labirinto (o relógio que corre e os quatro mecanismos de alinhar).
#
# Como rodar (Python 3 + numpy):
#   python assets/modelagem/audio/gerar_efeitos_corredor_tempo.py
#
# Gera, em assets/audio/efeitos/objetos/:
#   relogio_tique.wav    0,12 s: o tique seco do relógio. O jogo toca o mesmo
#                        arquivo com pitch_scale alternado (tique / taque).
#   tempo_acerto.wav     0,7 s: um sino curto, cada acerto dentro da janela
#   tempo_erro.wav       0,45 s: agulha arranhando o disco e um zumbido grave
#   tempo_alinhado.wav   1,2 s: duas notas subindo, o mecanismo travou no lugar
#   tempo_trava.wav      0,6 s: a porta do corredor trancando atrás do Gabriel
#   tempo_vencido.wav    2,0 s: os quatro sinos juntos, um acorde maior
#   genius_verde.wav, genius_vermelho.wav, genius_amarelo.wav, genius_azul.wav
#                        0,42 s cada: os quatro tons do Genius (sala dos jogos)
#
# Ferramentas (envelope, filtro pela FFT, reverberação, salvar) do
# gerar_efeitos_gabriel.py e o metal inarmônico do gerar_efeitos_labirinto.py.
#
# - SINO: soma de parciais inarmônicas (1; 2,76; 5,40 vezes a fundamental),
#   cada uma com seu decaimento exponencial e^(-t/tau). É a série de uma
#   barra presa numa ponta, que soa "metálica" porque não é múltipla inteira.
# - TIQUE: um clique de ruído agudo muito curto (tau de 4 ms) mais um corpo
#   de madeira de 1,9 kHz, para soar como o escape de um relógio de parede.
# - ARRANHÃO: ruído filtrado com a frequência de corte varrendo de 6 kHz a
#   900 Hz (a agulha atravessando os sulcos), por cima de um zumbido de 55 Hz
#   com harmônicos ímpares (onda quase quadrada, tanh de uma senoide).
# - ACORDE: Dó, Mi, Sol e Dó de cima (razões 1; 5/4; 3/2; 2) — a afinação
#   justa, com os quatro sinos entrando um depois do outro a cada 90 ms.
# - GENIUS: as frequências do brinquedo original (415, 310, 252 e 209 Hz),
#   com onda quase quadrada (tanh de 2,5 · seno), que dá o timbre de "bipe"
#   eletrônico dos anos 80, com ataque rápido e corte suave no fim.

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

PARCIAIS_SINO = ((1.0, 1.0, 0.45), (2.76, 0.45, 0.22), (5.40, 0.25, 0.09))


def sino(t, f, inicio, forca=1.0):
    return metal(t, f, inicio, PARCIAIS_SINO, forca)


def relogio_tique():
    g = np.random.default_rng(1985)
    t = tempo(0.12)
    clique = filtrar(g.standard_normal(len(t)), corte_baixo=2500, corte_alto=9000) * envelope(t, 0.0, 0.004)
    madeira = np.sin(2 * np.pi * 1900 * t) * envelope(t, 0.0, 0.012) * 0.6
    madeira += np.sin(2 * np.pi * 820 * t) * envelope(t, 0.0, 0.02) * 0.3
    return normalizar(sala(clique + madeira, segundos=0.15, mistura=0.08), -6.0)


def tempo_acerto():
    t = tempo(0.7)
    som = sino(t, 1318.5, 0.0) + sino(t, 659.3, 0.0, 0.3)
    return normalizar(sala(som, mistura=0.15), -8.0)


def tempo_erro():
    g = np.random.default_rng(1983)
    t = tempo(0.45)
    n = len(t)
    x = np.clip(t / 0.3, 0.0, 1.0)
    corte = 6000.0 * (1.0 - x) + 900.0 * x
    ruido = g.standard_normal(n)
    arranhao = np.zeros(n)
    passo = 512
    for i in range(0, n, passo):
        pedaco = ruido[i:i + passo]
        arranhao[i:i + passo] = filtrar(pedaco, corte_baixo=300, corte_alto=float(corte[i]))
    arranhao *= envelope(t, 0.0, 0.12) * 1.4
    zumbido = np.tanh(3.0 * np.sin(2 * np.pi * 55 * t)) * envelope(t, 0.02, 0.18, ataque=0.01) * 0.5
    return normalizar(sala(arranhao + zumbido, mistura=0.1), -6.0)


def tempo_alinhado():
    t = tempo(1.2)
    som = sino(t, 784.0, 0.0) + sino(t, 1046.5, 0.14)
    som += metal(t, 180, 0.0, ((1.0, 1.0, 0.05), (2.3, 0.4, 0.03)), 0.6)
    return normalizar(sala(som, segundos=0.5, mistura=0.2), -6.0)


def tempo_trava():
    g = np.random.default_rng(1984)
    t = tempo(0.6)
    baque = np.sin(2 * np.pi * 58 * t) * envelope(t, 0.0, 0.09)
    baque += filtrar(g.standard_normal(len(t)), corte_alto=600) * envelope(t, 0.0, 0.05) * 0.8
    ferrolho = metal(t, 420, 0.05, ((1.0, 1.0, 0.05), (2.7, 0.6, 0.03)), 0.7)
    ferrolho += metal(t, 610, 0.16, ((1.0, 1.0, 0.04), (3.1, 0.4, 0.02)), 0.5)
    return normalizar(sala(2.2 * baque + ferrolho, segundos=0.6, mistura=0.25), -4.0)


def tempo_vencido():
    t = tempo(2.0)
    base = 523.25
    som = np.zeros(len(t))
    for i, razao in enumerate((1.0, 5 / 4, 3 / 2, 2.0)):
        som += sino(t, base * razao, 0.09 * i)
    return normalizar(sala(som, segundos=0.8, mistura=0.25), -5.0)


TONS_GENIUS = {"verde": 415.3, "vermelho": 311.1, "amarelo": 252.0, "azul": 209.0}


def genius(f):
    t = tempo(0.42)
    corpo = np.tanh(2.5 * np.sin(2 * np.pi * f * t))
    fim = np.clip((0.42 - t) / 0.06, 0.0, 1.0)
    ataque = np.clip(t / 0.005, 0.0, 1.0)
    return normalizar(corpo * fim * ataque, -9.0)


def main():
    print("[efeitos do Corredor do Tempo]")
    salvar(os.path.join(PASTA_OBJETOS, "relogio_tique.wav"), relogio_tique())
    salvar(os.path.join(PASTA_OBJETOS, "tempo_acerto.wav"), tempo_acerto())
    salvar(os.path.join(PASTA_OBJETOS, "tempo_erro.wav"), tempo_erro())
    salvar(os.path.join(PASTA_OBJETOS, "tempo_alinhado.wav"), tempo_alinhado())
    salvar(os.path.join(PASTA_OBJETOS, "tempo_trava.wav"), tempo_trava())
    salvar(os.path.join(PASTA_OBJETOS, "tempo_vencido.wav"), tempo_vencido())
    for cor, f in TONS_GENIUS.items():
        salvar(os.path.join(PASTA_OBJETOS, f"genius_{cor}.wav"), genius(f))


if __name__ == "__main__":
    main()

# gerar_efeitos_visor.py — compõe por código o som do visor VR ligando,
# que toca junto com a tela de carregamento (cenas/visor/tela_carregando_vr.tscn).
#
# Como rodar (Python 3 + numpy):
#   python assets/modelagem/audio/gerar_efeitos_visor.py
#
# Gera:
#   assets/audio/efeitos/interface/visor_ligando.wav   3 s: o visor recebendo energia
#
# A linha do tempo é a mesma da tela (scripts/visor/tela_carregando_vr.gd):
#   0,00 s  o relé fecha (clique metálico e um baque grave);
#   0,10 a 0,43 s  a tela pisca: cada vez que ela acende (PISCADAS, abaixo,
#           iguais a PISCADAS_AO_LIGAR no script) sai um estalo elétrico e um
#           zumbido curto;
#   0,10 a 1,4 s  a "subida" da energia: um tom que sobe de 60 Hz a 900 Hz;
#   0,43 a 3,0 s  o zumbido de 120 Hz do aparelho ligado, baixo e constante;
#   2,65 s  a barra enche: dois bipes subindo (pronto).
# Se mudar os tempos de um lado, mude do outro.
#
# Ferramentas (envelope, filtro pela FFT, salvar) do gerar_efeitos_gabriel.py
# e o metal inarmônico do gerar_efeitos_labirinto.py. A conta nova:
#
# - SUBIDA da energia: a frequência segue uma exponencial,
#   f(t) = f0 · (f1/f0)^x, com x indo de 0 a 1. Subir por exponencial (e não
#   em linha reta) faz cada oitava levar o mesmo tempo, que é como o ouvido
#   percebe a altura. A fase é a integral da frequência (np.cumsum(f) / TAXA).
#   O tanh achata a senoide e acrescenta harmônicos, o timbre de um
#   transformador carregando.
# - ZUMBIDO elétrico: 120 Hz (o dobro dos 60 Hz da rede, porque o
#   transformador vibra nos dois sentidos da corrente) com os harmônicos
#   240 e 360 Hz, cada um mais fraco.

import importlib.util
import os

import numpy as np

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
PASTA_INTERFACE = os.path.join(PASTA_PROJETO, "assets", "audio", "efeitos", "interface")

_spec = importlib.util.spec_from_file_location(
    "gerar_efeitos_labirinto", os.path.join(PASTA_SCRIPT, "gerar_efeitos_labirinto.py"))
lab = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lab)

ef = lab.ef
TAXA = ef.TAXA
tempo, envelope, filtrar, normalizar, salvar, sala = ef.tempo, ef.envelope, ef.filtrar, ef.normalizar, ef.salvar, ef.sala
metal = lab.metal
rng = np.random.default_rng(2123)

DURACAO = 3.0
# (brilho, segundos) de cada trecho do pisca-pisca, na ordem.
PISCADAS = ((0.0, 0.10), (1.0, 0.04), (0.0, 0.07), (0.7, 0.03), (0.0, 0.10), (1.0, 0.05), (0.25, 0.04))
TEMPO_LIGADO = sum(d for _, d in PISCADAS)
TEMPO_PRONTO = 2.65


def ruido(n):
    return rng.standard_normal(n)


def janela(t, inicio, fim, borda=0.004):
    """1 entre 'inicio' e 'fim', 0 fora, com bordas de 'borda' segundos
    para não estalar o alto-falante."""
    sobe = np.clip((t - inicio) / borda, 0.0, 1.0)
    desce = np.clip((fim - t) / borda, 0.0, 1.0)
    return sobe * desce


def zumbido(t, fundamental=120.0):
    return (np.sin(2 * np.pi * fundamental * t)
            + 0.5 * np.sin(2 * np.pi * 2 * fundamental * t)
            + 0.25 * np.sin(2 * np.pi * 3 * fundamental * t))


def visor_ligando():
    t = tempo(DURACAO)
    n = len(t)

    rele = metal(t, 2400, 0.0, ((1.0, 1.0, 0.012), (2.7, 0.5, 0.008)), 0.6)
    rele += np.sin(2 * np.pi * 55 * t) * envelope(t, 0.0, 0.07) * 0.9

    piscadas = np.zeros(n)
    inicio = 0.0
    for brilho, duracao in PISCADAS:
        if brilho > 0.0:
            estalo = filtrar(ruido(n), corte_baixo=1200, corte_alto=7000) * envelope(t, inicio, 0.012, 0.0005)
            piscadas += estalo * brilho * 0.8
            piscadas += np.tanh(4 * zumbido(t, 120.0)) * janela(t, inicio, inicio + duracao) * brilho * 0.35
        inicio += duracao

    x = np.clip((t - 0.10) / 1.3, 0.0, 1.0)
    f = 60.0 * (900.0 / 60.0) ** x
    corpo = np.clip((t - 0.10) / 0.15, 0.0, 1.0) * (0.25 + 0.75 * np.exp(-np.maximum(t - 1.4, 0) / 0.35))
    fim = np.clip((DURACAO - t) / 0.25, 0.0, 1.0)
    subida = np.tanh(2.5 * np.sin(2 * np.pi * np.cumsum(f) / TAXA)) * corpo * fim * 0.22
    subida = filtrar(subida, corte_alto=5000)

    ligado = zumbido(t) * janela(t, TEMPO_LIGADO, DURACAO, borda=0.2) * 0.12
    ligado += filtrar(ruido(n), corte_baixo=4000, corte_alto=9000) * janela(t, TEMPO_LIGADO, DURACAO, borda=0.3) * 0.015

    pronto = np.zeros(n)
    for atraso, nota in ((0.0, 1318.5), (0.1, 1760.0)):
        pronto += np.sin(2 * np.pi * nota * t) * envelope(t, TEMPO_PRONTO + atraso, 0.12, 0.003) * 0.3

    return normalizar(sala(rele + piscadas + subida + ligado + pronto, mistura=0.1), -4.0)


def main():
    print("[efeitos do visor]")
    salvar(os.path.join(PASTA_INTERFACE, "visor_ligando.wav"), visor_ligando())


if __name__ == "__main__":
    main()

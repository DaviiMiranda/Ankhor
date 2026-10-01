# gerar_efeitos_gadgets.py — compõe por código os sons da porta e dos
# gadgets da sala de teste (cápsula de clarão, pedra e notebook).
#
# Como rodar (Python 3 + numpy):
#   python assets/modelagem/audio/gerar_efeitos_gadgets.py
#
# Gera:
#   assets/audio/efeitos/objetos/porta_abrir.wav      trinco, dobradiça rangendo e a porta batendo
#   assets/audio/efeitos/objetos/clarao_disparo.wav   estalo do flash e o capacitor recarregando
#   assets/audio/efeitos/objetos/pedra_impacto.wav    pedra batendo e quicando no concreto
#   assets/audio/efeitos/objetos/notebook_hack.wav    2,5 s de bipes e ruído de dados, com o "ok" no fim
#
# Ferramentas (envelope, filtro pela FFT, salvar) do gerar_efeitos_gabriel.py
# e o metal inarmônico do gerar_efeitos_labirinto.py. Novidades aqui:
#
# - RANGIDO da dobradiça: um tom com frequência que oscila devagar
#   (modulação de frequência). A fase é a integral da frequência, por isso
#   o np.cumsum(f) / TAXA: somar f amostra por amostra dá o ângulo da onda.
#   Multiplicar por uma onda "dente de serra" lenta faz os solavancos do
#   atrito (stick-slip): a dobradiça prende, solta, prende de novo.
# - VARREDURA do capacitor do flash: a frequência sobe de 2 kHz a 9 kHz
#   seguindo uma exponencial, como o apito de uma câmera antiga carregando.
# - BIPES do notebook: ondas quadradas (sinal de sin) em notas sorteadas,
#   que é o timbre dos alto-falantes de computador.

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
rng = np.random.default_rng(3026)


def ruido(n):
    return rng.standard_normal(n)


def porta_abrir():
    """Porta de metal velha: o trinco estala, a dobradiça range por quase
    um segundo e a porta bate no batente (baque grave + metal)."""
    t = tempo(1.4)
    n = len(t)
    trinco = metal(t, 1700, 0.0, ((1.0, 1.0, 0.015), (2.3, 0.6, 0.01)), 0.8)
    trinco += filtrar(ruido(n), corte_baixo=1500) * envelope(t, 0.0, 0.008) * 0.6
    f = 520 + 140 * np.sin(2 * np.pi * 1.7 * t) + 60 * np.sin(2 * np.pi * 5.3 * t)
    atrito = 0.5 + 0.5 * ((t * 11) % 1.0)
    janela = np.clip((t - 0.1) / 0.1, 0, 1) * np.clip((1.0 - t) / 0.2, 0, 1)
    rangido = np.tanh(3 * np.sin(2 * np.pi * np.cumsum(f) / TAXA)) * atrito * janela * 0.25
    rangido = filtrar(rangido, corte_baixo=300, corte_alto=4000)
    baque = np.sin(2 * np.pi * 70 * (t - 1.05)) * envelope(t, 1.05, 0.08)
    baque += filtrar(ruido(n), corte_alto=400) * envelope(t, 1.05, 0.05) * 0.8
    batente = metal(t, 380, 1.05, ((1.0, 1.0, 0.15), (2.76, 0.5, 0.08), (5.4, 0.3, 0.05)), 0.4)
    return normalizar(sala(trinco + rangido + baque + batente, mistura=0.2), -5.0)


def clarao_disparo():
    """O flash: um estalo seco e forte (ruído curtíssimo e brilhante) e, por
    cima, o apito agudo do capacitor subindo, que some aos poucos."""
    t = tempo(1.2)
    n = len(t)
    estalo = filtrar(ruido(n), corte_baixo=800) * envelope(t, 0.0, 0.03, 0.0005) * 1.5
    estalo += np.sin(2 * np.pi * 90 * t) * envelope(t, 0.0, 0.06)
    f = 2000 * (9000 / 2000) ** np.clip(t / 1.0, 0, 1)
    apito = np.sin(2 * np.pi * np.cumsum(f) / TAXA) * envelope(t, 0.05, 0.4, 0.05) * 0.12
    return normalizar(sala(estalo + apito, mistura=0.25), -3.0)


def pedra_impacto():
    """Uma pedra caindo no concreto: batida seca, depois dois quiques
    cada vez mais fracos e mais próximos, e grãos rolando."""
    t = tempo(0.7)
    n = len(t)
    s = np.zeros(n)
    for inicio, forca in ((0.0, 1.0), (0.16, 0.45), (0.27, 0.2)):
        s += filtrar(ruido(n), corte_baixo=200, corte_alto=3500) * envelope(t, inicio, 0.02, 0.0005) * forca
        s += np.sin(2 * np.pi * 160 * (t - inicio)) * envelope(t, inicio, 0.03) * forca * 0.6
    s += filtrar(ruido(n), corte_baixo=2000, corte_alto=7000) * envelope(t, 0.3, 0.15, 0.05) * 0.08
    return normalizar(sala(s, mistura=0.3), -4.0)


def notebook_hack():
    """2,5 s de invasão: bipes quadrados em notas sorteadas (dados
    passando), um chiado baixo de HD e, no fim, dois bipes subindo (ok)."""
    t = tempo(2.5)
    n = len(t)
    s = filtrar(ruido(n), corte_baixo=3000, corte_alto=8000) * 0.03
    notas = (880, 1175, 1318, 1568, 1760, 2093)
    inicio = 0.05
    while inicio < 2.1:
        f = notas[rng.integers(len(notas))]
        dur = rng.uniform(0.03, 0.08)
        janela = ((t >= inicio) & (t < inicio + dur)).astype(float)
        s += np.sign(np.sin(2 * np.pi * f * t)) * janela * 0.15
        inicio += dur + rng.uniform(0.02, 0.09)
    for inicio, f in ((2.2, 1318), (2.32, 1976)):
        janela = ((t >= inicio) & (t < inicio + 0.1)).astype(float)
        s += np.sign(np.sin(2 * np.pi * f * t)) * janela * 0.25
    s = filtrar(s, corte_alto=6000)
    return normalizar(s, -9.0)


def main():
    print("[efeitos dos gadgets]")
    for nome, funcao in (("porta_abrir", porta_abrir),
                         ("clarao_disparo", clarao_disparo),
                         ("pedra_impacto", pedra_impacto),
                         ("notebook_hack", notebook_hack)):
        salvar(os.path.join(PASTA_OBJETOS, f"{nome}.wav"), funcao())


if __name__ == "__main__":
    main()

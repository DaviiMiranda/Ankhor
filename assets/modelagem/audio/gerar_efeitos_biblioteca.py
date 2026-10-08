# gerar_efeitos_biblioteca.py — compõe por código os sons dos sistemas da
# fase da Biblioteca (docs/fases/biblioteca.md): o telefone do balcão, o
# bipe da Sentinela antes de virar, as batidas atrás da porta das obras
# raras, o disjuntor do quadro de energia e as teclas do painel da grade.
#
# Como rodar (Python 3 + numpy):
#   python assets/modelagem/audio/gerar_efeitos_biblioteca.py
#
# Gera:
#   assets/audio/efeitos/objetos/telefone_toque.wav   6 s em loop: dois toques
#                                                     e o silêncio entre eles
#   assets/audio/efeitos/robos/robo_bipe.wav          o bipe curto antes de virar
#   assets/audio/efeitos/objetos/batidas_porta.wav    três batidas abafadas
#   assets/audio/efeitos/objetos/disjuntor.wav        o "clac" de uma alavanca
#   assets/audio/efeitos/objetos/painel_tecla.wav     o bip de uma tecla
#
# As ferramentas (envelope, filtro pela FFT, normalizar, salvar) vêm do
# gerar_efeitos_gabriel.py, importado como módulo. A matemática delas está
# explicada lá.

import importlib.util
import os

import numpy as np

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
PASTA_OBJETOS = os.path.join(PASTA_PROJETO, "assets", "audio", "efeitos", "objetos")
PASTA_ROBOS = os.path.join(PASTA_PROJETO, "assets", "audio", "efeitos", "robos")

_spec = importlib.util.spec_from_file_location(
    "gerar_efeitos_gabriel", os.path.join(PASTA_SCRIPT, "gerar_efeitos_gabriel.py"))
ef = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ef)

TAXA = ef.TAXA
tempo, envelope, filtrar, normalizar, salvar = ef.tempo, ef.envelope, ef.filtrar, ef.normalizar, ef.salvar
rng = np.random.default_rng(1994)   # sorteios fixos: o ano da Clarice


def telefone_toque():
    """O toque de um telefone de mesa antigo: a campainha soa por 1 s, para
    por 0,4 s, soa de novo por 1 s e fica 3,6 s em silêncio (6 s ao todo,
    em loop).

    A campainha é uma soma de duas senoides próximas (440 e 480 Hz). Duas
    frequências quase iguais "batem": o volume sobe e desce 40 vezes por
    segundo (480 - 440 = 40), que é o tremido característico do toque. Por
    cima, um vibrato de 20 Hz no volume imita o martelinho batendo no sino.
    As frequências cabem um número inteiro de vezes nos 6 s, então o loop
    não estala na emenda."""
    duracao = 6.0
    t = tempo(duracao)
    sino = np.sin(2 * np.pi * 440 * t) + np.sin(2 * np.pi * 480 * t)
    martelo = 0.75 + 0.25 * np.sign(np.sin(2 * np.pi * 20 * t))
    ligado = ((t >= 0.0) & (t < 1.0)) | ((t >= 1.4) & (t < 2.4))
    # Rampa de 10 ms nas bordas de cada toque (sem clique ao ligar e desligar).
    rampa = np.convolve(ligado.astype(float), np.ones(int(0.01 * TAXA)) / int(0.01 * TAXA), mode="same")
    som = sino * martelo * rampa
    som = filtrar(som, corte_baixo=300, corte_alto=4000, ordem=2)
    return normalizar(som, -6)


def robo_bipe():
    """Bipe eletrônico curto: senoide de 1320 Hz por 0,12 s com ataque e
    queda rápidos, e um segundo bipe mais grave (990 Hz) logo depois: o
    "bi-bip" de um sensor que vai mudar de direção."""
    t = tempo(0.35)
    primeiro = np.sin(2 * np.pi * 1320 * t) * envelope(t, 0.0, 0.05, ataque=0.004)
    segundo = np.sin(2 * np.pi * 990 * t) * envelope(t, 0.16, 0.06, ataque=0.004)
    return normalizar(primeiro + segundo, -4)


def batidas_porta():
    """Três batidas abafadas atrás de uma porta grossa: cada batida é ruído
    com queda rápida, filtrado para ficar só no grave (a madeira e a
    distância comem os agudos), com um tom de 90 Hz por baixo (o corpo da
    porta vibrando)."""
    duracao = 1.6
    t = tempo(duracao)
    som = np.zeros_like(t)
    for inicio in (0.0, 0.32, 0.68):
        golpe = envelope(t, inicio, 0.05, ataque=0.003)
        som += rng.standard_normal(len(t)) * golpe
        som += 1.5 * np.sin(2 * np.pi * 90 * (t - inicio)) * envelope(t, inicio, 0.09, ataque=0.003)
    som = filtrar(som, corte_baixo=40, corte_alto=600, ordem=2)
    return normalizar(som, -3)


def disjuntor():
    """O "clac" de uma alavanca de disjuntor: um estalo seco (ruído muito
    curto e agudo) e o batente de metal logo depois (ruído médio com uma
    ressonância de 700 Hz)."""
    t = tempo(0.3)
    estalo = rng.standard_normal(len(t)) * envelope(t, 0.0, 0.006, ataque=0.0005)
    batente = rng.standard_normal(len(t)) * envelope(t, 0.02, 0.03, ataque=0.001)
    ressonancia = np.sin(2 * np.pi * 700 * t) * envelope(t, 0.02, 0.05, ataque=0.001)
    som = filtrar(estalo, corte_baixo=2000) + filtrar(batente, corte_baixo=300, corte_alto=3000) + 0.6 * ressonancia
    return normalizar(som, -4)


def painel_tecla():
    """O bip de uma tecla de painel: senoide de 1800 Hz por 60 ms, com um
    pouco do clique mecânico da tecla no começo."""
    t = tempo(0.12)
    bip = np.sin(2 * np.pi * 1800 * t) * envelope(t, 0.005, 0.03, ataque=0.003)
    clique = rng.standard_normal(len(t)) * envelope(t, 0.0, 0.004, ataque=0.0005)
    return normalizar(bip + 0.4 * filtrar(clique, corte_baixo=1500), -8)


if __name__ == "__main__":
    print("Gerando os sons da Biblioteca:")
    salvar(os.path.join(PASTA_OBJETOS, "telefone_toque.wav"), telefone_toque())
    salvar(os.path.join(PASTA_ROBOS, "robo_bipe.wav"), robo_bipe())
    salvar(os.path.join(PASTA_OBJETOS, "batidas_porta.wav"), batidas_porta())
    salvar(os.path.join(PASTA_OBJETOS, "disjuntor.wav"), disjuntor())
    salvar(os.path.join(PASTA_OBJETOS, "painel_tecla.wav"), painel_tecla())

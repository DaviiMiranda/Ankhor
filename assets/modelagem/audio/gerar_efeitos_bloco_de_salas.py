# gerar_efeitos_bloco_de_salas.py — compõe por código os sons dos puzzles do
# Bloco de salas (docs/fases/bloco_de_salas.md): a sirene do teste de
# alarme, a queda pelo buraco da sala 204 e a corrente da porta corta-fogo
# sendo cortada.
#
# Como rodar (Python 3 + numpy):
#   python assets/modelagem/audio/gerar_efeitos_bloco_de_salas.py
#
# Gera:
#   assets/audio/efeitos/objetos/sirene.wav            2 s em loop: o "uó-uó" da sirene
#   assets/audio/efeitos/objetos/queda.wav             o baque de cair no entulho
#   assets/audio/efeitos/objetos/corrente_cortada.wav  o estalo do alicate e a corrente caindo
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

_spec = importlib.util.spec_from_file_location(
    "gerar_efeitos_gabriel", os.path.join(PASTA_SCRIPT, "gerar_efeitos_gabriel.py"))
ef = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ef)

TAXA = ef.TAXA
tempo, envelope, filtrar, normalizar, salvar = ef.tempo, ef.envelope, ef.filtrar, ef.normalizar, ef.salvar
rng = np.random.default_rng(2008)   # sorteios fixos: o ano do Rafael


def sirene():
    """Sirene de alarme de prédio: um tom que sobe e desce sem parar
    (de 600 a 1100 Hz e de volta, uma volta por segundo, 2 s ao todo).

    A frequência muda com o tempo, então não dá para usar sin(2*pi*f*t)
    direto: a fase é a SOMA (integral) da frequência de cada instante,
    fase = 2*pi * cumsum(f) / taxa. A frequência segue um seno, então
    sobe e desce suave. Por cima, uma onda quadrada fraca (os harmônicos
    ímpares) deixa o som áspero de alto-falante barato. Uma volta inteira
    cabe nos 2 s e a fase total é múltipla de 2*pi, então o loop não estala."""
    duracao = 2.0
    t = tempo(duracao)
    frequencia = 850 - 250 * np.cos(2 * np.pi * 1.0 * t)
    fase = 2 * np.pi * np.cumsum(frequencia) / TAXA
    fase *= np.round(fase[-1] / (2 * np.pi)) * 2 * np.pi / fase[-1]
    som = np.sin(fase) + 0.25 * np.sign(np.sin(fase))
    som = filtrar(som, corte_baixo=300, corte_alto=5000, ordem=2)
    return normalizar(som, -5)


def queda():
    """Cair de um andar em cima de entulho: um baque grave (ruído filtrado
    no grave com um tom de 60 Hz, o corpo batendo no chão) e, logo depois,
    pedrinhas rolando (estalos curtos sorteados, cada vez mais espaçados)."""
    duracao = 1.4
    t = tempo(duracao)
    baque = rng.standard_normal(len(t)) * envelope(t, 0.0, 0.18, ataque=0.004)
    baque = filtrar(baque, corte_baixo=30, corte_alto=500, ordem=2)
    corpo = 2.0 * np.sin(2 * np.pi * 60 * t) * envelope(t, 0.0, 0.2, ataque=0.004)
    pedrinhas = np.zeros_like(t)
    inicio = 0.12
    for _ in range(14):
        inicio += rng.uniform(0.02, 0.09) * (1 + inicio)
        if inicio > duracao - 0.05:
            break
        pedrinhas += rng.uniform(0.3, 0.8) * rng.standard_normal(len(t)) * envelope(t, inicio, 0.015, ataque=0.001)
    pedrinhas = filtrar(pedrinhas, corte_baixo=800, corte_alto=6000)
    return normalizar(baque + corpo + 0.5 * pedrinhas, -2)


def corrente_cortada():
    """O alicate mordendo o elo: um estalo metálico seco (ruído agudo muito
    curto e duas ressonâncias de aço, 1900 e 3100 Hz, que somem rápido) e a
    corrente escorregando e batendo no chão: três tilintares cada vez mais
    fracos."""
    duracao = 1.3
    t = tempo(duracao)
    estalo = filtrar(rng.standard_normal(len(t)) * envelope(t, 0.0, 0.01, ataque=0.0005), corte_baixo=2500)
    aco = (np.sin(2 * np.pi * 1900 * t) + 0.6 * np.sin(2 * np.pi * 3100 * t)) * envelope(t, 0.0, 0.12, ataque=0.001)
    tilintar = np.zeros_like(t)
    for inicio, forca in ((0.35, 0.8), (0.55, 0.55), (0.72, 0.35)):
        tilintar += forca * np.sin(2 * np.pi * 2400 * (t - inicio)) * envelope(t, inicio, 0.06, ataque=0.001)
        tilintar += forca * 0.5 * rng.standard_normal(len(t)) * envelope(t, inicio, 0.02, ataque=0.001)
    tilintar = filtrar(tilintar, corte_baixo=900, corte_alto=7000)
    return normalizar(estalo + 0.5 * aco + 0.6 * tilintar, -3)


if __name__ == "__main__":
    print("Gerando os sons do Bloco de salas:")
    salvar(os.path.join(PASTA_OBJETOS, "sirene.wav"), sirene())
    salvar(os.path.join(PASTA_OBJETOS, "queda.wav"), queda())
    salvar(os.path.join(PASTA_OBJETOS, "corrente_cortada.wav"), corrente_cortada())

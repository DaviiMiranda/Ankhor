# gerar_efeitos_bunker.py — compõe por código os sons do bunker e da
# conversa com a Clarice.
#
# Como rodar (Python 3 + numpy):
#   python assets/modelagem/audio/gerar_efeitos_bunker.py
#
# Gera:
#   assets/audio/ambiente/bunker/bunker_zumbido.wav      4 s em loop: transformador e ventilação
#   assets/audio/ambiente/bunker/bunker_goteiras.wav     6 s em loop: pingos caindo em poça
#   assets/audio/efeitos/objetos/porta_blindada.wav      trava, pistão hidráulico e a porta de aço batendo
#   assets/audio/efeitos/objetos/porta_emperrada.wav     maçaneta chacoalhando numa porta que não abre
#   assets/audio/efeitos/objetos/teclado.wav             3 s em loop: alguém digitando num teclado mecânico
#   assets/audio/efeitos/interface/dialogo_bip.wav       o bipe de cada letra na caixa de diálogo
#
# Ferramentas (envelope, filtro pela FFT, salvar, reverberação) do
# gerar_efeitos_gabriel.py e o metal inarmônico do gerar_efeitos_labirinto.py.
# O que aparece de novo:
#
# - LOOP SEM EMENDA no zumbido: 60 Hz e as harmônicas têm um número inteiro
#   de ciclos em 4 s (60 × 4 = 240 ciclos), e o ruído da ventilação é
#   filtrado pela FFT, que é circular: o fim encaixa no começo.
# - PINGO D'ÁGUA: um seno cuja frequência SOBE rápido (de 900 para 1800 Hz
#   em poucos milissegundos). É a bolha de ar que o pingo prende ao cair na
#   poça: ela vibra cada vez mais agudo enquanto encolhe.
# - SIBILO HIDRÁULICO: ruído com um filtro passa-faixa que desliza para o
#   agudo, com envelope que sobe e cai: o ar escapando do pistão da porta.
# - TECLADO: cada tecla é um estalo curto (ruído agudo com queda de 4 ms)
#   mais um "toc" grave do fim de curso. Os intervalos são sorteados como
#   uma pessoa digitando: rajadas rápidas, pausas, e a barra de espaço mais
#   grave de vez em quando.

import importlib.util
import os

import numpy as np

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
PASTA_AUDIO = os.path.join(PASTA_PROJETO, "assets", "audio")

_spec = importlib.util.spec_from_file_location(
    "gerar_efeitos_labirinto", os.path.join(PASTA_SCRIPT, "gerar_efeitos_labirinto.py"))
lab = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lab)

ef = lab.ef
TAXA = ef.TAXA
tempo, envelope, filtrar, normalizar, salvar, sala = ef.tempo, ef.envelope, ef.filtrar, ef.normalizar, ef.salvar, ef.sala
metal = lab.metal
rng = np.random.default_rng(1994)


def ruido(n):
    return rng.standard_normal(n)


def bunker_zumbido():
    """Zumbido de transformador (60 Hz com harmônicas ímpares, que é o som
    da rede elétrica) por baixo de uma ventilação: ruído grave filtrado,
    com uma pulsação lenta de 0,5 Hz (a hélice do duto)."""
    t = tempo(4.0)
    n = len(t)
    s = sum(a * np.sin(2 * np.pi * f * t) for f, a in ((60, 1.0), (180, 0.35), (300, 0.15), (420, 0.06)))
    s = s * 0.25
    vento = filtrar(ruido(n), corte_baixo=80, corte_alto=900)
    s += vento * (0.6 + 0.25 * np.sin(2 * np.pi * 0.5 * t))
    return normalizar(s, -16.0)


def bunker_goteiras():
    """Três pingos em 6 s, em pontos diferentes do loop, com eco de
    corredor de concreto."""
    t = tempo(6.0)
    n = len(t)
    s = np.zeros(n)
    for inicio, forca, f0 in ((0.4, 1.0, 900), (2.3, 0.6, 1100), (4.1, 0.8, 800)):
        d = np.clip(t - inicio, 0, None)
        f = f0 + (f0 * 1.1) * (1 - np.exp(-d / 0.012))
        fase = 2 * np.pi * np.cumsum(f) / TAXA
        s += np.sin(fase) * envelope(t, inicio, 0.03, 0.0005) * forca
        s += filtrar(ruido(n), corte_baixo=2000) * envelope(t, inicio, 0.004, 0.0003) * 0.3 * forca
    return normalizar(sala(s, segundos=0.8, mistura=0.35), -10.0)


def porta_blindada():
    """Porta de aço de correr: a trava estala, o pistão sibila, a folha
    pesada desliza (ronco grave) e bate no fim do trilho."""
    t = tempo(1.8)
    n = len(t)
    trava = metal(t, 1400, 0.0, ((1.0, 1.0, 0.02), (2.2, 0.7, 0.015)), 0.9)
    trava += filtrar(ruido(n), corte_baixo=1200) * envelope(t, 0.0, 0.01) * 0.7
    janela = np.clip((t - 0.12) / 0.08, 0, 1) * np.clip((0.9 - t) / 0.3, 0, 1)
    sibilo = np.zeros(n)
    bruto = ruido(n)
    for i, (a, b) in enumerate(((1500, 3500), (2500, 5000), (3500, 7000))):
        trecho = (t >= 0.12 + i * 0.25) & (t < 0.12 + (i + 1) * 0.25 + 0.05)
        sibilo += filtrar(bruto, corte_baixo=a, corte_alto=b) * trecho
    sibilo *= janela * 0.5
    ronco = filtrar(ruido(n), corte_alto=180) * np.clip((t - 0.2) / 0.1, 0, 1) * np.clip((1.25 - t) / 0.2, 0, 1) * 1.4
    batida = np.sin(2 * np.pi * 55 * (t - 1.25)) * envelope(t, 1.25, 0.12) * 1.2
    batida += metal(t, 300, 1.25, ((1.0, 1.0, 0.25), (2.76, 0.6, 0.15), (5.4, 0.3, 0.08)), 0.6)
    return normalizar(sala(trava + sibilo + ronco + batida, segundos=0.7, mistura=0.3), -4.0)


def porta_emperrada():
    """Maçaneta forçada três vezes (metal curto) e um baque surdo da folha
    que não sai do lugar."""
    t = tempo(0.9)
    n = len(t)
    s = np.zeros(n)
    for inicio in (0.0, 0.13, 0.27):
        s += metal(t, 1100 + 80 * inicio, inicio, ((1.0, 1.0, 0.03), (1.7, 0.6, 0.02)), 0.7)
        s += filtrar(ruido(n), corte_baixo=800) * envelope(t, inicio, 0.01) * 0.3
    s += np.sin(2 * np.pi * 70 * (t - 0.45)) * envelope(t, 0.45, 0.07) * 0.9
    return normalizar(sala(s, segundos=0.5, mistura=0.25), -6.0)


def teclado():
    """3 s de digitação em loop. Nenhuma tecla começa nos últimos 60 ms,
    para o estalo não ser cortado na emenda do loop."""
    t = tempo(3.0)
    n = len(t)
    s = np.zeros(n)
    agora = 0.05
    while agora < 2.94:
        espaco = rng.random() < 0.12
        forca = rng.uniform(0.6, 1.0)
        estalo = filtrar(ruido(n), corte_baixo=2500, corte_alto=9000) * envelope(t, agora, 0.004, 0.0003)
        toc = np.sin(2 * np.pi * (140 if espaco else 260) * (t - agora)) * envelope(t, agora + 0.006, 0.02 if espaco else 0.012)
        s += (estalo * 0.8 + toc * (0.9 if espaco else 0.5)) * forca
        if rng.random() < 0.08:
            agora += rng.uniform(0.35, 0.6)
        else:
            agora += rng.uniform(0.06, 0.16)
    return normalizar(s, -12.0)


def dialogo_bip():
    """Bipe curtinho de computador (onda quase quadrada, filtrada para não
    ferir o ouvido). O jogo muda o tom para cada personagem (pitch_scale)."""
    t = tempo(0.05)
    s = np.tanh(3 * np.sin(2 * np.pi * 620 * t)) * envelope(t, 0.0, 0.018, 0.002)
    return normalizar(filtrar(s, corte_alto=3500), -14.0)


def main():
    print("[efeitos do bunker]")
    for pasta, nome, funcao in (("ambiente/bunker", "bunker_zumbido", bunker_zumbido),
                                ("ambiente/bunker", "bunker_goteiras", bunker_goteiras),
                                ("efeitos/objetos", "porta_blindada", porta_blindada),
                                ("efeitos/objetos", "porta_emperrada", porta_emperrada),
                                ("efeitos/objetos", "teclado", teclado),
                                ("efeitos/interface", "dialogo_bip", dialogo_bip)):
        salvar(os.path.join(PASTA_AUDIO, pasta, f"{nome}.wav"), funcao())


if __name__ == "__main__":
    main()

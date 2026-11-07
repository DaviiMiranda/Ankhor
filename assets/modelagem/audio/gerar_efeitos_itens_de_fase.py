# gerar_efeitos_itens_de_fase.py — compõe por código os sons das mecânicas de
# fase (placeholders).
#
# Como rodar (Python 3 + numpy):
#   python assets/modelagem/audio/gerar_efeitos_itens_de_fase.py
#
# Gera em assets/audio/efeitos/objetos/:
#   celula_zumbido.wav     2 s em loop: o transformador da Célula de Energia
#   sonar_pulso.wav        o pulso do módulo do Zane
#   mascara_respiracao.wav uma inspiração e uma expiração pelo filtro
#   tosse.wav              uma tosse curta, no ar do gás
#   gas_sibilo.wav         4 s em loop: gás escapando de um cano
#
# - LOOP SEM EMENDA: as frequências têm um número inteiro de ciclos na duração,
#   então o fim encaixa no começo; o ruído é filtrado pela FFT, que é circular.
# - WOW DA FITA: a fase da nota recebe um seno lento somado, que faz a altura
#   oscilar como uma fita gasta. A saturação é uma tangente hiperbólica.
# - PULSO DO SONAR: um seno cuja frequência cai exponencialmente, com eco.

import os
import wave

import numpy as np

TAXA = 22050
PASTA = os.path.dirname(os.path.abspath(__file__))
PROJETO = os.path.normpath(os.path.join(PASTA, "..", "..", ".."))
SAIDA = os.path.join(PROJETO, "assets", "audio", "efeitos", "objetos")
SORTEIO = np.random.default_rng(1990)


def salvar(nome, sinal):
    sinal = np.clip(sinal / max(1e-6, np.abs(sinal).max()) * 0.85, -1.0, 1.0)
    with wave.open(os.path.join(SAIDA, nome), "wb") as arquivo:
        arquivo.setnchannels(1)
        arquivo.setsampwidth(2)
        arquivo.setframerate(TAXA)
        arquivo.writeframes((sinal * 32767).astype(np.int16).tobytes())


def tempo(segundos):
    return np.arange(int(TAXA * segundos)) / TAXA


def ruido_filtrado(amostras, baixa, alta):
    espectro = np.fft.rfft(SORTEIO.normal(size=amostras))
    freq = np.fft.rfftfreq(amostras, 1 / TAXA)
    espectro[(freq < baixa) | (freq > alta)] = 0
    return np.fft.irfft(espectro, amostras)


def celula_zumbido():
    t = tempo(2.0)
    sinal = sum(np.sin(2 * np.pi * f * t) / (i + 1) for i, f in enumerate([60, 120, 180, 240]))
    salvar("celula_zumbido.wav", sinal * (0.85 + 0.15 * np.sin(2 * np.pi * 3 * t)))


def sonar_pulso():
    t = tempo(1.2)
    fase = 2 * np.pi * (1400 * (1 - np.exp(-6 * t)) / 6 + 500 * t)
    sinal = np.sin(fase) * np.exp(-5 * t)
    eco = np.zeros_like(sinal)
    atraso = int(0.22 * TAXA)
    eco[atraso:] = sinal[:-atraso] * 0.45
    salvar("sonar_pulso.wav", sinal + eco)


def mascara_respiracao():
    t = tempo(2.0)
    ar = ruido_filtrado(len(t), 300, 2400)
    inspira = np.exp(-((t - 0.45) / 0.28) ** 2)
    expira = 0.7 * np.exp(-((t - 1.35) / 0.32) ** 2)
    salvar("mascara_respiracao.wav", ar * (inspira + expira))


def tosse():
    t = tempo(0.7)
    ar = ruido_filtrado(len(t), 200, 3200)
    envelope = np.exp(-12 * t) + 0.7 * np.exp(-14 * np.maximum(t - 0.28, 0)) * (t >= 0.28)
    salvar("tosse.wav", ar * envelope)


def gas_sibilo():
    t = tempo(4.0)
    salvar("gas_sibilo.wav", ruido_filtrado(len(t), 2500, 8000) * (0.8 + 0.2 * np.sin(2 * np.pi * 0.5 * t)))


def main():
    celula_zumbido()
    sonar_pulso()
    mascara_respiracao()
    tosse()
    gas_sibilo()
    print("efeitos dos itens de fase gerados")


if __name__ == "__main__":
    main()

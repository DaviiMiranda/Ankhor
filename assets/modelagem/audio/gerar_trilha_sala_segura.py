# gerar_trilha_sala_segura.py — compõe e "toca", por código, o tema da sala
# segura e o som de salvar o jogo. Nenhum instrumento gravado: cada som é uma
# conta (senos, envelope, filtro). Não há problema de licença.
#
# Como rodar (Python 3 + numpy; ffmpeg para gerar o .ogg):
#
#   python assets/modelagem/audio/gerar_trilha_sala_segura.py
#
# O que sai:
#   assets/audio/musica/sala_segura/sala_segura_tema.ogg   64 s, estéreo, em loop sem emenda
#   assets/audio/efeitos/interface/salvar_jogo.wav         3,5 s, estéreo, o "pronto, salvou"
#
# ---------------------------------------------------------------------------
# A MÚSICA
# ---------------------------------------------------------------------------
#
# Clima: o único lugar onde o Gabriel pode respirar. Como a sala segura de
# *Resident Evil*: um piano solitário, devagar, num lugar fechado e quieto. Não
# há tensão nenhuma. Ainda assim é um tema um pouco triste, porque o Gabriel
# está a mil anos de casa, e é por isso que ele é suave em vez de alegre.
#
#   Lá menor com cores abertas, 60 batidas por minuto (1 batida = 1 s).
#   4 blocos de 16 s, um acorde por bloco:
#
#       Lá m9        Fá maj7(9)       Dó maj9         Sol6
#
#   O Lá m9 é a "casa"; o Fá e o Dó sobem de volta ao claro; o Sol6 deixa a
#   porta aberta, e o loop volta ao Lá m9 sem cadência pesada.
#
#   Camadas:
#     1. PIANO      um arpejo lento por cima do acorde, uma nota por batida,
#                   com algumas notas deixadas de fora (pausa também é música)
#                   e a força de cada nota levemente sorteada (mão humana).
#     2. MELODIA    poucas notas agudas, uma a cada 3 ou 4 s, sempre notas do
#                   acorde que está tocando. Bem longe, com muito eco.
#     3. CORDAS     um colchão de senos suaves nas notas do acorde, que sobe
#                   e desce devagar entre um acorde e o outro, sem corte.
#     4. GRAVE      a tônica do acorde, uma nota só por bloco, macia.
#
# ---------------------------------------------------------------------------
# A MATEMÁTICA
# ---------------------------------------------------------------------------
#
# - Nota -> frequência: f = 440 · 2^((n - 69) / 12) (n = número MIDI, 69 = Lá).
# - PIANO: soma de harmônicos k = 1..6 com amplitude 1/k^1,3 (som arredondado)
#   e decaimento mais rápido nos agudos, e = exp(-t / (1,4 / k^0,5)): assim o
#   timbre começa brilhante e vai escurecendo, como corda de piano de verdade.
# - CORDAS: cada nota tem duas cópias a ±0,12 Hz (batimento lento de ~4 s, que
#   dá a sensação de "coro") e um envelope em cosseno de 20 s que avança por
#   cima do acorde vizinho: os acordes se fundem em vez de trocar de repente.
# - ECO: a resposta de uma sala (ruído que decai e escurece) convoluída com o
#   som. Pela FFT, convolução vira multiplicação. A convolução é circular de
#   propósito: a cauda do eco da última nota entra no começo do loop.
# - LOOP SEM EMENDA: as notas que passam do fim voltam ao começo (a música é
#   um círculo), e os senos contínuos têm a frequência arredondada para um
#   número inteiro de ciclos em 64 s.

import os
import subprocess
import wave

import numpy as np

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
SAIDA_TEMA = os.path.join(PASTA_PROJETO, "assets", "audio", "musica", "sala_segura", "sala_segura_tema.ogg")
SAIDA_SALVAR = os.path.join(PASTA_PROJETO, "assets", "audio", "efeitos", "interface", "salvar_jogo.wav")

TAXA = 44100                 # amostras por segundo
BATIDA = 1.0                 # segundos por batida (60 bpm)
BLOCO = 16 * BATIDA          # segundos por acorde
DURACAO = 4 * BLOCO          # 64 s
N = int(DURACAO * TAXA)
T = np.arange(N) / TAXA      # o tempo de cada amostra, em segundos

rng = np.random.default_rng(2026)   # sorteios fixos: rodar de novo dá o mesmo som


def freq(midi):
    """Número MIDI -> frequência em Hz (69 = Lá 440)."""
    return 440.0 * 2.0 ** ((midi - 69) / 12.0)


def no_loop(f):
    """Arredonda a frequência para um número inteiro de ciclos em 64 s."""
    return round(f * DURACAO) / DURACAO


def passa_baixa(x, corte, ordem=2):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1.0 / TAXA)
    X *= 1.0 / np.sqrt(1.0 + (f / corte) ** (2 * ordem))
    return np.fft.irfft(X, len(x))


def passa_alta(x, corte, ordem=2):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1.0 / TAXA)
    X *= 1.0 / np.sqrt(1.0 + (corte / np.maximum(f, 1e-6)) ** (2 * ordem))
    return np.fft.irfft(X, len(x))


def eco(x, segundos=3.0, brilho=3500.0, semente=0):
    """Reverberação: ruído que decai e escurece, convoluído (circular) com o som."""
    r = np.random.default_rng(semente)
    m = int(segundos * TAXA)
    t = np.arange(m) / TAXA
    ir = r.standard_normal(m) * np.exp(-6.9 * t / segundos)   # -60 dB no fim
    ir = passa_baixa(np.pad(ir, (0, len(x) - m)), brilho)
    ir /= np.sqrt(np.sum(ir ** 2))
    return np.fft.irfft(np.fft.rfft(x) * np.fft.rfft(ir), len(x))


def somar_circular(destino, inicio, sinal):
    """Soma 'sinal' em 'destino' a partir da amostra 'inicio'; o que passar do
    fim volta ao começo (a música é um círculo)."""
    idx = (inicio + np.arange(len(sinal))) % len(destino)
    np.add.at(destino, idx, sinal)


def amostra(segundos):
    return int(round(segundos * TAXA)) % N


# ---------------------------------------------------------------------------
# Harmonia (cada acorde dura um bloco de 16 s)
# ---------------------------------------------------------------------------

# (grave, notas do acorde de baixo para cima)
ACORDES = [
    (33, [57, 60, 64, 67, 71]),   # Lá m9:     grave Lá;  Lá Dó Mi Sol Si
    (29, [57, 60, 64, 65, 69]),   # Fá maj7(9): grave Fá; Lá Dó Mi Fá Lá  (o Fá fica no grave)
    (36, [55, 59, 62, 64, 67]),   # Dó maj9:   grave Dó;  Sol Si Ré Mi Sol
    (31, [55, 59, 62, 64, 69]),   # Sol 6:     grave Sol; Sol Si Ré Mi Lá  (o Mi é a sexta)
]

# Ordem do arpejo, uma nota por batida (índices do acorde); None = pausa.
ARPEJO = [0, 2, 3, 4, 3, 2, 1, None, 0, 2, 4, 3, 2, None, 1, 2]

# Melodia: (bloco, batida, índice do acorde, oitava acima)
MELODIA = [
    (0, 2, 4, 12), (0, 7, 3, 12), (0, 12, 2, 12),
    (1, 1, 4, 12), (1, 6, 3, 12), (1, 11, 4, 12),
    (2, 2, 2, 12), (2, 8, 3, 12), (2, 13, 4, 12),
    (3, 0, 4, 12), (3, 5, 2, 12), (3, 10, 3, 12),
]


def piano(f, dur, forca):
    """Uma nota de piano macio: harmônicos que escurecem ao decair."""
    m = int(dur * TAXA)
    t = np.arange(m) / TAXA
    s = np.zeros(m)
    for k in range(1, 7):
        s += (1.0 / k ** 1.3) * np.sin(2 * np.pi * f * k * 1.0002 ** (k * k) * t) \
            * np.exp(-t / (1.4 / k ** 0.5))
    ataque = np.minimum(t / 0.008, 1.0)
    final = np.minimum((dur - t) / 0.3, 1.0)
    return s * ataque * final * forca


def camada_piano():
    esq = np.zeros(N)
    dir_ = np.zeros(N)
    for bloco, (_, notas) in enumerate(ACORDES):
        for batida, indice in enumerate(ARPEJO):
            if indice is None:
                continue
            inicio = amostra((bloco * 16 + batida) * BATIDA + rng.normal(0, 0.012))
            forca = 0.16 * (0.75 + 0.5 * rng.random())
            nota = piano(freq(notas[indice]), 5.0, forca)
            pan = 0.3 + 0.4 * (indice / 4.0)
            somar_circular(esq, inicio, nota * (1.0 - pan))
            somar_circular(dir_, inicio, nota * pan)
    return esq, dir_


def camada_melodia():
    s = np.zeros(N)
    for bloco, batida, indice, oitava in MELODIA:
        nota = ACORDES[bloco][1][indice] + oitava
        inicio = amostra((bloco * 16 + batida) * BATIDA)
        somar_circular(s, inicio, piano(freq(nota), 6.0, 0.13))
    return passa_baixa(s, 5000)


def camada_cordas():
    """Senos suaves nas notas de cada acorde, fundidos com o vizinho."""
    esq = np.zeros(N)
    dir_ = np.zeros(N)
    for bloco, (_, notas) in enumerate(ACORDES):
        centro = (bloco * BLOCO + BLOCO / 2) % DURACAO
        # Janela em cosseno de 32 s: cada acorde cobre o seu bloco e metade de cada vizinho.
        distancia = np.abs(((T - centro + DURACAO / 2) % DURACAO) - DURACAO / 2)
        janela = np.where(distancia < 16.0, 0.5 + 0.5 * np.cos(np.pi * distancia / 16.0), 0.0) ** 1.5
        for i, nota in enumerate(notas[:4]):
            f = no_loop(freq(nota))
            a = np.sin(2 * np.pi * (f - 0.12) * T + i)
            b = np.sin(2 * np.pi * (f + 0.12) * T + 2 * i)
            esq += janela * (0.6 * a + 0.4 * b) * 0.020
            dir_ += janela * (0.4 * a + 0.6 * b) * 0.020
    return esq, dir_


def camada_grave():
    s = np.zeros(N)
    for bloco, (grave, _) in enumerate(ACORDES):
        inicio = amostra(bloco * BLOCO)
        dur = BLOCO + 2.0
        m = int(dur * TAXA)
        t = np.arange(m) / TAXA
        env = np.minimum(t / 1.5, 1.0) * np.minimum((dur - t) / 3.0, 1.0)
        f = freq(grave)
        nota = (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t)) * env * 0.11
        somar_circular(s, inicio, nota)
    return s


def tema():
    print("Compondo o tema da sala segura (64 s, Lá menor, 60 bpm)...")
    pe, pd = camada_piano()
    me = camada_melodia()
    ce, cd = camada_cordas()
    gr = camada_grave()

    esq = pe + 0.9 * eco(pe, 3.0, 4000, 1) + 0.8 * me + 1.6 * eco(me, 5.0, 3000, 2) \
        + ce + 0.6 * eco(ce, 4.0, 2500, 3) + gr
    dir_ = pd + 0.9 * eco(pd, 3.0, 4000, 4) + 0.8 * me + 1.6 * eco(me, 5.0, 3000, 5) \
        + cd + 0.6 * eco(cd, 4.0, 2500, 6) + gr
    estereo = np.stack([passa_alta(esq, 30), passa_alta(dir_, 30)], axis=1)
    estereo *= 0.7 / np.max(np.abs(estereo))

    salto = np.max(np.abs(estereo[0] - estereo[-1]))
    vizinho = np.max(np.abs(np.diff(estereo, axis=0)))
    print("  emenda do loop: salto %.5f (máximo entre vizinhas: %.5f)" % (salto, vizinho))

    os.makedirs(os.path.dirname(SAIDA_TEMA), exist_ok=True)
    wav = SAIDA_TEMA[:-4] + ".wav"
    gravar_wav(wav, estereo)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-c:a", "libvorbis",
                    "-q:a", "5", SAIDA_TEMA], check=True)
    os.remove(wav)
    print("  salvo:", os.path.relpath(SAIDA_TEMA, PASTA_PROJETO))


# ---------------------------------------------------------------------------
# O som de salvar: três notas subindo (Lá, Mi, Lá agudo), como um "pronto",
# sobre um zumbido grave de máquina que acende e some. Dura 3,5 s.
# ---------------------------------------------------------------------------

def sino(f, dur, forca):
    """Nota de sino: parciais inarmônicos (razões 1, 2,76, 5,40) que decaem rápido."""
    t = np.arange(int(dur * TAXA)) / TAXA
    s = np.zeros_like(t)
    for razao, amp, tempo in ((1.0, 1.0, 1.2), (2.76, 0.3, 0.5), (5.40, 0.1, 0.25)):
        s += amp * np.sin(2 * np.pi * f * razao * t) * np.exp(-t / tempo)
    return s * np.minimum(t / 0.004, 1.0) * forca


def salvar():
    print("Compondo o som de salvar...")
    duracao = 3.5
    n = int(duracao * TAXA)
    t = np.arange(n) / TAXA
    esq = np.zeros(n)
    dir_ = np.zeros(n)
    for i, (nota, quando) in enumerate(((81, 0.15), (88, 0.45), (93, 0.80))):
        s = sino(freq(nota), 2.5, 0.35)
        inicio = int(quando * TAXA)
        fim = min(n, inicio + len(s))
        esq[inicio:fim] += s[:fim - inicio] * (0.7 - 0.2 * i)
        dir_[inicio:fim] += s[:fim - inicio] * (0.3 + 0.2 * i)
    zumbido = (np.sin(2 * np.pi * 110 * t) + 0.5 * np.sin(2 * np.pi * 220.5 * t)) \
        * np.sin(np.pi * np.clip(t / duracao, 0, 1)) ** 2 * 0.06
    esq += zumbido
    dir_ += zumbido
    estereo = np.stack([esq, dir_], axis=1)
    estereo *= np.minimum((duracao - t) / 0.2, 1.0)[:, None]
    estereo *= 0.6 / np.max(np.abs(estereo))
    os.makedirs(os.path.dirname(SAIDA_SALVAR), exist_ok=True)
    gravar_wav(SAIDA_SALVAR, estereo)
    print("  salvo:", os.path.relpath(SAIDA_SALVAR, PASTA_PROJETO))


def gravar_wav(caminho, estereo):
    with wave.open(caminho, "wb") as arq:
        arq.setnchannels(2)
        arq.setsampwidth(2)
        arq.setframerate(TAXA)
        arq.writeframes((estereo * 32767).astype("<i2").tobytes())


if __name__ == "__main__":
    tema()
    salvar()

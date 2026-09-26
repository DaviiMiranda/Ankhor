# gerar_tema_biblioteca.py — compõe e "toca", por código, a música da
# Biblioteca durante o jogo, DESENVOLVENDO a melodia que o Davi criou
# (arquivo melodia_anchor1.mp3, feito num programa de música).
#
# Como rodar (Python 3 + numpy; ffmpeg para gerar o .ogg):
#
#   python assets/modelagem/audio/gerar_tema_biblioteca.py
#
# O que sai:
#   assets/audio/musica/biblioteca/biblioteca_tema.ogg   ~165 s, estéreo, loop sem emenda
#
# ---------------------------------------------------------------------------
# O TEMA DO DAVI (transcrito do áudio original)
# ---------------------------------------------------------------------------
#
# A melodia foi transcrita por análise do som: os ATAQUES (quando cada nota
# começa) por fluxo espectral, e a ALTURA de cada nota pela FFT (qual
# frequência apareceu naquele instante). 140 batidas por minuto (aqui tocado a 70), uma frase
# de 2 compassos em colcheias, lá menor:
#
#   colcheia: 1    2    3        4  5    6        7  8  9    10 11       12..16
#   nota:     Dó5  Lá4  Mi4+Sol4 .  Lá4  Dó4+Mi4  .  .  Lá4  .  Dó4+Mi4  (pausa)
#
# ---------------------------------------------------------------------------
# O DESENVOLVIMENTO (técnicas clássicas de composição)
# ---------------------------------------------------------------------------
#
#   comp.  1–8   Silêncio: só o ar da sala; o COMEÇO do tema (Dó–Lá–Mi) soa
#                longe na caixinha de música do menu (liga as duas trilhas).
#   comp.  9–16  Tema: a melodia do Davi como ela é, no piano, 4 vezes.
#   comp. 17–24  SEQUÊNCIA DIATÔNICA: a melodia é deslocada pelos graus da
#                escala para caber em cada acorde (Lám, Fá, Rém, Mi). Cada
#                nota anda o mesmo número de GRAUS (não de semitons), então o
#                desenho da melodia continua reconhecível. No Mi maior entra
#                o Sol♯ (menor harmônica), que "puxa" de volta para o Lá.
#   comp. 25–32  Tensão: só o motivo inicial, INVERTIDO (sobe onde descia),
#                subindo a cada 2 compassos; acorde dissonante; o coração
#                acelera; "shhh" de ruído (a placa de SILÊNCIO).
#   comp. 33–40  CÂNONE: a melodia no piano e, 3 colcheias depois, a mesma
#                no violoncelo uma oitava abaixo, como eco nos corredores.
#   comp. 41–48  Retorno em AUMENTAÇÃO: a melodia com as durações dobradas
#                (duas vezes mais lenta), sumindo no drone até o loop.
#
# A matemática do som (nota -> frequência, série de Fourier, filtro e eco
# pela FFT, loop circular) está explicada em gerar_trilha_menu.py; aqui
# se usa o mesmo método.

import os
import subprocess
import wave

import numpy as np

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
SAIDA = os.path.join(PASTA_PROJETO, "assets", "audio", "musica", "biblioteca", "biblioteca_tema.ogg")

TAXA = 44100
BPM = 70                         # o tema original do Davi é 140; mais lento fica mais sombrio
COLCHEIA = 60.0 / BPM / 2        # ~0,43 s
COMPASSO = 8 * COLCHEIA          # ~3,43 s (4/4)
COMPASSOS = 48
DURACAO = COMPASSOS * COMPASSO   # ~165 s
N = int(round(DURACAO * TAXA))
T = np.arange(N) / TAXA

rng = np.random.default_rng(11)


def freq(midi):
    return 440.0 * 2.0 ** ((midi - 69) / 12.0)


def filtro(x, baixa=None, alta=None, ordem=2):
    """Passa-baixa e/ou passa-alta pela FFT (ganho Butterworth)."""
    X = np.fft.rfft(x)
    f = np.maximum(np.fft.rfftfreq(len(x), 1.0 / TAXA), 1e-6)
    if baixa:
        X *= 1.0 / np.sqrt(1.0 + (f / baixa) ** (2 * ordem))
    if alta:
        X *= 1.0 / np.sqrt(1.0 + (alta / f) ** (2 * ordem))
    return np.fft.irfft(X, len(x))


def eco(x, segundos, brilho, semente):
    """Reverberação por convolução CIRCULAR (o eco do fim volta no começo)."""
    r = np.random.default_rng(semente)
    m = int(segundos * TAXA)
    t = np.arange(m) / TAXA
    ir = np.pad(r.standard_normal(m) * np.exp(-6.9 * t / segundos), (0, N - m))
    ir = filtro(ir, baixa=brilho)
    ir /= np.sqrt(np.sum(ir ** 2))
    return np.fft.irfft(np.fft.rfft(x) * np.fft.rfft(ir), N)


def somar(destino, segundo, sinal):
    """Soma o sinal a partir do tempo dado; o que passa do fim volta no começo."""
    idx = (int(round(segundo * TAXA)) + np.arange(len(sinal))) % N
    np.add.at(destino, idx, sinal)


def em(compasso, colcheia=0.0):
    """Tempo (s) de uma colcheia dentro de um compasso (ambos contam de 0)."""
    return compasso * COMPASSO + colcheia * COLCHEIA


# ---------------------------------------------------------------------------
# O tema e as transformações
# ---------------------------------------------------------------------------

# (colcheia da frase, notas MIDI). 72 = Dó5, 69 = Lá4, 64 = Mi4, 67 = Sol4, 60 = Dó4.
TEMA = [(0, [72]), (1, [69]), (2, [64, 67]), (4, [69]), (5, [60, 64]), (8, [69]), (10, [60, 64])]

# Escala de lá menor natural, em semitons a partir do Lá: Lá Si Dó Ré Mi Fá Sol.
ESCALA = [0, 2, 3, 5, 7, 8, 10]


def deslocar(midi, graus, sensivel=False):
    """SEQUÊNCIA DIATÔNICA: anda 'graus' passos NA ESCALA (não em semitons).
    Ex.: Lá + 2 graus = Dó (Lá->Si->Dó). sensivel=True troca Sol por Sol♯
    (lá menor harmônica), para caber no acorde de Mi maior."""
    rel = midi - 57                       # distância do Lá3
    oitava, resto = divmod(rel, 12)
    grau = ESCALA.index(resto) + graus
    oit2, grau = divmod(grau, 7)
    novo = 57 + 12 * (oitava + oit2) + ESCALA[grau]
    if sensivel and (novo - 57) % 12 == 10:
        novo += 1
    return novo


def tema_em(graus=0, sensivel=False, oitava=0):
    return [(p, [deslocar(m, graus, sensivel) + 12 * oitava for m in ns]) for p, ns in TEMA]


def duracoes(frase, total=16):
    """Cada nota dura até a próxima (a última, até o fim da frase)."""
    saida = []
    for i, (p, ns) in enumerate(frase):
        fim = frase[i + 1][0] if i + 1 < len(frase) else total
        saida.append((p, ns, fim - p))
    return saida


# ---------------------------------------------------------------------------
# Harmonia (um acorde a cada 2 compassos = uma frase)
# ---------------------------------------------------------------------------

LAM = [45, 52, 57, 60, 64]          # Lá menor
DO = [48, 55, 60, 64]               # Dó maior
FA = [41, 48, 53, 57, 60]           # Fá maior
REM = [50, 57, 62, 65]              # Ré menor
MI = [40, 47, 52, 56, 59, 62]       # Mi com sétima (Mi Sol♯ Si Ré)
TENSO = [45, 57, 58, 64]            # Lá com Si♭ (nona menor): dissonante

HARMONIA = ([LAM] * 4                       # comp. 1–8
            + [LAM, DO, LAM, DO]            # 9–16
            + [LAM, FA, REM, MI]            # 17–24
            + [TENSO, TENSO, FA, MI]        # 25–32
            + [LAM, FA, DO, MI]             # 33–40
            + [LAM, LAM, FA, LAM])          # 41–48

# Deslocamento da sequência para cada acorde: (graus, sensível).
GRAUS_DO_ACORDE = {id(LAM): (0, False), id(FA): (-2, False), id(REM): (3, False),
                   id(MI): (4, True), id(DO): (2, False)}


# ---------------------------------------------------------------------------
# Instrumentos
# ---------------------------------------------------------------------------


def piano(destino_e, destino_d, midi, inicio, dur, forca=1.0, pan=0.5):
    """Piano: parciais levemente INARMÔNICOS (a corda dura estica as
    frequências altas: f_h = h·f·√(1 + B·h²)), cada um decaindo mais rápido
    quanto mais agudo, mais o "toque" do martelo (ruído curtinho). Ao soltar
    a tecla (fim da duração), o abafador corta o som em ~0,2 s."""
    f = freq(midi)
    tempo = dur + 0.25
    m = int(tempo * TAXA)
    t = np.arange(m) / TAXA
    B = 0.0004
    s = np.zeros(m)
    for h in range(1, 9):
        fh = h * f * np.sqrt(1 + B * h * h)
        if fh > 8000:
            break
        tau = 1.6 / (1 + 0.35 * h) * (440 / f) ** 0.3
        s += np.sin(2 * np.pi * fh * t + rng.uniform(0, 6.28)) * np.exp(-t / tau) / h ** 1.1
    martelo = rng.standard_normal(m) * np.exp(-t / 0.006) * 0.3
    s += martelo
    s *= np.minimum(t / 0.002, 1.0)
    solta = np.clip((t - dur) / 0.2, 0, 1)
    s *= np.exp(-4 * solta) * (1 - solta)
    s *= 0.11 * forca
    somar(destino_e, inicio, s * np.sqrt(1 - pan))
    somar(destino_d, inicio, s * np.sqrt(pan))


def caixinha(destino_e, destino_d, midi, inicio, forca=1.0):
    """A mesma caixinha de música da trilha do menu (parciais metálicos)."""
    f = freq(midi) * 2 ** (rng.choice([0, 0, 12]) / 1200)
    m = int(3.0 * TAXA)
    t = np.arange(m) / TAXA
    fase = 2 * np.pi * f * t
    s = (np.sin(fase) * np.exp(-t / 1.0) + 0.35 * np.sin(2 * fase) * np.exp(-t / 0.45)
         + 0.1 * np.sin(4.2 * fase) * np.exp(-t / 0.15))
    s *= np.minimum(t / 0.003, 1.0) * 0.12 * forca
    somar(destino_e, inicio, s * 0.5)
    somar(destino_d, inicio, s * 0.7)


def violoncelo(destino_e, destino_d, midi, inicio, dur, forca=1.0):
    """Corda friccionada grave: dente-de-serra (12 harmônicos), entrada lenta
    do arco (0,3 s), vibrato de 5 Hz que só começa depois de meio segundo."""
    f = freq(midi)
    m = int((dur + 0.6) * TAXA)
    t = np.arange(m) / TAXA
    vib = 1 + 0.004 * np.sin(2 * np.pi * 5 * t) * np.clip((t - 0.5) / 0.5, 0, 1)
    fase = 2 * np.pi * np.cumsum(f * vib) / TAXA
    s = sum(np.sin(h * fase) / h for h in range(1, 13) if h * f < 5000)
    env = np.minimum(t / 0.3, 1.0) * np.clip((dur + 0.6 - t) / 0.6, 0, 1)
    s *= env * 0.05 * forca
    somar(destino_e, inicio, s * 0.65)
    somar(destino_d, inicio, s * 0.45)


def pad():
    """Cordas ao fundo, bem escuras: um acorde por frase, com entrada e
    saída suaves que se sobrepõem."""
    e, d = np.zeros(N), np.zeros(N)
    dur = 2 * COMPASSO
    folga = 0.8
    m = int((dur + 2 * folga) * TAXA)
    t = np.arange(m) / TAXA
    rampa = int(2 * folga * TAXA)
    env = np.ones(m)
    env[:rampa] = 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, rampa))
    env[-rampa:] = env[:rampa][::-1]
    for i, acorde in enumerate(HARMONIA):
        # Mais baixo no silêncio do começo e no fim; mais presente no meio.
        vol = 0.5 if i in (0, 1, 2, 3, 22, 23) else 1.0
        for nota in acorde:
            for desafino, lado in ((-5, 0.75), (5, 0.25)):
                f = freq(nota) * 2 ** (desafino / 1200)
                onda = sum(np.sin(2 * np.pi * f * k * t + rng.uniform(0, 6.28)) / k for k in range(1, 7))
                s = onda * env * 0.02 * vol
                somar(e, i * dur - folga, s * np.sqrt(lado))
                somar(d, i * dur - folga, s * np.sqrt(1 - lado))
    return filtro(e, baixa=800, ordem=3), filtro(d, baixa=800, ordem=3)


def drone():
    """Lá grave constante, respirando devagar (período de 8 compassos: 6
    voltas na música, o loop encaixa)."""
    respira = 0.7 + 0.3 * np.sin(2 * np.pi * T / (8 * COMPASSO))
    s = (np.sin(2 * np.pi * freq(33) * T) * 0.05 + np.sin(2 * np.pi * freq(45) * T) * 0.06
         + np.sin(2 * np.pi * freq(52) * T) * 0.015) * respira
    return s, s


def coracao(destino, compasso, batidas):
    """Batimento grave (tum-tum): um seno que cai de 70 para 45 Hz, duas
    vezes, bem curto. 'batidas' = em quais batidas do compasso (0 a 3)."""
    m = int(0.35 * TAXA)
    t = np.arange(m) / TAXA
    f = 45 + 25 * np.exp(-t / 0.04)
    s = np.sin(2 * np.pi * np.cumsum(f) / TAXA) * np.exp(-t / 0.09)
    for b in batidas:
        somar(destino, em(compasso, 2 * b), s * 0.22)
        somar(destino, em(compasso, 2 * b) + 0.16, s * 0.12)


def shh(destino_e, destino_d, compasso):
    """Um "shhh" de biblioteca: ruído agudo que cresce e some em 2 compassos."""
    m = int(2 * COMPASSO * TAXA)
    t = np.linspace(0, 1, m)
    s = filtro(rng.standard_normal(m), baixa=6000, alta=2500)
    s *= np.sin(np.pi * t) ** 3 * 0.02
    somar(destino_e, em(compasso), s)
    somar(destino_d, em(compasso), s * 0.8)


def ar_da_sala():
    """Tom de sala vazia: ruído grave (vento distante) e um chiado baixo.
    O vento é ruído branco filtrado pela FFT (e não uma soma acumulada, que
    terminaria num valor diferente do começo e estalaria na volta do loop)."""
    canais = []
    for _ in range(2):
        vento = filtro(rng.standard_normal(N), baixa=150, alta=25) * 0.06
        chiado = filtro(rng.standard_normal(N), baixa=5000, alta=400) * 0.004
        canais.append(vento + chiado)
    return canais[0], canais[1]


# ---------------------------------------------------------------------------
# A partitura
# ---------------------------------------------------------------------------


def compor():
    pe, pd = np.zeros(N), np.zeros(N)       # piano
    ce, cd = np.zeros(N), np.zeros(N)       # caixinha
    ve, vd = np.zeros(N), np.zeros(N)       # violoncelo
    ee, ed = np.zeros(N), np.zeros(N)       # efeitos (shh)
    bat = np.zeros(N)                       # coração

    # comp. 1–8 — Silêncio: o começo do tema, longe, na caixinha.
    for c in (2, 6):
        for p, m in ((0, 84), (1, 81), (2, 76)):
            caixinha(ce, cd, m, em(c, p), forca=0.7)

    # comp. 9–16 — Tema, como o Davi fez.
    for frase in range(4):
        c0 = 8 + 2 * frase
        for p, ns, d in duracoes(TEMA):
            for m in ns:
                piano(pe, pd, m, em(c0, p), d * COLCHEIA, forca=1.0 if len(ns) == 1 else 0.75)
        coracao(bat, c0, [0])
        coracao(bat, c0 + 1, [0])

    # comp. 17–24 — Sequência diatônica pelos acordes Lám, Fá, Rém, Mi.
    for frase in range(4):
        c0 = 16 + 2 * frase
        acorde = HARMONIA[c0 // 2]
        graus, sensivel = GRAUS_DO_ACORDE[id(acorde)]
        for p, ns, d in duracoes(tema_em(graus, sensivel)):
            for m in ns:
                piano(pe, pd, m, em(c0, p), d * COLCHEIA, forca=1.0 if len(ns) == 1 else 0.75)
        violoncelo(ve, vd, acorde[0] + 12, em(c0), 2 * COMPASSO)
        coracao(bat, c0, [0, 2])
        coracao(bat, c0 + 1, [0, 2])

    # comp. 25–32 — Tensão: motivo invertido (Mi–Lá–Dó, subindo), mais alto
    # a cada 2 compassos, na caixinha e no piano agudo.
    motivo_invertido = [76, 81, 84]
    for i, c in enumerate(range(24, 32)):
        subida = [0, 0, 1, 1, 2, 2, 4, 4][i]
        sensivel = subida == 4
        for p, m in zip((0, 1, 2), motivo_invertido):
            nota = deslocar(m, subida, sensivel)
            caixinha(ce, cd, nota, em(c, p), forca=0.9)
            if i % 2 == 1:
                piano(pe, pd, nota - 12, em(c, p + 4), COLCHEIA * 2, forca=0.5, pan=0.7)
        coracao(bat, c, [0, 1, 2, 3])
    shh(ee, ed, 24)
    shh(ee, ed, 28)
    violoncelo(ve, vd, 45, em(24), 4 * COMPASSO, forca=1.2)
    violoncelo(ve, vd, 46, em(24, 4), 3.5 * COMPASSO, forca=0.6)   # Si♭: a dissonância
    violoncelo(ve, vd, 41, em(28), 2 * COMPASSO)
    violoncelo(ve, vd, 40, em(30), 2 * COMPASSO, forca=1.2)

    # comp. 33–40 — Cânone: piano e, 3 colcheias depois, violoncelo uma oitava abaixo.
    for frase in range(4):
        c0 = 32 + 2 * frase
        acorde = HARMONIA[c0 // 2]
        graus, sensivel = GRAUS_DO_ACORDE[id(acorde)]
        linha = duracoes(tema_em(graus, sensivel))
        for p, ns, d in linha:
            for m in ns:
                piano(pe, pd, m, em(c0, p), d * COLCHEIA, forca=0.9 if len(ns) == 1 else 0.65)
            violoncelo(ve, vd, max(ns) - 12, em(c0, p + 3), d * COLCHEIA, forca=0.8)
        coracao(bat, c0, [0, 2])

    # comp. 41–48 — Aumentação: o tema com as durações dobradas, sumindo.
    for frase, forca in ((0, 0.8), (1, 0.45)):
        c0 = 40 + 4 * frase
        for p, ns, d in duracoes(TEMA):
            for m in ns:
                piano(pe, pd, m, em(c0, 2 * p), 2 * d * COLCHEIA, forca=forca * (1 if len(ns) == 1 else 0.75))

    return (pe, pd), (ce, cd), (ve, vd), (ee, ed), bat


def main():
    print(f"Compondo o tema da Biblioteca ({DURACAO:.1f} s)...")
    (pe, pd), (ce, cd), (ve, vd), (ee, ed), bat = compor()
    ae, ad = pad()
    de, dd = drone()
    se, sd = ar_da_sala()
    bat = filtro(bat, baixa=200)
    # Sala grande e vazia: bastante eco no piano, na caixinha e no violoncelo.
    esq = (pe + 0.8 * eco(pe, 3.5, 3500, 1) + ce * 0.7 + 1.2 * eco(ce, 4.5, 4000, 2)
           + ve + 0.7 * eco(ve, 4.0, 2500, 3) + ae + 0.8 * eco(ae, 5.0, 2000, 4)
           + ee + eco(ee, 3.0, 5000, 5) + de + bat + se)
    dir_ = (pd + 0.8 * eco(pd, 3.5, 3500, 6) + cd * 0.7 + 1.2 * eco(cd, 4.5, 4000, 7)
            + vd + 0.7 * eco(vd, 4.0, 2500, 8) + ad + 0.8 * eco(ad, 5.0, 2000, 9)
            + ed + eco(ed, 3.0, 5000, 10) + dd + bat + sd)
    estereo = np.stack([filtro(esq, alta=30), filtro(dir_, alta=30)], axis=1)
    estereo *= 0.89 / np.max(np.abs(estereo))

    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    wav = SAIDA[:-4] + ".wav"
    with wave.open(wav, "wb") as arq:
        arq.setnchannels(2)
        arq.setsampwidth(2)
        arq.setframerate(TAXA)
        arq.writeframes((estereo * 32767).astype("<i2").tobytes())
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-c:a", "libvorbis",
                    "-q:a", "5", SAIDA], check=True)
    os.remove(wav)
    print("  salvo:", os.path.relpath(SAIDA, PASTA_PROJETO))


if __name__ == "__main__":
    main()

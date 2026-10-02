# gerar_trilha_bunker.py — compõe e "toca", por código, a trilha de fundo
# do Bunker (ÂNCORA-03). Nenhum instrumento gravado: cada som é uma conta
# (seno, envelope, filtro). Não há problema de licença.
#
# Como rodar (Python 3 + numpy; ffmpeg para gerar o .ogg):
#
#   python assets/modelagem/audio/gerar_trilha_bunker.py
#
# O que sai:
#   assets/audio/musica/bunker/bunker_trilha.ogg   64 s, estéreo, em loop sem emenda
#
# ---------------------------------------------------------------------------
# A MÚSICA
# ---------------------------------------------------------------------------
#
# Clima: enterrado. O bunker é o lugar mais seguro do jogo, mas é seguro como
# um túmulo: mil anos de concreto e terra em cima, a Âncora zumbindo embaixo,
# e a Clarice sozinha há tempo demais. Não é a música do susto (essa é a do
# labirinto), é a do peso.
#
# Nada de ruído largo subindo e descendo: era isso que fazia o ambiente antigo
# soar como mar. Aqui tudo é tom (senos e harmônicos), e o ruído só entra
# dentro do eco.
#
#   Dó frígio (Dó Ré♭ Mi♭ Fá Sol Lá♭ Si♭): o modo mais escuro que ainda tem
#   quinta justa. O Ré♭, meio-tom acima da tônica, é a "nota que pesa".
#   4 blocos de 16 s, sem andamento marcado (a música não anda, afunda).
#
#   Acordes (16 s cada), sempre por cima do mesmo Dó grave:
#       Dó m          Ré♭ maj (sobre Dó)     Sol♭ (o trítono)     Dó m(♭9)
#   O Sol♭ é o trítono do Dó: o intervalo mais instável que existe. A volta
#   ao Dó vem com o Ré♭ grudado (♭9): chega em casa, mas a casa está errada.
#
#   Camadas:
#     1. TERRA      o Dó grave (32,7 Hz) com um Dó desafinado que "bate" a
#                   cada 4 s: o peso em cima do bunker.
#     2. CORDAS     os acordes acima, graves e abafados, entrando devagar.
#     3. AÇO        a estrutura gemendo: um som de metal friccionado (parciais
#                   inarmônicas com ataque lento), duas vezes no loop.
#     4. GOLPE      um baque distante e abafado, como algo pesado lá em cima,
#                   a cada 16 s, sempre um pouco antes da troca de acorde.
#     5. FITA       a fita da Clarice (1994): quatro notas de um piano
#                   elétrico gasto, com a afinação oscilando (fita esticada),
#                   só na segunda metade, longe, com muito eco.
#     6. FIO        dois senos agudos a meio-tom de distância, quase
#                   inaudíveis, tremendo: a tensão que nunca vai embora.
#
# ---------------------------------------------------------------------------
# A MATEMÁTICA
# ---------------------------------------------------------------------------
#
# - Nota -> frequência: f = 440 · 2^((n - 69) / 12) (n = número MIDI, 69 = Lá).
# - BATIMENTO: somar dois senos de frequências f e f + Δ dá um som de
#   frequência média cujo volume pulsa Δ vezes por segundo:
#       sen(2πft) + sen(2π(f+Δ)t) = 2 · cos(πΔt) · sen(2π(f + Δ/2)t)
#   Com Δ = 0,25 Hz, o Dó grave "respira" a cada 4 s (camada TERRA) e os dois
#   senos do FIO, a meio-tom, batem rápido e áspero.
# - LOOP SEM EMENDA: os senos que tocam o tempo todo têm a frequência
#   arredondada para um múltiplo de 1/64 Hz, então completam um número
#   inteiro de ciclos em 64 s (o erro é de no máximo 0,008 Hz, inaudível).
#   As notas que começam e terminam são somadas em "círculo" (o que passa do
#   fim volta ao começo), e filtros e eco são feitos pela FFT, que é circular.
# - Timbre por SÉRIE DE FOURIER: soma de senos em f, 2f, 3f... (cordas).
# - Metal por PARCIAIS INARMÔNICAS: razões 1; 2,76; 5,40; 8,93 (as de uma
#   placa ou barra de aço), que não formam uma nota clara.
# - Piano elétrico por SÍNTESE FM (razão 1: harmônico, timbre de Rhodes), com
#   a fase da portadora deslocada por um "wow" de fita: a frequência oscila
#   ±18 cents duas vezes a cada 4 s.
# - Eco = CONVOLUÇÃO com a resposta ao impulso de uma sala de concreto
#   (ruído com queda exponencial), feita como produto na FFT.

import os
import subprocess
import wave

import numpy as np

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
SAIDA = os.path.join(PASTA_PROJETO, "assets", "audio", "musica", "bunker", "bunker_trilha.ogg")

TAXA = 44100                 # amostras por segundo
BLOCO = 16.0                 # segundos por acorde
DURACAO = 4 * BLOCO          # 64 s
N = int(DURACAO * TAXA)
T = np.arange(N) / TAXA      # o tempo de cada amostra, em segundos

rng = np.random.default_rng(1994)   # sorteios fixos: rodar de novo dá o mesmo som


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


def eco(x, segundos=4.0, brilho=3000.0, semente=0):
    """Reverberação: ruído que decai e escurece, convoluído (circular) com o som."""
    r = np.random.default_rng(semente)
    m = int(segundos * TAXA)
    t = np.arange(m) / TAXA
    ir = r.standard_normal(m) * np.exp(-6.9 * t / segundos)   # -60 dB no fim
    ir = passa_baixa(np.pad(ir, (0, N - m)), brilho)
    ir /= np.sqrt(np.sum(ir ** 2))
    return np.fft.irfft(np.fft.rfft(x) * np.fft.rfft(ir), N)


def somar_circular(destino, inicio, sinal):
    """Soma 'sinal' em 'destino' a partir da amostra 'inicio'; o que passar do
    fim volta ao começo (a música é um círculo)."""
    idx = (inicio + np.arange(len(sinal))) % N
    np.add.at(destino, idx, sinal)


def amostra(segundos):
    return int(round(segundos * TAXA)) % N


def rampa(m, sobe, desce):
    """Envelope de 'm' amostras: sobe e desce em cosseno (sem estalo)."""
    env = np.ones(m)
    a, b = int(sobe * TAXA), int(desce * TAXA)
    env[:a] = 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, a))
    env[m - b:] = 0.5 + 0.5 * np.cos(np.linspace(0, np.pi, b))
    return env


# ---------------------------------------------------------------------------
# Harmonia (cada acorde dura um bloco de 16 s)
# ---------------------------------------------------------------------------

ACORDES = [
    [36, 43, 48, 51, 55],        # Dó m:              Dó Sol Dó Mi♭ Sol
    [37, 44, 49, 53, 56],        # Ré♭ maj / Dó:      Ré♭ Lá♭ Ré♭ Fá Lá♭ (o Dó fica na TERRA)
    [42, 49, 54, 58, 61],        # Sol♭ (trítono):    Sol♭ Ré♭ Sol♭ Si♭ Ré♭
    [36, 43, 49, 51, 55],        # Dó m(♭9):          Dó Sol Ré♭ Mi♭ Sol
]


def terra():
    """O Dó grave: 32,7 Hz e a oitava acima, cada um somado a uma cópia
    0,25 Hz mais aguda (batimento de 4 s). Um pouco de 3º harmônico para o
    grave aparecer em caixas pequenas."""
    s = np.zeros(N)
    for nota, amp in ((24, 1.0), (36, 0.55)):
        f = no_loop(freq(nota))
        for k, peso in ((1, 1.0), (2, 0.3), (3, 0.18)):
            s += peso * amp * np.sin(2 * np.pi * f * k * T)
            s += peso * amp * np.sin(2 * np.pi * (f + 0.25) * k * T + 1.3)
    return passa_baixa(s * 0.06, 220)


def cordas():
    """Cordas graves: dente-de-serra suave (6 harmônicos), 3 vozes
    desafinadas por nota abertas no estéreo, entrando em 5 s e saindo em 5 s,
    com os acordes se sobrepondo na troca. Filtro bem escuro."""
    esq, dir_ = np.zeros(N), np.zeros(N)
    folga = 3.0
    m = int((BLOCO + 2 * folga) * TAXA)
    t = np.arange(m) / TAXA
    env = rampa(m, 5.0, 5.0)
    for i, acorde in enumerate(ACORDES):
        inicio = amostra(i * BLOCO - folga)
        for j, nota in enumerate(acorde):
            for desafino, lado in ((-9, 0.85), (0, 0.5), (9, 0.15)):
                f = freq(nota) * 2 ** (desafino / 1200)
                fase = rng.uniform(0, 2 * np.pi)
                onda = sum(np.sin(2 * np.pi * f * k * t + fase * k) / k for k in range(1, 7))
                volume = 0.034 if j > 0 else 0.045
                s = onda * env * volume
                somar_circular(esq, inicio, s * np.sqrt(lado))
                somar_circular(dir_, inicio, s * np.sqrt(1 - lado))
    return passa_baixa(esq, 650, 3), passa_baixa(dir_, 650, 3)


def aco():
    """A estrutura gemendo: parciais de barra de aço sobre um Sol♭1 e um Ré♭2,
    com ataque lento (fricção, não batida) e a altura caindo um pouco."""
    s = np.zeros(N)
    m = int(11.0 * TAXA)
    t = np.arange(m) / TAXA
    env = np.minimum(t / 3.0, 1.0) ** 2 * np.exp(-np.maximum(t - 3.0, 0) / 2.5)
    queda = 1 - 0.03 * (t / t[-1])
    for segundos, nota in ((6.0, 30), (38.0, 37)):
        f0 = freq(nota)
        som = np.zeros(m)
        for razao, amp in ((1.0, 1.0), (2.76, 0.6), (5.40, 0.35), (8.93, 0.18)):
            fase = 2 * np.pi * np.cumsum(f0 * razao * queda) / TAXA
            vibrato = 1 + 0.15 * np.sin(2 * np.pi * 5.3 * t * razao ** 0.3)
            som += amp * np.sin(fase) * vibrato
        somar_circular(s, amostra(segundos), som * env * 0.05)
    return passa_baixa(s, 2500)


def golpe():
    """Um baque grave e abafado lá em cima (seno de 45 Hz caindo para 30 Hz,
    com um 'toc' de concreto), 1,5 s antes de cada troca de acorde."""
    s = np.zeros(N)
    m = int(2.5 * TAXA)
    t = np.arange(m) / TAXA
    f_inst = 30 + 15 * np.exp(-t / 0.15)
    fase = 2 * np.pi * np.cumsum(f_inst) / TAXA
    baque = np.sin(fase) * np.exp(-t / 0.7) * np.minimum(t / 0.01, 1.0)
    toc = passa_baixa(np.pad(rng.standard_normal(int(0.04 * TAXA)), (0, m - int(0.04 * TAXA))), 400)
    baque += toc * np.exp(-t / 0.03) * 0.6
    for i, forca in enumerate((1.0, 0.6, 0.85, 0.5)):
        somar_circular(s, amostra((i + 1) * BLOCO - 1.5), baque * 0.22 * forca)
    return passa_baixa(s, 300)


# A fita da Clarice: (nota MIDI, segundo em que começa). Só na 2ª metade.
# Sol4 Mi♭4 Ré♭4 Dó4: desce até a tônica pelo Ré♭ (frígio). A primeira vez
# toca sobre o acorde do trítono (Sol♭), e o Sol da melodia raspa no Sol♭;
# a segunda chega no Dó, mas com o Ré♭ grudado no acorde.
MELODIA = [
    (67, 33.0), (63, 35.5), (61, 38.0), (60, 42.0),
    (67, 49.0), (63, 51.5), (61, 54.0), (60, 58.5),
]


def piano_eletrico(f, dur, wow):
    """Uma nota de piano elétrico (FM razão 1, índice que cai) com a
    frequência deformada pelo 'wow' da fita."""
    m = int(dur * TAXA)
    t = np.arange(m) / TAXA
    f_inst = f * 2 ** (wow[:m] * 18 / 1200)
    fase = 2 * np.pi * np.cumsum(f_inst) / TAXA
    indice = 1.6 * np.exp(-t / 0.4)
    s = np.sin(fase + indice * np.sin(fase))
    s += 0.2 * np.sin(2 * fase) * np.exp(-t / 0.3)
    return s * np.exp(-t / 1.8) * np.minimum(t / 0.005, 1.0)


def fita():
    """Melodia em mono, abafada (fita velha corta os agudos), com wow de
    0,5 Hz e um pouco de saturação (tanh), bem longe."""
    s = np.zeros(N)
    wow = np.sin(2 * np.pi * 0.5 * T) + 0.4 * np.sin(2 * np.pi * 1.25 * T + 0.7)
    for nota, segundos in MELODIA:
        inicio = amostra(segundos)
        trecho = np.roll(wow, -inicio)
        somar_circular(s, inicio, piano_eletrico(freq(nota), 5.0, trecho) * 0.10)
    s = np.tanh(s * 3.0) / 3.0
    return passa_alta(passa_baixa(s, 1800, 3), 180)


def fio():
    """Dó6 e Ré♭6 juntos (batimento de ~66 Hz, áspero), quase sem volume,
    com um tremolo lento que some e volta a cada 16 s."""
    a, b = no_loop(freq(84)), no_loop(freq(85))
    s = np.sin(2 * np.pi * a * T) + 0.8 * np.sin(2 * np.pi * b * T + 0.4)
    tremolo = 0.5 - 0.5 * np.cos(2 * np.pi * T / BLOCO)
    return s * tremolo ** 2 * 0.006


def main():
    print("Compondo a trilha do Bunker (64 s, Dó frígio)...")
    te = terra()
    ce, cd = cordas()
    ac = aco()
    go = golpe()
    fi = fita()
    fo = fio()

    # Eco de sala de concreto: muito no aço, na fita e no golpe; pouco nas
    # cordas; a terra fica seca (o grave com eco embola).
    esq = (te + ce + 0.5 * eco(ce, 4.0, 1500, 1) + 0.6 * ac + 1.4 * eco(ac, 6.0, 2500, 2)
           + go + 1.2 * eco(go, 3.0, 800, 3) + 0.4 * fi + 1.6 * eco(fi, 5.0, 2000, 4) + fo)
    dir_ = (te + cd + 0.5 * eco(cd, 4.0, 1500, 5) + 0.6 * ac + 1.4 * eco(ac, 6.0, 2500, 6)
            + go + 1.2 * eco(go, 3.0, 800, 7) + 0.4 * fi + 1.6 * eco(fi, 5.0, 2000, 8) + fo)
    estereo = np.stack([passa_alta(esq, 25), passa_alta(dir_, 25)], axis=1)
    # Normaliza: pico em -2 dB.
    estereo *= 0.8 / np.max(np.abs(estereo))

    # Confere a emenda do loop: a diferença entre a última e a primeira amostra
    # tem de ser do tamanho da diferença entre amostras vizinhas quaisquer.
    salto = np.max(np.abs(estereo[0] - estereo[-1]))
    vizinho = np.max(np.abs(np.diff(estereo, axis=0)))
    print("  emenda do loop: salto %.5f (máximo entre vizinhas: %.5f)" % (salto, vizinho))

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

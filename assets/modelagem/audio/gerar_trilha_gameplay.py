# gerar_trilha_gameplay.py — compõe e "toca", por código, a trilha de fundo
# do gameplay (a exploração da Biblioteca). Nenhum instrumento gravado: cada
# som é uma conta (seno, ruído, envelope). Não há problema de licença.
#
# Como rodar (Python 3 + numpy; ffmpeg para gerar o .ogg):
#
#   python assets/modelagem/audio/gerar_trilha_gameplay.py
#
# O que sai:
#   assets/audio/musica/gameplay/gameplay_trilha.ogg   70 s, estéreo, em loop sem emenda
#
# ---------------------------------------------------------------------------
# A MÚSICA
# ---------------------------------------------------------------------------
#
# Clima: mistério. A Biblioteca vazia, mil anos depois, com uma fenda no tempo
# respirando em algum lugar. Nada de susto: é a música de quem anda devagar,
# escuta e desconfia. (A trilha de perseguição, quando existir, é outra.)
#
#   48 batidas por minuto, 7 batidas por compasso (7/4, agrupadas 4+3).
#   1 compasso = 8,75 s. 8 compassos = 70 s.
#
#   Por que 7/4? Compasso par (4/4) "embala" e dá sensação de marcha, de
#   segurança. O 7/4 sempre manca: o corpo espera a batida e ela vem uma
#   antes ou depois. É o "tem algo errado aqui" em forma de ritmo.
#
#   Acordes (2 compassos cada), em torno do Mi:
#       Mi m(add9)   Dó maj7(#11)   Lá m(add9)/Mi   Si 7(sus4, ♭9)
#   O último acorde pede para voltar ao Mi, mas o Mi que volta é menor e
#   sem "conclusão": a música nunca chega em casa.
#
#   Camadas:
#     1. PAD            cordas escuras e abafadas, os acordes acima.
#     2. PULSO          um "tum" grave em cada grupo do 7/4 (batidas 1 e 5):
#                       o coração da fenda.
#     3. SINO DE VIDRO  a melodia: poucas notas, muito espaço, com eco em
#                       ping-pong e um "sopro ao contrário" antes de algumas.
#     4. ÂNCORA         um gongo grave e inarmônico, uma vez a cada 4 compassos:
#                       o eco do aparelho que explodiu.
#     5. FENDA          um tom de Shepard descendo sem parar (veja abaixo).
#     6. GOTEIRA        pingos distantes, fora do ritmo, na sala vazia.
#     7. VENTO          ruído filtrado que sobe e desce devagar.
#
# ---------------------------------------------------------------------------
# A MATEMÁTICA
# ---------------------------------------------------------------------------
#
# - Nota -> frequência: f = 440 · 2^((n - 69) / 12) (n = número MIDI, 69 = Lá).
# - Timbre por SÉRIE DE FOURIER: soma de senos em f, 2f, 3f... (pad).
# - Sino por SÍNTESE FM: seno cuja fase é modulada por outro seno numa razão
#   NÃO inteira (3,5). Isso cria parciais inarmônicas, o timbre de vidro/metal.
# - Filtros e reverberação pela FFT (produto no domínio da frequência; o eco
#   é a CONVOLUÇÃO com a resposta ao impulso da sala). Como a FFT é circular,
#   o rabo do eco no fim volta ao começo: o loop fica sem emenda.
# - TOM DE SHEPARD (a "fenda"): uma pilha de senos separados por oitavas, todos
#   descendo juntos, cada um com volume dado por uma gaussiana na altura
#   (em oitavas). Um som some no grave enquanto outro nasce no agudo, e o
#   ouvido escuta uma descida INFINITA que nunca chega ao fim. Em 70 s cada
#   seno desce exatamente 1 oitava: f_k(t) = f0 · 2^(k - t/70). A fase é a
#   integral da frequência:
#       fase_k(t) = -(f0 · 2^k · 70 / ln 2) · 2^(-t/70)
#   No fim (t = 70) o seno k tem a mesma fase que o seno k-1 tinha em t = 0,
#   então o loop não dá clique. É o "tempo sendo puxado" do enredo.
# - Todo o resto que oscila tem período que divide 70 s, para o loop encaixar.

import os
import subprocess
import wave

import numpy as np

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
SAIDA = os.path.join(PASTA_PROJETO, "assets", "audio", "musica", "gameplay", "gameplay_trilha.ogg")

TAXA = 44100                 # amostras por segundo
BPM = 48
BATIDA = 60.0 / BPM          # 1,25 s
COMPASSO = 7 * BATIDA        # 8,75 s
DURACAO = 8 * COMPASSO       # 70 s
BATIDAS_TOTAL = 56
N = int(DURACAO * TAXA)
T = np.arange(N) / TAXA      # o tempo de cada amostra, em segundos

rng = np.random.default_rng(3026)   # sorteios fixos: rodar de novo dá o mesmo som


def freq(midi):
    """Número MIDI -> frequência em Hz (69 = Lá 440)."""
    return 440.0 * 2.0 ** ((midi - 69) / 12.0)


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


def eco(x, segundos=4.0, brilho=3500.0, semente=0):
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


def amostra(batida):
    return int(round(batida * BATIDA * TAXA))


# ---------------------------------------------------------------------------
# Harmonia (cada acorde dura 2 compassos = 14 batidas)
# ---------------------------------------------------------------------------

ACORDES = [
    [40, 52, 55, 59, 66],        # Mi m(add9):        Mi Sol Si Fá♯
    [36, 48, 55, 59, 66],        # Dó maj7(#11):      Dó Sol Si Fá♯
    [40, 57, 60, 64, 71],        # Lá m(add9)/Mi:     Mi Lá Dó Mi Si
    [35, 47, 52, 54, 57, 60],    # Si 7 sus4 ♭9:      Si Mi Fá♯ Lá Dó
]
RAIZ_PULSO = [40, 36, 40, 35]   # nota do "tum" em cada acorde (Mi Dó Mi Si)


def pad():
    """Cordas sintéticas: dente-de-serra suave (8 harmônicos), 3 vozes
    desafinadas por nota, uma de cada lado do estéreo, e filtro escuro."""
    esq, dir_ = np.zeros(N), np.zeros(N)
    dur = 14 * BATIDA
    folga = 2.5
    m = int((dur + 2 * folga) * TAXA)
    t = np.arange(m) / TAXA
    env = np.ones(m)
    sobe = int(2 * folga * TAXA)
    rampa = 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, sobe))
    env[:sobe] = rampa
    env[-sobe:] = rampa[::-1]
    for i, acorde in enumerate(ACORDES):
        inicio = int((i * dur - folga) * TAXA)
        for nota in acorde:
            for desafino, lado in ((-7, 0.8), (0, 0.5), (7, 0.2)):
                f = freq(nota) * 2 ** (desafino / 1200)
                fase = rng.uniform(0, 2 * np.pi)
                onda = sum(np.sin(2 * np.pi * f * k * t + fase * k) / k for k in range(1, 9))
                s = onda * env * 0.038
                somar_circular(esq, inicio % N, s * np.sqrt(lado))
                somar_circular(dir_, inicio % N, s * np.sqrt(1 - lado))
    return passa_baixa(esq, 1000, 3), passa_baixa(dir_, 1000, 3)


def pulso():
    """O coração da fenda: um 'tum' grave nas batidas 1 e 5 de cada compasso
    (grupos 4+3). A frequência cai rápido logo depois do golpe (bumbo suave);
    o segundo golpe é mais fraco."""
    s = np.zeros(N)
    m = int(1.6 * TAXA)
    t = np.arange(m) / TAXA
    for comp in range(8):
        acorde = (comp * 7) // 14
        f0 = freq(RAIZ_PULSO[acorde])
        for offset, forca in ((0, 1.0), (4, 0.55)):
            f_inst = f0 * (1 + 0.9 * np.exp(-t / 0.05))
            fase = 2 * np.pi * np.cumsum(f_inst) / TAXA
            golpe = np.sin(fase) * np.exp(-t / 0.4) * np.minimum(t / 0.006, 1.0)
            somar_circular(s, amostra(comp * 7 + offset), golpe * 0.16 * forca)
    return s


# Melodia do sino de vidro: (nota MIDI, batida em que começa, com sopro antes?)
# Poucas notas, muito silêncio. Mi=76 Fá=77 Sol=79 Lá=81 Si=83 Dó=72 Ré=74.
MELODIA = [
    # Mi m(add9): sobe até o Si e desce devagar
    (83, 1.0, True), (79, 3.0, False), (78, 5.5, False), (76, 9.0, False),
    # Dó maj7(#11): o Fá♯ (a nota "errada" do acorde) fica no ar
    (79, 15.0, True), (83, 17.0, False), (78, 19.5, False), (74, 23.0, False),
    # Lá m(add9)/Mi
    (81, 29.0, True), (76, 31.0, False), (72, 33.5, False), (71, 37.0, False),
    # Si 7 sus4 ♭9: termina no Si, sem resolver o Dó (♭9) que pende antes
    (81, 43.0, True), (72, 45.5, False), (78, 49.0, False), (71, 52.0, False),
]


def sino_de_vidro(f, dur=6.0):
    """Uma nota de sino: FM com razão 3,5 (parciais inarmônicas = vidro)."""
    m = int(dur * TAXA)
    t = np.arange(m) / TAXA
    indice = 2.2 * np.exp(-t / 0.7)          # brilho que morre depressa
    fase = 2 * np.pi * f * t + indice * np.sin(2 * np.pi * f * 3.5 * t)
    s = np.sin(fase) * np.exp(-t / 2.0)
    s += 0.25 * np.sin(2 * np.pi * f * 2.0 * t) * np.exp(-t / 0.6)
    return s * np.minimum(t / 0.004, 1.0)


def sino():
    """Melodia + sopro ao contrário (a nota tocada de trás para frente, que
    'sobe' até o ataque) + eco em ping-pong de 2 batidas (2,5 s)."""
    mono = np.zeros(N)
    for nota, batida, sopro in MELODIA:
        f = freq(nota)
        inicio = amostra(batida)
        somar_circular(mono, inicio, sino_de_vidro(f) * 0.10)
        if sopro:
            cauda = passa_baixa(np.pad(sino_de_vidro(f, 2.0), (0, 0)), 2500)
            inverso = cauda[::-1] * 0.5
            somar_circular(mono, inicio - len(inverso), inverso * 0.10)
    mono = passa_baixa(mono, 6500)
    atraso = amostra(2.0)
    esq = 0.75 * mono
    dir_ = 0.55 * mono
    fb = 0.5
    for i in range(1, 6):
        c = np.roll(mono, i * atraso) * fb ** i
        if i % 2 == 1:
            dir_ += 0.9 * c
            esq += 0.35 * c
        else:
            esq += 0.9 * c
            dir_ += 0.35 * c
    return esq, dir_


def ancora():
    """O gongo do aparelho que explodiu: parciais inarmônicas de um Mi3,
    decaimento longo. Toca no compasso 1 e no compasso 5."""
    f = freq(52)
    m = int(9.0 * TAXA)
    t = np.arange(m) / TAXA
    s = np.zeros(m)
    for razao, amp, tau in ((1.0, 1.0, 5.0), (2.76, 0.5, 3.0), (5.40, 0.3, 2.0),
                            (8.93, 0.15, 1.2), (13.3, 0.07, 0.6)):
        s += amp * np.sin(2 * np.pi * f * razao * t) * np.exp(-t / tau)
    s *= np.minimum(t / 0.02, 1.0)
    saida = np.zeros(N)
    for batida in (0, 28):
        somar_circular(saida, amostra(batida), s * 0.045)
    return saida


def fenda():
    """Tom de Shepard descendo: 8 senos separados por oitavas, cada um
    descendo 1 oitava em 70 s, com volume gaussiano na altura (veja o topo)."""
    f0 = 55.0
    saida = np.zeros(N)
    for k in range(0, 8):
        pos = k - T / DURACAO                                   # altura, em oitavas
        amp = np.exp(-((pos - 2.5) ** 2) / (2 * 1.0 ** 2))       # gaussiana
        fase = -(f0 * 2.0 ** k * DURACAO / np.log(2)) * 2.0 ** (-T / DURACAO)
        saida += amp * np.sin(2 * np.pi * fase)
    tremolo = 0.8 + 0.2 * np.sin(2 * np.pi * T / 17.5)
    saida = passa_baixa(saida * tremolo * 0.022, 2200)
    return saida


def goteira():
    """Pingos distantes de água numa sala grande e vazia: um bip curto com a
    frequência caindo. Fora do compasso de propósito."""
    s = np.zeros(N)
    m = int(0.25 * TAXA)
    t = np.arange(m) / TAXA
    for batida, nota in ((10.6, 96), (24.3, 93), (33.2, 98), (47.7, 95), (54.4, 91)):
        f_inst = freq(nota) * (1 - 0.35 * (1 - np.exp(-t / 0.03)))
        fase = 2 * np.pi * np.cumsum(f_inst) / TAXA
        gota = np.sin(fase) * np.exp(-t / 0.05) * np.minimum(t / 0.002, 1.0)
        somar_circular(s, amostra(batida), gota * 0.10)
    return s


def vento():
    """Sopro de corrente de ar: ruído entre 150 e 900 Hz, com volume subindo
    e descendo (períodos de 35 s e 17,5 s: dividem 70 s)."""
    saida = []
    for _ in range(2):
        r = passa_baixa(passa_alta(rng.standard_normal(N), 150), 900, 3)
        vol = 0.5 + 0.3 * np.sin(2 * np.pi * T / 35.0) + 0.2 * np.sin(2 * np.pi * T / 17.5 + 1.0)
        saida.append(r * vol * 0.05)
    return saida[0], saida[1]


def main():
    print("Compondo a trilha do gameplay (70 s, 48 BPM, 7/4)...")
    pe, pd = pad()
    pu = pulso()
    se, sd = sino()
    an = ancora()
    fe = fenda()
    go = goteira()
    ve, vd = vento()

    # Eco: bastante no pad, no sino, no gongo e nas gotas (sala grande);
    # o pulso e a fenda ficam secos, para dar chão à música.
    esq = (pe + 0.8 * eco(pe, 5.0, 2500, 1) + pu + se * 0.8 + 1.0 * eco(se, 5.0, 4000, 2)
           + an + 1.5 * eco(an, 6.0, 3000, 3) + fe + 0.7 * go + 2.0 * eco(go, 3.5, 5000, 4) + ve)
    dir_ = (pd + 0.8 * eco(pd, 5.0, 2500, 5) + pu + sd * 0.8 + 1.0 * eco(sd, 5.0, 4000, 6)
            + an + 1.5 * eco(an, 6.0, 3000, 7) + fe + 0.7 * go + 2.0 * eco(go, 3.5, 5000, 8) + vd)
    estereo = np.stack([passa_alta(esq, 30), passa_alta(dir_, 30)], axis=1)
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

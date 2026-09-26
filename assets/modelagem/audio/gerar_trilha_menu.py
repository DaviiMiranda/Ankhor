# gerar_trilha_menu.py — compõe e "toca", por código, a trilha do menu
# principal. Nenhum instrumento gravado: cada som é uma conta (seno, ruído,
# envelope). Por isso não há problema de licença: a música é do grupo.
#
# Como rodar (Python 3 + numpy; ffmpeg para gerar o .ogg):
#
#   python assets/modelagem/audio/gerar_trilha_menu.py
#
# O que sai:
#   assets/audio/musica/menu/menu_trilha.ogg   64 s, estéreo, em loop sem emenda
#
# ---------------------------------------------------------------------------
# A MÚSICA
# ---------------------------------------------------------------------------
#
# Clima: a mesa de estudo de madrugada, na véspera das provas (o menu), e o
# sono que durou mil anos. Lenta, escura e melancólica, mas não assustadora
# ainda: o susto é para dentro do jogo.
#
#   60 batidas por minuto, 4 por compasso: 1 compasso = 4 s. 16 compassos = 64 s.
#   Acordes (2 compassos cada): Rém  Si♭  Solm  Lá   Rém  Si♭  Solm  Lá
#                               (ré menor, com o Lá maior puxando de volta)
#   Compassos 1–8:  só o "ar" da sala: pad, drone grave, relógio e chiado.
#   Compassos 9–16: entra a CAIXINHA DE MÚSICA com uma canção de ninar
#                   (o tema do sono), um pouco desafinada e com a "fita"
#                   oscilando, como uma gravação velha.
#
# ---------------------------------------------------------------------------
# A MATEMÁTICA
# ---------------------------------------------------------------------------
#
# - Nota -> frequência: f = 440 · 2^((n - 69) / 12), onde n é o número MIDI
#   (69 = Lá 440 Hz). Cada semitom multiplica a frequência por 2^(1/12).
# - Timbre por SÉRIE DE FOURIER: uma onda dente-de-serra é a soma de senos
#   nas frequências f, 2f, 3f... com amplitudes 1, 1/2, 1/3... Somamos só os
#   primeiros harmônicos (acima disso o som ficaria áspero).
# - Filtro passa-baixa pela TRANSFORMADA DE FOURIER (FFT): passamos o som
#   para o "domínio da frequência", multiplicamos cada frequência por um
#   ganho (1 nas graves, caindo nas agudas) e voltamos. Escurece o som.
# - Eco (reverberação) por CONVOLUÇÃO: o eco de uma sala é a "resposta ao
#   impulso" (o que se ouve depois de uma palma). Convoluir o som com ela
#   é o mesmo que multiplicar as duas FFTs. Como a FFT trata o sinal como
#   CIRCULAR, o eco que passa do fim da música volta no começo: o loop fica
#   sem emenda de graça.
# - Tudo que oscila (a fita, o tremolo) tem período que divide 64 s, para o
#   fim da música encaixar exatamente no começo.

import os
import subprocess
import wave

import numpy as np

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
SAIDA = os.path.join(PASTA_PROJETO, "assets", "audio", "musica", "menu", "menu_trilha.ogg")

TAXA = 44100                 # amostras por segundo
BPM = 60
BATIDA = 60.0 / BPM          # 1 s
COMPASSO = 4 * BATIDA        # 4 s
DURACAO = 16 * COMPASSO      # 64 s
N = int(DURACAO * TAXA)
T = np.arange(N) / TAXA      # o tempo de cada amostra, em segundos

rng = np.random.default_rng(7)   # sorteios fixos: rodar de novo dá o mesmo som


def freq(midi):
    """Número MIDI -> frequência em Hz (69 = Lá 440)."""
    return 440.0 * 2.0 ** ((midi - 69) / 12.0)


def passa_baixa(x, corte, ordem=2):
    """Filtro passa-baixa pela FFT (ganho de um filtro Butterworth)."""
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
    """Reverberação: resposta ao impulso de ruído que decai (exponencial) e
    fica mais escura com o tempo, convoluída de forma CIRCULAR com o som."""
    r = np.random.default_rng(semente)
    m = int(segundos * TAXA)
    t = np.arange(m) / TAXA
    ir = r.standard_normal(m) * np.exp(-6.9 * t / segundos)   # -60 dB no fim
    ir = passa_baixa(np.pad(ir, (0, N - m)), brilho)          # mesmo tamanho do som
    ir /= np.sqrt(np.sum(ir ** 2))
    return np.fft.irfft(np.fft.rfft(x) * np.fft.rfft(ir), N)


def somar_circular(destino, inicio, sinal):
    """Soma 'sinal' em 'destino' a partir da amostra 'inicio'; o que passar
    do fim volta no começo (a música é um círculo)."""
    idx = (inicio + np.arange(len(sinal))) % N
    np.add.at(destino, idx, sinal)


# ---------------------------------------------------------------------------
# Harmonia
# ---------------------------------------------------------------------------

# Cada acorde: notas MIDI (62 = Ré4). Dura 2 compassos (8 s).
RE, SIb, SOL, LA = 62, 58, 55, 57
ACORDES = [
    [RE - 12, RE, RE + 3, RE + 7],            # Rém:  Ré Fá Lá
    [SIb - 12, SIb + 4, SIb + 7, SIb + 12],   # Si♭:  Si♭ Ré Fá
    [SOL - 12, SOL + 3, SOL + 7, SOL + 10],   # Solm: Sol Si♭ Ré (+Fá)
    [LA - 12, LA + 4, LA + 7, LA + 12],       # Lá:   Lá Dó♯ Mi
] * 2


def pad():
    """Cordas sintéticas: dente-de-serra suave (8 harmônicos), 3 vozes
    levemente desafinadas por nota (± 6 centésimos: é o "coro" que dá corpo),
    uma de cada lado do estéreo. Cada acorde entra e sai devagar (2 s),
    sobrepondo com o vizinho."""
    esq, dir_ = np.zeros(N), np.zeros(N)
    dur = 2 * COMPASSO
    folga = 2.0
    m = int((dur + 2 * folga) * TAXA)
    t = np.arange(m) / TAXA
    # Envelope: sobe em 'folga' segundos, fica, desce em 'folga' (cosseno).
    env = np.ones(m)
    sobe = int(2 * folga * TAXA)
    rampa = 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, sobe))
    env[:sobe] = rampa
    env[-sobe:] = rampa[::-1]
    for i, acorde in enumerate(ACORDES):
        inicio = int((i * dur - folga) * TAXA)
        for nota in acorde:
            for desafino, lado in ((-6, 0.8), (0, 0.5), (6, 0.2)):
                f = freq(nota) * 2 ** (desafino / 1200)
                fase = rng.uniform(0, 2 * np.pi)
                onda = sum(np.sin(2 * np.pi * f * k * t + fase * k) / k for k in range(1, 9))
                s = onda * env * 0.05
                somar_circular(esq, inicio % N, s * np.sqrt(lado))
                somar_circular(dir_, inicio % N, s * np.sqrt(1 - lado))
    # Escuro e abafado, como ouvido do outro lado de uma parede.
    return passa_baixa(esq, 900, 3), passa_baixa(dir_, 900, 3)


def drone():
    """Ré grave (Ré2 + Ré1) constante, com um "respirar" lento de volume
    (período de 16 s: 4 voltas em 64 s, encaixa no loop)."""
    respira = 0.75 + 0.25 * np.sin(2 * np.pi * T / 16.0)
    # O Ré1 (37 Hz) quase não se ouve em caixa de notebook: fica baixinho,
    # só para "encher" em fone e caixa boa. Quem carrega o drone é o Ré2.
    s = (np.sin(2 * np.pi * freq(38) * T) * 0.07 + np.sin(2 * np.pi * freq(26) * T) * 0.03
         + np.sin(2 * np.pi * freq(45) * T) * 0.025) * respira
    return s, s


# Canção de ninar (compassos 9–16): (nota MIDI, batida em que começa).
# Uma nota por batida, com pausas; segue os acordes Rém, Si♭, Solm, Lá.
MELODIA = [
    # Rém (compassos 9–10)
    (69, 32), (74, 33), (77, 34), (76, 35), (74, 36), (69, 38),
    # Si♭ (11–12)
    (77, 40), (74, 41), (70, 42), (74, 43), (72, 44),
    # Solm (13–14)
    (74, 48), (70, 49), (67, 50), (70, 51), (69, 52),
    # Lá (15–16): sobe e para no Lá, esperando o loop voltar ao Rém
    (73, 56), (76, 57), (81, 58), (79, 59), (76, 60), (73, 62),
]


def caixinha():
    """Caixinha de música: cada nota é um "pente de metal" batido. Parciais
    quase harmônicas (a 4ª é desafinada de propósito: é o que soa metálico),
    ataque instantâneo e decaimento exponencial.
    A FITA: a frequência de todas as notas oscila junto,
        f(t) = f · (1 + 0.004·sen(2π t / 8) + 0.0015·sen(2π · 5 · t)),
    um "wow" lento (8 s) e um "flutter" rápido (5 Hz), como gravação velha.
    A fase é a soma (integral) da frequência ao longo do tempo."""
    esq, dir_ = np.zeros(N), np.zeros(N)
    fita = 1 + 0.004 * np.sin(2 * np.pi * T / 8.0) + 0.0015 * np.sin(2 * np.pi * 5.0 * T)
    dur = 3.5
    m = int(dur * TAXA)
    t = np.arange(m) / TAXA
    for nota, batida in MELODIA:
        inicio = int(batida * BATIDA * TAXA)
        # Algumas notas saem um pouco altas (dente do pente gasto).
        desafino = 2 ** (rng.choice([0, 0, 0, 14]) / 1200)
        idx = (inicio + np.arange(m)) % N
        f_inst = freq(nota) * desafino * fita[idx]
        fase = 2 * np.pi * np.cumsum(f_inst) / TAXA
        s = (np.sin(fase) * np.exp(-t / 1.1)
             + 0.35 * np.sin(2 * fase) * np.exp(-t / 0.5)
             + 0.12 * np.sin(3 * fase) * np.exp(-t / 0.3)
             + 0.10 * np.sin(4.2 * fase) * np.exp(-t / 0.15))
        s *= np.minimum(t / 0.003, 1.0) * 0.30
        somar_circular(esq, inicio, s * 0.62)
        somar_circular(dir_, inicio, s * 0.45)
    return passa_baixa(esq, 5000), passa_baixa(dir_, 5000)


def relogio():
    """Tique-taque do relógio da parede do menu: um estalo curto de ruído
    por batida, alternando dois tons (tique mais agudo, taque mais grave).
    Baixinho e mais para a direita (o relógio fica à direita na tela)."""
    s = np.zeros(N)
    m = int(0.03 * TAXA)
    t = np.arange(m) / TAXA
    for b in range(int(DURACAO / BATIDA)):
        estalo = rng.standard_normal(m) * np.exp(-t / 0.004)
        tom = 3200 if b % 2 == 0 else 2300
        estalo += np.sin(2 * np.pi * tom * t) * np.exp(-t / 0.006) * 0.6
        somar_circular(s, int(b * BATIDA * TAXA), estalo * 0.06)
    s = passa_alta(s, 800)
    return s * 0.45, s * 0.8


def chiado():
    """Chiado de fita: ruído branco filtrado, bem baixo (é ruído: a emenda
    do loop não se ouve)."""
    e = passa_baixa(passa_alta(rng.standard_normal(N), 300), 6000) * 0.006
    d = passa_baixa(passa_alta(rng.standard_normal(N), 300), 6000) * 0.006
    return e, d


def main():
    print("Compondo a trilha do menu (64 s)...")
    pe, pd = pad()
    de, dd = drone()
    ce, cd = caixinha()
    re_, rd = relogio()
    he, hd = chiado()
    # Eco: muito no pad e na caixinha (sala vazia e grande), pouco no relógio.
    esq = (pe + 0.9 * eco(pe, 5.0, 2500, 1) + de + ce * 0.8 + 1.2 * eco(ce, 4.0, 4000, 2)
           + re_ + 0.3 * eco(re_, 1.5, 3000, 3) + he)
    dir_ = (pd + 0.9 * eco(pd, 5.0, 2500, 4) + dd + cd * 0.8 + 1.2 * eco(cd, 4.0, 4000, 5)
            + rd + 0.3 * eco(rd, 1.5, 3000, 6) + hd)
    estereo = np.stack([esq, dir_], axis=1)
    # Sem graves inaudíveis (abaixo de 30 Hz só gastam volume).
    estereo = np.stack([passa_alta(estereo[:, 0], 30), passa_alta(estereo[:, 1], 30)], axis=1)
    # Normaliza: o pico fica em -1 dB (0,89 do máximo).
    estereo *= 0.89 / np.max(np.abs(estereo))

    wav = SAIDA[:-4] + ".wav"
    with wave.open(wav, "wb") as arq:
        arq.setnchannels(2)
        arq.setsampwidth(2)
        arq.setframerate(TAXA)
        arq.writeframes((estereo * 32767).astype("<i2").tobytes())
    # WAV -> OGG Vorbis (qualidade 5 ≈ 160 kbps): bem menor, mesma coisa de ouvido.
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-c:a", "libvorbis",
                    "-q:a", "5", SAIDA], check=True)
    os.remove(wav)
    print("  salvo:", os.path.relpath(SAIDA, PASTA_PROJETO))


if __name__ == "__main__":
    main()

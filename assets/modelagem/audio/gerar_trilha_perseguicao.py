# gerar_trilha_perseguicao.py — compõe por código a trilha sonora de
# PERSEGUIÇÃO do jogo Ankhor. Nenhum instrumento gravado ou sample de fora:
# síntese analógica pura (Fourier, modulação em frequência, filtros por FFT,
# eco circular e saturação não-linear).
#
# Como rodar (Python 3 + numpy; ffmpeg para gerar o .ogg):
#   python assets/modelagem/audio/gerar_trilha_perseguicao.py
#
# O que sai:
#   assets/audio/musica/perseguicao/perseguicao_trilha.ogg   32,0 s em loop sem emenda
#
# ---------------------------------------------------------------------------
# A MÚSICA
# ---------------------------------------------------------------------------
#
# Clima: Pânico mecânico no escuro. O farol vermelho de um robô travou no
# Gabriel. A exploração quieta da biblioteca e das ruínas dá lugar a uma
# fuga desesperada: batimentos cardíacos no limite, passos apressados no
# concreto, esteiras metálicas e engrenagens acelerando atrás dele.
#
#   120 batidas por minuto, 4/4.
#   1 batida = 0,5 s · 1 compasso = 2,0 s · 16 compassos = 32,0 s.
#
# Tonalidade: Ré FRÍGIO (Ré, Mi♭, Fá, Sol, Lá, Si♭, Dó).
#   O semitom Ré–Mi♭ é o intervalo que define o terror no Ankhor.
#
# Harmonia (4 blocos de 4 compassos):
#   1. Compassos 1–4:   Ré m(add9)   — arrancada, o alarme inicial
#   2. Compassos 5–8:   Mi♭ / Ré     — o robô aproxima; o semitom que raspa
#   3. Compassos 9–12:  Si♭ m        — desespero no labirinto de estantes
#   4. Compassos 13–16: Lá 7(♭9)     — clímax da perseguição; resolve no Ré
#
# Camadas:
#   1. PULSO SUB       taiko / bumbo industrial pesado com pitch drop e distorção
#   2. BAIXO OSTINATO  linha rápida em semicolcheias com dente-de-serra saturado
#   3. PERCUSSÃO METAL bigorna e chapas de aço nas batidas 2 e 4 com eco
#   4. MÁQUINAS/CHIMBAL semicolcheias de ruído filtrado (esteiras e engrenagens)
#   5. SIRENE ALARME   senos deslizando e saturando com o farol do robô
#   6. TOM DE SHEPARD  subida infinita contínua (urgência psicológica constante)
#   7. STABS DISSONANTES acordes cortantes de sintetizador com eco no salão
#   8. DRONE SUB       subgrave em Ré com batimento lento que vibra a sala
#
# ---------------------------------------------------------------------------
# A MATEMÁTICA DO LOOP SEM EMENDA
# ---------------------------------------------------------------------------
#
# 1. Todos os tons contínuos (drone, Shepard) têm frequências travadas em
#    múltiplos exatos de 1 / DURACAO (1/32 Hz).
# 2. Eventos pontuais (bumbo, metal, stabs) são somados com índice modular
#    (% N), garantindo que caudas de eco transbordem para o início.
# 3. Filtros Butterworth e reverberações são convoluções no domínio da
#    frequência (FFT / rfft), nativamente circulares.
# 4. Emenda do loop: erro de amplitude na junção inferior a 0,001.

import os
import subprocess
import wave
import numpy as np

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
PASTA_SAIDA = os.path.join(PASTA_PROJETO, "assets", "audio", "musica", "perseguicao")
ARQUIVO_SAIDA = os.path.join(PASTA_SAIDA, "perseguicao_trilha.ogg")

TAXA = 44100
BPM = 120
BATIDA = 60.0 / BPM            # 0,5 s
COMPASSO = 4 * BATIDA          # 2,0 s
COMPASSOS = 16
DURACAO = COMPASSOS * COMPASSO  # 32,0 s
N = int(round(DURACAO * TAXA))
T = np.arange(N) / TAXA

rng = np.random.default_rng(2026)

# Harmonia por bloco de 4 compassos: (nota do baixo MIDI, vozes do acorde)
BLOCOS = [
    (38, [50, 53, 57, 63]),        # Ré m(add9):  Ré Fá Lá Mi♭
    (38, [51, 55, 58, 62]),        # Mi♭ / Ré:    Mi♭ Sol Si♭ Ré (baixo Ré)
    (34, [46, 49, 53, 58]),        # Si♭ m:       Si♭ Ré♭ Fá Si♭
    (33, [45, 49, 55, 58]),        # Lá 7(♭9):    Lá Dó♯ Sol Si♭
]


def freq(midi: float) -> float:
    return 440.0 * 2.0 ** ((midi - 69) / 12.0)


def f_loop(f: float) -> float:
    """Ajusta a frequência para dar um número inteiro de ciclos em DURACAO."""
    return max(1.0, round(f * DURACAO)) / DURACAO


def passa_baixa(x: np.ndarray, corte: float, ordem: int = 2) -> np.ndarray:
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1.0 / TAXA)
    X *= 1.0 / np.sqrt(1.0 + (f / corte) ** (2 * ordem))
    return np.fft.irfft(X, len(x))


def passa_alta(x: np.ndarray, corte: float, ordem: int = 2) -> np.ndarray:
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1.0 / TAXA)
    X *= 1.0 / np.sqrt(1.0 + (corte / np.maximum(f, 1e-6)) ** (2 * ordem))
    return np.fft.irfft(X, len(x))


def passa_banda(x: np.ndarray, f_min: float, f_max: float) -> np.ndarray:
    return passa_baixa(passa_alta(x, f_min, 2), f_max, 2)


def eco_circular(x: np.ndarray, segundos: float = 2.5, brilho: float = 3200.0, semente: int = 0) -> np.ndarray:
    """Reverberação espacial de corredor de concreto por FFT circular."""
    r = np.random.default_rng(semente)
    m = int(segundos * TAXA)
    t = np.arange(m) / TAXA
    ir = r.standard_normal(m) * np.exp(-6.5 * t / segundos)
    ir = passa_baixa(np.pad(ir, (0, N - m)), brilho)
    ir /= np.sqrt(np.sum(ir ** 2))
    return np.fft.irfft(np.fft.rfft(x) * np.fft.rfft(ir), N)


def somar_circular(destino: np.ndarray, inicio: int, sinal: np.ndarray) -> None:
    idx = (inicio + np.arange(len(sinal))) % N
    np.add.at(destino, idx, sinal)


def amostra(batida: float) -> int:
    return int(round(batida * BATIDA * TAXA))


def serra(fase: np.ndarray, harmonicos: int = 14) -> np.ndarray:
    return sum(np.sin(k * fase) / k for k in range(1, harmonicos + 1))


def bloco_do_compasso(compasso: int) -> tuple:
    return BLOCOS[(compasso // 4) % len(BLOCOS)]


# ---------------------------------------------------------------------------
# Instrumentos
# ---------------------------------------------------------------------------

def pulso_sub() -> np.ndarray:
    """Bumbo/taiko industrial: pitch drop de 120 Hz para 38 Hz com saturação.
    Marca o ritmo frenético da perseguição em semicolcheias sincopadas."""
    s = np.zeros(N)
    m = int(0.55 * TAXA)
    t = np.arange(m) / TAXA
    # Pitch drop agressivo
    f_inst = 38.0 + 82.0 * np.exp(-t / 0.035)
    corpo = np.sin(2 * np.pi * np.cumsum(f_inst) / TAXA) * np.exp(-t / 0.18)
    # Clique mecânico transiente
    clique = passa_alta(rng.standard_normal(m), 2200) * np.exp(-t / 0.005) * 0.4
    golpe = np.tanh(2.2 * (corpo + clique)) * np.minimum(t / 0.002, 1.0)

    # Padrão sincopado de perseguição (semicolcheias 0, 3, 6, 8, 11, 14 em cada compasso)
    padrao = [(0, 1.0), (3, 0.75), (6, 0.8), (8, 0.95), (11, 0.7), (14, 0.85)]
    for comp in range(COMPASSOS):
        for semi, forca in padrao:
            inicio = amostra(comp * 4 + semi / 4.0)
            somar_circular(s, inicio, golpe * 0.35 * forca)

    return s + 0.25 * eco_circular(s, 1.2, 1600, 101)


def baixo_ostinato() -> tuple[np.ndarray, np.ndarray]:
    """Linha de baixo analógica em semicolcheias contínuas.
    Dente-de-serra saturado com envelope rápido de filtro passa-baixa."""
    s = np.zeros(N)
    dur = BATIDA / 4.0  # semicolcheia = 0,125 s
    m = int(dur * TAXA)
    t = np.arange(m) / TAXA

    # Sequência de semitons em relação à raiz do bloco (16 semicolcheias por compasso)
    # Ré -> Ré -> Mi♭ -> Ré -> Fá -> Mi♭ -> Ré -> Dó -> Ré -> Ré -> Mi♭ -> Ré -> Si♭ -> Lá -> Mi♭ -> Ré
    notas_padrao = [0, 0, 1, 0, 3, 1, 0, -2, 0, 0, 1, 0, -4, -5, 1, 0]

    for comp in range(COMPASSOS):
        raiz, _ = bloco_do_compasso(comp)
        for i, delta in enumerate(notas_padrao):
            f = freq(raiz + delta)
            onda = serra(2 * np.pi * f * t, 14)
            # Envelope de filtro: abre no ataque e fecha rápido
            brilho = passa_baixa(onda, 1100) * np.exp(-t / 0.04) + passa_baixa(onda, 320)
            nota = np.tanh(3.2 * brilho) * np.minimum(t / 0.002, 1.0) * np.minimum((dur - t) / 0.008, 1.0)
            forca = 1.0 if (i % 4 == 0) else (0.8 if (i % 2 == 0) else 0.65)
            somar_circular(s, amostra(comp * 4 + i / 4.0), nota * 0.16 * forca)

    # Leve separação estéreo com micro-delay
    esq = s
    dir_ = np.roll(s, int(0.008 * TAXA)) * 0.95 + s * 0.05
    return esq, dir_


def percussao_metal() -> tuple[np.ndarray, np.ndarray]:
    """Impactos de chapa de aço e bigorna nas batidas 2 e 4 (contratempos fortes).
    Síntese FM inarmônica com eco metálico cavernoso."""
    esq, dir_ = np.zeros(N), np.zeros(N)
    m = int(0.85 * TAXA)
    t = np.arange(m) / TAXA
    f = 295.0
    # Parciais inarmônicas metálicas
    s = sum(amp * np.sin(2 * np.pi * f * mult * t) * np.exp(-t / tau)
            for mult, amp, tau in ((1.0, 1.0, 0.32), (2.76, 0.65, 0.18), (4.32, 0.45, 0.11), (6.18, 0.3, 0.06)))
    s *= np.minimum(t / 0.001, 1.0) * 0.22

    for comp in range(COMPASSOS):
        for batida, lado in ((1, 0.3), (3, 0.7)):
            inicio = amostra(comp * 4 + batida)
            somar_circular(esq, inicio, s * lado)
            somar_circular(dir_, inicio, s * (1 - lado))

    return (esq + 0.45 * eco_circular(esq, 2.2, 3800, 201),
            dir_ + 0.45 * eco_circular(dir_, 2.2, 3800, 202))


def chimbal_maquinas() -> tuple[np.ndarray, np.ndarray]:
    """Esteiras e engrenagens mecânicas: ruído filtrado em semicolcheias rápidas,
    com acentuações alternando de lado."""
    esq, dir_ = np.zeros(N), np.zeros(N)
    m = int(0.07 * TAXA)
    t = np.arange(m) / TAXA
    total_semis = COMPASSOS * 16

    for semi in range(total_semis):
        forca = 1.0 if semi % 4 == 2 else (0.6 if semi % 2 == 0 else 0.4)
        ruido = rng.standard_normal(m) * np.exp(-t / 0.015) * forca * 0.13
        lado = 0.7 if semi % 2 == 0 else 0.3
        inicio = amostra(semi / 4.0)
        somar_circular(esq, inicio, ruido * lado)
        somar_circular(dir_, inicio, ruido * (1 - lado))

    return passa_banda(esq, 5500, 12000), passa_banda(dir_, 5500, 12000)


def alarme_sirene() -> tuple[np.ndarray, np.ndarray]:
    """Sirene do robô em perseguição: sweep de pitch ascendente distorcido
    no compasso 4 de cada bloco (compassos 3, 7, 11 e 15)."""
    esq, dir_ = np.zeros(N), np.zeros(N)
    m = int(1.6 * TAXA)
    t = np.arange(m) / TAXA
    # Curva exponencial de 520 Hz até 1350 Hz
    curva = 520.0 * 2.0 ** (1.38 * t / 1.6)

    for desafino, lado in ((1.0, 0.75), (1.018, 0.25)):
        fase = 2 * np.pi * np.cumsum(curva * desafino) / TAXA
        s = np.tanh(3.5 * np.sin(fase)) * np.sin(np.pi * t / 1.6) ** 2 * 0.09
        for bloco in range(COMPASSOS // 4):
            # Toca no 4º compasso do bloco, batida 2
            inicio = amostra((bloco * 4 + 3) * 4 + 1.0)
            somar_circular(esq, inicio, s * lado)
            somar_circular(dir_, inicio, s * (1 - lado))

    return passa_baixa(esq, 4500), passa_baixa(dir_, 4500)


def shepard_ascendente() -> np.ndarray:
    """Tom de Shepard ascendente infinito: 8 senos subindo continuamente 1 oitava
    a cada 32 segundos. Gera ilusão acústica de aceleração ininterrupta."""
    f0 = 48.0
    saida = np.zeros(N)
    for k in range(8):
        pos = k + T / DURACAO
        amp = np.exp(-((pos - 3.5) ** 2) / (2 * 1.15 ** 2))
        fase = f0 * 2.0 ** k * DURACAO / np.log(2.0) * 2.0 ** (T / DURACAO)
        saida += amp * np.sin(2 * np.pi * fase)
    return passa_banda(saida * 0.045, 120, 3200)


def stabs_dissonantes() -> tuple[np.ndarray, np.ndarray]:
    """Acordes cortantes de sintetizador analógico nos tempos 1 e no contratempo
    do 2 de cada compasso. Dissonâncias agudas com reverberação de salão."""
    esq, dir_ = np.zeros(N), np.zeros(N)
    m = int(0.5 * TAXA)
    t = np.arange(m) / TAXA
    env = np.minimum(t / 0.008, 1.0) * np.exp(-t / 0.16)

    for comp in range(COMPASSOS):
        _, vozes = bloco_do_compasso(comp)
        for batida, forca in ((0, 1.0), (1.5, 0.75)):
            acorde_e, acorde_d = np.zeros(m), np.zeros(m)
            for nota in vozes:
                for desafino, lado in ((-8, 0.75), (8, 0.25)):
                    f = freq(nota) * 2 ** (desafino / 1200.0)
                    onda = serra(2 * np.pi * f * t + rng.uniform(0, 6.28), 8)
                    acorde_e += onda * lado
                    acorde_d += onda * (1 - lado)
            for canal, dest in ((acorde_e, esq), (acorde_d, dir_)):
                inicio = amostra(comp * 4 + batida)
                filtrado = passa_baixa(canal, 1600) * env * 0.065 * forca
                somar_circular(dest, inicio, filtrado)

    return (esq + 0.4 * eco_circular(esq, 2.5, 2800, 301),
            dir_ + 0.4 * eco_circular(dir_, 2.5, 2800, 302))


def drone_sub() -> tuple[np.ndarray, np.ndarray]:
    """Drone grave constante em Ré (36,7 Hz) com leve batimento de 0,25 Hz.
    Vibra o subwoofer/fones de ouvido mantendo a tensão de fundo."""
    esq, dir_ = np.zeros(N), np.zeros(N)
    for nota, amp in ((26, 1.0), (38, 0.5)):
        for desafino, lado in ((-0.125, 0.65), (0.125, 0.35)):
            f = f_loop(freq(nota) + desafino)
            s = np.sin(2 * np.pi * f * T) * amp * 0.07
            esq += s * lado
            dir_ += s * (1 - lado)
    return passa_baixa(esq, 150), passa_baixa(dir_, 150)


# ---------------------------------------------------------------------------
# Gravação e Masterização
# ---------------------------------------------------------------------------

def gravar(estereo: np.ndarray, caminho_ogg: str) -> None:
    caminho_wav = caminho_ogg[:-4] + ".wav"
    with wave.open(caminho_wav, "wb") as arq:
        arq.setnchannels(2)
        arq.setsampwidth(2)
        arq.setframerate(TAXA)
        dados = (np.clip(estereo, -1.0, 1.0) * 32767).astype("<i2").tobytes()
        arq.writeframes(dados)

    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", caminho_wav,
        "-c:a", "libvorbis", "-q:a", "5",
        caminho_ogg
    ], check=True)

    if os.path.exists(caminho_wav):
        os.remove(caminho_wav)

    salto = np.max(np.abs(estereo[0] - estereo[-1]))
    tamanho = os.path.getsize(caminho_ogg) / 1024
    print(f"  Salvo: {os.path.relpath(caminho_ogg, PASTA_PROJETO)}")
    print(f"  Tamanho: {tamanho:.1f} KB | Emenda do loop: {salto:.5f}")


def main() -> None:
    print(f"Compondo a trilha de perseguição do Ankhor ({DURACAO:.1f} s, {BPM} BPM, Ré frígio)...")

    # Sintetizando camadas
    print("  - Pulso sub (kick/taiko industrial)...")
    sub = pulso_sub()

    print("  - Baixo ostinato (acid synth saturado)...")
    bx_e, bx_d = baixo_ostinato()

    print("  - Percussão metálica (bigorna e chapas FM)...")
    met_e, met_d = percussao_metal()

    print("  - Máquinas e chimbal (esteiras rápidas)...")
    chi_e, chi_d = chimbal_maquinas()

    print("  - Sirene de alarme (sweep de sensores dos robôs)...")
    sir_e, sir_d = alarme_sirene()

    print("  - Tom de Shepard ascendente (escalada contínua)...")
    shep = shepard_ascendente()

    print("  - Stabs dissonantes (sintetizador analógico)...")
    stab_e, stab_d = stabs_dissonantes()

    print("  - Drone subgrave (batimento em Ré)...")
    dr_e, dr_d = drone_sub()

    # Mixagem estéreo
    mix_e = sub + bx_e + met_e + chi_e + sir_e + shep + stab_e + dr_e
    mix_d = sub + bx_d + met_d + chi_d + sir_d + shep + stab_d + dr_d

    # Filtro de corte de subgraves inaudíveis (< 25 Hz)
    mix_e = passa_alta(mix_e, 25)
    mix_d = passa_alta(mix_d, 25)

    # Masterização: pico controlado em -1,2 dBFS (~0,87)
    estereo = np.stack([mix_e, mix_d], axis=1)
    pico = np.max(np.abs(estereo))
    if pico > 0:
        estereo = estereo * (0.87 / pico)

    os.makedirs(PASTA_SAIDA, exist_ok=True)
    gravar(estereo, ARQUIVO_SAIDA)
    print("Pronto! Trilha de perseguição gerada com sucesso.")


if __name__ == "__main__":
    main()

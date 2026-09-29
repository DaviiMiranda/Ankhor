# gerar_trilha_labirinto.py — compõe por código a trilha do LABIRINTO, em
# duas camadas que tocam juntas e sincronizadas:
#
#   assets/audio/musica/perseguicao/labirinto_tensao.ogg       38,4 s em loop
#   assets/audio/musica/perseguicao/labirinto_perseguicao.ogg  38,4 s em loop
#
# Como rodar (Python 3 + numpy; ffmpeg para gerar o .ogg):
#   python assets/modelagem/audio/gerar_trilha_labirinto.py
#
# ---------------------------------------------------------------------------
# A IDEIA: MÚSICA ADAPTATIVA EM CAMADAS
# ---------------------------------------------------------------------------
#
# No labirinto, o Gabriel passa a maior parte do tempo se escondendo e, de
# repente, está correndo. Trocar de música quando o robô aparece daria um
# corte seco. Por isso a trilha é feita de duas camadas com o MESMO
# andamento, a MESMA duração e a MESMA harmonia:
#
#   TENSÃO       toca sempre. Drone grave, coração, metal arrastado e o
#                barulho distante das máquinas. É o "tem algo aqui".
#   PERSEGUIÇÃO  começa junto, mas em silêncio. Quando um robô vê o
#                Gabriel, o volume dela sobe em ~1 s (cenas/sistemas/
#                musica_labirinto.tscn); quando os robôs desistem, desce.
#                Tambores, baixo martelando, golpes de metal, um tom que
#                sobe sem parar e o alarme dos robôs.
#
# Como as duas começam no mesmo instante e têm o mesmo tamanho, o tambor
# da perseguição sempre cai em cima do coração da tensão: a música "acorda"
# em vez de trocar.
#
# ---------------------------------------------------------------------------
# A MÚSICA
# ---------------------------------------------------------------------------
#
#   100 batidas por minuto, 4/4. 1 compasso = 2,4 s. 16 compassos = 38,4 s.
#   Tonalidade: Ré FRÍGIO (Ré menor com o Mi abaixado para Mi♭). O intervalo
#   Ré–Mi♭ (meio tom) é o som clássico de "tubarão chegando": duas notas
#   coladas, que o ouvido não consegue separar direito.
#
#   Harmonia (4 compassos cada):
#       Ré m(add9)  |  Mi♭/Ré  |  Si♭ m  |  Lá 7(♭9)
#   O Mi♭ sobre o baixo Ré raspa; o Lá com ♭9 empurra de volta para o Ré.
#
# ---------------------------------------------------------------------------
# A MATEMÁTICA DO LOOP SEM EMENDA
# ---------------------------------------------------------------------------
#
# 1. Tons contínuos (drone, Shepard) têm frequência ajustada para dar um
#    número INTEIRO de ciclos nos 38,4 s: f' = round(f · D) / D. Assim a
#    última amostra encaixa na primeira.
# 2. Eventos (tambor, metal) são somados "em círculo": o que passa do fim
#    volta para o começo (somar_circular).
# 3. Reverberação e filtros pela FFT, que já é circular.
# 4. TOM DE SHEPARD SUBINDO: pilha de senos separados por oitavas, todos
#    subindo juntos 1 oitava em 38,4 s, com volume gaussiano na altura.
#    f_k(t) = f0 · 2^(k + t/D). A fase é a integral da frequência:
#       fase_k(t) = f0 · 2^k · D / ln 2 · 2^(t/D)
#    Em t = D, o seno k está exatamente onde o seno k+1 estava em t = 0.
#    O ouvido escuta uma subida infinita: urgência sem fim. É o espelho do
#    tom de Shepard que DESCE na trilha da Biblioteca.
# 5. Tremolos usam frequências presas à batida (ex.: semicolcheias =
#    100/60 · 4 Hz), que também dão um número inteiro de ciclos no loop.

import os
import subprocess
import wave

import numpy as np

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
PASTA_SAIDA = os.path.join(PASTA_PROJETO, "assets", "audio", "musica", "perseguicao")

TAXA = 44100
BPM = 100
BATIDA = 60.0 / BPM            # 0,6 s
COMPASSO = 4 * BATIDA          # 2,4 s
COMPASSOS = 16
DURACAO = COMPASSOS * COMPASSO  # 38,4 s
N = int(round(DURACAO * TAXA))
T = np.arange(N) / TAXA
rng = np.random.default_rng(3026)

# Por bloco de 4 compassos: nota do baixo e as vozes do acorde (MIDI).
BLOCOS = [
    (38, [50, 53, 57, 64]),        # Ré m(add9):  Ré Fá Lá Mi
    (38, [51, 55, 58, 62]),        # Mi♭/Ré:      Mi♭ Sol Si♭ Ré (com Ré no baixo)
    (34, [46, 49, 53, 60]),        # Si♭ m:       Si♭ Ré♭ Fá Dó
    (33, [45, 49, 55, 58]),        # Lá 7(♭9):    Lá Dó♯ Sol Si♭
]


# ---------------------------------------------------------------------------
# Ferramentas
# ---------------------------------------------------------------------------

def freq(midi):
    return 440.0 * 2.0 ** ((midi - 69) / 12.0)


def f_loop(f):
    """Frequência mais próxima que dá um número inteiro de ciclos no loop."""
    return max(1.0, round(f * DURACAO)) / DURACAO


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


def eco(x, segundos=3.0, brilho=3000.0, semente=0):
    """Reverberação: convolução circular com ruído que decai (um corredor
    de concreto comprido: cauda longa e escura)."""
    r = np.random.default_rng(semente)
    m = int(segundos * TAXA)
    t = np.arange(m) / TAXA
    ir = r.standard_normal(m) * np.exp(-6.9 * t / segundos)
    ir = passa_baixa(np.pad(ir, (0, N - m)), brilho)
    ir /= np.sqrt(np.sum(ir ** 2))
    return np.fft.irfft(np.fft.rfft(x) * np.fft.rfft(ir), N)


def somar_circular(destino, inicio, sinal):
    idx = (inicio + np.arange(len(sinal))) % N
    np.add.at(destino, idx, sinal)


def amostra(batida):
    return int(round(batida * BATIDA * TAXA))


def serra(fase, harmonicos=12):
    """Dente-de-serra por série de Fourier: soma de sen(k·fase)/k."""
    return sum(np.sin(k * fase) / k for k in range(1, harmonicos + 1))


def bloco_do_compasso(compasso):
    return BLOCOS[(compasso // 4) % 4]


# ---------------------------------------------------------------------------
# Camada de TENSÃO
# ---------------------------------------------------------------------------

def drone():
    """Ré grave (36,7 Hz e 73 Hz) em dente-de-serra, com dois senos
    levemente desafinados que "batem" (o volume ondula devagar). Um filtro
    abre e fecha ao longo do loop inteiro: o corredor respira."""
    esq, dir_ = np.zeros(N), np.zeros(N)
    for nota, amp in ((26, 1.0), (38, 0.6)):
        for desafino, lado in ((-0.18, 0.75), (0.18, 0.25)):
            f = f_loop(freq(nota) + desafino)
            s = serra(2 * np.pi * f * T, 10) * amp
            esq += s * lado
            dir_ += s * (1 - lado)
    abertura = 0.5 - 0.5 * np.cos(2 * np.pi * T / DURACAO)
    saida = []
    for canal in (esq, dir_):
        escuro = passa_baixa(canal, 140, 3)
        claro = passa_baixa(canal, 520, 3)
        saida.append((escuro * (1 - abertura) + claro * abertura) * 0.05)
    return saida


def coracao():
    """Batimento: 'tum-tum' grave nas batidas 1 e 3. O segundo golpe vem
    uma semicolcheia depois do primeiro e é mais fraco, como um coração."""
    s = np.zeros(N)
    m = int(0.5 * TAXA)
    t = np.arange(m) / TAXA
    f_inst = 52 * (1 + 0.6 * np.exp(-t / 0.03))
    golpe = np.sin(2 * np.pi * np.cumsum(f_inst) / TAXA) * np.exp(-t / 0.12) * np.minimum(t / 0.004, 1)
    for batida in range(0, COMPASSOS * 4, 2):
        somar_circular(s, amostra(batida), golpe * 0.30)
        somar_circular(s, amostra(batida + 0.25), golpe * 0.17)
    return passa_baixa(s, 180)


def metal_arrastado():
    """Uma chapa de metal raspada por um arco: síntese FM com razão
    inarmônica (1,41) e ataque lento. Entra no 3º compasso de cada bloco,
    na nota do acorde, e vai para um lado do estéreo diferente a cada vez."""
    esq, dir_ = np.zeros(N), np.zeros(N)
    m = int(6.0 * TAXA)
    t = np.arange(m) / TAXA
    env = np.minimum(t / 2.0, 1.0) * np.exp(-np.maximum(t - 2.0, 0) / 1.5)
    for i, (_, vozes) in enumerate(BLOCOS):
        f = freq(vozes[1] + 12)
        indice = 1.5 + 1.2 * np.sin(2 * np.pi * 0.7 * t)
        s = np.sin(2 * np.pi * f * t + indice * np.sin(2 * np.pi * f * 1.41 * t)) * env * 0.05
        lado = 0.8 if i % 2 == 0 else 0.2
        inicio = amostra((i * 4 + 2) * 4)
        somar_circular(esq, inicio, s * lado)
        somar_circular(dir_, inicio, s * (1 - lado))
    return eco(esq, 4.0, 2500, 1) + 0.3 * esq, eco(dir_, 4.0, 2500, 2) + 0.3 * dir_


def maquinas():
    """Servomotores ao longe: um zumbido que sobe e desce de altura, como
    um braço mecânico se mexendo em outro corredor. Passa por um filtro
    escuro e muito eco: está longe."""
    s = np.zeros(N)
    for batida, f0, subida in ((6, 700, 1.6), (22, 900, 0.7), (37, 650, 1.9), (54, 820, 1.3)):
        m = int(1.8 * TAXA)
        t = np.arange(m) / TAXA
        curva = f0 * (1 + (subida - 1) * np.sin(np.pi * t / 1.8) ** 2)
        curva *= 1 + 0.01 * np.sin(2 * np.pi * 9 * t)
        fase = 2 * np.pi * np.cumsum(curva) / TAXA
        zumbido = (np.sin(fase) + 0.4 * np.sin(2 * fase)) * np.sin(np.pi * t / 1.8) ** 2
        somar_circular(s, amostra(batida), zumbido * 0.035)
    s = passa_baixa(s, 1800)
    return eco(s, 5.0, 2000, 3), eco(s, 5.0, 2000, 4)


def cordas_agudas():
    """Cluster agudo e dissonante (Ré, Mi♭ e Lá bem no alto) em tremolo de
    semicolcheia, crescendo na segunda metade do loop: a tensão sobe."""
    esq, dir_ = np.zeros(N), np.zeros(N)
    tremolo = 0.6 + 0.4 * np.sin(2 * np.pi * (BPM / 60 * 4) * T)
    crescendo = np.clip((T - DURACAO / 2) / (DURACAO / 2), 0, 1) ** 1.5
    crescendo *= 0.5 + 0.5 * np.cos(np.clip((T - DURACAO + 1.5) / 1.5, 0, 1) * np.pi)
    for nota, lado in ((86, 0.3), (87, 0.7), (81, 0.5)):
        f = f_loop(freq(nota))
        s = serra(2 * np.pi * f * T, 5) * tremolo * crescendo * 0.036
        esq += s * lado
        dir_ += s * (1 - lado)
    return passa_baixa(esq, 5000), passa_baixa(dir_, 5000)


# ---------------------------------------------------------------------------
# Camada de PERSEGUIÇÃO
# ---------------------------------------------------------------------------

# Onde os tambores graves caem no compasso, em semicolcheias (0 a 15), e a
# força de cada golpe. Síncope no 3 e no 11: empurra para a frente.
TAMBOR = [(0, 1.0), (3, 0.7), (6, 0.8), (8, 1.0), (10, 0.6), (11, 0.8), (14, 0.7)]


def tambores():
    """Taiko sintético: seno cuja frequência despenca de 90 para 48 Hz
    (a pele do tambor relaxando), mais um estalo de ruído no ataque."""
    s = np.zeros(N)
    m = int(0.7 * TAXA)
    t = np.arange(m) / TAXA
    f_inst = 48 + 42 * np.exp(-t / 0.04)
    corpo = np.sin(2 * np.pi * np.cumsum(f_inst) / TAXA) * np.exp(-t / 0.22)
    estalo = passa_alta(rng.standard_normal(m), 1500) * np.exp(-t / 0.008) * 0.3
    golpe = (corpo + estalo) * np.minimum(t / 0.002, 1)
    for comp in range(COMPASSOS):
        for semi, forca in TAMBOR:
            somar_circular(s, amostra(comp * 4 + semi / 4), golpe * 0.33 * forca)
    return s + 0.3 * eco(s, 1.5, 1500, 5)


def metal_bate():
    """Bigorna nas batidas 2 e 4: parciais inarmônicas curtas (1; 2,4; 3,9;
    5,2 vezes a fundamental), como uma chapa grossa levando uma pancada."""
    esq, dir_ = np.zeros(N), np.zeros(N)
    m = int(0.9 * TAXA)
    t = np.arange(m) / TAXA
    f = 310.0
    s = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t / tau)
            for r, a, tau in ((1.0, 1.0, 0.35), (2.4, 0.6, 0.2), (3.9, 0.4, 0.12), (5.2, 0.3, 0.07)))
    s *= np.minimum(t / 0.001, 1) * 0.16
    for comp in range(COMPASSOS):
        for batida, lado in ((1, 0.35), (3, 0.65)):
            somar_circular(esq, amostra(comp * 4 + batida), s * lado)
            somar_circular(dir_, amostra(comp * 4 + batida), s * (1 - lado))
    return esq + 0.5 * eco(esq, 2.0, 4000, 6), dir_ + 0.5 * eco(dir_, 2.0, 4000, 7)


def chimbal():
    """Semicolcheias de ruído agudo (de 7 a 12 kHz, bem curtas), fortes nos
    contratempos, alternando de lado: a pressa."""
    esq, dir_ = np.zeros(N), np.zeros(N)
    m = int(0.06 * TAXA)
    t = np.arange(m) / TAXA
    for semi in range(COMPASSOS * 16):
        forca = 1.0 if semi % 4 == 2 else (0.55 if semi % 2 == 0 else 0.35)
        s = rng.standard_normal(m) * np.exp(-t / 0.012) * forca * 0.11
        lado = 0.65 if semi % 2 else 0.35
        somar_circular(esq, amostra(semi / 4), s * lado)
        somar_circular(dir_, amostra(semi / 4), s * (1 - lado))
    return passa_alta(esq, 7000, 3), passa_alta(dir_, 7000, 3)


# O baixo em colcheias: distância (em semitons) da nota do baixo do bloco.
# O "+1" é o Mi♭ sobre o Ré: meio tom acima, o som de tubarão.
OSTINATO = [0, 0, 1, 0, 0, 0, -2, 0]


def baixo():
    """Dente-de-serra grave, colcheia por colcheia, com um filtro que abre
    no ataque e fecha logo (o "uau" de sintetizador) e saturação por tanh
    (arredonda os picos: soa sujo e pesado)."""
    s = np.zeros(N)
    dur = BATIDA / 2
    m = int(dur * TAXA)
    t = np.arange(m) / TAXA
    for comp in range(COMPASSOS):
        raiz, _ = bloco_do_compasso(comp)
        for i, desloc in enumerate(OSTINATO):
            f = freq(raiz + desloc)
            onda = serra(2 * np.pi * f * t, 16)
            brilho = passa_baixa(onda, 900) * np.exp(-t / 0.05) + passa_baixa(onda, 250)
            nota = np.tanh(2.5 * brilho) * np.minimum(t / 0.003, 1) * np.minimum((dur - t) / 0.01, 1)
            somar_circular(s, amostra(comp * 4 + i / 2), nota * 0.10)
    return s


def metais():
    """Golpes de "metais" (saws desafinadas com filtro que fecha rápido) no
    1 e no contratempo do 2 de cada compasso, com as vozes do acorde."""
    esq, dir_ = np.zeros(N), np.zeros(N)
    m = int(0.45 * TAXA)
    t = np.arange(m) / TAXA
    env = np.minimum(t / 0.01, 1) * np.exp(-t / 0.18)
    for comp in range(COMPASSOS):
        _, vozes = bloco_do_compasso(comp)
        for batida, forca in ((0, 1.0), (1.5, 0.7)):
            acorde_e, acorde_d = np.zeros(m), np.zeros(m)
            for nota in vozes:
                for desafino, lado in ((-9, 0.8), (9, 0.2)):
                    f = freq(nota) * 2 ** (desafino / 1200)
                    onda = serra(2 * np.pi * f * t + rng.uniform(0, 6.28), 8)
                    acorde_e += onda * lado
                    acorde_d += onda * (1 - lado)
            for canal, dest in ((acorde_e, esq), (acorde_d, dir_)):
                somar_circular(dest, amostra(comp * 4 + batida), passa_baixa(canal, 1400) * env * 0.066 * forca)
    return esq + 0.4 * eco(esq, 2.5, 3000, 8), dir_ + 0.4 * eco(dir_, 2.5, 3000, 9)


def shepard_subindo():
    """Tom de Shepard SUBINDO (veja o topo): 8 senos, 1 oitava por loop."""
    f0 = 55.0
    saida = np.zeros(N)
    for k in range(8):
        pos = k + T / DURACAO
        amp = np.exp(-((pos - 3.5) ** 2) / (2 * 1.1 ** 2))
        fase = f0 * 2.0 ** k * DURACAO / np.log(2) * 2.0 ** (T / DURACAO)
        saida += amp * np.sin(2 * np.pi * fase)
    return passa_baixa(saida * 0.03, 3000)


def alarme():
    """O alarme dos robôs: dois senos desafinados deslizando para cima, com
    saturação, na última batida de cada bloco de 4 compassos (logo antes da
    harmonia mudar)."""
    esq, dir_ = np.zeros(N), np.zeros(N)
    m = int(0.9 * TAXA)
    t = np.arange(m) / TAXA
    curva = 600 * 2 ** (1.2 * t / 0.9)
    for desafino, lado in ((1.0, 0.7), (1.013, 0.3)):
        fase = 2 * np.pi * np.cumsum(curva * desafino) / TAXA
        s = np.tanh(3 * np.sin(fase)) * np.sin(np.pi * t / 0.9) ** 2 * 0.075
        for bloco in range(COMPASSOS // 4):
            inicio = amostra(bloco * 16 + 15)
            somar_circular(esq, inicio, s * lado)
            somar_circular(dir_, inicio, s * (1 - lado))
    return passa_baixa(esq, 4000), passa_baixa(dir_, 4000)


# ---------------------------------------------------------------------------

def gravar(estereo, nome):
    caminho = os.path.join(PASTA_SAIDA, nome)
    wav = caminho[:-4] + ".wav"
    with wave.open(wav, "wb") as arq:
        arq.setnchannels(2)
        arq.setsampwidth(2)
        arq.setframerate(TAXA)
        arq.writeframes((np.clip(estereo, -1, 1) * 32767).astype("<i2").tobytes())
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-c:a", "libvorbis",
                    "-q:a", "5", caminho], check=True)
    os.remove(wav)
    salto = np.max(np.abs(estereo[0] - estereo[-1]))
    print(f"  salvo: {os.path.relpath(caminho, PASTA_PROJETO)} (emenda do loop: {salto:.4f})")


def main():
    print(f"Compondo a trilha do labirinto ({DURACAO:.1f} s, {BPM} BPM, Ré frígio)...")
    dr = drone()
    co = coracao()
    me = metal_arrastado()
    ma = maquinas()
    cg = cordas_agudas()
    tensao = [dr[i] + co + me[i] + ma[i] + cg[i] for i in range(2)]

    ta = tambores()
    mb = metal_bate()
    ch = chimbal()
    ba = baixo()
    mt = metais()
    sh = shepard_subindo()
    al = alarme()
    perseguicao = [ta + mb[i] + ch[i] + ba + mt[i] + sh + al[i] for i in range(2)]

    tensao = np.stack([passa_alta(c, 25) for c in tensao], axis=1)
    perseguicao = np.stack([passa_alta(c, 25) for c in perseguicao], axis=1)
    # Um ganho só para as duas camadas, calculado com as duas somadas (é
    # assim que elas tocam na perseguição): pico em -1,5 dB.
    ganho = 0.84 / np.max(np.abs(tensao + perseguicao))
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    gravar(tensao * ganho, "labirinto_tensao.ogg")
    gravar(perseguicao * ganho, "labirinto_perseguicao.ogg")


if __name__ == "__main__":
    main()

# gerar_efeitos_gabriel.py — compõe por código os efeitos sonoros do Gabriel:
# os passos e os sons de abrir e fechar o inventário (a mochila).
#
# Como rodar (Python 3 + numpy):
#   python assets/modelagem/audio/gerar_efeitos_gabriel.py
#
# Gera (efeitos curtos são .wav: tocam sem atraso, ver assets/audio/README.md):
#   assets/audio/efeitos/gabriel/gabriel_passo_ceramica_01.wav ... _06.wav
#   assets/audio/efeitos/interface/inventario_abrir.wav
#   assets/audio/efeitos/interface/inventario_fechar.wav
#
# Nenhuma gravação: todo som aqui é soma de ondas e de RUÍDO (números
# sorteados) passando por filtros. É a mesma ideia dos scripts das trilhas
# (gerar_trilha_menu.py), só que em sons de menos de um segundo.
#
# A matemática usada:
#
# 1. Envelope exponencial. Quase todo som de impacto começa forte e morre
#    rápido. A curva e^(-t/τ) faz isso: em t = τ o som já caiu para 37%, em
#    t = 3τ para 5%. Um τ pequeno (5 ms) dá um estalo; um τ maior (40 ms), um
#    baque.
#
# 2. Filtros pela FFT. A Transformada Rápida de Fourier (FFT) separa um som
#    nas frequências que o compõem. Multiplicando cada frequência por um
#    peso e voltando (FFT inversa), escolhemos o que passa:
#      passa-baixa  → só os graves (baque abafado)
#      passa-alta   → só os agudos (areia, chiado)
#      passa-faixa  → uma faixa do meio (a borracha do tênis no piso)
#    O ruído branco tem todas as frequências com a mesma força; filtrado,
#    vira "cor": ruído grave parece pancada, ruído agudo parece areia.
#
# 3. Variação aleatória. Seis passos iguais soam como uma máquina. Cada
#    variação sorteia pequenas diferenças (força, duração, grãos de areia),
#    e o Godot ainda sorteia qual das seis toca e muda um pouco a altura
#    (AudioStreamRandomizer, na cena cenas/sistemas/passos.tscn).

import os
import wave

import numpy as np

PASTA_PROJETO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
PASTA_GABRIEL = os.path.join(PASTA_PROJETO, "assets", "audio", "efeitos", "gabriel")
PASTA_INTERFACE = os.path.join(PASTA_PROJETO, "assets", "audio", "efeitos", "interface")

TAXA = 44100                 # amostras por segundo
VARIACOES_PASSO = 6
rng = np.random.default_rng(26)   # sorteios fixos: rodar de novo dá o mesmo som


# ---------------------------------------------------------------------------
# Ferramentas
# ---------------------------------------------------------------------------

def tempo(segundos):
    """Os instantes de cada amostra de um som com essa duração."""
    return np.arange(int(segundos * TAXA)) / TAXA


def envelope(t, inicio, tau, ataque=0.002):
    """Sobe em 'ataque' segundos a partir de 'inicio' e cai como e^(-t/tau).
    O ataque curto (e não instantâneo) evita um clique digital no começo."""
    d = t - inicio
    sobe = np.clip(d / ataque, 0.0, 1.0)
    return np.where(d >= 0, sobe * np.exp(-np.maximum(d, 0) / tau), 0.0)


def filtrar(x, corte_baixo=None, corte_alto=None, ordem=2):
    """Filtro pela FFT: guarda as frequências entre corte_baixo e corte_alto.
    A curva 1 / (1 + (f/corte)^(2·ordem)) é a do filtro Butterworth: deixa
    passar abaixo do corte e vai cortando cada vez mais acima dele."""
    espectro = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1.0 / TAXA)
    f[0] = 1e-9   # evita divisão por zero na frequência 0
    ganho = np.ones_like(f)
    if corte_alto:
        ganho *= 1.0 / np.sqrt(1.0 + (f / corte_alto) ** (2 * ordem))
    if corte_baixo:
        ganho *= 1.0 / np.sqrt(1.0 + (corte_baixo / f) ** (2 * ordem))
    return np.fft.irfft(espectro * ganho, len(x))


def ruido(n):
    return rng.standard_normal(n)


def sala(x, segundos=0.35, brilho=2500.0, mistura=0.12):
    """Um pouco da reverberação da Biblioteca (salão grande e vazio): soma
    ao som uma cópia "espalhada" dele, feita com uma resposta ao impulso de
    ruído que decai. É a mesma técnica do eco das trilhas, bem mais curta."""
    m = int(segundos * TAXA)
    t = np.arange(m) / TAXA
    ir = filtrar(ruido(m), corte_alto=brilho) * np.exp(-6.9 * t / segundos)
    ir /= np.sqrt(np.sum(ir ** 2))
    cauda = np.convolve(x, ir)[: len(x)]
    return x + mistura * cauda


def normalizar(x, pico_db):
    """Ajusta o volume para o ponto mais alto ficar em 'pico_db' (0 dB = o
    máximo que o arquivo aguenta)."""
    return x / np.max(np.abs(x)) * 10 ** (pico_db / 20)


def salvar(caminho, x):
    """Grava em .wav mono, 16 bits. Mono porque o Godot posiciona o som no
    espaço (AudioStreamPlayer2D): esquerda/direita vem de onde o Gabriel está."""
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    x = np.clip(x, -1.0, 1.0)
    with wave.open(caminho, "wb") as arq:
        arq.setnchannels(1)
        arq.setsampwidth(2)
        arq.setframerate(TAXA)
        arq.writeframes((x * 32767).astype("<i2").tobytes())
    print("  salvo:", os.path.relpath(caminho, PASTA_PROJETO))


# ---------------------------------------------------------------------------
# Passo: tênis numa cerâmica antiga, com poeira e areia por cima
# ---------------------------------------------------------------------------

def passo():
    """Um passo tem três partes, uma depois da outra:
      1. calcanhar: baque grave (uma onda de ~100 Hz que morre em 25 ms) com
         um pouco de ruído grave, o peso do corpo chegando no chão;
      2. sola: ~60 ms depois, a ponta do pé encosta; ruído de faixa média
         (a borracha do tênis), mais fraco e mais curto;
      3. areia: grãos esmagados sob o tênis, estalos agudos espalhados
         pelos primeiros 150 ms. É o que diz "ruína" em vez de "prédio limpo"."""
    t = tempo(0.45)
    n = len(t)

    # 1. Calcanhar
    f_baque = rng.uniform(85, 115)
    # A frequência cai um pouco durante o baque (de 1,3·f para f): soa como
    # um corpo pesado, não como um tom de sintetizador.
    fase = 2 * np.pi * np.cumsum(f_baque * (1 + 0.3 * np.exp(-t / 0.01))) / TAXA
    calcanhar = np.sin(fase) * envelope(t, 0.0, rng.uniform(0.020, 0.030))
    calcanhar += 0.5 * filtrar(ruido(n), corte_alto=900) * envelope(t, 0.0, 0.015)

    # 2. Sola
    atraso = rng.uniform(0.050, 0.075)
    sola = filtrar(ruido(n), corte_baixo=400, corte_alto=2200) * envelope(t, atraso, rng.uniform(0.010, 0.018))
    sola *= rng.uniform(0.35, 0.55)

    # 3. Areia: cada grão é um estalo de 1 ms; sorteamos quantos e quando.
    graos = np.zeros(n)
    for _ in range(rng.integers(12, 25)):
        quando = int(rng.uniform(0.0, 0.15) * TAXA)
        graos[quando] += rng.uniform(-1, 1)
    areia = filtrar(np.convolve(graos, np.hanning(40), "same"), corte_baixo=2500, corte_alto=9000)
    # Os grãos são mais fortes no começo, quando o pé chega com mais peso.
    areia *= envelope(t, 0.0, 0.08, ataque=0.001) * rng.uniform(0.15, 0.25) / (np.max(np.abs(areia)) + 1e-9)

    som = calcanhar + sola + areia
    som = sala(som)
    # Pico em -6 dB: o volume final (andar, correr, agachado) é decidido no
    # Godot, pela cena dos passos. Aqui todas as variações ficam iguais.
    return normalizar(som, -6.0)


# ---------------------------------------------------------------------------
# Abrir o inventário: o zíper da mochila e o pano mexendo
# ---------------------------------------------------------------------------

def inventario_abrir():
    """O zíper é uma sequência de "dentes": cada dente que passa pelo cursor
    é um estalo curto. O ritmo dos dentes segue a mão: acelera no começo e
    freia no fim (uma curva em forma de sino, sin(π·u)). Por baixo, o
    tecido da mochila: ruído que sobe e desce devagar."""
    duracao = 0.55
    t = tempo(duracao)
    n = len(t)

    ziper = som_ziper(n, 0.03, 0.33, velocidade_max=140)
    tecido = pano(t, duracao)

    # A aba da mochila caindo aberta no fim: um baque macio e grave.
    aba = filtrar(ruido(n), corte_alto=500) * envelope(t, 0.36, 0.035)
    aba *= 0.8 / (np.max(np.abs(aba)) + 1e-9)

    som = 0.6 * ziper + tecido + aba
    # Pequeno fade-out nos últimos 30 ms, para o fim não cortar seco.
    som *= np.clip((duracao - t) / 0.03, 0, 1)
    return normalizar(sala(som, mistura=0.08), -6.0)


def inventario_fechar():
    """O contrário de abrir, na ordem de quem fecha a mochila com pressa:
    primeiro a aba é empurrada para baixo (baque), depois o zíper corre
    mais RÁPIDO que ao abrir (um puxão decidido) e termina num "tec": o
    cursor batendo no fim do zíper. Mais curto que abrir: o jogo volta logo."""
    duracao = 0.45
    t = tempo(duracao)
    n = len(t)

    # A aba empurrada: baque grave logo no começo.
    aba = filtrar(ruido(n), corte_alto=450) * envelope(t, 0.01, 0.03)
    aba *= 0.7 / (np.max(np.abs(aba)) + 1e-9)

    inicio, fim = 0.08, 0.30
    ziper = som_ziper(n, inicio, fim, velocidade_max=200)
    tecido = pano(t, duracao)

    # O "tec" do fim: um estalo metálico curto (duas frequências que não
    # formam acorde, como metal batendo) logo depois do último dente.
    tec = (np.sin(2 * np.pi * 2900 * t) + 0.6 * np.sin(2 * np.pi * 4700 * t))
    tec *= envelope(t, fim + 0.01, 0.006, ataque=0.0005) * 0.9

    som = aba + 0.6 * ziper + tecido + tec
    som *= np.clip((duracao - t) / 0.03, 0, 1)
    return normalizar(sala(som, mistura=0.08), -6.0)


def som_ziper(n, inicio, fim, velocidade_max):
    """Os dentes do zíper passando pelo cursor, de 'inicio' a 'fim' segundos.
    'u' vai de 0 a 1 ao longo do puxão; a velocidade (dentes por segundo) é
    40 + velocidade_max·sin(π·u): a mão acelera, chega no máximo no meio do
    caminho e freia no fim."""
    dentes = np.zeros(n)
    instante = inicio
    while instante < fim:
        u = (instante - inicio) / (fim - inicio)
        velocidade = 40 + velocidade_max * np.sin(np.pi * u)
        dentes[int(instante * TAXA)] += rng.uniform(0.6, 1.0)
        instante += 1.0 / velocidade * rng.uniform(0.85, 1.15)
    # Cada dente vira um estalo de ~2 ms, com a cor de metal e plástico.
    estalo = np.hanning(90) * np.sin(2 * np.pi * 3200 * np.arange(90) / TAXA)
    ziper = filtrar(np.convolve(dentes, estalo, "same"), corte_baixo=1200, corte_alto=7000)
    return ziper / (np.max(np.abs(ziper)) + 1e-9)


def pano(t, duracao):
    """O tecido da mochila mexendo: ruído de faixa média, com um envelope
    suave que sobe e desce (sin² vai de 0 a 1 e volta a 0)."""
    tecido = filtrar(ruido(len(t)), corte_baixo=300, corte_alto=3000)
    tecido /= np.max(np.abs(tecido))
    forma = np.sin(np.pi * np.clip(t / duracao, 0, 1)) ** 2
    return 0.35 * tecido * forma


def main():
    print("[efeitos do Gabriel]")
    for i in range(1, VARIACOES_PASSO + 1):
        salvar(os.path.join(PASTA_GABRIEL, f"gabriel_passo_ceramica_{i:02d}.wav"), passo())
    salvar(os.path.join(PASTA_INTERFACE, "inventario_abrir.wav"), inventario_abrir())
    salvar(os.path.join(PASTA_INTERFACE, "inventario_fechar.wav"), inventario_fechar())


if __name__ == "__main__":
    main()

# gerar_som_cena_final.py — compõe por código o som da CENA FINAL (a volta dos
# Homo sideralis, no núcleo da Âncora: Enredo, seção 8, "O final").
#
# Como rodar (Python 3 + numpy; ffmpeg para o .ogg):
#   python assets/modelagem/audio/gerar_som_cena_final.py
#
# Gera:
#   assets/audio/efeitos/objetos/final_pulso.wav          2,0 s: o pulso eletromagnético
#                                                         que traz os Homo sideralis
#   assets/audio/efeitos/objetos/final_sideralis_surgir.wav  0,7 s: um deles aparecendo
#   assets/audio/efeitos/objetos/final_queda_carlos.wav   1,4 s: o disparo e a queda do Carlos
#   assets/audio/efeitos/objetos/final_ancora_completa.wav   3,6 s: a Âncora sendo terminada
#   assets/audio/musica/final/final_tema.ogg              48 s, estéreo, em loop sem emenda
#
# As ferramentas (envelope, filtro pela FFT, ruído, normalizar, salvar) vêm do
# gerar_efeitos_gabriel.py, importado como módulo.
#
# AS IDEIAS DE SÍNTESE
#
# 1. Varredura (sweep). Um tom cuja frequência muda com o tempo não é
#    sin(2π · f(t) · t): isso erraria a fase. A fase é a INTEGRAL da frequência,
#    φ(t) = 2π · ∫ f(t) dt, e no computador a integral é a soma acumulada
#    (np.cumsum) dividida pela taxa de amostragem. O pulso e a aparição
#    usam isso.
#
# 2. Gongo. Um sino ou gongo de metal tem parciais que NÃO são múltiplos
#    inteiros da fundamental (1; 1,59; 2,14; 2,3; 2,65; 3,5...), por isso soa
#    "metálico" e não "musical". Cada parcial cai com a sua própria velocidade.
#
# 3. Loop sem emenda do tema. O fim encaixa no começo se cada oscilação der
#    um número INTEIRO de voltas nos 48 s: a função inteira() arredonda cada
#    frequência para k / 48 Hz.
#
# O que é provisório: como os Homo sideralis soam de verdade depende do Enredo,
# seção 10.6. O pulso e o tema só dizem o que já está decidido: algo frio,
# eletromagnético, que cresce.

import importlib.util
import os
import subprocess
import wave

import numpy as np

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
PASTA_OBJETOS = os.path.join(PASTA_PROJETO, "assets", "audio", "efeitos", "objetos")
SAIDA_TEMA = os.path.join(PASTA_PROJETO, "assets", "audio", "musica", "final", "final_tema.ogg")

_spec = importlib.util.spec_from_file_location(
    "gerar_efeitos_gabriel", os.path.join(PASTA_SCRIPT, "gerar_efeitos_gabriel.py"))
ef = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ef)

TAXA = ef.TAXA
tempo, envelope, filtrar, normalizar, salvar = ef.tempo, ef.envelope, ef.filtrar, ef.normalizar, ef.salvar
rng = np.random.default_rng(3026)   # sorteios fixos: rodar de novo dá o mesmo som


def ruido(n):
    return rng.standard_normal(n)


def varredura(f):
    """Tom senoidal cuja frequência instantânea é o vetor f (em Hz)."""
    return np.sin(2 * np.pi * np.cumsum(f) / TAXA)


def estalos(n, quantidade, tau, corte_baixo=1500, corte_alto=9000):
    """Estalos soltos de estática: impulsos em instantes sorteados (mais
    densos no começo, pela distribuição exponencial), filtrados."""
    x = np.zeros(n)
    posicoes = np.minimum((rng.exponential(tau, quantidade) * TAXA).astype(int), n - 1)
    for p in posicoes:
        x[p] += rng.uniform(-1, 1)
    x = filtrar(x, corte_baixo=corte_baixo, corte_alto=corte_alto)
    return x / (np.max(np.abs(x)) + 1e-9)


def gongo(t, inicio, fundamental, tau, ganho=1.0):
    """Gongo de metal: parciais inarmônicas, as mais agudas caindo mais rápido."""
    razoes = [1.0, 1.59, 2.14, 2.30, 2.65, 3.50]
    saida = np.zeros_like(t)
    for k, r in enumerate(razoes):
        saida += (1.0 / (1 + k * 0.6)) * np.sin(2 * np.pi * fundamental * r * t) \
            * envelope(t, inicio, tau / (1 + 0.5 * k), ataque=0.003)
    return ganho * saida


def pulso():
    """O pulso eletromagnético: uma varredura que sobe em 0,2 s (o campo se
    carregando), um estrondo grave no instante do clarão, o zumbido de rede
    elétrica (60 Hz e harmônicos) e a chuva de estalos de estática."""
    t = tempo(2.0)
    n = len(t)
    carga = np.clip(t / 0.2, 0.0, 1.0)
    subida = varredura(150 + 2850 * carga ** 2) * carga ** 2 * (t < 0.2)
    boom = varredura(40 + 55 * np.exp(-t / 0.25)) * envelope(t, 0.2, 0.55, ataque=0.004)
    rede = sum(np.sin(2 * np.pi * 60 * k * t) / k for k in range(1, 6)) * envelope(t, 0.2, 0.9)
    chuva = estalos(n, 90, 0.5) * envelope(t, 0.2, 0.7, ataque=0.005)
    brilho = filtrar(ruido(n), corte_baixo=2500, corte_alto=8000) * envelope(t, 0.2, 0.18, ataque=0.003)
    x = 0.55 * subida + 1.0 * boom + 0.12 * rede + 0.45 * chuva + 0.35 * brilho
    return normalizar(x, -4.0)


def sideralis_surgir():
    """Um Homo sideralis se materializando: um tom que cai de 3200 a 700 Hz
    com tremolo rápido (o brilho), uma lufada de ruído agudo e uma pancada
    grave curta no fim, de quando o corpo "pousa"."""
    t = tempo(0.7)
    n = len(t)
    f = 700 + 2500 * np.exp(-t / 0.12)
    tom = varredura(f) * (0.6 + 0.4 * np.sin(2 * np.pi * 22 * t)) * envelope(t, 0.0, 0.2, ataque=0.01)
    lufada = filtrar(ruido(n), corte_baixo=3000, corte_alto=9000) * envelope(t, 0.0, 0.1, ataque=0.005)
    pouso = varredura(110 - 50 * np.clip((t - 0.2) / 0.3, 0.0, 1.0)) * envelope(t, 0.2, 0.15, ataque=0.005)
    return normalizar(0.6 * tom + 0.4 * lufada + 0.8 * pouso, -6.0)


def queda_carlos():
    """O disparo (um estalo seco de energia, 0,2 s) e a queda: pancada
    abafada do corpo (senoide grave caindo de 90 a 45 Hz mais ruído filtrado
    em 300 Hz), o tecido do jaleco, e uma segunda pancada menor, de quando
    o corpo quica. Sem som de dor, de propósito: a cena não mostra sangue."""
    t = tempo(1.4)
    n = len(t)
    disparo = filtrar(ruido(n), corte_baixo=1200, corte_alto=7000) * envelope(t, 0.0, 0.035, ataque=0.001)
    disparo += 0.5 * varredura(2200 - 1800 * np.clip(t / 0.15, 0.0, 1.0)) * envelope(t, 0.0, 0.07, ataque=0.001)
    pancada1 = varredura(90 - 45 * np.clip((t - 0.45) / 0.2, 0.0, 1.0)) * envelope(t, 0.45, 0.12, ataque=0.003)
    corpo1 = filtrar(ruido(n), corte_alto=300) * envelope(t, 0.45, 0.07, ataque=0.002)
    pano = filtrar(ruido(n), corte_baixo=400, corte_alto=2500) * envelope(t, 0.5, 0.18, ataque=0.05)
    pancada2 = varredura(80 - 35 * np.clip((t - 0.8) / 0.2, 0.0, 1.0)) * envelope(t, 0.8, 0.08, ataque=0.003)
    corpo2 = filtrar(ruido(n), corte_alto=300) * envelope(t, 0.8, 0.05, ataque=0.002)
    x = 0.7 * disparo + 1.0 * (pancada1 + 0.6 * corpo1) + 0.25 * pano + 0.55 * (pancada2 + 0.5 * corpo2)
    return normalizar(x, -5.0)


def ancora_completa():
    """A Âncora sendo terminada: 0,6 s de crescendo (uma pilha de harmônicos
    cuja altura sobe, mais ruído que sobe junto), o estrondo no pico (o
    clarão da cena está em 25% de 2,4 s, ou seja, em 0,6 s), o gongo da
    Âncora (o mesmo do tema do jogo) e uma nuvem fria e longa de três
    notas, que fica depois do estrondo."""
    t = tempo(3.6)
    n = len(t)
    subida = np.clip(t / 0.6, 0.0, 1.0)
    altura = 70 * (1 + 3 * subida ** 2)
    pilha = sum(varredura(altura * k) / k for k in range(1, 7)) * subida ** 2 * (t < 0.6)
    vento = filtrar(ruido(n), corte_baixo=300, corte_alto=4000) * subida ** 3 * (t < 0.6)
    boom = varredura(45 + 40 * np.exp(-(t - 0.6) / 0.3)) * envelope(t, 0.6, 0.9, ataque=0.004)
    metal = gongo(t, 0.6, 130.0, 1.6)
    chuva = estalos(n, 70, 0.7) * envelope(t, 0.6, 1.0, ataque=0.005)
    nuvem = np.zeros(n)
    for freq, detune in ((220.0, 0.4), (277.2, -0.5), (329.6, 0.3)):
        vibrato = 1 + 0.004 * np.sin(2 * np.pi * 5 * t)
        nuvem += np.sin(2 * np.pi * (freq + detune) * t * vibrato) + np.sin(2 * np.pi * (freq - detune) * t)
    nuvem *= envelope(t, 0.6, 1.4, ataque=0.25) * np.clip((3.6 - t) / 0.8, 0.0, 1.0)
    x = 0.6 * pilha + 0.35 * vento + 1.0 * boom + 0.5 * metal + 0.3 * chuva + 0.12 * nuvem
    return normalizar(x, -3.0)


# ---------------------------------------------------------------------------
# O tema: 48 s em loop. Frio, eletromagnético, cresce e volta.
# ---------------------------------------------------------------------------

DURACAO_TEMA = 48.0


def inteira(f):
    """Arredonda a frequência para um número inteiro de voltas em 48 s
    (f = k / 48), para o fim do arquivo encaixar no começo sem estalo."""
    return round(f * DURACAO_TEMA) / DURACAO_TEMA


def tema():
    t = tempo(DURACAO_TEMA)
    n = len(t)
    ciclo = 2 * np.pi * t / DURACAO_TEMA

    raiz = np.sin(2 * np.pi * inteira(36.71) * t) + 0.5 * np.sin(2 * np.pi * inteira(73.42) * t)
    raiz *= 0.55 + 0.25 * np.sin(2 * np.pi * 4 * t / DURACAO_TEMA + 0.5)

    esq = np.zeros(n)
    dir_ = np.zeros(n)
    notas = (146.83, 220.0, 311.13, 440.0)
    for k, freq in enumerate(notas):
        lfo = 0.5 + 0.5 * np.sin(2 * np.pi * (3 + k) * t / DURACAO_TEMA + k * 1.3)
        esq += np.sin(2 * np.pi * inteira(freq + 0.17) * t) * lfo
        dir_ += np.sin(2 * np.pi * inteira(freq - 0.17) * t + 0.7) * (1.0 - 0.5 * lfo)
    esq *= 0.16
    dir_ *= 0.16

    batida = np.zeros(n)
    passo = int(1.2 * TAXA)
    corpo_t = tempo(0.5)
    corpo = varredura(55 - 20 * np.clip(corpo_t / 0.4, 0.0, 1.0)) * np.exp(-corpo_t / 0.14)
    for inicio in range(0, n, passo):
        fim = min(inicio + len(corpo), n)
        batida[inicio:fim] += corpo[: fim - inicio]
    inchaco = 0.35 + 0.65 * (0.5 - 0.5 * np.cos(ciclo))
    batida *= inchaco

    fio_e = np.zeros(n)
    fio_d = np.zeros(n)
    for k in range(4):
        inicio = 12.0 * k + 3.0
        local = np.clip((t - inicio) / 6.0, 0.0, 1.0)
        dentro = (t >= inicio) & (t < inicio + 6.0)
        f = 800 + 1600 * local ** 2
        fio = varredura(f) * np.sin(np.pi * local) ** 2 * dentro * 0.05
        if k % 2 == 0:
            fio_e += fio
        else:
            fio_d += fio

    poeira = estalos(n, 140, DURACAO_TEMA / 3.0, corte_baixo=3000, corte_alto=10000) * 0.03

    esquerda = raiz * 0.5 + esq + 0.9 * batida + fio_e + poeira
    direita = raiz * 0.5 + dir_ + 0.9 * batida + fio_d + poeira
    estereo = np.stack([esquerda, direita], axis=1)
    estereo = estereo / np.max(np.abs(estereo)) * 10 ** (-3.0 / 20)
    return estereo


def salvar_ogg(estereo):
    os.makedirs(os.path.dirname(SAIDA_TEMA), exist_ok=True)
    wav = SAIDA_TEMA[:-4] + ".wav"
    with wave.open(wav, "wb") as arq:
        arq.setnchannels(2)
        arq.setsampwidth(2)
        arq.setframerate(TAXA)
        arq.writeframes((np.clip(estereo, -1.0, 1.0) * 32767).astype("<i2").tobytes())
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-c:a", "libvorbis",
                    "-q:a", "5", SAIDA_TEMA], check=True)
    os.remove(wav)
    print("  salvo:", os.path.relpath(SAIDA_TEMA, PASTA_PROJETO))


def main():
    print("Efeitos da cena final:")
    salvar(os.path.join(PASTA_OBJETOS, "final_pulso.wav"), pulso())
    salvar(os.path.join(PASTA_OBJETOS, "final_sideralis_surgir.wav"), sideralis_surgir())
    salvar(os.path.join(PASTA_OBJETOS, "final_queda_carlos.wav"), queda_carlos())
    salvar(os.path.join(PASTA_OBJETOS, "final_ancora_completa.wav"), ancora_completa())
    print("Tema:")
    estereo = tema()
    salto = np.max(np.abs(estereo[0] - estereo[-1]))
    vizinho = np.max(np.abs(np.diff(estereo, axis=0)))
    print("  emenda do loop: salto %.5f (máximo entre vizinhas: %.5f)" % (salto, vizinho))
    salvar_ogg(estereo)


if __name__ == "__main__":
    main()

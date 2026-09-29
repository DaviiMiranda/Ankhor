# gerar_efeitos_labirinto.py — compõe por código os efeitos sonoros do
# labirinto: os robôs, a vida do Gabriel, o checkpoint e a lanterna.
#
# Como rodar (Python 3 + numpy):
#   python assets/modelagem/audio/gerar_efeitos_labirinto.py
#
# Gera:
#   assets/audio/efeitos/robos/sentinela_passo.wav    pisada pesada de metal
#   assets/audio/efeitos/robos/rastreador_passo.wav   garras correndo no concreto
#   assets/audio/efeitos/robos/robo_zumbido.wav       2 s em loop: o motor ligado
#   assets/audio/efeitos/robos/robo_alerta.wav        o guincho de quando vê o Gabriel
#   assets/audio/efeitos/gabriel/gabriel_dano.wav     a pancada de quando é pego
#   assets/audio/efeitos/interface/morte.wav          a tela de morte
#   assets/audio/efeitos/interface/checkpoint.wav     o posto de emergência acendendo
#   assets/audio/efeitos/objetos/lanterna_clique.wav  o botão da lanterna
#   assets/audio/efeitos/objetos/pilha_troca.wav      a tampa abrindo e a pilha encaixando
#
# As ferramentas (envelope, filtro pela FFT, salvar) vêm do
# gerar_efeitos_gabriel.py; a matemática está explicada lá. Aqui aparecem:
#
# - SÍNTESE INARMÔNICA para metal: senos em razões que não são inteiras
#   (1; 2,76; 5,40...). Corda e voz têm harmônicos inteiros (f, 2f, 3f) e
#   soam "afinadas"; chapa de metal não, e é isso que o ouvido reconhece.
# - DISTORÇÃO por tanh: tanh(g·x) achata os picos da onda. Quanto maior o
#   ganho g, mais a onda vira quadrada e mais harmônicos ásperos aparecem:
#   é o que deixa o guincho do robô agressivo.
# - LOOP SEM EMENDA no zumbido: frequências com número inteiro de ciclos
#   em 2 s e ruído filtrado pela FFT (que é circular), como no chiado do
#   rádio (gerar_efeitos_registros.py).

import importlib.util
import os

import numpy as np

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
PASTA_AUDIO = os.path.join(PASTA_PROJETO, "assets", "audio", "efeitos")

_spec = importlib.util.spec_from_file_location(
    "gerar_efeitos_gabriel", os.path.join(PASTA_SCRIPT, "gerar_efeitos_gabriel.py"))
ef = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ef)

TAXA = ef.TAXA
tempo, envelope, filtrar, normalizar, salvar, sala = ef.tempo, ef.envelope, ef.filtrar, ef.normalizar, ef.salvar, ef.sala
rng = np.random.default_rng(404)


def ruido(n):
    return rng.standard_normal(n)


def metal(t, f, inicio, parciais, forca=1.0):
    """Soma de parciais inarmônicas (razão, amplitude, tempo de queda)."""
    s = sum(a * np.sin(2 * np.pi * f * r * (t - inicio)) * envelope(t, inicio, tau, 0.0008)
            for r, a, tau in parciais)
    return s * forca


def sentinela_passo():
    """Pisada de 2 m de metal: baque grave (o peso) e, logo depois, o
    tilintar das garras e das juntas soltas (metal inarmônico curto)."""
    t = tempo(0.7)
    n = len(t)
    baque = np.sin(2 * np.pi * np.cumsum(55 * (1 + 0.8 * np.exp(-t / 0.03))) / TAXA) * envelope(t, 0, 0.09)
    baque += 0.5 * filtrar(ruido(n), corte_alto=300) * envelope(t, 0, 0.04)
    junta = metal(t, 420, 0.015, ((1.0, 1.0, 0.12), (2.76, 0.6, 0.07), (5.4, 0.35, 0.04)), 0.35)
    garras = metal(t, 1900, 0.03, ((1.0, 1.0, 0.02), (1.51, 0.7, 0.015)), 0.2)
    return normalizar(sala(baque + junta + garras, mistura=0.2), -4.0)


def rastreador_passo():
    """Trote do cão de metal: quatro garras batendo quase juntas (como
    pingos de chuva em lata), rápidas e secas."""
    t = tempo(0.25)
    n = len(t)
    s = np.zeros(n)
    for inicio, f in ((0.0, 2400), (0.018, 2150), (0.041, 2600), (0.057, 2250)):
        s += metal(t, f, inicio, ((1.0, 1.0, 0.012), (1.73, 0.5, 0.008)))
        s += 0.4 * filtrar(ruido(n), corte_baixo=3000) * envelope(t, inicio, 0.004, 0.0003)
    return normalizar(sala(s, mistura=0.15), -8.0)


def robo_zumbido():
    """O motor do robô ligado: 60 Hz (a rede elétrica) com harmônicos,
    um "ronco" de engrenagem que sobe e desce 2 vezes por segundo e um
    chiado de ventoinha. Tudo com ciclos inteiros em 2 s: o loop fecha."""
    duracao = 2.0
    t = tempo(duracao)
    n = len(t)
    hum = sum(a * np.sin(2 * np.pi * 60 * k * t) for k, a in ((1, 1.0), (2, 0.5), (3, 0.35), (5, 0.2)))
    ronco = 1 + 0.3 * np.sin(2 * np.pi * 2 * t)
    ventoinha = filtrar(ruido(n), corte_baixo=800, corte_alto=2500)
    ventoinha /= np.max(np.abs(ventoinha))
    return normalizar(np.tanh(1.5 * hum) * ronco + 0.25 * ventoinha, -10.0)


def robo_alerta():
    """O guincho: dois senos desafinados subindo de 300 para 1400 Hz em
    0,4 s, distorcidos por tanh, com um estalo metálico no começo. É o
    som de "te vi": o jogador precisa reconhecer na hora."""
    t = tempo(0.9)
    n = len(t)
    curva = 300 * (1400 / 300) ** np.clip(t / 0.4, 0, 1)
    s = np.zeros(n)
    for desafino in (1.0, 1.03, 0.51):
        s += np.sin(2 * np.pi * np.cumsum(curva * desafino) / TAXA)
    forma = np.minimum(t / 0.02, 1) * np.exp(-np.maximum(t - 0.45, 0) / 0.12)
    s = np.tanh(4 * s) * forma
    estalo = metal(t, 700, 0.0, ((1.0, 1.0, 0.05), (2.76, 0.6, 0.03)), 0.8)
    return normalizar(sala(0.6 * s + estalo, mistura=0.25), -3.0)


def gabriel_dano():
    """A pancada: um baque surdo (o golpe no corpo), um raspão de metal
    (a garra) e um zumbido agudo que some devagar (o ouvido apitando)."""
    t = tempo(1.2)
    n = len(t)
    baque = filtrar(ruido(n), corte_alto=250) * envelope(t, 0, 0.08)
    baque /= np.max(np.abs(baque))
    raspao = filtrar(ruido(n), corte_baixo=1500, corte_alto=5000) * envelope(t, 0.01, 0.07)
    raspao /= np.max(np.abs(raspao))
    apito = 0.12 * np.sin(2 * np.pi * 3800 * t) * envelope(t, 0.05, 0.5, 0.05)
    return normalizar(baque + 0.5 * raspao + apito, -2.0)


def morte():
    """Tela de morte (2,5 s): um impacto grave e um acorde de metal
    inarmônico que desce de altura enquanto some, como uma máquina
    desligando. Termina em silêncio."""
    t = tempo(2.5)
    n = len(t)
    impacto = filtrar(ruido(n), corte_alto=180) * envelope(t, 0, 0.3)
    impacto /= np.max(np.abs(impacto))
    queda = 2.0 ** (-t / 1.2)
    s = np.zeros(n)
    for r, a in ((1.0, 1.0), (2.76, 0.5), (5.4, 0.25)):
        s += a * np.sin(2 * np.pi * np.cumsum(110 * r * queda) / TAXA)
    s *= envelope(t, 0.0, 0.9, 0.01)
    som = impacto + 0.6 * np.tanh(2 * s)
    som *= np.clip((2.5 - t) / 0.3, 0, 1)
    return normalizar(sala(som, segundos=1.2, mistura=0.3), -3.0)


def checkpoint():
    """O posto de emergência acendendo: o "tunc" de um relé, um zumbido
    elétrico curto e dois bipes subindo (Mi e Si): alívio."""
    t = tempo(0.9)
    n = len(t)
    rele = filtrar(ruido(n), corte_baixo=500, corte_alto=3000) * envelope(t, 0, 0.01)
    zumbido = 0.2 * np.tanh(3 * np.sin(2 * np.pi * 120 * t)) * envelope(t, 0.01, 0.12)
    bipes = np.zeros(n)
    for inicio, f in ((0.18, 659.3), (0.36, 987.8)):
        bipes += np.sin(2 * np.pi * f * t) * envelope(t, inicio, 0.18, 0.005)
    return normalizar(0.6 * rele + zumbido + 0.5 * bipes, -6.0)


def lanterna_clique():
    """O botão de borracha da lanterna: um clique abafado de 2 estalos."""
    t = tempo(0.08)
    n = len(t)
    s = filtrar(ruido(n), corte_baixo=1000, corte_alto=4500) * (envelope(t, 0, 0.003, 0.0003)
                                                               + 0.6 * envelope(t, 0.02, 0.002, 0.0003))
    return normalizar(s, -10.0)


def pilha_troca():
    """Troca de pilha: a tampa de plástico abrindo (raspão curto), a pilha
    velha saindo, a nova entrando com um "clec" de mola e a tampa fechando."""
    t = tempo(0.6)
    n = len(t)
    s = filtrar(ruido(n), corte_baixo=1500, corte_alto=6000) * envelope(t, 0.0, 0.03)
    s += metal(t, 1300, 0.22, ((1.0, 1.0, 0.03), (2.3, 0.5, 0.02)), 0.6)
    s += filtrar(ruido(n), corte_baixo=800, corte_alto=5000) * envelope(t, 0.42, 0.006, 0.0005) * 1.5
    return normalizar(s, -8.0)


def main():
    print("[efeitos do labirinto]")
    for pasta, nome, funcao in (("robos", "sentinela_passo", sentinela_passo),
                                ("robos", "rastreador_passo", rastreador_passo),
                                ("robos", "robo_zumbido", robo_zumbido),
                                ("robos", "robo_alerta", robo_alerta),
                                ("gabriel", "gabriel_dano", gabriel_dano),
                                ("interface", "morte", morte),
                                ("interface", "checkpoint", checkpoint),
                                ("objetos", "lanterna_clique", lanterna_clique),
                                ("objetos", "pilha_troca", pilha_troca)):
        salvar(os.path.join(PASTA_AUDIO, pasta, f"{nome}.wav"), funcao())


if __name__ == "__main__":
    main()

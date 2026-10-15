# gerar_efeitos_porta_bloco.py — compõe por código o som da porta de aço
# de correr do Bloco de salas (com trinco eletromecânico, rodízios e amortecedor).
#
# Como rodar (Python 3 + numpy):
#   python assets/modelagem/audio/gerar_efeitos_porta_bloco.py
#
# Gera:
#   assets/audio/efeitos/objetos/porta_bloco.wav   1,1 s: destrave de solenóide,
#                                                 clique mecânico, rolamento no trilho
#                                                 de aço e amortecedor pneumático.
#
# A porta do Bloco de salas em 3026 é uma porta pesada de aço com visor de
# vidro aramado, que desliza de lado ("correndo pro lado") num trilho superior
# de embutir com amortecedor pneumático de desaceleração.
#
# Componentes sintetizados:
#   1. Solenóide e trava elétrica: pulso agudo curto (1650 e 2800 Hz) e estalo
#      de choque eletromecânico rápido (0.00 a 0.05 s).
#   2. Bipe suave de liberação eletrônica (C7 - 2093 Hz).
#   3. Desengate do trinco mecânico de pressão: baque metálico de baixa-média frequência
#      (210 e 540 Hz) com ruído de mola desarmando (0.07 a 0.15 s).
#   4. Rolamento dos rodízios industriais no trilho de aço: ruído filtrado entre 100 e
#      800 Hz modulado pela velocidade v(t) = sen(pi * x)^1.2 e pulso periódico do giro.
#   5. Raspar metálico suave da guia inferior no canal de piso (1200 a 4500 Hz).
#   6. Descompressão do amortecedor pneumático: hiss de ar pressurizado (1800 a 6000 Hz).
#   7. Batente de fim de curso suave com ressonância no corredor do prédio.

import importlib.util
import os
import numpy as np

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
PASTA_OBJETOS = os.path.join(PASTA_PROJETO, "assets", "audio", "efeitos", "objetos")

_spec = importlib.util.spec_from_file_location(
    "gerar_efeitos_gabriel", os.path.join(PASTA_SCRIPT, "gerar_efeitos_gabriel.py")
)
ef = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ef)

TAXA = ef.TAXA
tempo, envelope, filtrar, normalizar, salvar, sala = (
    ef.tempo,
    ef.envelope,
    ef.filtrar,
    ef.normalizar,
    ef.salvar,
    ef.sala,
)


def porta_bloco() -> np.ndarray:
    rng = np.random.default_rng(3026)
    duracao = 1.1
    t = tempo(duracao)
    n = len(t)

    # 1. Trava eletromecânica e pulso de solenóide (0.00s a 0.05s)
    solenoide = np.sin(2 * np.pi * 140 * t) * envelope(t, 0.0, 0.04, ataque=0.001)
    solenoide += (
        np.sin(2 * np.pi * 1650 * t) + 0.6 * np.sin(2 * np.pi * 2800 * t)
    ) * envelope(t, 0.005, 0.03, ataque=0.0005)
    solenoide += (
        filtrar(
            rng.standard_normal(n) * envelope(t, 0.005, 0.02, ataque=0.0005),
            corte_baixo=2000,
            corte_alto=8000,
        )
        * 0.8
    )

    # Bipe sutil de liberação eletrônica (tom C7 - 2093 Hz)
    bipe = np.sin(2 * np.pi * 2093 * t) * envelope(t, 0.01, 0.04, ataque=0.002) * 0.25

    # 2. Desengate do trinco mecânico de aço (0.07s a 0.16s)
    t_trinco = 0.07
    trinco = (
        np.sin(2 * np.pi * 210 * (t - t_trinco))
        * envelope(t, t_trinco, 0.08, ataque=0.002)
        * 1.2
    )
    trinco += (
        np.sin(2 * np.pi * 540 * (t - t_trinco))
        * envelope(t, t_trinco, 0.05, ataque=0.001)
        * 0.7
    )
    trinco += (
        filtrar(
            rng.standard_normal(n) * envelope(t, t_trinco, 0.04, ataque=0.001),
            corte_baixo=400,
            corte_alto=3500,
        )
        * 0.9
    )

    # 3. Movimento de deslizamento em trilho com rodízios de aço (0.10s a 0.78s)
    x = np.clip((t - 0.10) / 0.68, 0.0, 1.0)
    v = np.sin(np.pi * x) ** 1.2

    # Rodízios no trilho superior de aço
    giro = 8.0 + 20.0 * v
    fase = np.cumsum(giro) / TAXA
    pulso = np.abs(np.sin(np.pi * fase)) ** 3
    rodinhas = (
        filtrar(rng.standard_normal(n), corte_baixo=100, corte_alto=800)
        * (0.3 + 0.7 * pulso)
        * v
        * 1.5
    )

    # Raspar suave da guia no canal inferior
    raspar = (
        filtrar(rng.standard_normal(n), corte_baixo=1200, corte_alto=4500)
        * 0.3
        * (v**1.3)
    )

    # Ressonância de chapa oca em movimento
    folha = np.sin(2 * np.pi * 92 * t) * v * 0.5
    folha += np.sin(2 * np.pi * 180 * t) * v * 0.3

    # 4. Amortecedor pneumático (descompressão suave)
    ar = (
        filtrar(rng.standard_normal(n), corte_baixo=1800, corte_alto=6000)
        * (v**1.2)
        * 0.25
    )

    # 5. Batente do amortecedor / parada no fim de curso (0.78s)
    t_fim = 0.78
    baque = (
        np.sin(2 * np.pi * 82 * (t - t_fim))
        * envelope(t, t_fim, 0.12, ataque=0.005)
        * 1.1
    )
    baque += (
        np.sin(2 * np.pi * 320 * (t - t_fim))
        * envelope(t, t_fim, 0.06, ataque=0.002)
        * 0.5
    )
    baque += (
        filtrar(
            rng.standard_normal(n) * envelope(t, t_fim, 0.05, ataque=0.002),
            corte_baixo=100,
            corte_alto=1500,
        )
        * 0.6
    )

    soma = solenoide + bipe + trinco + rodinhas + raspar + folha + ar + baque
    return normalizar(sala(soma, mistura=0.25), -4.0)


def main() -> None:
    print("[efeito sonoro da porta de correr do Bloco de salas]")
    caminho = os.path.join(PASTA_OBJETOS, "porta_bloco.wav")
    salvar(caminho, porta_bloco())
    print(f"Salvo: {caminho}")


if __name__ == "__main__":
    main()

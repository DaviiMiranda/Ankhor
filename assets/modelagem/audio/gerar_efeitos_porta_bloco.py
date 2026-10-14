# gerar_efeitos_porta_bloco.py — compõe por código o som da porta de aço
# institucional/corta-fogo do Bloco de salas (com trinco eletromecânico e amortecedor).
#
# Como rodar (Python 3 + numpy):
#   python assets/modelagem/audio/gerar_efeitos_porta_bloco.py
#
# Gera:
#   assets/audio/efeitos/objetos/porta_bloco.wav   1,1 s: destrave de solenóide,
#                                                 clique mecânico, giro em dobradiças
#                                                 pesadas de aço e amortecedor pneumático.
#
# Ao contrário da porta de correr de madeira da Biblioteca (porta_correr.wav)
# ou do rangido de dobradiça antiga de madeira (porta_abrir.wav), a porta do
# Bloco de salas em 3026 é pesada, de aço maciço com vidro aramado, controlada
# por teclado numérico e trinco de pressão.
#
# Componentes sintetizados:
#   1. Solenóide e trava elétrica: pulso agudo curto (1650 e 2800 Hz) e estalo
#      de choque eletromecânico rápido (0.0 a 0.05 s).
#   2. Bipe suave de liberação eletrônica (C7 - 2093 Hz).
#   3. Desengate do trinco de pressão: baque metálico de média-baixa frequência
#      (210 e 540 Hz) com ruído de mola desarmando (0.07 a 0.15 s).
#   4. Giro da folha de aço: ressonância oca de chapa (95 e 185 Hz) multiplicada
#      pelo perfil de velocidade angular v(t) = sen(pi * x)^1.3.
#   5. Fricção metálica da dobradiça pesada: ruído filtrado entre 800 e 2600 Hz.
#   6. Descompressão do amortecedor pneumático: hiss de ar pressurizado (1800 a 6500 Hz).
#   7. Fim de curso suave com ressonância no corredor do prédio.

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

    # 3. Movimento angular da chapa de aço e dobradiças pesadas (0.12s a 0.80s)
    x = np.clip((t - 0.12) / 0.65, 0.0, 1.0)
    v = np.sin(np.pi * x) ** 1.3

    # Ressonância de chapa oca em deslocamento
    folha = np.sin(2 * np.pi * 95 * t) * v * 0.7
    folha += np.sin(2 * np.pi * 185 * t) * v * 0.4
    folha += filtrar(rng.standard_normal(n), corte_baixo=120, corte_alto=900) * v * 0.5

    # Fricção das dobradiças pesadas
    dobradica = (
        filtrar(rng.standard_normal(n), corte_baixo=800, corte_alto=2600)
        * (v**1.5)
        * 0.35
    )

    # 4. Amortecedor pneumático (descompressão suave)
    ar = (
        filtrar(rng.standard_normal(n), corte_baixo=1800, corte_alto=6500)
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

    soma = solenoide + bipe + trinco + folha + dobradica + ar + baque
    return normalizar(sala(soma, mistura=0.25), -4.0)


def main() -> None:
    print("[efeito sonoro da porta do Bloco de salas]")
    caminho = os.path.join(PASTA_OBJETOS, "porta_bloco.wav")
    salvar(caminho, porta_bloco())
    print(f"Salvo: {caminho}")


if __name__ == "__main__":
    main()

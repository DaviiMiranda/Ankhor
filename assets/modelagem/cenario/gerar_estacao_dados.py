# gerar_estacao_dados.py — desenha por código, pixel a pixel, a estação de
# trabalho da sala de dados do bunker (a "central_dados"), sem ninguém
# sentado nela: mesa, três monitores de tubo, gaveteiro e torre.
#
# Por que existe: a estação da Clarice era desenhada junto com ela, no mesmo
# sprite (clarice_digitando.png, gerado por gerar_clarice.py). Com o Henrique
# no lugar dela (docs/decisoes.md, 2026-10-11), a estação precisa existir
# sozinha, e o Henrique (em pé, de costas) fica na frente dela. As três telas
# agora mostram as câmeras do campus, que é o que o Henrique vê.
#
# Mesmo estilo e mesma paleta do gerar_objetos_biblioteca.py, que é importado
# como módulo (cores e a classe Desenho).
#
# Como rodar (Python 3 + Pillow):
#   python assets/modelagem/cenario/gerar_estacao_dados.py
#
# O que sai:
#   assets/sprites/cenario/objetos/estacao_dados.png   160 x 128 px
#
# Medidas: o quadro tem o mesmo tamanho (160 x 128) e a mesma ancoragem dos
# quadros do clarice_digitando.png, para a cena usar escala 0,5 e offset
# (-80, -120), e as colisões da mesa continuarem valendo:
#   - a mesa ocupa x = 45..130, y = 56..70 do quadro (52 x 9 px na cena);
#   - o chão (os pés de quem fica em pé na frente) fica em y = 120.

import importlib.util
import os

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))

_spec = importlib.util.spec_from_file_location(
    "gerar_objetos_biblioteca", os.path.join(PASTA_SCRIPT, "gerar_objetos_biblioteca.py"))
ob = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ob)

Desenho, cor = ob.Desenho, ob.cor
PASTA_OBJETOS = ob.PASTA_OBJETOS
CONTORNO, METAL_ESCURO, METAL, METAL_CLARO = ob.CONTORNO, ob.METAL_ESCURO, ob.METAL, ob.METAL_CLARO
BEGE, BEGE_ESCURO, ETIQUETA = ob.BEGE, ob.BEGE_ESCURO, ob.ETIQUETA
VERMELHO, AMARELO = ob.VERMELHO, ob.AMARELO

MESA = cor("#6f6658")
MESA_CLARA = cor("#8b8171")
MESA_ESCURA = cor("#4a443b")
TELA = cor("#2f7a4a")
TELA_ESCURA = cor("#1c4a2e")
TELA_CLARA = cor("#7cf09a")
SOMBRA = (0, 0, 0, 70)

LARGURA, ALTURA = 160, 128


def bloco(d, x, y, c):
    """Um 'pixel' de 2 x 2: detalhes pequenos que ainda precisam aparecer."""
    d.ret(x, y, x + 1, y + 1, c)


def monitor(d, x0, y0, tipo):
    """Monitor de tubo de 22 x 20 px: carcaça bege, moldura escura e tela
    verde com linhas de varredura. `tipo` escolhe o que a câmera mostra."""
    d.caixa(x0, y0, x0 + 21, y0 + 19, BEGE, ETIQUETA, BEGE_ESCURO)
    d.ret(x0 + 3, y0 + 3, x0 + 18, y0 + 14, CONTORNO)
    ix0, iy0, ix1, iy1 = x0 + 4, y0 + 4, x0 + 17, y0 + 13
    for y in range(iy0, iy1 + 1):
        d.ret(ix0, y, ix1, y, TELA if (y - iy0) % 2 == 0 else TELA_ESCURA)
    if tipo == "corredor":
        # um corredor em perspectiva: as paredes convergem para o fundo
        for i in range(4):
            d.px(ix0 + i, iy0 + 1 + i, TELA_CLARA)
            d.px(ix1 - i, iy0 + 1 + i, TELA_CLARA)
            d.px(ix0 + i, iy1 - 1 - i, TELA_CLARA)
            d.px(ix1 - i, iy1 - 1 - i, TELA_CLARA)
        d.ret(ix0 + 5, iy0 + 3, ix1 - 5, iy1 - 3, TELA_ESCURA)
    elif tipo == "grade":
        # quatro câmeras de uma vez
        d.ret(ix0 + 6, iy0, ix0 + 7, iy1, TELA_CLARA)
        d.ret(ix0, iy0 + 4, ix1, iy0 + 5, TELA_CLARA)
        bloco(d, ix0 + 2, iy0 + 1, TELA_CLARA)
        bloco(d, ix0 + 9, iy0 + 6, TELA_CLARA)
    else:
        # uma sala com uma silhueta parada no meio
        d.ret(ix0 + 1, iy1 - 2, ix1 - 1, iy1 - 2, TELA_CLARA)
        d.ret(ix0 + 6, iy0 + 3, ix0 + 7, iy1 - 3, TELA_CLARA)
        bloco(d, ix0 + 6, iy0 + 1, TELA_CLARA)
    # o ponto vermelho de "gravando"
    bloco(d, ix0 + 1, iy0 + 1, VERMELHO)
    # pescoço e base
    d.ret(x0 + 7, y0 + 20, x0 + 14, y0 + 22, BEGE_ESCURO)
    d.ret(x0 + 5, y0 + 23, x0 + 16, y0 + 23, CONTORNO)


def perna(d, x):
    d.ret(x, 71, x + 3, 108, CONTORNO)
    d.ret(x + 1, 71, x + 2, 107, METAL)
    d.ret(x + 1, 71, x + 1, 107, METAL_CLARO)


def estacao():
    d = Desenho(LARGURA, ALTURA)

    # sombra no chão, embaixo da mesa e da torre
    d.ret(46, 109, 148, 112, SOMBRA)

    # pernas e gaveteiro
    perna(d, 46)
    perna(d, 126)
    d.caixa(108, 71, 125, 104, METAL, METAL_CLARO, METAL_ESCURO)
    d.ret(110, 82, 123, 82, CONTORNO)
    d.ret(110, 93, 123, 93, CONTORNO)
    d.ret(114, 77, 119, 78, METAL_CLARO)
    d.ret(114, 88, 119, 89, METAL_CLARO)
    d.ret(114, 98, 119, 99, METAL_CLARO)

    # torre do computador, ao lado da mesa
    d.caixa(135, 76, 147, 107, BEGE, ETIQUETA, BEGE_ESCURO)
    d.ret(138, 84, 144, 85, CONTORNO)
    d.ret(138, 90, 144, 91, CONTORNO)
    bloco(d, 140, 100, VERMELHO)
    # o cabo da torre até a mesa
    d.ret(130, 72, 134, 73, CONTORNO)
    d.ret(134, 73, 135, 77, CONTORNO)

    # tampo da mesa
    d.caixa(45, 56, 130, 70, MESA, MESA_CLARA, MESA_ESCURA)

    # monitores: câmera do corredor, grade de câmeras e uma sala
    monitor(d, 45, 36, "corredor")
    monitor(d, 69, 32, "grade")
    monitor(d, 97, 36, "sala")

    # teclado, mouse, caneca e papéis em cima da mesa
    d.ret(50, 62, 63, 65, CONTORNO)
    d.ret(51, 63, 62, 64, METAL_ESCURO)
    d.px(53, 63, AMARELO)
    d.px(57, 63, AMARELO)
    d.ret(66, 63, 68, 65, METAL)
    d.ret(96, 59, 99, 65, VERMELHO)
    d.ret(96, 59, 99, 59, ETIQUETA)
    d.ret(108, 62, 120, 65, ETIQUETA)
    d.ret(110, 63, 118, 63, BEGE_ESCURO)

    return d


def main():
    print("Estação da sala de dados:")
    estacao().salvar(PASTA_OBJETOS, "estacao_dados.png")


if __name__ == "__main__":
    main()

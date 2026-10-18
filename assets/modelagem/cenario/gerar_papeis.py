# gerar_papeis.py — desenha, por código, os sprites dos PAPÉIS que o Gabriel acha
# no chão do Centro de Convivência (os documentos para ler): o bilhete do
# lanterninha, os canhotos de ingresso, os avisos e as ordens.
#
# Como rodar (Python 3 + numpy + Pillow):
#
#   python assets/modelagem/cenario/gerar_papeis.py
#
# O que sai (em assets/sprites/cenario/objetos/papel_<nome>.png): um sprite
# pequeno por documento, visto de cima e de lado, como os itens no chão
# (assets/sprites/itens/*_chao.png). O pé do sprite é o meio da borda de baixo,
# a mesma regra do ItemNoChao (cenas/itens/papel_no_mundo.tscn).
# Com CATALOGO=1 monta uma folha com os papéis. Não commitar.
#
# Como cada papel se distingue de longe:
#   - o BILHETE é uma folha com a dobra no canto e linhas de letra à mão;
#   - o CANHOTO é uma tira com o picotado no lado esquerdo e uma faixa de cor
#     no direito (uma cor por amigo: Léo ciano, Bia magenta, Caio âmbar; o do
#     ingresso sem nome é violeta);
#   - o AVISO, a ORDEM e o PANFLETO são folhas com um cabeçalho colorido, na
#     cor da loja de onde vêm (azul, limão, âmbar, vermelho).
#
# O papel é desenhado achatado no chão, então o lado de cima é puxado 1 px para
# a direita (como se víssemos o papel um pouco de lado), e uma linha de sombra
# fica embaixo.

import numpy as np

import gerar_praca_base as base

Imagem, RAMPAS, SOMBRA = base.Imagem, base.RAMPAS, base.SOMBRA


def papel_de_base(img, poligono, tom=0.84):
    """Pinta o papel: claro no meio, mais escuro na borda de baixo e na da
    direita (a luz vem de cima, da esquerda)."""
    X, Y = img.X, img.Y
    forma = img.poligono(poligono)
    img.pintar(forma, "papel_branco", tom - 0.12 * (Y > img.h - 4) - 0.06 * (X > img.w - 4))
    return forma


def sombra_embaixo(img, forma):
    abaixo = np.roll(forma, 1, axis=0) & ~forma
    img.cor(abaixo, SOMBRA)


def linhas_de_texto(img, forma, x0, x1, y0, passo, quantas, tom=0.2, semente=0):
    rng = np.random.default_rng(semente)
    for k in range(quantas):
        comp = int(rng.integers(max(2, (x1 - x0) // 2), x1 - x0 + 1))
        img.pintar(img.ret(x0, y0 + k * passo, x0 + comp, y0 + k * passo + 1) & forma, "grafite", tom, achatar=False)


def bilhete():
    """Bilhete escrito à mão: uma folha com a dobra no canto e linhas tortas."""
    img = Imagem(15, 11)
    forma = papel_de_base(img, [(3, 1), (13, 1), (14, 8), (2, 8)])
    linhas_de_texto(img, forma, 4, 12, 3, 2, 3, 0.18, 1)
    img.pintar(img.poligono([(10, 1), (13, 1), (13, 4)]) & forma, "papel_branco", 0.46)
    img.pintar(img.ret(5, 6, 9, 7) & forma, "neon_azul", 0.36, achatar=False)
    sombra_embaixo(img, forma)
    img.contornar()
    return img, 7, 10


def canhoto(cor):
    """Canhoto de ingresso: a tira com o picotado à esquerda (dentes vazados),
    duas linhas de letra e a faixa colorida à direita."""
    img = Imagem(16, 9)
    X, Y = img.X, img.Y
    forma = papel_de_base(img, [(3, 1), (14, 1), (15, 6), (2, 6)], 0.88)
    picotado = forma & (X <= 3) & ((Y % 2) == 0)
    img.apagar(picotado)
    forma = forma & ~picotado
    img.pintar(img.ret(11, 1, 14, 6) & forma, cor, 0.56)
    img.pintar(img.ret(11, 1, 14, 2) & forma, cor, 0.8, achatar=False)
    img.pintar(img.ret(5, 2, 10, 3) & forma, "grafite", 0.2, achatar=False)
    img.pintar(img.ret(5, 4, 9, 5) & forma, "grafite", 0.3, achatar=False)
    sombra_embaixo(img, forma)
    img.contornar()
    return img, 8, 8


def folha_com_cabecalho(cor, tipo):
    """Folha impressa: o cabeçalho colorido, as linhas de texto e uma marca que
    muda com o tipo (o carimbo da ordem, o furo do formulário contínuo da
    impressora, o ícone do panfleto)."""
    img = Imagem(15, 12)
    X, Y = img.X, img.Y
    forma = papel_de_base(img, [(3, 1), (13, 1), (14, 10), (2, 10)])
    img.pintar(img.ret(3, 1, 14, 4) & forma, cor, 0.52)
    img.pintar(img.ret(3, 1, 14, 2) & forma, cor, 0.8, achatar=False)
    linhas_de_texto(img, forma, 4, 12, 5, 2, 3, 0.2, 7 + len(tipo))
    if tipo == "ordem":
        img.pintar(img.elipse(11, 8, 2, 1.5) & forma, "neon_vermelho", 0.5, achatar=False)
    elif tipo == "impressao":
        img.pintar((Y % 2 == 0) & ((X == 3) | (X == 13)) & forma, "grafite", 0.1, achatar=False)
    elif tipo == "panfleto":
        img.pintar(img.elipse(8, 8, 2, 1.5) & forma, cor, 0.7, achatar=False)
    sombra_embaixo(img, forma)
    img.contornar()
    return img, 7, 11


PAPEIS = {
    "papel_bilhete": bilhete,
    "papel_canhoto_leo": lambda: canhoto("ciano"),
    "papel_canhoto_bia": lambda: canhoto("neon_magenta"),
    "papel_canhoto_caio": lambda: canhoto("neon_ambar"),
    "papel_canhoto_ingresso": lambda: canhoto("neon_violeta"),
    "papel_aviso_loja": lambda: folha_com_cabecalho("neon_azul", "aviso"),
    "papel_ordem_impressao": lambda: folha_com_cabecalho("neon_limao", "impressao"),
    "papel_ordem_servico": lambda: folha_com_cabecalho("neon_ambar", "ordem"),
    "papel_panfleto": lambda: folha_com_cabecalho("neon_vermelho", "panfleto"),
}


def main():
    print("Gerando os papéis em assets/sprites/cenario/objetos")
    pasta = base.os.path.join(base.PASTA_PROJETO, "assets", "sprites", "cenario", "objetos")
    amostra = []
    for nome, funcao in PAPEIS.items():
        img, px, py = funcao()
        img.salvar(f"{nome}.png", pasta)
        print(f"    {nome}: pé em ({px}, {py}) -> offset = Vector2({-px}, {-py})")
        amostra.append((nome, img))
    base.salvar_catalogo("papeis", amostra, 5, 8)


if __name__ == "__main__":
    main()

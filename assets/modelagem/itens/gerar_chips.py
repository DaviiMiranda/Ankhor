# Desenha o microcontrolador em pixels para a mochila e o chão.
# A placa verde, o circuito preto e as trilhas de cobre seguem a arte detalhada.
from pathlib import Path
from PIL import Image

PASTA = Path(__file__).resolve().parents[2] / 'sprites' / 'itens'
PALETA = {
    '.': (0, 0, 0, 0), 'k': (17, 21, 19, 255),
    'e': (34, 47, 33, 255), 'v': (66, 81, 54, 255),
    'l': (99, 113, 77, 255), 'c': (159, 101, 69, 255),
    'p': (39, 39, 39, 255), 's': (140, 139, 124, 255),
}
ICONE = [
    '................',
    '.........kkk....',
    '.......kkeevk...',
    '.....kkevclvvk..',
    '...kkevckkkkvvk.',
    '..kevlckppppkvek',
    '.kevlckpppppksvk',
    '.kevcskppppkssvk',
    '.kevvckkkkkscvvk',
    '..kecksssscclvk.',
    '...ksskcvcclvk..',
    '....kskvcclvk...',
    '.....kkvclvk....',
    '......kkvvk.....',
    '........kk......',
    '................',
]


def salvar(grade, nome):
    imagem = Image.new('RGBA', (len(grade[0]), len(grade)))
    for y, linha in enumerate(grade):
        assert len(linha) == imagem.width
        for x, cor in enumerate(linha):
            imagem.putpixel((x, y), PALETA[cor])
    imagem.save(PASTA / nome)


if __name__ == '__main__':
    salvar(ICONE, 'chips.png')
    # O sprite mantém a mesma grade para ficar legível no cenário.
    salvar(ICONE[2:14], 'chips_chao.png')

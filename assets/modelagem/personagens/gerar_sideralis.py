# gerar_sideralis.py -- desenha o sprite PROVISORIO dos Homo sideralis.
#
# Como rodar (precisa do Pillow):
#
#   python assets/modelagem/personagens/gerar_sideralis.py
#
# Sai assets/sprites/personagens/sideralis/sideralis.png, 96 x 112, no mesmo
# tamanho dos humanos do jogo (o Godot mostra com escala 0,5). E um placeholder
# para a cena final (Enredo, secao 8, "O final"): como eles sao de verdade
# (implantes, rosto, voz) esta pendente no Enredo, secao 10.6. A silhueta so
# conta o que ja esta decidido: uma especie humana mais alta e esguia, feita
# para o espaco, com implantes ciano (o ciano e a cor da tecnologia de 3026).
from PIL import Image, ImageDraw, ImageFilter
import os

LARGURA, ALTURA = 96, 112
CONTORNO = (12, 16, 28, 255)
ROUPA = (36, 44, 70, 255)
ROUPA_ESCURA = (26, 32, 52, 255)
PELE = (176, 190, 208, 255)
CIANO = (90, 240, 255, 255)
CIANO_FORTE = (200, 255, 255, 255)

img = Image.new("RGBA", (LARGURA, ALTURA), (0, 0, 0, 0))
d = ImageDraw.Draw(img)

# pernas e botas
d.rectangle((38, 66, 45, 108), fill=ROUPA_ESCURA)
d.rectangle((51, 66, 58, 108), fill=ROUPA_ESCURA)
d.rectangle((36, 106, 46, 111), fill=ROUPA)
d.rectangle((50, 106, 60, 111), fill=ROUPA)
d.line((41, 70, 41, 103), fill=CIANO)
d.line((54, 70, 54, 103), fill=CIANO)

# bracos longos, com as maos palidas
d.rectangle((24, 38, 29, 76), fill=ROUPA)
d.rectangle((67, 38, 72, 76), fill=ROUPA)
d.rectangle((23, 76, 30, 84), fill=PELE)
d.rectangle((66, 76, 73, 84), fill=PELE)
d.line((26, 42, 26, 72), fill=CIANO)
d.line((69, 42, 69, 72), fill=CIANO)

# tronco: ombros largos, cintura fina, e o nucleo no peito
d.polygon([(28, 36), (68, 36), (60, 68), (36, 68)], fill=ROUPA)
d.rectangle((44, 46, 51, 55), fill=CIANO)
d.rectangle((46, 48, 49, 53), fill=CIANO_FORTE)
d.line((36, 40, 44, 46), fill=CIANO)
d.line((60, 40, 52, 46), fill=CIANO)

# pescoco, cabeca alongada, visor e o implante na tempora
d.rectangle((45, 28, 50, 35), fill=PELE)
d.ellipse((37, 4, 59, 31), fill=PELE)
d.rectangle((40, 16, 56, 20), fill=CIANO)
d.rectangle((43, 17, 53, 19), fill=CIANO_FORTE)
d.rectangle((57, 11, 60, 21), fill=ROUPA_ESCURA)
d.point((58, 13), fill=CIANO)
d.point((58, 18), fill=CIANO)
d.line((47, 0, 48, 5), fill=CIANO)

# contorno de 1 px, para a silhueta ler contra o chao escuro
alfa = img.split()[3]
borda = alfa.filter(ImageFilter.MaxFilter(3))
contorno = Image.new("RGBA", img.size, CONTORNO)
contorno.putalpha(borda)
contorno.alpha_composite(img)

pasta = os.path.join(os.path.dirname(__file__), "..", "..", "sprites", "personagens", "sideralis")
os.makedirs(pasta, exist_ok=True)
contorno.save(os.path.join(pasta, "sideralis.png"))
print("ok")

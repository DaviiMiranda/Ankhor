// Falha temporal: a imagem "pula" quando a fenda se abre (cena 8 do prólogo,
// docs/historia/roteiro/cutscenes/seg_prologo.md). Vai no material de um
// Sprite2D; o parâmetro "forca" (0 a 1) é animado pelo AnimationPlayer.
//
// Dois efeitos, os dois presos à grade de pixels para não borrar a pixel art:
//
// 1. Faixas deslocadas (interferência). A imagem é cortada em faixas
//    horizontais de "altura_faixa" pixels. A cada quadro do efeito
//    (TIME * velocidade, arredondado para baixo) cada faixa sorteia um número
//    de 0 a 1 com o ruído clássico fract(sin(n) * 43758.5453): o seno de um
//    número grande varia tão rápido que a parte fracionária parece aleatória,
//    mas é sempre a mesma para o mesmo n (não pisca sem motivo). Se o sorteio
//    passa do limiar, a faixa anda alguns pixels para o lado. Quanto maior a
//    força, mais baixo o limiar e maior o deslocamento: mais faixas tremem.
//
// 2. Aberração cromática. Em lentes reais, cada cor se desvia um pouco
//    diferente. Aqui o canal vermelho é lido alguns pixels à direita e o azul
//    à esquerda; o verde fica no lugar. Nas bordas dos objetos aparecem
//    franjas vermelhas e azuis, o "fantasma" de imagem com defeito.
//
// Todo deslocamento é um número inteiro de pixels da textura: pegamos a
// posição em pixels (UV / TEXTURE_PIXEL_SIZE), somamos o desvio, arredondamos
// e voltamos para UV pelo centro do pixel (+ 0.5). Assim a amostra cai
// sempre em cima de um pixel do desenho, nunca entre dois.
//
// A cor do vértice (o "modulate" do Sprite2D) é guardada no vertex() e
// multiplicada no fim, para o fade do AnimationPlayer continuar valendo.

shader_type canvas_item;

uniform float forca : hint_range(0.0, 1.0) = 0.0;
uniform float deslocamento_max = 4.0;
uniform float altura_faixa = 5.0;
uniform float velocidade = 14.0;
uniform float separacao_max = 2.0;

varying vec4 cor_do_vertice;

float ruido(float n) {
	return fract(sin(n * 12.9898) * 43758.5453);
}

vec2 centro_do_pixel(vec2 pixel, vec2 tamanho_pixel) {
	return (floor(pixel) + 0.5) * tamanho_pixel;
}

void vertex() {
	cor_do_vertice = COLOR;
}

void fragment() {
	vec2 pixel = UV / TEXTURE_PIXEL_SIZE;
	float faixa = floor(pixel.y / altura_faixa);
	float quadro = floor(TIME * velocidade);

	float sorteio = ruido(faixa + quadro * 31.0);
	float tremendo = step(1.0 - forca * 0.4, sorteio);
	float desvio = (ruido(faixa * 7.0 + quadro) - 0.5) * 2.0 * deslocamento_max * forca * tremendo;
	vec2 base = pixel + vec2(round(desvio), 0.0);

	float separacao = round(forca * separacao_max);
	vec4 meio = texture(TEXTURE, centro_do_pixel(base, TEXTURE_PIXEL_SIZE));
	float vermelho = texture(TEXTURE, centro_do_pixel(base + vec2(separacao, 0.0), TEXTURE_PIXEL_SIZE)).r;
	float azul = texture(TEXTURE, centro_do_pixel(base - vec2(separacao, 0.0), TEXTURE_PIXEL_SIZE)).b;

	COLOR = vec4(vermelho, meio.g, azul, meio.a) * cor_do_vertice;
}

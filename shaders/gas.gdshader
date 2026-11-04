// gas.gdshader — a nuvem de gás do setor B do bunker.
//
// A densidade vem de uma textura pequena (uma célula de 16 px vira um pixel),
// atualizada por scripts/sistemas/zona_de_gas.gd, que resolve a equação da
// difusão na grade (ver docs/computacao/difusao_do_gas.md). Aqui entram só as
// contas de imagem:
//
// 1. ALISAR: o filtro linear da GPU interpola as células vizinhas, e a grade
//    grossa vira uma mancha contínua.
// 2. RUÍDO DE VALOR: em cada ponto inteiro de uma grade sorteia-se um número
//    (o seno de um produto escalar, truncado, é a "função de espalhamento"
//    clássica de shader) e o meio é interpolado com a curva 3t² - 2t³.
// 3. FBM: somam-se três oitavas do ruído, cada uma com o dobro da frequência e
//    metade da força. A nuvem ganha detalhe em várias escalas.
// 4. MOVIMENTO: as coordenadas do ruído andam com o tempo, cada oitava numa
//    velocidade, e o gás parece revirar sem que a densidade mude.
//
// render_mode unshaded: o gás não escurece com o CanvasModulate da sala.
shader_type canvas_item;
render_mode unshaded;

uniform sampler2D densidade : filter_linear, repeat_disable;
uniform vec3 cor_gas = vec3(0.55, 0.68, 0.32);
uniform float opacidade_maxima = 0.4;

float sorteio(vec2 p) {
	return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
}

float ruido(vec2 p) {
	vec2 i = floor(p);
	vec2 f = fract(p);
	vec2 u = f * f * (3.0 - 2.0 * f);
	float a = sorteio(i);
	float b = sorteio(i + vec2(1.0, 0.0));
	float c = sorteio(i + vec2(0.0, 1.0));
	float d = sorteio(i + vec2(1.0, 1.0));
	return mix(mix(a, b, u.x), mix(c, d, u.x), u.y);
}

float fbm(vec2 p) {
	float soma = 0.0;
	float forca = 0.5;
	for (int oitava = 0; oitava < 3; oitava++) {
		soma += forca * ruido(p + TIME * 0.12 * float(oitava + 1));
		p *= 2.0;
		forca *= 0.5;
	}
	return soma;
}

void fragment() {
	float d = texture(densidade, UV).r;
	vec2 proporcao = vec2(TEXTURE_PIXEL_SIZE.y / TEXTURE_PIXEL_SIZE.x, 1.0);
	float nuvem = fbm(UV * proporcao * 18.0);
	float alfa = smoothstep(0.05, 0.75, d) * mix(0.55, 1.0, nuvem) * opacidade_maxima;
	COLOR = vec4(cor_gas, alfa);
}

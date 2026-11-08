// Silhueta de óculos VR: escurece tudo o que fica fora das duas lentes,
// como se o jogador olhasse a tela por dentro do visor.
//
// Vai num ColorRect que cobre a tela inteira, por cima do conteúdo.
//
// A conta:
// 1. O ponto da tela vira coordenada centrada (0,0 no meio) com a proporção
//    da tela corrigida, para as lentes não ficarem esticadas. Antes disso, ele
//    é arredondado para a grade de pixels da interface (640 x 360), para a borda
//    sair em degraus de pixel art, como o resto do jogo.
// 2. Cada lente é uma superelipse: |x/a|^n + |y/b|^n = 1. Com n = 2 seria uma
//    elipse; com n maior ela vira um retângulo de cantos arredondados, que é o
//    formato da lente de um visor. A função "lente" devolve um valor que é
//    negativo dentro, zero na borda e positivo fora.
// 3. As duas lentes são unidas com um mínimo suave (smooth min). O mínimo
//    comum daria duas lentes coladas com um bico no meio; o suave preenche
//    o vão entre elas, formando a ponte do visor.
// 4. O encaixe do nariz é um círculo embaixo, no meio, tirado da forma com um
//    máximo suave (o contrário do mínimo suave).
// 5. Fora da forma, a cor da carcaça (quase preta). Na borda de dentro, uma
//    linha fina ciano (a luz dos óculos do Zane) e uma sombra que escurece
//    um pouco o conteúdo perto da borda, para parecer profundidade.

shader_type canvas_item;

uniform vec2 resolucao = vec2(640.0, 360.0);
uniform vec2 centro_da_lente = vec2(0.40, -0.01);
uniform vec2 raio_da_lente = vec2(0.43, 0.41);
uniform float expoente_da_lente = 3.2;
uniform float suavidade_da_ponte = 0.35;
uniform vec2 centro_do_nariz = vec2(0.0, 0.50);
uniform float raio_do_nariz = 0.2;
uniform float suavidade_do_nariz = 0.12;
uniform vec4 cor_da_carcaca : source_color = vec4(0.008, 0.01, 0.012, 1.0);
uniform vec4 cor_da_borda : source_color = vec4(0.25, 1.0, 0.8, 0.55);
uniform float largura_da_borda = 0.012;
uniform float largura_da_sombra = 0.14;
uniform float forca_da_sombra = 0.7;

float lente(vec2 p, vec2 centro) {
	vec2 q = abs(p - centro) / raio_da_lente;
	float n = expoente_da_lente;
	return pow(pow(q.x, n) + pow(q.y, n), 1.0 / n) - 1.0;
}

float minimo_suave(float a, float b, float k) {
	float h = clamp(0.5 + 0.5 * (b - a) / k, 0.0, 1.0);
	return mix(b, a, h) - k * h * (1.0 - h);
}

float maximo_suave(float a, float b, float k) {
	return -minimo_suave(-a, -b, k);
}

void fragment() {
	vec2 pixel = (floor(UV * resolucao) + 0.5) / resolucao;
	vec2 p = (pixel - 0.5) * vec2(resolucao.x / resolucao.y, 1.0);
	float forma = minimo_suave(
		lente(p, vec2(-centro_da_lente.x, centro_da_lente.y)),
		lente(p, centro_da_lente),
		suavidade_da_ponte);
	float nariz = raio_do_nariz - length(p - centro_do_nariz);
	forma = maximo_suave(forma, nariz, suavidade_do_nariz);

	if (forma > 0.0) {
		COLOR = cor_da_carcaca;
	} else if (forma > -largura_da_borda) {
		COLOR = cor_da_borda;
	} else {
		float sombra = 1.0 - smoothstep(0.0, largura_da_sombra, -forma);
		COLOR = vec4(cor_da_carcaca.rgb, sombra * forca_da_sombra);
	}
}

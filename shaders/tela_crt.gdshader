// Efeito de monitor antigo (CRT), desenhado por cima da tela do menu.
// Não mexe nos botões embaixo: só escurece por cima com linhas, bordas,
// cantos arredondados e cintilação, e clareia de leve com uma faixa que desce.
shader_type canvas_item;
render_mode unshaded;

// Quanto as linhas horizontais escurecem a imagem.
uniform float forca_linhas : hint_range(0.0, 1.0) = 0.28;
// Quanto as bordas da tela escurecem (vinheta).
uniform float forca_vinheta : hint_range(0.0, 3.0) = 1.1;
// Quanto a tela pisca.
uniform float forca_cintilacao : hint_range(0.0, 0.3) = 0.03;
// Raio dos cantos arredondados do vidro, em fração da altura da tela.
uniform float raio_cantos : hint_range(0.0, 0.5) = 0.1;
// Faixa clara que desce devagar pela tela (o "rolar" dos CRTs antigos).
uniform float forca_faixa : hint_range(0.0, 0.5) = 0.12;
uniform float velocidade_faixa = 0.12;
// Proporção largura / altura do retângulo da tela (140 / 102).
uniform float proporcao = 1.3725;

// Distância com sinal até um retângulo de cantos arredondados centrado na
// origem: negativa dentro, positiva fora. "metade" é a metade do tamanho.
float distancia_retangulo_arredondado(vec2 p, vec2 metade, float raio) {
	vec2 q = abs(p) - metade + vec2(raio);
	return length(max(q, vec2(0.0))) + min(max(q.x, q.y), 0.0) - raio;
}

void fragment() {
	// Linhas: um pixel sim, um pixel não, fica mais escuro.
	// Uma linha a cada pixel DO JOGO (180 na altura), qualquer que seja o
	// tamanho da janela: FRAGCOORD.y * SCREEN_PIXEL_SIZE.y vai de 0 a 1.
	float linha = mod(floor(FRAGCOORD.y * SCREEN_PIXEL_SIZE.y * 180.0), 2.0) * forca_linhas;

	// Vinheta: quanto mais longe do centro (UV = 0.5, 0.5), mais escuro.
	vec2 do_centro = UV - vec2(0.5);
	float vinheta = dot(do_centro, do_centro) * forca_vinheta;

	// Cintilação: uma onda rápida que sobe e desce com o tempo.
	float cintilacao = (sin(TIME * 50.0) * 0.5 + 0.5) * forca_cintilacao;

	// Faixa: posição que desce de 0 a 1 e recomeça (fract). A intensidade cai
	// com a distância até ela, numa curva suave (smoothstep).
	float posicao_faixa = fract(TIME * velocidade_faixa);
	float faixa = (1.0 - smoothstep(0.0, 0.08, abs(UV.y - posicao_faixa))) * forca_faixa;

	// Cantos: medimos em unidades da altura (x esticado pela proporção) para
	// que o arredondado seja um círculo, e não uma elipse. Fora do retângulo
	// arredondado o vidro fica preto, como a borda funda de um tubo de CRT.
	vec2 p = do_centro * vec2(proporcao, 1.0);
	float fora = distancia_retangulo_arredondado(p, vec2(proporcao * 0.5, 0.5), raio_cantos);
	float canto = step(0.0, fora);

	// Preto com transparência: quanto maior o alfa, mais escuro fica o que está embaixo.
	// Onde a faixa passa, as linhas e o escuro diminuem um pouco.
	float escuro = clamp(linha * (1.0 - faixa * 4.0) + vinheta + cintilacao - faixa, 0.0, 1.0);
	COLOR = vec4(0.0, 0.0, 0.0, max(escuro, canto));
}

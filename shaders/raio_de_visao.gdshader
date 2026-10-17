// Raio de visão: só se enxerga dentro de um círculo em volta do Gabriel. Fora
// dele fica tudo escuro, com a borda em pixels "xadrez" (dithering), como a
// vinheta (shaders/vinheta.gdshader).
//
// Vai num ColorRect de tela cheia, dentro de um CanvasLayer por cima da sala
// e por baixo da interface. Quem calcula onde o Gabriel está na tela e passa
// os valores é scripts/sistemas/raio_de_visao.gd, todo quadro.
//
// A matemática, em 3 passos:
//
// 1. Distância ao Gabriel. "centro" é a posição dele na tela, em pixels da
//    tela. Para cada bloco de pixels medimos distance(ponto, centro), que é o
//    comprimento do vetor entre os dois (teorema de Pitágoras). Os pixels da
//    tela são quadrados, então a figura é um círculo e não precisa achatar o
//    x como na vinheta.
//
// 2. Força da escuridão. smoothstep(raio_livre, raio_escuro, d) vale 0 até
//    d = raio_livre (tudo visível), 1 a partir de d = raio_escuro (preto
//    total) e sobe em S no meio. É o que dá a borda suave do círculo.
//
// 3. Dithering ordenado (matriz de Bayer 4×4), igual ao da vinheta: a
//    escuridão é cortada em poucos níveis e, para cada pixel, o limiar da
//    matriz decide se ele arredonda para cima ou para baixo. Os blocos do
//    xadrez têm o tamanho de um pixel do jogo ("passo", que é o zoom da
//    câmera), para o desenho combinar com o cenário.
shader_type canvas_item;
render_mode unshaded;

// Cor da escuridão (quase preto, um pouco azulado: frio).
uniform vec4 cor : source_color = vec4(0.01, 0.01, 0.03, 1.0);
// Posição do Gabriel na tela, em pixels da tela.
uniform vec2 centro = vec2(320.0, 180.0);
// Até onde tudo é visível, e onde fica preto total (pixels da tela).
uniform float raio_livre = 112.0;
uniform float raio_escuro = 192.0;
// Quantos níveis de escuridão. Poucos = mais "pixel art".
uniform float niveis = 4.0;
// Tamanho da tela em pixels da tela (o retângulo que este shader cobre).
uniform vec2 tamanho = vec2(640.0, 360.0);
// Quantos pixels da tela cobre um pixel do jogo (o zoom da câmera).
uniform float passo = 2.0;

// Matriz de Bayer 4×4, lida linha a linha. Somamos 0,5 e dividimos por 16
// para os limiares ficarem entre 0 e 1.
const float BAYER[16] = float[](
	0.0,  8.0,  2.0, 10.0,
	12.0, 4.0, 14.0,  6.0,
	3.0, 11.0,  1.0,  9.0,
	15.0, 7.0, 13.0,  5.0
);

void fragment() {
	// Qual pixel do jogo é este (coluna e linha inteiras) e onde fica o meio dele.
	vec2 bloco = floor(UV * tamanho / passo);
	vec2 meio_do_bloco = (bloco + 0.5) * passo;

	// 1. Distância ao Gabriel.
	float d = distance(meio_do_bloco, centro);

	// 2. Força: 0 dentro do raio livre, 1 depois do raio escuro.
	float v = smoothstep(raio_livre, raio_escuro, d);

	// 3. Dithering: posição do pixel dentro do bloco 4×4 -> limiar.
	int i = int(mod(bloco.x, 4.0)) + int(mod(bloco.y, 4.0)) * 4;
	float limiar = (BAYER[i] + 0.5) / 16.0;
	float a = floor(v * niveis + limiar) / niveis;

	COLOR = vec4(cor.rgb, clamp(a, 0.0, 1.0));
}

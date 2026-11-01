// A derrota de Hora Morta: a película trava no projetor e queima do centro para as
// bordas. A imagem de baixo aparece onde ainda não queimou (alfa zero).
shader_type canvas_item;

uniform float progresso : hint_range(0.0, 1.0) = 0.0;

// Borda irregular: soma de senos em torno do centro. Cada seno tem uma frequência
// diferente (7, 13 e 29 ondas por volta), e a soma não parece se repetir, mas continua
// suave. O último termo depende da posição, para a borda mudar conforme o buraco cresce.
float irregularidade(vec2 ponto) {
	float angulo = atan(ponto.y, ponto.x);
	return sin(angulo * 7.0 + 1.3) * 0.06
		+ sin(angulo * 13.0 + 4.1) * 0.04
		+ sin(angulo * 29.0) * 0.02
		+ sin(ponto.x * 23.0) * sin(ponto.y * 19.0) * 0.04;
}

void fragment() {
	// Corrige a proporção da tela (16:9) para o buraco crescer redondo, e deixa a
	// borda dele irregular, como papel queimando.
	vec2 ponto = (UV - vec2(0.5)) * vec2(16.0 / 9.0, 1.0);
	float distancia = length(ponto) + irregularidade(ponto);
	float limite = progresso * 1.5 - 0.15;

	float queimado = 1.0 - smoothstep(limite - 0.01, limite + 0.01, distancia);
	float brasa = 1.0 - smoothstep(0.0, 0.08, abs(distancia - limite));
	float claro = 1.0 - smoothstep(0.0, 0.025, abs(distancia - limite));

	vec3 cor = mix(vec3(0.0), vec3(1.0, 0.36, 0.08), brasa);
	cor = mix(cor, vec3(1.0, 0.92, 0.7), claro);
	COLOR = vec4(cor, max(queimado, brasa));
}

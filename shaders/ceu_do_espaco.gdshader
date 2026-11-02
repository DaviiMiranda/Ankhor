// O espaço visto pelas janelas de Hora Morta: estrelas sorteadas, um planeta com a
// borda iluminada e uma estrela perto, que aparece durante a Varredura.
shader_type sky;

uniform vec3 direcao_da_estrela = vec3(1.0, 0.0, 0.0);
uniform float brilho_da_estrela = 0.0;
uniform float giro = 0.0;
uniform vec3 direcao_do_planeta = vec3(0.72, -0.62, -0.32);
uniform float cosseno_do_planeta = 0.9;

// Número "aleatório" entre 0 e 1 que depende só da célula: a mesma célula sempre
// sorteia o mesmo valor, então as estrelas não piscam de um quadro para o outro.
float sorteio(vec3 celula) {
	return fract(sin(dot(celula, vec3(12.9898, 78.233, 37.719))) * 43758.5453);
}

// Duas camadas de estrelas: muitas fracas e poucas fortes. O céu é dividido em cubinhos
// e só uma pequena parte acende.
float estrelas(vec3 olhar) {
	vec3 miudas = floor(olhar * 420.0);
	vec3 grandes = floor(olhar * 170.0);
	float fracas = step(0.9978, sorteio(miudas)) * (0.15 + 0.5 * sorteio(miudas + 1.0));
	float fortes = step(0.9988, sorteio(grandes)) * (0.5 + 0.8 * sorteio(grandes + 2.0));
	return fracas + fortes;
}

void sky() {
	// Matriz de rotação em torno do eixo Y: é o giro da nave passando nas janelas.
	float c = cos(giro);
	float s = sin(giro);
	vec3 olhar = vec3(c * EYEDIR.x + s * EYEDIR.z, EYEDIR.y, -s * EYEDIR.x + c * EYEDIR.z);

	vec3 fundo = vec3(0.004, 0.006, 0.014);
	fundo += vec3(0.008, 0.012, 0.03) * (0.5 + 0.5 * sin(olhar.x * 3.1 + olhar.y * 5.3));

	// Planeta: o produto escalar entre o olhar e o centro dele diz se o raio o atinge.
	// t vai de 0 (centro do disco) a 1 (borda). A atmosfera acende perto da borda, e só
	// no lado virado para o sol, o que desenha um crescente.
	vec3 centro = normalize(direcao_do_planeta);
	float alinhado = dot(olhar, centro);
	float dentro = smoothstep(cosseno_do_planeta, cosseno_do_planeta + 0.0015, alinhado);
	float t = clamp((1.0 - alinhado) / (1.0 - cosseno_do_planeta), 0.0, 1.0);
	vec3 lateral = normalize(olhar - centro * alinhado + vec3(0.0001));
	float lado_do_sol = clamp(dot(lateral, normalize(vec3(-0.4, 0.8, -0.5))), 0.0, 1.0);
	float crescente = pow(t, 7.0) * lado_do_sol;
	vec3 planeta = vec3(0.012, 0.02, 0.035) + vec3(0.42, 0.68, 1.0) * crescente * 1.6;
	float fora = max(cosseno_do_planeta - alinhado, 0.0);
	vec3 atmosfera = vec3(0.25, 0.48, 1.0) * lado_do_sol * exp(-fora * 90.0) * 0.8;

	// A estrela usa EYEDIR, sem o giro: quem controla a posição dela é a Varredura.
	float alinhamento = max(dot(EYEDIR, normalize(direcao_da_estrela)), 0.0);
	float disco = smoothstep(0.996, 0.999, alinhamento);
	float halo = pow(alinhamento, 48.0) * 0.6;
	vec3 luz_da_estrela = vec3(1.0, 0.86, 0.66) * (disco * 7.0 + halo) * brilho_da_estrela;

	vec3 ceu = fundo + vec3(estrelas(olhar)) * vec3(0.8, 0.86, 1.0) + atmosfera;
	COLOR = mix(ceu, planeta, dentro) + luz_da_estrela;
}

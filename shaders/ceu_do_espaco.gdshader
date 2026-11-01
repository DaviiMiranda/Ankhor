// O espaço visto pelas janelas de Hora Morta: estrelas sorteadas e uma estrela
// perto, que aparece durante a Varredura.
shader_type sky;

uniform vec3 direcao_da_estrela = vec3(1.0, 0.0, 0.0);
uniform float brilho_da_estrela = 0.0;
uniform float giro = 0.0;

// Número "aleatório" entre 0 e 1 que depende só da célula: a mesma célula sempre
// sorteia o mesmo valor, então as estrelas não piscam de um quadro para o outro.
float sorteio(vec3 celula) {
	return fract(sin(dot(celula, vec3(12.9898, 78.233, 37.719))) * 43758.5453);
}

void sky() {
	// Matriz de rotação em torno do eixo Y: é o giro da nave passando nas janelas.
	float c = cos(giro);
	float s = sin(giro);
	vec3 olhar = vec3(c * EYEDIR.x + s * EYEDIR.z, EYEDIR.y, -s * EYEDIR.x + c * EYEDIR.z);

	// Divide o céu em cubinhos e acende só cerca de 0,25% deles.
	vec3 celula = floor(olhar * 260.0);
	float estrela = step(0.9975, sorteio(celula)) * (0.25 + 0.75 * sorteio(celula + 1.0));

	// Produto escalar entre o olhar e a estrela: 1 quando apontam para o mesmo lugar.
	// A potência alta concentra o halo em volta do disco.
	float alinhamento = max(dot(EYEDIR, normalize(direcao_da_estrela)), 0.0);
	float disco = smoothstep(0.996, 0.999, alinhamento);
	float halo = pow(alinhamento, 48.0) * 0.6;

	vec3 fundo = vec3(0.004, 0.006, 0.014);
	vec3 luz_da_estrela = vec3(1.0, 0.86, 0.66) * (disco * 7.0 + halo) * brilho_da_estrela;
	COLOR = fundo + vec3(estrela) * vec3(0.8, 0.86, 1.0) + luz_da_estrela;
}

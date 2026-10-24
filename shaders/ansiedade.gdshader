shader_type canvas_item;

uniform sampler2D screen_texture : hint_screen_texture, repeat_disable, filter_nearest;
uniform float intensidade : hint_range(0.0, 1.0) = 0.0;

void fragment() {
	vec2 uv = SCREEN_UV;
	float onda_x = sin(uv.y * 12.0 + TIME * 4.5);
	float onda_y = cos(uv.x * 10.0 - TIME * 3.7);
	uv += vec2(onda_x * 0.004, onda_y * 0.003) * intensidade;
	uv += vec2(sin(TIME * 2.8), cos(TIME * 2.1)) * intensidade * 0.002;
	float separacao = intensidade * 0.004;
	float vermelho = texture(screen_texture, uv + vec2(separacao, 0.0)).r;
	float verde = texture(screen_texture, uv).g;
	float azul = texture(screen_texture, uv - vec2(separacao, 0.0)).b;
	vec3 cor = vec3(vermelho, verde, azul);
	float pulsacao = (sin(TIME * 7.0) + 1.0) * 0.5;
	vec3 tom_ansioso = mix(vec3(1.0, 0.82, 0.78), vec3(1.0, 0.66, 0.62), pulsacao);
	cor = mix(cor, cor * tom_ansioso, intensidade * 0.42);
	float distancia_borda = length((SCREEN_UV - vec2(0.5)) * vec2(1.4, 1.0));
	float vinheta = smoothstep(0.28, 0.78, distancia_borda);
	cor *= 1.0 - vinheta * intensidade * 0.32;
	COLOR = vec4(cor, 1.0);
}

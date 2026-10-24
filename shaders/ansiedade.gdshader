shader_type canvas_item;

uniform sampler2D screen_texture : hint_screen_texture, repeat_disable, filter_nearest;
uniform float intensidade : hint_range(0.0, 1.0) = 0.0;

void fragment() {
	vec2 uv = SCREEN_UV;
	float tremor = intensidade * 0.0016;
	uv.x += sin(uv.y * 36.0 + TIME * 4.0) * tremor;
	uv.y += cos(uv.x * 28.0 + TIME * 3.2) * tremor * 0.45;
	float separacao = intensidade * 0.0012;
	float vermelho = texture(screen_texture, uv + vec2(separacao, 0.0)).r;
	float verde = texture(screen_texture, uv).g;
	float azul = texture(screen_texture, uv - vec2(separacao, 0.0)).b;
	vec3 cor = vec3(vermelho, verde, azul);
	cor = mix(cor, cor * vec3(1.0, 0.75, 0.72), intensidade * 0.2);
	COLOR = vec4(cor, intensidade * 0.12);
}

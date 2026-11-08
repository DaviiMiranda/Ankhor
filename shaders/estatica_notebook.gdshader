shader_type canvas_item;

void fragment() {
	vec2 pixel = floor(UV * vec2(256.0, 160.0));
	float quadro = floor(TIME * 30.0);
	float ruido = fract(sin(dot(pixel + vec2(quadro * 17.0, quadro * 9.0), vec2(12.9898, 78.233))) * 43758.5453);
	float linha = sin((pixel.y + quadro * 3.0) * 0.55) * 0.09;
	float brilho = clamp(ruido * 0.78 + linha + 0.1, 0.0, 1.0);
	COLOR = vec4(vec3(brilho), 1.0);
}

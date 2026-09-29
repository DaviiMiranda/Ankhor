# Computação — Geometria, Visão e Shaders

## 1. Campo de Visão por Produto Escalar (*Dot Product*)

Para determinar se Gabriel está dentro do campo visual de um robô em vista lateral 2.5D, aplicamos geometria vetorial analítica com o produto escalar:

1. **Vetor de Orientação ($\vec{f}$):** Vetor unitário que aponta na direção em que o robô está olhando:
   $$\vec{f} = \begin{cases} (1, 0), & \text{olhando para a direita} \\ (-1, 0), & \text{olhando para a esquerda} \end{cases}$$
2. **Vetor de Posição Relativa ($\vec{d}$):** Vetor normalizado que parte do robô até Gabriel:
   $$\vec{d} = \frac{\vec{p}_{gabriel} - \vec{p}_{robo}}{\|\vec{p}_{gabriel} - \vec{p}_{robo}\|}$$
3. **Cálculo Angular:** Pela definição do produto escalar:
   $$\vec{f} \cdot \vec{d} = \cos(\theta)$$
   onde $\theta$ é o ângulo entre a linha de olhar do robô e a posição de Gabriel.
4. **Critério de Detecção Angular:**
   O jogador só está potencialmente visível se:
   $$\cos(\theta) \ge \cos\left(\frac{\theta_{campo}}{2}\right) \quad \text{e} \quad \|\vec{p}_{gabriel} - \vec{p}_{robo}\| \le R_{alcance}$$

---

## 2. Oclusão e Visibilidade por *Raycasting 2D*

Estar dentro do cone angular não basta; paredes, estantes e portas fechadas bloqueiam a visão:

```gdscript
func pode_ver_jogador(pos_robo: Vector2, pos_jogador: Vector2, dir_olhar: Vector2) -> bool:
    var dist = pos_robo.distance_to(pos_jogador)
    if dist > alcance_visao:
        return false
        
    var dir_jogador = (pos_jogador - pos_robo).normalized()
    var dot = dir_olhar.dot(dir_jogador)
    if dot < cos(deg_to_rad(angulo_visao / 2.0)):
        return false
        
    # Raycast para testar oclusão física no espaço 2D
    var space_state = get_world_2d().direct_space_state
    var query = PhysicsRayQueryParameters2D.create(pos_robo, pos_jogador)
    query.collision_mask = mascara_paredes_e_obstaculos
    var resultado = space_state.intersect_ray(query)
    
    return resultado.is_empty() # Se não colidiu com parede, a visão é direta
```

---

## 3. Shaders Gráficos (GDShader)

### Raios de Sol Volumétricos (`shaders/raios_de_sol.gdshader`)
- Simula feixes de luz que descem através das lajes quebradas da Biblioteca e salas de aula.
- Utiliza funções de ruído procedural com coordenadas rotacionadas para criar faixas dinâmicas de luz solar que interagem com a poeira e pólen suspensos no ar.

### Atenuação e Tremor das Luzes de Emergência
- No fragment shader de iluminação 2D, o decaimento luminoso é calculado com atenuação quadrática suave combinada a uma função senoidal lenta para o tremor das lâmpadas de emergência (o feixe da lanterna usa, além disso, a queda com o ângulo, calculada por produto escalar: ver `gerar_labirinto.py`, função `luz_cone`):
  $$\text{Intensidade}(r, t) = \frac{I_{base} + A \sin(\omega t)}{1.0 + k \cdot r^2}$$

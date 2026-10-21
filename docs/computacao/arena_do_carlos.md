# A arena do Carlos: cone de visão, onda periódica e máquina de estados

O confronto final do Laboratório ([`../fases/dtec.md`](../fases/dtec.md), seção 3.1, parte 3) é um duelo de percepção. O Gabriel não luta: o Carlos vigia a sala com a lupa, a Âncora solta ondas que revelam quem está à vista, e o Gabriel invade dois consoles e chega ao núcleo. Três conteúdos de computação fazem isso funcionar.

---

## 1. A lupa: cone de visão no chão

**No jogo.** Um feixe vermelho sai do Carlos e varre a sala de um lado para o outro. Ficar dentro dele, sem nada no caminho, enche a suspeita; quando ela enche, o Carlos dá o alarme. A Âncora, os consoles, os racks e os cilindros fazem sombra.

**A matemática.** A sala é vista de lado, em 2.5D: o eixo $y$ da tela é a profundidade do chão, e no chão as distâncias em $y$ aparecem achatadas. Por isso a conta é feita **no plano do chão**, desfazendo o achatamento $a = 0{,}6$:

$$\vec{v} = \left(x_G - x_C,\ \frac{y_G - y_C}{a}\right)$$

A direção da lupa é um vetor unitário $\vec{d} = (\cos\theta, \sin\theta)$, e $\theta$ varre a sala com uma senoide no tempo:

$$\theta(t) = 90^\circ + 62^\circ \cdot \sin\!\left(\frac{2\pi t}{T}\right)$$

com período $T$ de 7, 5 ou 3,5 s, conforme a fase. O Gabriel está no feixe quando as três condições valem:

1. **Alcance:** $|\vec{v}| \le 600$.
2. **Ângulo:** $\vec{d} \cdot \dfrac{\vec{v}}{|\vec{v}|} \ge \cos(15^\circ)$. O produto escalar de dois vetores unitários é o cosseno do ângulo entre eles, então isso diz "o ângulo entre a lupa e o Gabriel é no máximo metade da abertura de 30°", sem calcular ângulo nenhum.
3. **Oclusão:** um raio (raycast) do Carlos até o Gabriel não bate em nenhum móvel da camada de paredes.

Para desenhar o feixe, a conta volta para a tela: os pontos do leque $r(\cos\alpha, \sin\alpha)$ têm o $y$ multiplicado por $a$.

**No código** (`scripts/personagens/carlos_chefe.gd`): `direcao_da_lupa()` é $\vec{d}$, `ve_o_ponto(ponto)` faz os três testes, `_no_chao()` e `_do_chao()` convertem entre a tela e o chão. É o mesmo cone por produto escalar dos robôs (`docs/computacao/geometria_e_shaders.md`), só que com a origem fixa e a direção girando.

---

## 2. A onda da Âncora: uma função periódica

**No jogo.** A partir da fase B, um anel ciano sai da Âncora a cada 2,4 s e varre o chão. Quem o anel alcança, fora da sombra de um móvel, fica à vista da lupa.

**A matemática.** A animação da Âncora já é um laço de 2,4 s (a fase do ciclo é $u = (t \bmod 2{,}4)/2{,}4$), e a onda do sprite sai do núcleo de $u = 0{,}25$ a $u = 0{,}80$. A onda do chão usa o mesmo relógio, então as duas saem juntas:

$$p = \frac{u - 0{,}25}{0{,}80 - 0{,}25}, \qquad r(t) = 24 + (440 - 24)\, p \quad (0 \le p \le 1)$$

O anel é uma elipse (o chão achatado de novo, agora com $a = 0{,}5$): um ponto está a uma distância $\delta = \left|\left(x - x_A,\ \frac{y - y_A}{a}\right)\right|$ do pé da Âncora, e o anel o alcança quando $|\delta - r(t)| \le 16$. Cada ciclo revela no máximo uma vez. Por fim, um raio da Âncora até o Gabriel decide se ele estava na sombra.

**No código** (`scripts/sistemas/onda_ancora.gd`): `raio_agora()` é $r(t)$, `distancia_no_chao()` é $\delta$, e o sinal `revelou` avisa o Carlos.

---

## 3. O Carlos: máquina de estados em três fases

**No jogo.** Cada console invadido muda o comportamento do Carlos. A fase vem do progresso (quantos consoles estão invadidos), então volta certa depois de um game over.

| Fase | Consoles | Varredura | Vista até o alarme | Robôs no máximo | O que muda |
|---|---|---|---|---|---|
| A | 0 | 7 s | 0,8 s | 2 | — |
| B | 1 | 5 s | 0,6 s | 3 | a onda liga; a porta norte do salão trava |
| C | 2 | 3,5 s | 0,4 s | 3 | a onda dá alarme na hora; o núcleo abre |

Dentro de cada fase há três estados:

```
           vê o Gabriel (suspeita enche)            suspeita = 1
 VARRENDO ───────────────────────────────▶ DESCONFIANDO ──────────▶ ALARME
    ▲   ◀─────────────────────────────────      │                     │
    │        perde de vista (suspeita esvazia)  │                     │ chama 1 robô,
    │                                           │                     │ manda todos
    │   6 s                                     ▼                     │ para onde o
 ATORDOADO ◀────────── clarão no feixe ou a 110 px do Carlos          │ Gabriel estava
                                                                      ▼
                                                           espera 3 s e volta a VARRENDO
```

A suspeita é um número de 0 a 1: sobe $\Delta t / t_{\text{alarme}}$ por quadro enquanto a lupa vê o Gabriel, e desce pela metade disso quando não vê. Assim, um relance não dispara o alarme, mas ficar no feixe dispara.

**No código** (`scripts/personagens/carlos_chefe.gd`): `fase`, `suspeita` e `_atordoado` são o estado; `_process()` faz as transições; `_dar_alarme()` chama o robô (instancia a Sentinela numa das entradas e liga a grade de navegação da sala, a mesma do `RobosDaSala`) e usa `Robo.distrair()` para mandar os robôs ao último ponto visto. O clarão (`scripts/itens/clarao.gd`) atordoa quem está no grupo `atordoaveis`.

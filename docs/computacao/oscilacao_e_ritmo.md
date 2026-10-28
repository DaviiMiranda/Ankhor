# Oscilação, ângulos e contagem modular — o Corredor do Tempo

Os quatro mecanismos do Corredor do Tempo (Labirinto) são problemas de **tempo**: alguma coisa se repete de forma periódica, e o jogador precisa apertar `E` no instante em que ela passa por um alvo. Cada um usa uma ideia de matemática diferente. A mecânica está em [`../mecanicas/corredor_do_tempo.md`](../mecanicas/corredor_do_tempo.md).

---

## 1. Movimento circular uniforme (toca-discos e anéis)

Um disco que gira com velocidade angular constante $\omega$ (rad/s) tem, depois de $t$ segundos, o ângulo

$$\theta(t) = \theta_0 + \omega t \pmod{2\pi}$$

No código, a cada quadro: `_angulo = wrapf(_angulo + velocidade * delta, 0, TAU)`. O `wrapf` faz o "mod $2\pi$": o ângulo volta a 0 depois de uma volta. Velocidade negativa gira ao contrário (um dos anéis).

### Quando um ângulo "está em cima" do outro?

A agulha está em $-\pi/2$ (em cima). A faixa verde tem centro $\theta_f$ e largura $L$. O acerto é

$$|\,\Delta(\theta_f, -\pi/2)\,| \le \frac{L}{2}$$

O cuidado é a **diferença de ângulos**: $350°$ e $10°$ estão a $20°$ um do outro, não a $340°$. Por isso não basta subtrair: a diferença é levada para o intervalo $(-\pi, \pi]$. O Godot faz isso com `angle_difference(a, b)`; a mesma conta pode ser escrita como

$$\Delta(a, b) = \operatorname{atan2}(\sin(b - a),\ \cos(b - a))$$

que é como o gerador do sprite da máquina dos anéis (`gerar_corredor_tempo.py`) recorta a fenda de cada anel.

**Dificuldade crescente:** a cada acerto, $\omega$ é multiplicado por 1,35 e $L$ por 0,75. A janela de tempo para acertar é $L/\omega$ segundos, então ela cai para $0{,}75 / 1{,}35 \approx 56\%$ da anterior: de 0,375 s para 0,21 s e 0,12 s.

## 2. Movimento harmônico simples (pêndulo)

Para ângulos pequenos, um pêndulo obedece a $\ddot\theta = -\frac{g}{\ell}\theta$, cuja solução é

$$\theta(t) = A \sin(\omega t), \qquad \omega = \sqrt{g/\ell}$$

O código guarda a **fase** $\varphi = \omega t$ e soma `frequencia * delta` a cada quadro; o ângulo é `amplitude * sin(_fase)`.

O que torna o pêndulo diferente do disco é a **velocidade variável**: $\dot\theta(t) = A\omega\cos(\omega t)$. Ela é máxima no meio do arco ($\theta = 0$) e zero nas pontas ($\theta = \pm A$). Uma faixa verde perto da ponta é fácil (o peso "para" ali); perto do meio, o peso passa voando. Como o alvo é sorteado em $[-0{,}7A,\ 0{,}7A]$, cada rodada tem uma dificuldade diferente.

O peso é desenhado em $\text{pivô} + \ell\,(\cos\alpha, \sin\alpha)$ com $\alpha = \pi/2 - \theta$ (no Godot o eixo $y$ aponta para baixo, então $\pi/2$ é "pendurado").

## 3. Contador modular (quadros de De Volta para o Futuro)

Embaixo de cada quadro, um visor de anos rola como o painel de tempo do carro do filme: 1980, 1981, …, 1995, e volta para 1980. Cada ano fica $\Delta$ segundos no visor. O ano mostrado no instante $t$ é

$$\text{ano}(t) = 1980 + \left(\left\lfloor \frac{t - t_0}{\Delta} \right\rfloor \bmod 16\right)$$

A divisão inteira conta quantos "passos" o contador já deu; o **resto da divisão por 16** faz o contador dar a volta, como as horas de um relógio, que voltam a 1 depois de 12 (aritmética modular). No código: `PRIMEIRO_ANO + posmod(floori((_tempo - _inicio) / _segundos_por_ano), 16)`. O `posmod` é o resto que nunca dá negativo.

O acerto é exato: $\text{ano}(t) = $ ano de lançamento do filme (1985, 1989 e 1990, um quadro por vez). A janela para apertar é o tempo que esse ano fica no visor, $\Delta$. No pior caso, o jogador espera uma volta inteira, $16\Delta$, até o ano certo aparecer de novo.

- **Dificuldade crescente:** a cada acerto, $\Delta$ é dividido por 1,3: de 0,38 s para 0,29 s e 0,22 s. O contador do terceiro quadro dá a volta em 3,6 s.
- **Sem decorar a posição:** a cada quadro novo (e a cada erro), o contador recomeça num ano sorteado. Para isso, o início é deslocado por um número inteiro de passos: $t_0 = t - k\,\Delta$, com $k$ sorteado entre 0 e 15. Assim $\text{ano}(t) = 1980 + k$ no mesmo instante.

## 4. O relógio do corredor e a ansiedade

- **Pressão:** com $p = $ tempo gasto / tempo total $\in [0, 1]$, a pressão sobre a ansiedade é $p^{1{,}6}$. A curva cresce devagar no começo e rápido no fim: com metade do tempo gasto a pressão é 0,33; com 90%, 0,84. É o "quanto menor o tempo, maior a ansiedade".
- **Tique-taque:** o intervalo entre tiques é a interpolação linear $\text{lerp}(1{,}0;\ 0{,}22;\ p^{1{,}3})$ segundos.
- **Piso da ansiedade:** a barra é atualizada como antes (sobe com robôs por perto, desce longe deles) e, no fim, `valor = max(valor, pressão)`.

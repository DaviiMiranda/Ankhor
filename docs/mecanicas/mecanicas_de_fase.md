# Mecânicas — O que cada fase acrescenta

Cada fase ensina **uma ação nova**, entrega **um item com custo** e cobra as duas num **desafio próprio**. A ordem de leitura é a do jogo. O D-Tec ficou de fora desta rodada (`docs/decisoes.md`, 2026-11-04).

| Fase | Mecânica nova | Item novo | Desafio novo |
|---|---|---|---|
| Biblioteca | Esconder-se na cabine, com microgame de respiração | Nenhum: a fase já entrega lanterna, rádio e clarão | Voltar pelo salão iluminado usando as cabines como abrigo |
| Bloco de salas | Ações demoradas e barulhentas (segurar `E`) | Nenhum | Cortar a corrente leva 5 s, no trecho da Sentinela |
| Labirinto | Sonar: a onda mostra corredores e robôs | Módulo de pulso do Zane | O Nó 3 não pausa, e o salão é um beco sem saída |
| Centro de Convivência | Carga: a Célula pesa, zumbe e impede de correr | Mapa da Diana | Levar a Célula pela praça ou pela galeria |
| Bunker | Gás no setor B | Máscara de gás | Passar pelo Escafandro com a máscara, cuja respiração ele ouve |

---

## 1. A base: o que mudou para todas as fases

### 1.1 Fugir custa estamina

O Gabriel anda a 60 px/s e corre a 108 px/s. Rastreador (72), Mariposa (70) e Caçador (68) agora perseguem mais rápido do que ele anda: para fugir deles é preciso correr, e correr gasta estamina e faz barulho. Sentinela (36), Ronda (38) e Escafandro (38) continuam lentos: contra eles o perigo é outro. Os números ficam nas cenas `cenas/personagens/robo_*.tscn` e ainda pedem teste de jogo. Como ficam na cena do robô, o Caçador e o Rastreador do D-Tec também ficaram mais rápidos.

### 1.2 O robô atravessa a porta

Trocar de sala não encerra mais a perseguição. `PerseguicaoEntreSalas` (`scripts/sistemas/perseguicao_entre_salas.gd`) funciona assim:

1. Ao atravessar uma porta, o jogo anota o robô que persegue mais perto dela e o tempo do trajeto: `distância / velocidade_perseguicao`, entre 1,2 s e 9 s. Quem está a mais de 9 s de caminho perde o rastro.
2. Na sala nova, passado esse tempo, o robô entra pela mesma porta, com o som dela e o aviso "Algo atravessou a porta atrás de você".
3. Se a sala já tem um robô do mesmo tipo, é esse que vem, para não haver dois iguais. Se a sala não tinha robô, ela ganha a grade de navegação na hora (`RobosDaSala`).
4. O visitante procura o Gabriel. Se não acha, volta para a porta e some.

**Não entram:** as salas seguras, a 103 da Clarice, a Tapioca Orbital, a sala de dados do Henrique, o Corredor do Tempo (lista `SALAS_PROTEGIDAS`) e o D-Tec inteiro (`PREFIXOS_SEM_PERSEGUICAO`). Uma porta com `robo_atravessa = false` também não leva robô (o buraco da 204).

### 1.3 Puzzle sem pausa

`pausa_o_jogo = false` em `PainelCodigo`, `Cofre` e `QuadroEnergia`, e `hack_sem_pausa = true` em `Porta` e `NoHackeavel`, abrem a tela sem pausar: os robôs seguem andando, o Gabriel fica parado e levar dano fecha a tela. Hoje valem para o cofre do bufê, o quadro do bar e o Nó 3. Os outros puzzles opcionais continuam pausando. Enquanto uma tela dessas está aberta, `Hackeamento.tela_em_tempo_real` impede de abrir a pausa ou o inventário.

### 1.4 Segurar `E`

Todo `Interagivel` tem `segundos_segurar` e `ruido_ao_segurar`. Com tempo maior que zero, o aviso vira `[Segure E]` e uma barra aparece sobre o Gabriel (`AcaoDemorada`). Soltar a tecla ou levar dano cancela. A cada segundo a ação faz barulho, se tiver ruído.

### 1.5 Recursos

- **Chave usada sai da mochila:** ao destrancar, a `Porta` tira a chave do inventário. Sem isso, a grade de 12 espaços encheria no meio do jogo.
- **Pilha serve a dois gadgets:** ao pegar uma pilha, ela vai para o que estiver mais fraco entre lanterna e notebook.
- **Menos sobras:** o Centro de Convivência perdeu 2 pilhas (mezanino e cabine do cinema) e o Bunker perdeu 2 flashes (arsenal e depósito). O D-Tec não mudou.

---

## 2. Biblioteca: a cabine

`cenas/sistemas/esconderijo_cabine.tscn`, duas no salão e duas na ala leste. `E` entra: o Gabriel some, a lanterna apaga e nenhum robô o vê ou encosta nele. Com um robô a menos de 110 px, começa o microgame: um cursor vai e volta numa barra, e `E` tem de cair na faixa verde.

- **Três acertos** acalmam: 2,5 s de folga antes de recomeçar, se o robô continuar perto.
- **Duas falhas** (apertar fora da faixa ou deixar passar duas varreduras) fazem o Gabriel engasgar: ele sai da cabine e o robô mais perto o persegue.
- **Quanto mais ansioso,** menor a faixa (de 34% para 16%) e mais rápido o cursor. **Cansado,** a faixa perde mais 25%. Entrar correndo de um robô é mais difícil do que entrar com calma.

---

## 3. Bloco de salas: as ações demoradas

- **A corrente da porta corta-fogo:** segurar `E` por 5 s, com barulho de alcance 40 a cada segundo. Como a Sentinela passa por ali depois do alicate, é preciso esperar a Sentinela passar antes de começar.
- **O molho na areia:** segurar `E` por 2 s, sem barulho.

---

## 4. Labirinto: o sonar, o Nó 3 e os nichos

- **Módulo de pulso** (`dados/itens/modulo_pulso.tres`): o Zane entrega com o notebook. Sem alvo de hack por perto, a tecla do notebook solta um pulso (`scripts/itens/pulso_sonar.gd`). A onda é uma BFS na grade da sala, até 450 px, e cada célula acende quando a frente chega. Robôs alcançados ganham uma marca vermelha por 2 s. O pulso gasta 10% da bateria e faz barulho de alcance 10. Funciona em qualquer sala com grade de robôs.
- **Nó 3:** o minigame não pausa, e o nó grita ao cair (barulho de alcance 24).
- **Nichos:** cada beco com pilha ganhou caixas e um `NichoEsconderijo`. Parado, de lanterna apagada, o Gabriel some da visão, como nos corredores do Bloco.

---

## 5. Centro de Convivência: a carga e a galeria

- **A Célula é carga** (`carga_pesada` em `celula_energia.tres`): com ela na mochila o Gabriel não corre e, a cada 1,5 s, o zumbido faz barulho de alcance 8 (`ZumbidoDaCarga`). A tecla `G` larga no chão. Ela fica onde caiu, mesmo depois de morrer ou trocar de sala (`Inventario.largados`, `ItensLargados`). O comutador consome a Célula.
  - **Como o jogador fica sabendo:** enquanto carrega a Célula, a barra de estamina da HUD fica cinza e o rótulo troca de `ESTAMINA` para `CARGA: SEM CORRER [G]` (`hud.gd`). Cada vez que ele aperta correr com ela na mochila, aparece o aviso de que não dá para correr e de que `G` larga (`ZumbidoDaCarga`). Antes disso, a barra ficava cheia e normal, e um testador achou que a corrida tinha quebrado depois de a estamina zerar (2026-11-05).
- **Mapa da Diana** (`mapa_diana.tres`): fica perto do balcão da Tapioca Orbital, e a Diana conta dele pelo rádio ao Gabriel entrar. Sem o mapa, as portinholas nem aparecem. Com ele, surgem no Self Nebulosa, na Pizzaria Quasar e no Churrasco Solar (`PortaDaGaleria`).
- **A galeria** (`cenas/salas/centro_de_convivencia/galeria.tscn`): 2000 px de corredor escuro, chão de entulho (ruído ×1,5), um Rastreador e nenhum esconderijo. Encurta o caminho e evita as Sentinelas, mas quem leva a Célula não consegue correr dele e tem de largá-la.
- **Cofre do bufê e quadro do bar:** agora sem pausa, com o Rastreador e o Caçador por perto.

---

## 6. Bunker: o gás e a máscara

- **O gás** (`ZonaDeGas`, em `corredor_b.tscn`) cobre o Corredor B de x 360 a 1860. A densidade é calculada por difusão ([`../computacao/difusao_do_gas.md`](../computacao/difusao_do_gas.md)). Onde ela passa de 0,25, o Gabriel perde 1 coração a cada 5 s e tosse, o que faz barulho.
- **O gerador trocou de lugar com o arquivo:** agora fica em x 1561, no fundo do gás. Antes ficava logo depois da escada, e o gás não faria diferença.
- **Máscara de gás** (`mascara_gas.tres`): na enfermaria; há filtros extras no dormitório e no depósito. A tecla liga e desliga. Cada filtro dura 45 s, e cabem 3. Com ela ligada, a respiração faz barulho de alcance 6 a cada 2 s, e o Escafandro ouve bem (×2,2).
- **Ventilação:** religar a energia (`bunker_energia`) liga os exaustores. As fontes fecham, a perda sobe e o gás some em alguns segundos.

---

## 7. Para testar

A `sala_teste` tem um exemplar de cada item novo. Os números estão no Inspetor de cada cena, ou como `@export` nos scripts, e todos são primeiro chute: precisam de teste de jogo.

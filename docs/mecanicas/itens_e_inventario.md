# Mecânicas — Itens, Inventário e Gadgets

Como o Gabriel pega, guarda, equipa e usa itens. As regras de cada item estão no documento da mecânica dele (a lanterna, por exemplo, em [`iluminacao_e_lanterna.md`](iluminacao_e_lanterna.md)). Aqui fica o sistema que serve para todos.

---

## 1. Como funciona no jogo

| Tecla | O que faz |
|---|---|
| `E` | Interage com o que está mais perto: pega um item do chão, troca a pilha da lanterna |
| `Tab` ou `I` | Abre e fecha o inventário na aba **Itens** (o jogo pausa enquanto ele está aberto) |
| `N` | Abre o inventário direto na aba **Anotações** |
| `Q` | Com o inventário aberto, troca entre as abas **Itens** e **Anotações** (também dá para clicar na aba) |
| `1`, `2`, `3` | Usam o gadget equipado naquele espaço. Com o inventário aberto, equipam o item escolhido |

- **Inventário:** uma grade de **3 linhas × 4 colunas**. Todo item pego entra no primeiro espaço livre.
- **Cabeçalho com abas:** no alto da janela ficam **ITENS** e **ANOTAÇÕES**. A aba aberta fica clara e sublinhada. Quando há anotação não lida, a aba mostra um ponto (`ANOTAÇÕES •`). A aba Anotações está explicada em [`registros_e_caderno.md`](registros_e_caderno.md).
- **Destaque no cenário:** todo item que dá para pegar (itens no chão e pilhas) tem uma **luz fraca que pulsa** em volta e, de tempos em tempos, um **brilho de pixel** que pisca em cima do desenho, visível até no escuro. Assim o jogador sabe o que é coletável sem precisar de seta ou contorno.
- **Gadgets:** **3 espaços**, um para cada ferramenta equipável prevista em [`docs/personagens/gabriel.md`](../personagens/gabriel.md): lanterna, cápsulas de clarão e objetos de arremesso. Equipar não tira o item da grade; o espaço de gadget é um atalho para ele.
- Ao pegar um gadget com um espaço livre, ele já é equipado.
- Na tela, os espaços de gadget ficam no canto de baixo à esquerda, com o número da tecla. A borda acende enquanto o gadget está em uso (pote destampado), e a barrinha embaixo mostra a carga.

### Lanterna

- Fica no chão, perto de onde o Gabriel acorda na Biblioteca (e perto do início do labirinto). Pegar com `E` já equipa no espaço 1.
- Liga e desliga com a tecla do espaço. A bateria dura 4 minutos acesa; troca-se com **pilhas** achadas no mapa (`E` perto da pilha: "Trocar a pilha").
- Regras completas em [`iluminacao_e_lanterna.md`](iluminacao_e_lanterna.md).

### Gadgets em teste (sala de teste)

Os três estão na sala de teste (menu Fases → Teste, só pelo editor) e ainda não entraram em nenhuma fase. Os números estão no Inspetor da cena de cada um e são um primeiro chute para o grupo ajustar jogando.

| Gadget | Como usa | O que faz | O custo |
|---|---|---|---|
| **Cápsula de clarão** (`clarao`) | Tecla do espaço | Flash que paralisa por 3,5 s os robôs a até 110 px. O tempo é multiplicado pelo `fator_clarao` do robô: Sentinela ×1,5 (enxerga, sofre mais), Rastreador ×0,6 | No máximo **2**. Paralisado, o robô apaga os olhos; depois procura o Gabriel onde está |
| **Pedra** (`pedra`) | Tecla do espaço | Joga uma pedra ~110 px para onde o Gabriel olha (para antes de uma parede). Onde cai, faz barulho: os robôs que ouvem vão investigar | No máximo **5**. Não serve numa perseguição |
| **Notebook** (`notebook`) | Tecla do espaço, parado perto do alvo (44 px) | Hackeia em 2,5 s: **porta trancada** abre; **robô** fica desligado 8 s. Uma barra em cima do Gabriel mostra o progresso | Gasta 25% da bateria (4 hacks). Durante o hack o Gabriel não se mexe e a tela acesa conta como lanterna para o Sentinela. Levar dano interrompe. Robô **só por trás** |

- **Itens que empilham:** um item com `maximo_unidades` maior que 0 ocupa um espaço só; pegar outro soma 1 até o máximo (cheio, fica no chão com o aviso "no máximo N"). A barrinha do espaço de gadget mostra quantas unidades sobram.
- **Conteúdo de computação:** o barulho da pedra é a mesma **BFS** do som dos passos (`Robo.ouvir_barulho`); o "só por trás" do notebook é **produto escalar** entre a direção do olhar do robô e a direção até o Gabriel (negativo = atrás). Detalhes em [`../computacao/ia_e_perseguicao.md`](../computacao/ia_e_perseguicao.md).
- **Paralisado** é o estado `ATORDOADO` da máquina de estados do robô: não anda, não vê, não ouve, não ataca.

---

## 2. Conteúdo de computação: inventário em grade (matriz)

O inventário é uma **matriz**: uma lista de linhas, e cada linha uma lista de colunas. `grade[linha][coluna]` é o item naquela posição, ou `null` se está vazia.

```
grade = [ [pote, null, null, null],     linha 0
          [null, null, null, null],     linha 1
          [null, null, null, null] ]    linha 2
```

- **Guardar:** percorre linha por linha e coluna por coluna (a ordem de leitura de um texto) até o primeiro `null`. No pior caso olha os 12 espaços: O(linhas × colunas).
- **Cursor da tela:** também é uma posição (coluna, linha). Andar com as setas soma 1 ou −1 numa delas; o resto da divisão (`posmod`) faz o cursor dar a volta de uma borda para a outra.
- **Gadgets:** uma lista de 3 posições que aponta para itens da matriz (uma referência, não uma cópia).
- **Estado dos itens** (carga do pote, aceso ou não) e **itens já pegos** no mapa: dicionários, pelo id. Por isso o pote não volta a aparecer no chão ao entrar de novo na sala.

---

## 3. Onde está no projeto

| O quê | Onde |
|---|---|
| Inventário (autoload `Inventario`, vive o jogo inteiro) | `scripts/sistemas/inventario.gd` |
| Tipo de item (`Item`, um recurso) | `scripts/itens/item.gd` |
| Os itens do jogo | `dados/itens/*.tres` |
| Item no chão | `cenas/itens/item_no_chao.tscn` |
| Base de tudo que interage com `E` (`Interagivel`) | `scripts/itens/interagivel.gd` |
| Efeito da lanterna equipada (a luz) | `cenas/itens/lanterna.tscn` |
| Pilha no chão (recarga) | `cenas/itens/pilha_no_chao.tscn` |
| Cápsula de clarão, pedra, notebook (efeitos) | `cenas/itens/clarao.tscn`, `pedra.tscn` (e `pedra_arremessada.tscn`), `notebook.tscn` |
| Destaque dos coletáveis (luz que pulsa e brilho) | `cenas/itens/destaque_coletavel.tscn` |
| HUD (espaços de gadget, aviso "[E]", mensagem) | `cenas/interface/hud.tscn` |
| Tela do inventário (abas Itens e Anotações) | `cenas/interface/tela_inventario.tscn` |
| Aba Anotações | `cenas/interface/painel_anotacoes.tscn` |
| Ícones e peças da interface (gerados por script) | `assets/modelagem/interface/gerar_interface.py` |

O HUD e a tela do inventário já estão no `modelo_sala.tscn`: toda sala nova herda os dois.

---

## 4. Como criar um item novo

1. **Desenho:** escreva a função do ícone (16 × 16) e, se quiser, a do item no chão em `gerar_interface.py`, adicione no dicionário `ICONES` e rode `python assets/modelagem/interface/gerar_interface.py`. Abra o Godot para gerar os `.import`.
2. **Dados:** no Godot, botão direito em `dados/itens/` → *Novo* → *Recurso...* → `Item`. Preencha `id`, `nome`, `descricao`, `icone` e `sprite_chao`.
3. **Se for gadget:** marque `equipavel` e crie a cena do efeito (como `cenas/itens/lanterna.tscn`), com um script que tenha a função `usar()`. Coloque essa cena em `cena_gadget`. Guarde o que precisa sobreviver à troca de sala em `Inventario.estado_de(id)`, não no script.
4. **No mapa:** arraste `cenas/itens/item_no_chao.tscn` para o nó `Objetos` da sala (a origem é o pé) e escolha o item no Inspetor. O destaque já vem junto e se ajusta ao tamanho do desenho.

Para destacar outra coisa coletável, instancie `cenas/itens/destaque_coletavel.tscn` como filho dela: o brilho procura um irmão chamado `Sprite2D` e pisca só onde o desenho tem pixel. A intensidade da luz, o ritmo do pulso e a frequência do brilho estão no Inspetor.

---

## 5. Ainda não feito

- Descartar ou usar itens que não são gadgets pelo inventário.
- A luz do pote chamar a atenção dos robôs (depende da IA deles).
- Salvar o inventário ao dormir (depende do sistema de save).

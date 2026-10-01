# Diálogos — como funcionam no Ankhor

Conversas com personagens (hoje, a Clarice no bunker). Cada conversa é um arquivo **JSON** em `dados/dialogos/`, escrito sem precisar mexer em código. O formato está em [`template_dialogo.md`](template_dialogo.md).

---

## 1. No jogo

- Perto de um personagem aparece `[E] Conversar`. Ao apertar, o **jogo pausa** (robôs, luzes e música param) e a caixa de diálogo abre **no alto da tela**, para não cobrir os personagens, que ficam no chão, na metade de baixo.
- A caixa mostra o **retrato** de quem fala (ocupa 40 × 40 na tela; a imagem tem 80 × 80, para o rosto sair com o dobro de detalhe), o **nome** na cor da pessoa (Clarice em verde-azulado, Gabriel em vermelho) e o texto aparecendo **letra por letra**, com um bipe a cada duas letras. O tom do bipe muda com quem fala (a Clarice mais aguda). Depois de ponto, vírgula, `?` e `!`, a escrita dá uma pausa curta, como quem respira.
- `E` (ou `Enter`) mostra a fala inteira de uma vez; se ela já está inteira, passa para a próxima. Quando a fala terminou, pisca um `E` no canto.
- Nas **escolhas**, `W`/`S` (ou as setas) movem o cursor `>` e `E` escolhe.
- Fala sem `retrato` (um narrador, um bilhete lido em voz alta) usa a largura toda da caixa.
- No fim, o jogo despausa. Se a conversa tiver `anotacao`, ela entra no **Caderno do Gabriel** (aba Anotações), como os bilhetes.

---

## 2. Como é feito

| Peça | Onde | O que faz |
|---|---|---|
| Autoload `Dialogos` | `scripts/sistemas/dialogos.gd` | Lê o JSON, anda pelos trechos, pausa e despausa o jogo, guarda quais conversas já aconteceram (`vistos`) e manda a anotação para o Caderno |
| Caixa de diálogo | `cenas/interface/caixa_dialogo.tscn` | A tela: retrato, nome, texto letra por letra, escolhas e o bipe. Já está no `modelo_sala.tscn`, então toda sala nova tem |
| `ConversaNpc` | `scripts/personagens/conversa_npc.gd` | Área de interação (`Interagivel`) que começa a conversa. Tem dois campos: `primeira_conversa` e `conversa_de_novo` (a que toca a partir da segunda vez) |

Os três conversam por **sinais**, como o resto do jogo:

```
Dialogos.comecou(caminho)                         a conversa abriu
Dialogos.fala_mostrada(quem, texto, retrato)       uma fala nova
Dialogos.escolhas_mostradas(opcoes)                as opções do fim de um trecho
Dialogos.terminou(caminho)                         a conversa acabou
```

A caixa só escuta esses sinais e chama `Dialogos.avancar()` e `Dialogos.escolher(i)`. Um personagem pode olhar `Dialogos.ativo` para reagir (a Clarice vira a cadeira para o Gabriel enquanto conversam).

### Um diálogo é um grafo

Cada **trecho** é um nó; cada **escolha** e cada `vai_para` é uma aresta que aponta para outro trecho, pelo nome. Por isso uma conversa pode **voltar** a um trecho que já passou (o menu "Mais alguma coisa?" da Clarice volta para as mesmas perguntas) sem repetir texto no arquivo. A conversa acaba quando chega a um trecho sem escolhas e sem `vai_para` (ou a um nome que não existe).

---

## 3. Como pôr uma conversa num personagem novo

1. Escreva o JSON em `dados/dialogos/` seguindo o [`template_dialogo.md`](template_dialogo.md).
2. Retratos: PNG de 80 × 80 em `assets/sprites/personagens/<pasta>/` (a caixa mostra em 40 × 40). No JSON, o campo `retrato` é o caminho a partir de `assets/sprites/personagens/`, sem o `.png` (ex.: `clarice/clarice_retrato_sorrindo`).
3. Na cena do personagem, adicione uma `Area2D` com o script `conversa_npc.gd` e uma `CollisionShape2D` (o alcance). No Inspetor: `texto_acao = Conversar`, `primeira_conversa` e, se quiser, `conversa_de_novo`.
4. Nome com cor própria e tom de bipe: `CORES_NOMES` e `TOM_VOZ` no começo de `scripts/interface/caixa_dialogo.gd`.

Exemplo pronto: `cenas/personagens/clarice.tscn` com `dados/dialogos/clarice_primeiro_encontro.json` e `clarice_de_novo.json`.

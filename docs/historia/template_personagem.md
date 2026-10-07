# Modelo de ficha de personagem

Cada personagem tem **um arquivo** em [`personagens/`](personagens/), com o nome dele em `snake_case` (ex.: `clarice.md`). A ficha **faz parte do [Enredo Principal](enredo_principal.md)** e tem a mesma autoridade: quem o personagem é vale como está escrito nela.

Personagem novo é decisão de história: entra no mesmo PR na ficha nova, na lista da seção 4.2 do Enredo Principal e em [`../decisoes.md`](../decisoes.md). Para robôs, siga o formato de [`personagens/robos.md`](personagens/robos.md).

Copie daqui para baixo. Dentro de `personagens/`, os links para o Enredo começam com `../`.

---

# Nome (ano)

> **Status:** [Em definição / Em desenvolvimento / Concluído]
> **Lei do projeto:** esta ficha faz parte do Enredo Principal e tem a mesma autoridade: quem o personagem é vale como está escrito aqui. A história em volta dele (o acidente, a ordem dos acontecimentos, as pendências) está no Enredo.

---

## 1. Quem é

- **Época de origem:**
- **Quem é:** [ocupação, idade (cerca de 20 anos), ligação com a região da Unifor]
- **História:** [o que fazia no ponto quando foi puxado e como está sobrevivendo em 3026]

## 2. Personalidade

- **Essência:** [uma frase]
- **Traços:**
- **Como fala:** [jeito de falar, gírias, exemplos de fala]
- **O que quer:**
- **O que teme:**
- **Defeito:**
- **Arco:** [como muda ao longo do jogo]

## 3. Relações

| Com | Dinâmica |
|---|---|
| [outro personagem] | |

## 4. No jogo

- **Onde aparece:** [fases e salas]
- **Esconderijo:** [onde vive em 3026, e com quem divide]
- **Como chega ao jogador:** [em pessoa, registros, rádio, telefone, sonho]
- **Função na jogabilidade:** [o que ensina ou destrava]
- **Parte para consertar a Âncora:** [seção 3.1 do Enredo Principal]

## 5. Registros

- **Suporte:** [papel, tinta, moldura, mídia]
- **Já escritos:** [arquivos em `dados/`]

## 6. Direção de arte

- **O que a aparência precisa comunicar:** [época, idade, personalidade]
- **Visual definido:** [link para o `visual.md`, se houver]

## 7. Arquivos

- **Cena:** `cenas/personagens/nome.tscn`
- **Sprites:** `assets/sprites/personagens/nome/`
- **Gerador:** `assets/modelagem/personagens/gerar_nome.py`
- **Diálogos:** `dados/dialogos/nome_*.json`

## 8. Pendências

[O que falta decidir. As pendências de história ficam na seção 12 do Enredo Principal; aqui só aponte para elas.]

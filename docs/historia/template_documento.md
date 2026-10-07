# Modelo de documento (bilhete, diário, relatório)

Use este modelo para escrever um documento novo antes de criar o arquivo no Godot. Os campos são os mesmos do recurso `Documento` (`scripts/itens/documento.gd`), então o texto pronto aqui vira `dados/documentos/<id>.tres` sem adaptação. O passo a passo no Godot está em [`../mecanicas/registros_e_caderno.md`](../mecanicas/registros_e_caderno.md), seção 4.

Antes de escrever, leia a ficha de quem escreve no [Enredo Principal](enredo_principal.md) (seção 4.3). O texto precisa soar como aquela pessoa: o Baltazar escreve em português arcaico, a Diana exagera, a Clarice debocha.

---

## 1. Campos

| Campo | O que é | Exemplo |
|---|---|---|
| `id` | Único, em `snake_case`. É também o nome do arquivo | `diario_baltazar` |
| `titulo` | Vai no alto da folha | `Diário de pergaminho` |
| `autor` | Vira o título da anotação no caderno | `Baltazar, 1750` |
| `papel` | O visual da folha (seção 2) | `pergaminho` |
| `paginas` | O texto, uma entrada por página (seção 3) | — |
| `anotacao` | O que vai para o Caderno do Gabriel ao fechar: só o que é útil | `Robôs têm um olho só...` |

## 2. Papel de cada época

| Quem escreve | `papel` | Estado |
|---|---|---|
| Baltazar (~1750) | `pergaminho` | Pronto |
| Clarice (1994) | `caderno_clarice` | Pronto |
| Gabriel (2026) | `caderno_gabriel` | Pronto |
| Diana (1978), Rafael (2008), o pesquisador (2019), Zane (2123) | — | Falta desenhar. O suporte de cada um está na seção "Registros" da ficha em [`personagens/`](personagens/) |

Papel novo: ver "Papel novo" em [`../mecanicas/registros_e_caderno.md`](../mecanicas/registros_e_caderno.md), seção 4.

## 3. Limites do texto

- Cada página tem no máximo **8 linhas** de ~45 caracteres. A linha em branco entre parágrafos conta.
- Termine cada página no fim de um parágrafo.
- A `anotacao` também cabe em 8 linhas.

---

## 4. Ficha do documento

Copie daqui para baixo e preencha.

- **`id`:**
- **`titulo`:**
- **`autor`:**
- **`papel`:**
- **Onde fica:** [fase, sala e objeto do cenário em que o jogador acha o documento]
- **`texto_acao`:** [o aviso no mapa, ex.: `Ler o bilhete`]

**`paginas`:**

> Página 1:
>
> Página 2:

**`anotacao`:**

> 

**Função no jogo:**

- **Mecânica:** [dica, senha ou rota que o documento ensina, se houver]
- **Narrativa:** [o que revela sobre quem escreveu ou sobre o que aconteceu]

**Conferência:**

- [ ] Combina com a ficha de quem escreve no Enredo Principal (personalidade, época, o que sabe)?
- [ ] Não responde nenhuma pendência do Enredo Principal (seção 12) como se estivesse decidida?
- [ ] Cada página cabe em 8 linhas?

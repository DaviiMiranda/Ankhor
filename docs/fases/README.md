# Fases — Estrutura e Funcionamento

Este documento define como as fases e áreas do **Ankhor** funcionam em termos de arquitetura, fluxo de jogo e design de níveis (*level design*).

> [!IMPORTANT]
> **Primeira Fase Definida:** A primeira fase do jogo é a **Biblioteca** ([`biblioteca.md`](biblioteca.md)). O **Labirinto** ([`labirinto.md`](labirinto.md)) é jogável pelo menu Fases; a posição dele na história está a definir. O **Bloco de salas** ([`bloco_de_salas.md`](bloco_de_salas.md)) tem cenário e portas prontos, sem história ainda. O **Bunker** ([`bunker.md`](bunker.md)) é o esconderijo da Clarice, com a primeira conversa do jogo. As fases seguintes serão definidas em conjunto com a equipe. Este módulo fornece a **estrutura conceitual e o template padronizado** para documentação de cada área.

---

## 🏗️ Como Funciona uma Fase no Jogo

Diferente de fases lineares isoladas com telas de carregamento tradicionais, o mundo do jogo é concebido como um **campus contínuo** modelado como um grafo de salas e corredores:

1. **Topologia e Conexões:**
   - Cada fase corresponde a um conjunto de cômodos (nós do grafo) conectados por passagens físicas (portas, vãos, janelas, buracos de desabamento).
   - Áreas exploradas anteriormente continuam acessíveis ou sofrem alterações (novas passagens abertas, caminhos bloqueados por escombros).

2. **Fluxo de Objetivos:**
   - **Objetivo Principal:** Uma meta clara que motiva o jogador a atravessar a área (ex.: encontrar uma chave, alcançar um terminal, desobstruir uma passagem).
   - **Objetivos Secundários:** Exploração opcional para coletar recursos adicionais (pilhas, cápsulas de clarão, documentos ou relíquias).

3. **Dinâmica de Inimigos (Robôs):**
   - Cada área possui robôs alocados que operam sob uma rotina inicial ditada pela grade horária.
   - O nível de desafio é modulado pela densidade de inimigos, pelos tipos de sentidos dominantes (audição, visão, luz) e pela disponibilidade de esconderijos na área.

4. **Puzzles e Travessia:**
   - Obstáculos mecânicos que exigem o uso das ferramentas de jogo: travessia silenciosa sobre pisos barulhentos, manipulação de luz em áreas escuras ou uso de senhas e códigos aprendidos nos sonhos.

5. **Sala Segura (*Safe Room*):**
   - Toda área deve conter pelo menos uma sala protegida com tranca funcional.
   - É nela que o jogador pode realizar o salvamento de estado e acionar a mecânica de dormir/sonhar para obter novas informações no passado.

---

## 📋 Como Criar uma Nova Fase

Para documentar uma nova fase ou área assim que o grupo fechar o escopo:
1. Copie o arquivo modelo [`template_fase.md`](template_fase.md).
2. Nomeie o novo arquivo seguindo o padrão `nome_da_area.md` (ex.: `biblioteca.md`, `blocos_aula.md`).
3. Preencha todos os campos do template.

# Pendências de produção

O que falta fazer ou decidir em **arte, mecânica, fases e textos já escritos** para o jogo acompanhar a história. Nada aqui muda a história: as perguntas de história ficam no [Enredo Principal](historia/História_Completa.md), seção 10.

Estes itens estavam nas pendências do Enredo até 2026-10-15 e saíram de lá quando o Enredo ficou só com a história. Quando um item for resolvido, ele sai daqui (e, se for decisão de design, entra em [`decisoes.md`](decisoes.md)).

---

## Textos já escritos que citam a versão antiga da história

- **Bunker:** as conversas `dados/dialogos/clarice_primeiro_encontro.json` e `clarice_de_novo.json` e a arte da estação de trabalho (`gerar_clarice.py`) foram feitas para a Clarice no computador da central de dados. A Clarice agora fica no Bloco de salas, e a cena do bunker mostra o **Henrique** na estação. As conversas da Clarice, com as falas de loop ("Você sempre lê" e outras), ficaram sem uso e podem ser apagadas.
- **Zane no bunker:** falta a cena e as conversas dele na sala de dados.
- **Mudanças de 2026-10-15** (em andamento no PR #119): o bilhete da Clarice (`dados/documentos/bilhete_clarice.tres`), [`fases/bunker.md`](fases/bunker.md) (robôs no bunker, o Henrique sozinho) e as conversas do Henrique no bunker (`henrique_primeiro_encontro.json` e `henrique_de_novo.json`).
- **Prólogo:** o `seg_prologo` mostra uma "aula de cálculo", e a cadeira do caderno agora é **Modelagem e Simulação**.

## Personagens: arte e mecânica

- **Diana:** ainda sem visual, então a cena da sala 103 mostra só a Clarice.
- **Henrique:** se o acesso às câmeras do campus vira uma mecânica (ver o campus, avisar de ronda nova).
- **Gadgets:** em que fase cada gadget aparece e se cada um vem de um personagem.

## Fases e cenários

- **Bunker:** o que destrava o setor B (senhas nos disquetes, religar o gerador) e se os robôs entram também no setor B. As **salas antigas**: quantas são, de que épocas e lugares, e onde ficam (a origem fica sem explicação no jogo).
- **Cenários mais futuristas.** Pedido do Davi: os cenários precisam mostrar mais a tecnologia de 3026 (telas, máquinas, a estrutura do centro de pesquisa e do D-Tec), misturada às ruínas e à vegetação. A Biblioteca e o Bloco de salas já estão assim. Falta decidir quanto do resto do campus tem esse visual e onde ele aparece mais.
- **De onde vem a grade horária dos robôs.** Antes vinha da coloração de grafos da semana de provas; hoje a patrulha é programada pelo Carlos, com a IA como ferramenta. Falta decidir como isso aparece no jogo e na apresentação da disciplina.

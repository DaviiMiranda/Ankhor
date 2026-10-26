# Roteiro e Narrativa

Esta pasta abriga a estrutura de roteirização cinematográfica e cutscenes do jogo.

---

## 📚 Mapa da Narrativa Completa

A narrativa e os roteiros do jogo estão distribuídos nos seguintes módulos integrados:

- 📝 **Roteiro (Word):** [`Roteiro.docx`](Roteiro.docx). O documento onde o roteiro é escrito: prólogo e seis atos, um por fase, com o que acontece em cada cena (ações, jogabilidade, caderno e documentos). As falas não ficam nele: cada conversa aparece numa linha FALAS, com o id e um resumo. Como usar está no início do arquivo.
- 🎬 **Cutscenes do Jogo:** [`cutscenes/`](cutscenes/)
  - Padrão de implementação e estrutura técnica de cutscenes no Godot: [`cutscenes/README.md`](cutscenes/README.md)
  - Cutscene de Abertura: [`cutscenes/seg_acordar.md`](cutscenes/seg_acordar.md)
- 📖 **Estrutura Narrativa:** [`../`](../)
  - **Enredo Principal** (a lei do projeto: história, mundo, personagens e pendências): [`../História_Completa.md`](../História_Completa.md)
  - Funcionamento da entrega narrativa e narrativa ambiental: [`../README.md`](../README.md)
  - Modelo para novos documentos e relíquias: [`../template_documento.md`](../template_documento.md)
- 👥 **Personagens:** [`../personagens/`](../personagens/)
  - Uma ficha por personagem; a lista está na seção 4.2 do [Enredo Principal](../História_Completa.md)
  - Modelo para novas fichas: [`../template_personagem.md`](../template_personagem.md)
- 💬 **Diálogos (Word):** [`../dialogos/Dialogos.docx`](../dialogos/Dialogos.docx). Todas as falas do jogo, fase por fase, com os mesmos números de cena do roteiro, as falas novas em rascunho (barra azul) e as revisões das falas. O que toca no jogo continua sendo `dados/dialogos/` (conversas) e `dados/transmissoes/` (rádio e telefone).

---

> [!NOTE]
> Todo roteiro segue o [Enredo Principal](../História_Completa.md), a lei do projeto. Qualquer ideia nova que altere a história deve ser acordada em grupo e entrar no mesmo PR no Enredo Principal e em [`../../decisoes.md`](../../decisoes.md).

---

## ✍️ Guia de escrita

Estas duas partes estavam no Enredo Principal (seções 9 e 10) até 2026-10-15. Saíram de lá porque o Enredo ficou só com a história; aqui servem de guia para quem escreve falas, documentos e cutscenes.

### Temas e tom

- **Estranhamento do familiar:** o jogador reconhece a catraca, o bebedouro, a Biblioteca. O mundo em volta não reconhece mais nada disso.
- **Gente de épocas diferentes:** jovens da mesma idade e do mesmo lugar, separados por séculos, tentando se entender (gírias, costumes, tecnologia).
- **Família e origem:** Gabriel descobre que a família dele sempre esteve naquele chão.
- **Tempo como relógio mortal:** os robôs seguem rotinas, e quem aprende a rotina sobrevive.
- **Vulnerabilidade:** Gabriel é um estudante, não um soldado.
- Terror silencioso, de tensão e mistério, mais do que de susto. O maior choque é perceber **quanto tempo passou**.
- **Público:** 14+, sem violência explícita. Os lugares da Unifor são só cenário; pessoas, pesquisa e acontecimentos são fictícios.

### Como a história chega ao jogador

| Camada | O que é | Onde está |
|---|---|---|
| **Narrativa ambiental** | Marcas no cenário, relíquias de épocas diferentes, os tracinhos nas lousas, os riscos de estrelas na árvore | [`fases/`](../../fases/) |
| **Documentos** | Diários, bilhetes, disquetes. Cada época tem um papel próprio. As pistas úteis viram anotações no **Caderno do Gabriel** | [`mecanicas/registros_e_caderno.md`](../../mecanicas/registros_e_caderno.md) e o modelo [`template_documento.md`](../template_documento.md) |
| **Inventário** | O anel da avó, e a comparação com o anel do Baltazar | [`mecanicas/itens_e_inventario.md`](../../mecanicas/itens_e_inventario.md) |
| **Rádio** | Clarice ao vivo, na frequência do grupo, com o que o Henrique vê nas câmeras, sem pausar o jogo | [`mecanicas/registros_e_caderno.md`](../../mecanicas/registros_e_caderno.md) |
| **Ligações e diálogos** | Zane por telefone; todos em pessoa nos esconderijos, com retratos e escolhas | [`Dialogos.docx`](../dialogos/Dialogos.docx) |
| **Sonhos** | O sono continua como mecânica; o que os sonhos mostram está pendente (Enredo, seção 10.5) | [`mecanicas/sono_e_sonhos.md`](../../mecanicas/sono_e_sonhos.md) |
| **Cutscenes** | A abertura (`seg_prologo` e `seg_acordar`) e as que o grupo decidir | [`cutscenes/`](cutscenes/) |

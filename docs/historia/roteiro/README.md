# Roteiro e Narrativa

Esta pasta abriga a estrutura de roteirização cinematográfica e cutscenes do jogo.

---

## 📚 Mapa da Narrativa Completa

A narrativa e os roteiros do jogo estão distribuídos nos seguintes módulos integrados:

- 🎬 **Cutscenes do Jogo:** [`cutscenes/`](cutscenes/)
  - Padrão de implementação e estrutura técnica de cutscenes no Godot: [`cutscenes/README.md`](cutscenes/README.md)
  - Cutscene de Abertura: [`cutscenes/seg_acordar.md`](cutscenes/seg_acordar.md)
- 📖 **Estrutura Narrativa:** [`../`](../)
  - **Enredo Principal** (a lei do projeto: história, mundo, personagens e pendências): [`../enredo_principal.md`](../enredo_principal.md)
  - Funcionamento da entrega narrativa e narrativa ambiental: [`../README.md`](../README.md)
  - Modelo para novos documentos e relíquias: [`../template_documento.md`](../template_documento.md)
- 👥 **Personagens:** [`../personagens/`](../personagens/)
  - Uma ficha por personagem; a lista está na seção 4.2 do [Enredo Principal](../enredo_principal.md)
  - Modelo para novas fichas: [`../template_personagem.md`](../template_personagem.md)
- 💬 **Diálogos:** [`../../dialogos/`](../../dialogos/)
  - Arquitetura técnica do sistema de diálogos: [`../../dialogos/README.md`](../../dialogos/README.md)
  - Modelo estrutural para redação de falas: [`../../dialogos/template_dialogo.md`](../../dialogos/template_dialogo.md)

---

> [!NOTE]
> Todo roteiro segue o [Enredo Principal](../enredo_principal.md), a lei do projeto. Qualquer ideia nova que altere a história deve ser acordada em grupo e entrar no mesmo PR no Enredo Principal e em [`../../decisoes.md`](../../decisoes.md).

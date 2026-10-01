# Fase — Bunker

> **Status:** Em desenvolvimento (cenário, portas, a Clarice e o primeiro diálogo prontos; salas lacradas para depois)  
> **Área:** bunker de pesquisa embaixo do núcleo da Âncora ("ÂNCORA-03")  
> **No menu Fases:** **Bunker** (começa na entrada)

---

## 1. Visão Geral da Área

- **O que é:** um bunker do centro de pesquisa, construído para proteger a equipe da Âncora. Fechado e seco, ainda de pé depois de mil anos, mas gasto: concreto aparente em cima e tinta verde-oliva descascando embaixo, eletrocalhas com cabos pendurados, portas de aço de correr, faixas de perigo amarelas e pretas.
- **Luz:** só o que a Âncora ainda alimenta. Tubos fluorescentes frios que piscam e luzes de emergência vermelhas. O setor B (lá embaixo) está quase todo no vermelho e alagado.
- **Som:** o zumbido do transformador e da ventilação em todo o bunker, goteiras no setor B e o motor do gerador.
- **Quem vive aqui:** a **Clarice** (1994). Os robôs não descem ao bunker (ou não sabem que ele existe), por isso aqui não há perseguição: é o lugar mais seguro do jogo até agora.
- **Clarice pelas paredes:** "NÃO CONFIE NAS LUZES" pichado no corredor, a seta "→ DADOS C." apontando para a sala dela, "NÃO ABRE. JÁ TENTEI. C." perto das portas lacradas, e o grafo das rotas dos robôs na parede da central.

---

## 2. Topologia e Salas (Nós do Grafo)

Cada ligação é uma `Porta` (`cenas/sistemas/porta.tscn`) com o som da porta blindada. As escadas ficam no mesmo x nos dois corredores.

```
                 ENTRADA ── (escotilha: lacrada)
                    │       (elevador: lacrado)
                    │
  CORREDOR A ── dormitório
   (setor A)  ── refeitório
              ── enfermaria
              ── central de dados (Clarice)
              ── ARSENAL (lacrado)
                    │ escada
                    │
  CORREDOR B ── gerador
   (setor B)  ── depósito
              ── LABORATÓRIO (lacrado)
              ── ARQUIVO (lacrado)
              ── NÚCLEO (comporta, lacrada)
```

| Cena (`cenas/salas/bunker/`) | Largura | O que tem | Itens |
|---|---|---|---|
| `entrada` | 960 | Escada da superfície, descontaminação (chuveiros e faixas de perigo), armários, posto de guarda (mesa, cadeira, lampião), planta de evacuação, elevador lacrado e a porta para o setor A | — |
| `corredor_a` | 2560 | O corredor principal: portas com placas, janela para a sala dos servidores, canos, quadros elétricos, pichações da Clarice e a escada para o setor B | — |
| `corredor_b` | 2240 | Nível de baixo: água no chão, luz vermelha, infiltração nas paredes, três portas lacradas e a **comporta do núcleo** | — |
| `dormitorio` | 960 | Seis beliches, armários, caixas | 1 pilha |
| `refeitorio` | 960 | Mesas compridas de aço, prateleiras de latas, planta do bunker | 1 cápsula de clarão |
| `enfermaria` | 800 | Macas, suportes de soro, biombos, armários de remédios | 1 pilha |
| `central_dados` | 1120 | **A sala da Clarice:** racks de servidores, janela para os servidores, a parede do grafo, a estação dela (três monitores de tubo) e o canto onde ela dorme (colchão, cobertor roxo, latas, lampião) | — |
| `gerador` | 960 | Dois geradores a diesel ligados, tambores de combustível, quadros elétricos | — |
| `deposito` | 800 | Estantes, caixotes, tambores | 1 pilha, 1 cápsula de clarão, 2 pedras |

### Salas lacradas (para fazer depois)

As portas existem, com placa e o visual de porta lacrada (fita vermelha e branca, corrente e cadeado), mas usam `bloqueada = true`: apertar `E` só mostra o aviso e toca a maçaneta emperrada. O notebook não abre porta bloqueada. Quando uma sala for feita, basta tirar o `bloqueada`, preencher `cena_destino` e `porta_destino` e trocar a peça da parede por `bunker_porta`.

| Porta (`id`) | Onde | Aviso de hoje | Ideia |
|---|---|---|---|
| `escada_superficie` | entrada | "A escotilha lá em cima emperrou." | Ligação com as outras fases (por onde o Gabriel chega) |
| `elevador` | entrada | "O elevador está sem energia." | Atalho entre os setores depois de religar a energia no gerador |
| `arsenal` | corredor A | "Arsenal: acesso só com autorização." | Cápsulas de clarão e equipamento |
| `laboratorio` | corredor B | "Lacrada pelo sistema. A Clarice está tentando abrir." | Pesquisa da Âncora; talvez parte da pesquisa do professor |
| `arquivo` | corredor B | idem | Registros da Âncora (o nome de usuário de 2026?) |
| `nucleo` | corredor B (comporta) | "A comporta do núcleo não se mexe. Nem um milímetro." | Acesso ao núcleo da Âncora: reta final |

A própria Clarice explica no diálogo que o setor B está lacrado pelo sistema e que ela está quebrando a senha "um disquete por vez": as salas fechadas viram gancho de história, não parede invisível.

---

## 3. Objetivos e Progressão

- **Hoje:** explorar o bunker, achar a Clarice e conversar com ela (a conversa anota "Clarice está viva" no caderno).
- **A definir com a equipe:** em que ponto da história o Gabriel chega ao bunker (ver `docs/decisoes.md`: a ficha dizia que os dois só se viam no final), o que destrava o setor B (senhas nos disquetes? religar o gerador?) e se os robôs entram aqui em algum momento.

---

## 4. Onde está no projeto

| O quê | Onde |
|---|---|
| Cenas das salas | `cenas/salas/bunker/` |
| Kit do bunker (paredes, chão, objetos) | `cenas/cenario/bunker/`, sprites em `assets/sprites/cenario/bunker/` |
| Gerador do kit | `assets/modelagem/cenario/gerar_bunker.py` |
| Luzes (tubo fluorescente e emergência) | `cenas/cenario/luzes/luz_tubo.tscn`, `luz_emergencia.tscn` |
| Clarice | `cenas/personagens/clarice.tscn` (visual em `assets/sprites/personagens/clarice/visual.md`) |
| Diálogos da Clarice | `dados/dialogos/clarice_primeiro_encontro.json`, `clarice_de_novo.json` |
| Sons | `assets/modelagem/audio/gerar_efeitos_bunker.py` |

### Peças do kit do bunker

- **Paredes (80 × 112):** `bunker_lisa`, `bunker_rachada` (infiltração), `bunker_canos`, `bunker_luminaria` (tubo fluorescente: ponha uma `luz_tubo` em x + 40, y 34), `bunker_emergencia` (giroflex: `luz_emergencia` em x + 40, y 30), `bunker_porta` (aberta), `bunker_porta_fechada`, `bunker_porta_lacrada`, `bunker_comporta`, `bunker_armarios`, `bunker_painel`, `bunker_mapa`, `bunker_grafo`, `bunker_vidro`, `bunker_prateleiras`, `bunker_remedios`, `bunker_descontaminacao`, `bunker_escada_sobe`, `bunker_escada_desce`, e o `pilar_bunker` (16 px) para as pontas.
- **Chão (128 × 68):** `chao_bunker`, `chao_bunker_grade`, `chao_bunker_agua`, `chao_bunker_faixa`.
- **Objetos:** `beliche`, `mesa_refeitorio`, `maca`, `suporte_soro`, `biombo`, `gerador`, `tambor`, `tambor_verde`, `caixas`, `rack_servidor`, `colchao`, `estante_metal`, `latas`, `mesa_metal`.
- **Placas das portas:** são `Label` dentro de `Paredes` (fundo de aço escuro, letra amarela), em cima da plaquinha que as peças de porta já trazem. As pichações da Clarice também são `Label`, em vermelho.

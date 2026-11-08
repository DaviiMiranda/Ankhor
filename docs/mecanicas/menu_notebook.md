# Menu na escrivaninha do Gabriel

Cena independente: `cenas/interface/menu_notebook.tscn`. Abra essa cena no Godot
4.7.x e use **F6**. Por escolha do Davi, o menu inicial atual continua
sendo a entrada do jogo e esta cena fica separada para avaliação.

O cenário usa a geometria da escrivaninha, do notebook, da luminária, da caneca,
dos livros, da janela, da cortina e do cacto do quarto VR. O enquadramento é
fixo, de frente para o notebook, com um céu noturno estrelado atrás dele.
O notebook é remodelado nas dimensões da versão de escala 1,6 e fica na
frente do peitoril. A câmera fica em `(-1.429099, 1.23, -0.2)`, com campo de visão
vertical de 40°, mais próxima da tela. Os arquivos originais do quarto não mudam.

## Arquivos de arte

- `assets/modelagem/menu/menu_notebook.blend`: modelo editável, com câmera,
  iluminação e textos de demonstração separados da geometria.
- `assets/modelos/menu_notebook.glb`: cenário exportado para o Godot, sem os
  textos de demonstração, sem câmera e sem luzes de prévia.
- `assets/modelagem/menu/menu_notebook_previa.png`: renderização do Blender.
- `assets/modelagem/menu/menu_notebook_animacao_previa.png`: quadro da animação
  com a fumaça saindo da caneca.
- `assets/modelagem/menu/gerar_menu_notebook.py`: gerador reproduzível.
- `assets/modelagem/menu/animar_menu_notebook.py`: aplica as animações ao
  `.blend` já editado e reexporta o GLB, preservando ajustes manuais.
- `assets/modelagem/menu/detalhar_menu_notebook.py`: peças e curvas do modelo.
- `assets/modelagem/menu/texturizar_menu_notebook.py`: gerador das texturas.
- `assets/sprites/menu/notebook/`: texturas próprias desta cena.

Para regenerar, na raiz da pasta de trabalho:

```powershell
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' -b --factory-startup --python assets/modelagem/menu/gerar_menu_notebook.py
```

O gerador lê as funções e os materiais de `gerar_sala_visor.py` pela árvore
sintática, sem executar o `main` dele. Assim reaproveita as mesmas peças sem
exportar novamente nem sobrescrever `sala_visor.glb`. No `.blend`, as texturas
ficam empacotadas para que o arquivo continue editável em outro computador.

## Modelagem e materiais de perto

O cenário passa de 2.732 para 71.282 triângulos. As teclas têm geometria
individual, bordas arredondadas e legendas em malha. O notebook tem carcaça
em duas peças, junta, deck metálico, trackpad embutido, dobradiças cilíndricas,
webcam, conectores USB, ventilação, alto-falantes e LED de energia.

As bordas dos móveis recebem chanfros com mais segmentos e normais ponderadas.
A caneca tem parede interna, borda arredondada e alça tubular. O vaso é uma
superfície de revolução; o cacto tem gomos e braços curvos. As curvas recebem
polígonos onde mudam a silhueta, com menos segmentos nos detalhes minúsculos.

A madeira usa mapas de 1024 × 1024; metal, tecido e parede usam 512 × 512.
Cada material tem cor, rugosidade e normal. Os veios e a granulação variam a
cor e o brilho; o gradiente do campo de altura gera o relevo da normal.
São texturas procedurais criadas e salvas pelo Blender, com semente fixa.
Mantêm filtro Nearest e mipmaps para reduzir cintilação à distância.

`texturas_menu_notebook.gd` herda o aplicador do quarto e substitui somente
os materiais refinados. As texturas são projetadas em metros no mundo;
o notebook, a mesa e os objetos compartilham uma escala de detalhe coerente.

Para regenerar apenas os arquivos, sem renderizar a prévia, acrescente
`-- --sem-render` ao comando do Blender. A prévia completa usa Cycles.

## Iluminação noturna

O quarto fica com a luz geral apagada. A luminária da mesa é a única luz
do cenário: luz quente de alcance curto, com sombras, concentrada nos objetos
próximos. A iluminação ambiente e as luzes auxiliares da janela e do notebook
foram retiradas. A tela continua legível pelo material sem sombreamento.
A orientação e a posição da luz no Godot acompanham os ajustes salvos no
arquivo Blender.

A janela usa `assets/sprites/menu/notebook/ceu_noturno.png`, gerado no Blender
com um gradiente azul escuro e estrelas discretas. A paisagem aparece pela
janela sem iluminar o quarto. O céu original do prólogo e do quarto VR não muda.
O arquivo Blender também usa apenas a luminária, com a iluminação do mundo
zerada e o céu excluído dos raios de iluminação indireta.

## Animações discretas

A cortina tem uma chave de forma que mantém o topo preso e desloca pouco a
parte inferior, como uma brisa lenta. Três faixas translúcidas sobem da
posição atual do café, com bordas e pontas suaves. As duas animações duram
cerca de oito segundos e se repetem no menu. No Blender, use a barra de espaço
para reproduzir a linha do tempo entre os quadros 1 e 193.

Para reaplicar as animações depois de ajustar o `.blend`, execute:

```powershell
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' -b assets/modelagem/menu/menu_notebook.blend --python assets/modelagem/menu/animar_menu_notebook.py
```

O script encontra a superfície do café na geometria atual; por isso a fumaça
acompanha mudanças de posição da caneca quando o café é movido junto.

Se as animações já estiverem no `.blend` e a intenção for apenas atualizar o
jogo com ajustes manuais, salve o arquivo no Blender e use `--apenas-exportar`.
Esse modo não recria a fumaça nem a cortina:

```powershell
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' -b assets/modelagem/menu/menu_notebook.blend --python assets/modelagem/menu/animar_menu_notebook.py -- --apenas-exportar
```

## Interface e entrada

`tela_menu_notebook.tscn` contém a interface do menu, com o script
`tela_menu_notebook.gd` herdando de `menu_principal.gd`. As ações de campanha,
os seis espaços de salvamento, as fases, as configurações, os controles,
os créditos e os sons continuam usando a implementação existente.

A interface é desenhada em um `SubViewport` de 256 × 160. A textura dele
é o material da malha `TelaNotebook`: os botões ficam no aparelho em 3D.
A fonte continua Galmuri7 em tamanhos 8 e 16 e com filtro Nearest. A tela é
LCD; não recebe a máscara arredondada de CRT do antigo monitor.

O mouse é convertido com uma interseção entre seu raio e o plano da tela.
Se O é o canto superior esquerdo e U e V são os vetores das duas bordas,
um ponto P na tela tem coordenadas:

```text
u = produto_escalar(P - O, U) / comprimento_ao_quadrado(U)
v = produto_escalar(P - O, V) / comprimento_ao_quadrado(V)
pixel = (u, v) * tamanho_do_viewport
```

As coordenadas UV do GLB identificam os cantos. O cálculo acompanha a
resolução da janela, sem uma região de clique fixa na imagem.
O controlador encaminha os eventos ao viewport do notebook usando
[`Viewport.push_input`](https://docs.godotengine.org/en/stable/classes/class_viewport.html#class-viewport-method-push-input).
Mouse, roda, setas, WASD, Enter/E, Esc e controle usam esse mesmo caminho.

O cenário 3D é desenhado na resolução da janela, com MSAA 2×, como o quarto
VR. A interface externa continua na base 640 × 360. O enquadramento é fixo
para manter o texto e as regiões de clique estáveis.

## Validação

Conferido no Godot 4.7.2 com renderização OpenGL Compatibility:

- Foco inicial, cliques e projeção do mouse sobre os botões do notebook.
- Abrir Opções, Controles, Créditos e Fases; voltar com Esc.
- Mover a seleção com setas e confirmar com E.
- Projeção do mouse e resolução do 3D em 1280 × 720, 1920 × 1080 e 1024 × 768.
- Os quatro cantos da tela do notebook continuam visíveis nessas resoluções.
- Novo jogo abre `seg_prologo.tscn`.
- Importação final limpa e execução sem erros de script.

Captura do jogo: `assets/modelagem/menu/menu_notebook_godot.png`.

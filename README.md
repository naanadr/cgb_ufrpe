# cgb_ufrpe
Projeto da disciplina de Computação Gráfica Básica ministrada na UFRPE

## Especificação do Projeto

Carregar na memória uma malha de triângulos referente a um objeto 3D armazenada em arquivo de texto e desenhar seus vértices na tela. O arquivo utilizado para armazenar uma malha com **n vértices** e **k triângulos** possui o seguinte formato:

```
<no de vértices> <no de triângulos>
<coordenada x do vértice 1> <coordenada y do vértice 1> <coordenada z do vértice 1>
<coordenada x do vértice 2> <coordenada y do vértice 2> <coordenada z do vértice 2>
...
<coordenada x do vértice n> <coordenada y do vértice n> <coordenada z do vértice n>
<índice do vértice 1 do triângulo 1> <índice do vértice 2 do triângulo 1> <índice do vértice 3 do triângulo 1>
<índice do vértice 1 do triângulo 2> <índice do vértice 2 do triângulo 2> <índice do vértice 3 do triângulo 2>
...
<índice do vértice 1 do triângulo k> <índice do vértice 2 do triângulo k> <índice do vértice 3 do triângulo k>
```

Uma vez que a malha foi carregada na memória, deve-se obter a projeção em perspectiva de seus vértices.

A aplicação deverá carregar a partir de um arquivo de texto os seguintes parâmetros da
câmera virtual:
* Ponto C;
* Vetores N e V;
* Escalares d, hx e hy.

Exemplo de parâmetros de câmera:
```
N = 0 1 -1
V = 0 -1 -1
d = 5
hx = 2
hy = 2
C = 0 -500 500
```

![parametros](docs/parametros.png)

> hx, hy: escalares que determinam o retângulo de vista.
> C: ponto de foco
> d: escalar que define distância do foco ao plano de vista
> U, V, N : base ortonormal que determina sistema de coordenadas de vista


O usuário deve ser capaz de alterar os valores dos parâmetros no arquivo de texto, recarregá-los e redesenhar o objeto sem precisar fechar a aplicação e abri-la novamente (ex: o usuário pode pressionar uma tecla específica para recarregar os parâmetros a partir do arquivo de texto e redesenhar o objeto).

Deve-se converter os vértices do objeto de coordenadas mundiais para coordenadas de vista, realizar a projeção em perspectiva, converter para coordenadas normalizadas e por fim para coordenadas de tela. Após isso, deve-se utilizar o algoritmo de rasterização de polígonos scan line conversion (varredura) para preencher os triângulos projetados. Os pixels da tela correspondentes aos triângulos projetados e preenchidos devem ser pintados de branco, enquanto que os demais pixels devem ser pintados de preto.

A única função gráfica que pode ser utilizada é a que desenha um pixel colorido na tela. Apenas as bibliotecas padrão da linguagem escolhida podem ser usadas.

OBS.: caso desejado, é permitido usar uma biblioteca externa que ofereça a função de pintar um pixel colorido na tela.

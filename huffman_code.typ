#import "@preview/klaro-ifsc-sj:0.1.0": report
#show: doc => report(
  title: "Avaliação: Códigos de Huffman",
  subtitle: "SISTEMAS DE COMUNICAÇÃO II (COM029008)",
  // Se apenas um autor colocar , no final para indicar que é um array
  authors:("Rhenzo Hideki Silva Kajikawa",),
  date: "27 de Janeiro de 2025",
  doc,
)

= Introdução

= Desenvolvimento
== Questão 1
Considere uma fonte discreta sem memória (DMS) com alfabeto dado por $𝒳 = {𝑎, 𝑏, 𝑐}$ e probabilidades respectivas dadas por $𝑝_𝑋 = [ 3/10 , 6/10 , 1/10 ]$.
\ (a) Calcule a entropia da fonte.
\ (b) Determine um código de Huffman para a fonte. Qual o comprimento médio do código obtido?
\ (c) Calcule a entropia da extensão de segunda ordem da fonte.
\ (d) Determine um código de Huffman para a extensão de segunda ordem da fonte. Qual o comprimento médio do código obtido? Comente o resultado.

== Calculo da entropia da fonte
Para calcular a entropia da fonte será utilizada a seguinte formula:
$
H(X) = - sum _(x in X ) p(x)log_2 p(x)
$

Logo para está fonte podemos:
$
H(X) = 3/10 dot log_2(3/10) + 6/10 dot log_2(6/10) + 1/10 dot log_2(1/10)
$

$
H(X) = 0,521 + 0,442 + 0,332 = 1,295
$


== Código Huffman da fonte e comprimento
Para fazer o código Huffman e o comprimento iremos fazer primeiro o diagrama:

#figure(
  image("./DiagramaHuffman.jpg",width:100%),
  caption: [
   Fonte: Elaborada pelo autor
  ],
  supplement: "Figura"
);
A partir desse diagrama é possivel achar que :
dado por $𝒳 = {𝑎, 𝑏, 𝑐}$ temos  $[(1, 0), (0), (1, 1)]$

Agora para calcular o comprimento temos :
$
l = 1 * 0,6 + 2*0,3 + 2*0,1
l = 1.4 "bits/letras"
$
== Calculo da extensão do código de Huffman para para segunda

== Determinando a extensão de segunda ordem e comprimento médio


== Questão 2

= Conclusão
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

#pagebreak()
= Desenvolvimento
== Questão 1
Considere uma fonte discreta sem memória (DMS) com alfabeto dado por $𝒳 = {𝑎, 𝑏, 𝑐}$ e probabilidades respectivas dadas por $𝑝_𝑋 = [ 3/10 , 6/10 , 1/10 ]$.
\ (a) Calcule a entropia da fonte.
\ (b) Determine um código de Huffman para a fonte. Qual o comprimento médio do código obtido?
\ (c) Calcule a entropia da extensão de segunda ordem da fonte.
\ (d) Determine um código de Huffman para a extensão de segunda ordem da fonte. Qual o comprimento médio do código obtido? Comente o resultado.
#pagebreak()
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

Código para validar:
```py
import komm
import numpy as np  

px = [3/10, 6/10, 1/10]

#Calculando entropia da fonte
dms = komm.DiscreteMemorylessSource(px)
print(dms.entropy())
```
#pagebreak()
== Código Huffman da fonte e comprimento
Para fazer o código Huffman e o comprimento iremos fazer primeiro o diagrama:

#figure(
  image("./Figures/DiagramaHuffman.jpg",width:100%),
  caption: [
   Fonte: Elaborada pelo autor
  ],
  supplement: "Figura"
);
A partir desse diagrama é possivel achar que :
dado por $𝒳 = {𝑎, 𝑏, 𝑐}$ temos  $[10, 0, 11]$

Agora para calcular o comprimento temos :
$
l = 1 * 0,6 + 2*0,3 + 2*0,1
l = 1.4 "bits/letras"
$

Código para validar:
```py
huffman_code = komm.HuffmanCode(px)
print(huffman_code.codewords , huffman_code.rate(px))
```
#pagebreak()
== Calculo da extensão do código de Huffman para para segunda
Para extender o código para a segunda ordem, é seguida da seguinte forma :
$
  X^2 = {"aa","ab","ac","bb","ba","bc","cc","ca","cb"}
\ P_x ^2 = {"0.09","0.18","0.03","0.36","0.18","0.06","0.01","0.03","0.06"}
\ H(X^2 ) = 0.09 dot log_2(0.09) + 0.18 dot log_2(0.18) + 0.03 dot log_2(0.03) \ + 0.36 dot log_2(0.36) + 0.18 dot log_2(0.18) + 0.06 dot log_2(0.06) \ + 0.01 dot log_2(0.01) + 0.03 dot log_2(0.03) + 0.06 dot log_2(0.06)
\ H(X^2) = 2.59 "bits/superpalavras"
$

Código para validar:
```py
H_X = dms.entropy()

# Entropia da extensão de segunda ordem
H_X2 = 2 * H_X

print(f"Entropia da fonte original (H(X)): {H_X:.4f} bits")
print(f"Entropia da extensão de segunda ordem (H(X^2)): {H_X2:.4f} bits")
```
#pagebreak()
== Determinando a extensão de segunda ordem e comprimento médio
#figure(
  image("./Figures/DiagramaHuffman-Página-2.jpg",width:100%),
  caption: [
   Fonte: Elaborada pelo autor
  ],
  supplement: "Figura"
);

$
   X^2 = {"aa","ab","ac","bb","ba","bc","cc","ca","cb"}
  \ "Temos na sequência as palavras"
  \ {0100,11,010100,10,00,0111,01011,0110,010101}
  
$
Para o comprimento médio temos:
$
\ {"aa","ab","ac","bb","ba","bc","cc","ca","cb"}
\  {"0.09","0.18","0.03","0.36","0.18","0.06","0.01","0.03","0.06"}
\  {0100,    11, 010100,   00,   10,    0111, 010101,01011,0110 }
\  {4,2,6,2,2,4,5,4,6}
\ l = 0.09*4 + 0.18*2 + 0.03*6  +0.36*2 + 0.18*2 + 0.06*4 + 0.01*6+0.03*5+0.06*4
\ l = 2.67
$
#pagebreak()
Código para validar:
```py
# Símbolos e probabilidades da fonte original
symbols = ['a', 'b', 'c']
probabilities = [3/10, 6/10, 1/10]

# Criação dos símbolos da extensão de segunda ordem
symbols_second_order = [s1 + s2 for s1 in symbols for s2 in symbols]

# Cálculo das probabilidades da extensão de segunda ordem
probabilities_second_order = [p1 * p2 for p1 in probabilities for p2 in probabilities]

# Criação do código de Huffman para a extensão de segunda ordem
huffman_code_second_order = komm.HuffmanCode(probabilities_second_order)

# Exibição do código de Huffman
print("Código de Huffman para a extensão de segunda ordem:")
for symbol, code in zip(symbols_second_order, huffman_code_second_order.codewords):
    print(f"Símbolo: {symbol}, Código: {code}")

# Cálculo do comprimento médio do código
average_code_length = sum(len(code) * prob for code, prob in zip(huffman_code_second_order.codewords, probabilities_second_order))
print(f"Comprimento médio do código: {average_code_length:.4f}")
```
#pagebreak()
== Questão 2

#pagebreak()
= Conclusão
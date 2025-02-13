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
Escreva um programa para comprimir e descomprimir arquivos de texto usando códigos de
Huffman. Seu programa deve:

• Determinar a frequência de cada caractere do arquivo de entrada.

• Utilizar essas frequências para construir o código de Huffman.

• Comprimir o arquivo de entrada .txt usando o código de Huffman, gerando um arquivo de saída com extensão .bin.

• Descomprimir o arquivo de saída .bin , gerando um arquivo .txt idêntico ao arquivo de entrada.

Por simplicidade, assuma que o código de Huffman seja conhecido tanto na compressão quanto na descompressão — na prática, o código deve ser armazenado no arquivo de saída para que o arquivo de entrada possa ser descomprimido.

Teste seu programa com o livro Alice’s Adventures in Wonderland, de Lewis Carroll, disponível em https://www.gutenberg.org/files/11/11-0.txt. Para este caso, determine:

(a) A entropia da distribuição de frequências dos caracteres do livro.

(b) O comprimento médio do código de Huffman obtido.

(c) O tamanho (em bytes) e a taxa de compressão do arquivo comprimido

Compare com a tabela a seguir, que mostra o tamanho do arquivo original e dos arquivos comprimidos com diferentes formatos de compressão

#align(center)[
#table(
  columns: (auto,auto,auto),
  table.header([Formato],[Tamanho(bytes)],[Taxa de compressão]),
  [original], [154573], [0.00%],
  [zip], [54176], [64.95%],
  [gz], [54037], [65.04%],
  [zst], [48789], [68.44%],
  [7z], [48280], [68.77%],
  [xz], [48232], [68.80%],
  [bz2], [42779], [72.32%],
  [bz3], [40362], [73.89%]
)
]

#pagebreak()
== Entropia da distribuição e Comprimento médio
Para fazer o calculo de entropia é necessário fazer a abertura e leitura do arquivo e armazenar a quantia de caracteres.
sendo assim foi criado uma função para fazer a contagem dos characteres, gerar e gerar a pmf
```py

def contar_caracteres(arquivo):
    contador = {}
    pmf = {}
    
    # Ler o arquivo e contar caracteres
    with open(arquivo, 'rb') as f:  # Mudado para 'rb'
        texto = f.read().decode('utf-8')  # Decodifica após ler os bytes
        total_chars = len(texto)
        
        for char in texto:
            contador[char] = contador.get(char, 0) + 1
    
    # Calcular PMF
    for char, freq in contador.items():
        pmf[char] = freq / total_chars
    
    return contador, pmf, texto
```
```py
arquivo = 'alice.txt'

# Contar caracteres e obter texto
contador, pmf, texto_original = contar_caracteres(arquivo)


# Exibir contagem de caracteres em ordem decrescente
print("Contagem de caracteres:")
# Ordenar por quantidade (valor) em ordem decrescente
for char, quantidade in sorted(contador.items(), key=lambda x: x[1], reverse=True):
    print(f'{char}: {quantidade}')
```
Esta primeira parte apenas mostra os characteres e a sua respectiva quantidade no livro.
```Bash
Contagem de caracteres:
 : 24633
e: 13552
t: 10345
a: 8239
...
```
Após apresentar os caracteres é mostrada a pmf , calculada a entropia e comprimento médio  
```py
# Ordenar a PMF em ordem decrescente
sorted_pmf = sorted(pmf.items(), key=lambda item: item[1], reverse=True)

# Criar código de Huffman
probs = [prob for _, prob in sorted_pmf]



print("\nPMF:")
for char, prob in sorted_pmf:
    print(f'{char}: {prob:.6f}')
    
huffman = komm.HuffmanCode(probs)

dms = komm.DiscreteMemorylessSource(probs)
print("A entropia da distribuição de frequências dos caracteres do livro:", dms.entropy())
print("Comprimento médio do código de Huffman obtido:", huffman.rate(probs))
```
temos como saida:
```sh

PMF:
 : 0.166352
e: 0.091519
t: 0.069862
a: 0.055640
o: 0.054519
...
A entropia da distribuição de frequências dos caracteres do livro: 4.620542049477668
Comprimento médio do código de Huffman obtido: 4.661185321249611
```
Assim é obtido que a entropia obtida pelo livro é de aproximadamente 4.62 e o comprimento médio do código de huffman obtido é de 4.66
== Tamanho (em bytes) e a taxa de compressão do arquivo comprimido

#pagebreak()
= Conclusão
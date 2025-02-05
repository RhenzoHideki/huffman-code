# Célula 1: Importações e Funções
from collections import Counter
import numpy as np
import komm
import math
import matplotlib.pyplot as plt

def contar_caracteres(arquivo):
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            texto = f.read()
        contador = Counter(texto)
        total_caracteres = sum(contador.values())
        pmf = {char: quantidade / total_caracteres for char, quantidade in contador.items()}
        return contador, pmf, texto
    except FileNotFoundError:
        print("Arquivo não encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

def percentage(occurrences, total):
    return [occurrence / total for occurrence in occurrences]

# Célula 2: Ler arquivo, contar caracteres e calcular PMF
arquivo = 'pg11.txt'  # Substitua pelo caminho do seu arquivo
contador, pmf, texto = contar_caracteres(arquivo)

# Ordenar PMF e exibir resultados
sorted_pmf = sorted(pmf.items(), key=lambda item: item[1], reverse=True)
print("Contagem de caracteres:")
for char, quantidade in sorted(contador.items()):
    print(f'{char}: {quantidade}')
print("\nPMF:")
for char, prob in sorted_pmf:
    print(f'{char}: {prob:.6f}')

# Célula 3: Gráficos de Ocorrências e Porcentagens
letters = list(contador.keys())
occurrences = list(contador.values())
total_letters = sum(occurrences)
percentages = percentage(occurrences, total_letters)

# Gráfico de Ocorrências (Escala Logarítmica)
sorted_letters = [letter for _, letter in sorted(zip(occurrences, letters), reverse=True)]
sorted_occurrences = [occurrence for occurrence, _ in sorted(zip(occurrences, letters), reverse=True)]

plt.figure(figsize=(16, 9))
plt.bar(sorted_letters, sorted_occurrences)
plt.yscale("log")
plt.xlabel("Letters")
plt.ylabel("Occurrences")
plt.title("Occurrences of each Character (Log Scale)")
plt.show()

# Gráfico de Porcentagem (Escala Logarítmica)
sorted_percentages = [percentage for _, percentage in sorted(zip(occurrences, percentages), reverse=True)]

plt.figure(figsize=(16, 9))
plt.bar(sorted_letters, sorted_percentages)
plt.xlabel("Letter")
plt.ylabel("Percentage")
plt.title("Percentage of each Character (Log Scale)")
plt.yscale("log")
plt.show()

# Célula 4: Código de Huffman e Codificação/Decodificação
probs = [prob for _, prob in sorted_pmf]
huff = komm.HuffmanCode(probs)
print("\nCódigo de Huffman:")
for (char, _), codeword in zip(sorted_pmf, huff.codewords):
    print(f'{char}: {codeword}')

# Indexação de Caracteres
index = {i: letter for i, letter in enumerate(letters)}
encoded_text = [list(index.keys())[list(index.values()).index(letter)] for letter in texto]
huff_encoded = huff.encode(encoded_text)

# Exportar texto codificado
with open("huff_encoded.com2", "w") as file:
    file.write("".join(map(str, huff_encoded)))

# Ler e decodificar o texto
with open("huff_encoded.com2", "r") as file:
    huff_encoded = file.read()

huff_encoded_list = list(map(int, huff_encoded))
decoded_text = huff.decode(huff_encoded_list)
decoded_text = [index[i] for i in decoded_text]

# Salvar texto decodificado
with open("huff_decoded.txt", "w") as file:
    file.write("".join(decoded_text))

print("\nTexto decodificado (primeiros 100 caracteres):")
print("".join(decoded_text[:100]))
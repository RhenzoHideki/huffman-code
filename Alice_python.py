from collections import Counter
import numpy as np
import komm
import struct

def contar_caracteres(arquivo):
    contador = {}
    pmf = {}
    
    # Ler o arquivo e contar caracteres
    with open(arquivo, 'r', encoding='Unicode') as f:
        texto = f.read()
        total_chars = 0
        
        for char in texto:
            if char in contador:
                contador[char] += 1
            else:
                contador[char] = 1
            total_chars += 1
    
    # Calcular PMF (Função Massa de Probabilidade)
    for char in contador:
        pmf[char] = contador[char] / total_chars
    
    return contador, pmf, texto

def contar_bytes(arquivo):
    try:
        with open(arquivo, 'rb') as f:
            conteudo = f.read()
            tamanho_bytes = len(conteudo)
            
        return {
            'bytes': tamanho_bytes,
            'KB': round(tamanho_bytes / 1024, 2),
            'MB': round(tamanho_bytes / (1024 * 1024), 2)
        }
    except FileNotFoundError:
        return f"Erro: Arquivo '{arquivo}' não encontrado."
    except Exception as e:
        return f"Erro ao ler arquivo: {str(e)}"

def comprimir_arquivo(texto, huffman, caracteres_ordenados, arquivo_saida):
    # Criar dicionário de códigos
    codigos = {}
    for i, char in enumerate(caracteres_ordenados):
        code = huffman.encode([i])
        codigos[char] = ''.join(map(str, code))
    
    # Codificar o texto
    texto_codificado = ''.join(codigos[char] for char in texto)
    
    # Adicionar padding
    padding = 8 - (len(texto_codificado) % 8)  # Corrigido aqui
    if padding != 8:
        texto_codificado += '0' * padding
    
    # Converter para bytes
    bytes_array = bytearray()
    for i in range(0, len(texto_codificado), 8):
        byte = texto_codificado[i:i+8]
        bytes_array.append(int(byte, 2))
    
    # Salvar arquivo comprimido
    with open(arquivo_saida, 'wb') as f:
        # Escrever padding
        f.write(bytes([padding]))
        
        # Escrever número de caracteres
        f.write(struct.pack('I', len(caracteres_ordenados)))
        
        # Escrever caracteres e seus tamanhos
        for char in caracteres_ordenados:
            char_bytes = char.encode('Unicode')
            f.write(struct.pack('B', len(char_bytes)))  # Tamanho do caractere em bytes
            f.write(char_bytes)  # O caractere em si
        
        # Escrever dados comprimidos
        f.write(bytes_array)
    
    return len(bytes_array) + 5 + sum(len(char.encode('Unicode')) + 1 for char in caracteres_ordenados)

def descomprimir_arquivo(arquivo_entrada, arquivo_saida, huffman, caracteres_ordenados):
    with open(arquivo_entrada, 'rb') as f:
        # Ler padding
        padding = int.from_bytes(f.read(1), byteorder='big')
        
        # Ler número de caracteres
        num_chars = struct.unpack('I', f.read(4))[0]
        
        # Ler caracteres
        chars = []
        for _ in range(num_chars):
            char_size = struct.unpack('B', f.read(1))[0]  # Ler tamanho do caractere
            char = f.read(char_size).decode('Unicode')  # Ler e decodificar o caractere
            chars.append(char)
        
        # Ler dados comprimidos
        dados_comprimidos = f.read()
    
    # Converter para bits
    bits = ''.join(format(byte, '08b') for byte in dados_comprimidos)
    if padding != 8:
        bits = bits[:-padding]
    
    # Criar dicionário reverso de códigos
    codigos_reversos = {}
    for i, char in enumerate(caracteres_ordenados):
        code = huffman.encode([i])
        codigos_reversos[''.join(map(str, code))] = char
    
    # Decodificar
    codigo_atual = ''
    texto_decodificado = ''
    for bit in bits:
        codigo_atual += bit
        if codigo_atual in codigos_reversos:
            texto_decodificado += codigos_reversos[codigo_atual]
            codigo_atual = ''
    
    # Salvar arquivo descomprimido
    with open(arquivo_saida, 'w', encoding='Unicode') as f:
        f.write(texto_decodificado)

# Arquivo de entrada
arquivo = 'alice.txt'

# Contar caracteres e obter texto
contador, pmf, texto_original = contar_caracteres(arquivo)

# Ordenar PMF e caracteres
sorted_pmf = sorted(pmf.items(), key=lambda x: x[1], reverse=True)
caracteres_ordenados = [char for char, _ in sorted_pmf]
probs = [prob for _, prob in sorted_pmf]

# Criar código de Huffman
huffman = komm.HuffmanCode(probs)

# Exibir estatísticas iniciais
print("\nEstatísticas iniciais:")
dms = komm.DiscreteMemorylessSource(probs)
print(f"Entropia da distribuição: {dms.entropy():.4f} bits/símbolo")
print(f"Comprimento médio do código: {huffman.rate(probs):.4f} bits/símbolo")

# Comprimir arquivo
arquivo_comprimido = 'alice.bin'
tamanho_comprimido = comprimir_arquivo(texto_original, huffman, caracteres_ordenados, arquivo_comprimido)

# Descomprimir arquivo
arquivo_descomprimido = 'alice_descomprimido.txt'
descomprimir_arquivo(arquivo_comprimido, arquivo_descomprimido, huffman, caracteres_ordenados)

# Calcular e exibir estatísticas finais
tamanho_original = contar_bytes(arquivo)['bytes']
tamanho_descomprimido = contar_bytes(arquivo_descomprimido)['bytes']
taxa_compressao = (1 - (tamanho_comprimido / tamanho_original)) * 100

print("\nEstatísticas de compressão:")
print(f"Tamanho original: {tamanho_original:,} bytes")
print(f"Tamanho comprimido: {tamanho_comprimido:,} bytes")
print(f"Tamanho descomprimido: {tamanho_descomprimido:,} bytes")
print(f"Taxa de compressão: {taxa_compressao:.2f}%")
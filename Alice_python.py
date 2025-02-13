from collections import Counter
import numpy as np
import komm
import struct

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

def criar_codigo_huffman(pmf):
    """Cria os códigos de Huffman usando diretamente as probabilidades"""
    # Converter o dicionário PMF em uma lista ordenada de probabilidades
    sorted_pmf = sorted(pmf.items(), key=lambda x: x[1], reverse=True)
    caracteres = [char for char, _ in sorted_pmf]
    probabilidades = [prob for _, prob in sorted_pmf]
    
    # Criar o código Huffman
    huffman = komm.HuffmanCode(probabilidades)
    
    # Converter os codewords (que são tuplas) em strings binárias
    codigos = {}
    for i, char in enumerate(caracteres):
        codeword = huffman.codewords[i]
        codigo_binario = ''.join(str(bit) for bit in codeword)
        codigos[char] = codigo_binario
    
    return huffman, codigos
def comprimir_arquivo(texto, codigos, arquivo_saida):
    """Codifica o texto e salva como arquivo binário com a tabela de códigos embutida"""
    # Codificar o texto
    texto_codificado = ''.join(codigos[char] for char in texto)
    
    # Adicionar padding
    padding = 8 - (len(texto_codificado) % 8)
    if padding != 8:
        texto_codificado += '0' * padding
    
    # Converter para bytes
    bytes_array = bytearray()
    for i in range(0, len(texto_codificado), 8):
        byte = texto_codificado[i:i+8]
        bytes_array.append(int(byte, 2))
    
    # Salvar arquivo comprimido
    with open(arquivo_saida, 'wb') as f:
        # Salvar padding
        f.write(bytes([padding]))
        
        # Salvar tabela de códigos
        # Primeiro salvamos o número de entradas na tabela
        f.write(struct.pack('I', len(codigos)))
        
        # Salvar cada par (caractere, código)
        for char, code in codigos.items():
            # Salvar o caractere
            char_bytes = char.encode('utf-8')
            f.write(struct.pack('B', len(char_bytes)))
            f.write(char_bytes)
            
            # Salvar o código
            code_len = len(code)
            f.write(struct.pack('B', code_len))
            f.write(int(code, 2).to_bytes((code_len + 7) // 8, byteorder='big'))
        
        # Salvar dados comprimidos
        f.write(bytes_array)
    
    return len(bytes_array)

def descomprimir_arquivo(arquivo_entrada, arquivo_saida):
    """Lê o arquivo binário e reconstrói o texto original usando a tabela de códigos embutida"""
    with open(arquivo_entrada, 'rb') as f:
        # Ler padding
        padding = int.from_bytes(f.read(1), byteorder='big')
        
        # Ler tabela de códigos
        num_codes = struct.unpack('I', f.read(4))[0]
        codigos = {}
        
        # Reconstruir tabela de códigos
        for _ in range(num_codes):
            # Ler caractere
            char_size = struct.unpack('B', f.read(1))[0]
            char = f.read(char_size).decode('utf-8')
            
            # Ler código
            code_len = struct.unpack('B', f.read(1))[0]
            code_bytes = f.read((code_len + 7) // 8)
            code = format(int.from_bytes(code_bytes, byteorder='big'), f'0{code_len}b')
            
            codigos[char] = code
        
        # Ler dados comprimidos
        dados_comprimidos = f.read()
    
    # Converter para bits
    bits = ''.join(format(byte, '08b') for byte in dados_comprimidos)
    if padding != 8:
        bits = bits[:-padding]
    
    # Decodificar
    codigos_reversos = {v: k for k, v in codigos.items()}
    codigo_atual = ''
    texto_decodificado = []
    
    for bit in bits:
        codigo_atual += bit
        if codigo_atual in codigos_reversos:
            texto_decodificado.append(codigos_reversos[codigo_atual])
            codigo_atual = ''
    
    # Salvar arquivo descomprimido
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        f.write(''.join(texto_decodificado))
        
# Arquivo de entrada
arquivo = 'alice.txt'

# Contar caracteres e obter texto
contador, pmf, texto_original = contar_caracteres(arquivo)

# Criar código de Huffman
huffman, codigos = criar_codigo_huffman(pmf)

print("Começo dos códigos:\n",codigos)
print("\nFinal dos códigos")

# Exibir estatísticas iniciais
print("\nEstatísticas iniciais:")
dms = komm.DiscreteMemorylessSource(list(pmf.values()))
print(f"Entropia da distribuição: {dms.entropy():.4f} bits/símbolo")
print(f"Comprimento médio do código: {huffman.rate(list(pmf.values())):.4f} bits/símbolo")

# Comprimir arquivo
arquivo_comprimido = 'alice.bin'
tamanho_comprimido = comprimir_arquivo(texto_original, codigos, arquivo_comprimido)

# Descomprimir arquivo
arquivo_descomprimido = 'alice_descomprimido.txt'
descomprimir_arquivo(arquivo_comprimido, arquivo_descomprimido)

# Calcular e exibir estatísticas finais
tamanho_original = contar_bytes(arquivo)['bytes']
tamanho_descomprimido = contar_bytes(arquivo_descomprimido)['bytes']
taxa_compressao = (1 - (tamanho_comprimido / tamanho_original)) * 100

print("\nEstatísticas de compressão:")
print(f"Tamanho original: {tamanho_original:,} bytes")
print(f"Tamanho comprimido: {tamanho_comprimido:,} bytes")
print(f"Tamanho descomprimido: {tamanho_descomprimido:,} bytes")
print(f"Taxa de compressão: {taxa_compressao:.2f}%")

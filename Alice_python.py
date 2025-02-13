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
    """Cria os códigos de Huffman corretamente associando caracteres aos códigos binários"""
    sorted_pmf = sorted(pmf.items(), key=lambda x: x[1], reverse=True)
    caracteres_ordenados = [char for char, _ in sorted_pmf]
    probs = [prob for _, prob in sorted_pmf]

    huffman = komm.HuffmanCode(probs)

    # Gerar os códigos corretamente
    codigos = {caracteres_ordenados[i]: ''.join(map(str, huffman.encode([i]))) for i in range(len(caracteres_ordenados))}
    
    return huffman, codigos, caracteres_ordenados


def comprimir_arquivo(texto, codigos, caracteres_ordenados, arquivo_saida):
    """Codifica o texto e salva como arquivo binário"""
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
        # Escrever cabeçalho
        f.write(bytes([padding]))
        f.write(struct.pack('I', len(caracteres_ordenados)))
        
        # Escrever tabela de caracteres
        for char in caracteres_ordenados:
            char_bytes = char.encode('utf-8')
            f.write(struct.pack('B', len(char_bytes)))
            f.write(char_bytes)
        
        # Escrever dados comprimidos
        f.write(bytes_array)
    
    return len(bytes_array) + 5 + sum(len(char.encode('utf-8')) + 1 for char in caracteres_ordenados)

def descomprimir_arquivo(arquivo_entrada, arquivo_saida, codigos, caracteres_ordenados):
    """Lê o arquivo binário e reconstrói o texto original"""
    with open(arquivo_entrada, 'rb') as f:
        # Ler cabeçalho
        padding = int.from_bytes(f.read(1), byteorder='big')
        num_chars = struct.unpack('I', f.read(4))[0]
        
        # Ler tabela de caracteres
        chars = []
        for _ in range(num_chars):
            char_size = struct.unpack('B', f.read(1))[0]
            char = f.read(char_size).decode('utf-8')
            chars.append(char)
        
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
huffman, codigos, caracteres_ordenados = criar_codigo_huffman(pmf)

# Exibir estatísticas iniciais
print("\nEstatísticas iniciais:")
dms = komm.DiscreteMemorylessSource(list(pmf.values()))
print(f"Entropia da distribuição: {dms.entropy():.4f} bits/símbolo")
print(f"Comprimento médio do código: {huffman.rate(list(pmf.values())):.4f} bits/símbolo")

# Comprimir arquivo
arquivo_comprimido = 'alice.bin'
tamanho_comprimido = comprimir_arquivo(texto_original, codigos, caracteres_ordenados, arquivo_comprimido)

# Descomprimir arquivo
arquivo_descomprimido = 'alice_descomprimido.txt'
descomprimir_arquivo(arquivo_comprimido, arquivo_descomprimido, codigos, caracteres_ordenados)

# Calcular e exibir estatísticas finais
tamanho_original = contar_bytes(arquivo)['bytes']
tamanho_descomprimido = contar_bytes(arquivo_descomprimido)['bytes']
taxa_compressao = (1 - (tamanho_comprimido / tamanho_original)) * 100

print("\nEstatísticas de compressão:")
print(f"Tamanho original: {tamanho_original:,} bytes")
print(f"Tamanho comprimido: {tamanho_comprimido:,} bytes")
print(f"Tamanho descomprimido: {tamanho_descomprimido:,} bytes")
print(f"Taxa de compressão: {taxa_compressao:.2f}%")

import numpy as np

# Matriz chave
matriz_chave = np.array([[4, 3], [1, 2]])
matriz_chave_inv = np.linalg.inv(matriz_chave)

# Modulo 27 alfabeto (A-Z + espaço)
mod = 27

# Função para encontrar o inverso modular de um número
def mod_inv(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError(f"Não existe inverso modular para {a} no módulo {m}")

# Inverso da matriz chave no modulo 27
det = int(np.round(np.linalg.det(matriz_chave)))
det_inv = mod_inv(det % mod, mod)
matriz_chave_inv_mod = (det_inv * np.round(det * np.linalg.inv(matriz_chave)).astype(int) % mod) % mod

# Mapear caracteres para índices e vice-versa
def char_para_indice(char):
    if char == ' ':
        return 26
    return ord(char) - ord('A')

def indice_para_char(indice):
    if indice == 26:
        return ' '
    return chr(indice + ord('A'))

# Função para criptografar uma mensagem
def criptografar(mensagem):
    mensagem = mensagem.upper()

    if len(mensagem) % 2 != 0:
        mensagem += ' '
    
    mensagem_criptografada = ""
    for i in range(0, len(mensagem), 2):
        par = [char_para_indice(mensagem[i]), char_para_indice(mensagem[i+1])]
        par_criptografado = np.dot(matriz_chave, par) % mod
        mensagem_criptografada += ''.join(indice_para_char(x) for x in par_criptografado)
    
    return mensagem_criptografada

# Função para descriptografar uma mensagem
def descriptografar(mensagem_criptografada):
    mensagem_descriptografada = ""
    for i in range(0, len(mensagem_criptografada), 2):
        par = [char_para_indice(mensagem_criptografada[i]), char_para_indice(mensagem_criptografada[i+1])]
        par_descriptografado = np.dot(matriz_chave_inv_mod, par) % mod
        mensagem_descriptografada += ''.join(indice_para_char(x) for x in par_descriptografado)
    
    return mensagem_descriptografada

# Exemplo de uso
mensagem = str(input("Digite sua mensagem: "))
mensagem_criptografada = criptografar(mensagem)
mensagem_descriptografada = descriptografar(mensagem_criptografada)

print(f"Mensagem original: {mensagem}")
print(f"Mensagem criptografada: {mensagem_criptografada}")
print(f"Mensagem descriptografada: {mensagem_descriptografada}")

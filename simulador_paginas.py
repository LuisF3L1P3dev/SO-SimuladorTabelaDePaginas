
def valor_padrao(mensagem, valor_padrao):
    """Simula a função readWithPattern do C++."""
    entrada = input(f"{mensagem} (Enter = {valor_padrao}): ").strip()
    
    if not entrada:
        return valor_padrao
    
    try:
        return int(entrada)
    except ValueError:
        print("Entrada inválida. Usando valor padrão.")
        return valor_padrao

def main():
    #entradas
    memoria_fisica = valor_padrao("Memoria fisica (bytes)", 2147483648)  # 2GB
    memoria_logica = valor_padrao("Memoria logica (bytes)", 4294967296)  # 4GB
    tamanho_pagina = valor_padrao("Tamanho da pagina (bytes)", 4096)     # 4KB
    endereco_logico = valor_padrao("Endereco logico a ser buscado", 20500)
    print("\nqual nivel paginacao:(Nivel 1 ou Nivel 2)")
    
    modo = int(input("Escolha: "))

    # Cálculos básicos
    num_paginas = memoria_logica // tamanho_pagina
    num_molduras = memoria_fisica // tamanho_pagina

    pagina_logica = endereco_logico // tamanho_pagina
    deslocamento = endereco_logico % tamanho_pagina
        
    print("=============================")
    print(f"Pagina logica: {pagina_logica}")
    print(f"Deslocamento: {deslocamento}")
    print("=============================")
    moldura = 0
    if modo == 1:
        # Tabela de 1 nível
        tabela = [-1] * num_paginas # Tabela de paginas
        for i in range(min(num_molduras, num_paginas)):
            tabela[i] = (i * 3) % num_molduras

        moldura = tabela[pagina_logica]
        print("=== TABELA DE PAGINAS (1 NIVEL)===")
        print("Pagina | Moldura")
        print("----------------")
        for i in range(10):
            if i == pagina_logica:
                print(f">>> {i:2} | {tabela[i]} <<<")
            else:
                print(f"{i:4} | {tabela[i]}")
    
    elif modo == 2:
        print('modo 2')
    
if __name__ == "__main__":
    main()
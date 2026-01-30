
def main():
    #entradas
    memoria_fisica = int(input("Memoria fisica (bytes) [padrão 2147483648]: "))
    memoria_logica = int(input("Memoria logica (bytes) [padrão 4294967296]: "))
    tamanho_pagina = int(input("Tamanho da pagina (bytes) [padrão 4096]: "))
    endereco_logico = int(input("Endereco logico a ser buscado [padrão 20500]: "))

    print("Tabela de paginas (1 nivel)")

    # Cálculos básicos
    num_paginas = memoria_logica // tamanho_pagina
    num_molduras = memoria_fisica // tamanho_pagina

    pagina_logica = endereco_logico // tamanho_pagina
    deslocamento = endereco_logico % tamanho_pagina

    print(f"\nPagina logica: {pagina_logica}")
    print(f"Deslocamento: {deslocamento}")

    # Tabela de 1 nível
    tabela = [-1] * num_paginas # Tabela de paginas
    for i in range(min(num_molduras, num_paginas)):
        tabela[i] = (i * 3) % num_molduras

    moldura = tabela[pagina_logica]
    print(f"Moldura: {moldura}")

if __name__ == "__main__":
    main()
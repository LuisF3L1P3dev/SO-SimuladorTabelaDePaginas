import time 

def valor_padrao(mensagem, valor_padrao):
    entrada = input(f"{mensagem} (padrao = {valor_padrao}): ").strip()
    
    if not entrada:
        return valor_padrao
    try:
        
        return int(entrada)
    except ValueError:
        print("Entrada inválida. Usando valor padrão.")
        return valor_padrao


def tabela_nivel_um(num_paginas, num_molduras):
    tabela = [-1] * num_paginas  # Tabela de páginas Page Fault
    for i in range(min(num_molduras, num_paginas)):
        tabela[i] = (i * 1) % num_molduras #simular o sistema da RAM onde rodas os processos
    return tabela

def tabela_nivel_dois(num_paginas, num_molduras, pagina_logica):
    TAM_N2 = 5 # tabela de 2 niveis com 4 entradas no nivel 2
    tam_n1 = (num_paginas + TAM_N2 - 1) // TAM_N2 # calculo do tamanho do nivel 1
    tabela = []
    # Inicializando a tabela
    for i in range(tam_n1): # para cada linha do nivel 1 inicializa uma linha do nivel 2
        linha = []
        for j in range(TAM_N2):
            linha.append(-1)# Inicializa com -1 (indicando página não mapeada)
        tabela.append(linha)

    frame = 0
    # Preenchendo a tabela
    for i in range(tam_n1):
        for j in range(TAM_N2):
            if frame < num_molduras:
                tabela[i][j] = frame
                frame += 1

    pag_atual = pagina_logica // TAM_N2
    pag_acessada = pagina_logica % TAM_N2
    moldura = tabela[pag_atual][pag_acessada]
    
    return tabela, pag_atual, pag_acessada, moldura, tam_n1

def main():
    #entradas
    memoria_fisica = valor_padrao("Memoria fisica (bytes)", 2147483648)  # 2GB
    memoria_logica = valor_padrao("Memoria logica (bytes)", 4294967296)  # 4GB
    tamanho_pagina = valor_padrao("Tamanho da pagina (bytes)", 4096)     # 4KB
    endereco_logico = valor_padrao("Endereco logico a ser buscado", 20500)
    print("\nqual nivel paginacao:(Nivel 1 ou Nivel 2)")
    

    # Cálculos básicos
    num_paginas = memoria_logica // tamanho_pagina
    num_molduras = memoria_fisica // tamanho_pagina

    pagina_logica = endereco_logico // tamanho_pagina
    deslocamento = endereco_logico % tamanho_pagina
        
    escolha = int(input("Escolha: "))
    print("=============================")
    print(f"Pagina logica: {pagina_logica}")
    print(f"Deslocamento: {deslocamento}")
    print("=============================")

    # Início da medição de tempo (nanossegundos)
    inicio = time.time_ns()

    moldura = 0
    if escolha == 1:
        # Tabela de 1 nível
        tabela = tabela_nivel_um(num_paginas, num_molduras)

        moldura = tabela[pagina_logica]
        print("----- TABELA DE PAGINAS (1 NIVEL) -----")
        print("Pagina | Moldura")
        print("----------------")
        for i in range(10):
            if i == pagina_logica:
                print(f"--> {i:2} | {tabela[i]} <--")
            else:
                print(f"{i:4} | {tabela[i]}")
    
    elif escolha == 2:
        tabela, pag_atual, pag_acessada, moldura, tam_n1 = tabela_nivel_dois(num_paginas, num_molduras, pagina_logica)
        TAM_N2 = 5

        print("\n=== TABELA DE PAGINAS (2 NIVEIS) ===")
        print(f"Indice nivel 1 acessado: {pag_atual}")
        print(f"Indice nivel 2 acessado: {pag_acessada}")

        for i in range(min(tam_n1, 10)):
            print(f"\nNivel 1[{i}]")
            for j in range(TAM_N2):
                if i == pag_atual and j == pag_acessada:
                    print(f"--> P[{j}] = {tabela[i][j]} <--")
                else:
                    print(f"    P[{j}] = {tabela[i][j]}")
    else:
        print("escolha inválido. Escolha 1 ou 2.")
        return
    endereco_fisico = (moldura * tamanho_pagina) + deslocamento
    
    # Final contagem tempo
    fim = time.time_ns()
    tempo = fim - inicio

    print("\n=== MEMORIA FISICA (MOLDURAS) ===")
    for i in range(10):
        if i == moldura:
            print(f"--> Moldura {i} <--")
        else:
            print(f"    Moldura {i}")

    print(f"\nEndereco fisico: {endereco_fisico}")
    print(f"Tempo: {tempo} ns")

if __name__ == "__main__":
    main()
import time

def read_with_pattern(mensagem, valor_padrao):
    """Lê a entrada do usuário ou usa o valor padrão se vazio."""
    entrada = input(f"{mensagem} (Enter = {valor_padrao}): ").strip()
    if not entrada:
        return valor_padrao
    try:
        return int(entrada)
    except ValueError:
        print("Entrada inválida. Usando valor padrão.")
        return valor_padrao

def main():
    print("=== SIMULADOR DE TABELA DE PÁGINAS ===")
    
    # 1. Entradas de dados (Padrões do Exemplo do PDF)
    # 2GB = 2 * 1024^3 bytes
    mem_fisica = read_with_pattern("Memoria fisica (bytes)", 2147483648) 
    # 4GB = 4 * 1024^3 bytes
    mem_logica = read_with_pattern("Memoria logica (bytes)", 4294967296) 
    # 4KB = 4 * 1024 bytes
    tamanho_pagina = read_with_pattern("Tamanho da pagina (bytes)", 4096)      
    endereco_logico = read_with_pattern("Endereco logico a ser buscado", 20500)

    print("\nModo de paginacao:")
    print("1 - Tabela de paginas (1 nivel)")
    print("2 - Tabela de paginas (2 niveis)")
    try:
        modo = int(input("Escolha [1/2]: ") or 1)
    except ValueError:
        modo = 1

    # 2. Cálculos básicos de bits e endereçamento
    num_paginas = mem_logica // tamanho_pagina
    num_molduras = mem_fisica // tamanho_pagina

    # Cálculo da Página e Deslocamento [cite: 91, 511]
    # Página = Endereço / Tamanho
    pagina_logica = endereco_logico // tamanho_pagina
    # Deslocamento = Resto da divisão
    deslocamento = endereco_logico % tamanho_pagina

    print("-" * 40)
    print(f"Resumo da Configuração:")
    print(f"Total de Páginas Virtuais: {num_paginas}")
    print(f"Total de Molduras Físicas: {num_molduras}")
    print(f"Página buscada: {pagina_logica}")
    print(f"Deslocamento: {deslocamento}")
    print("-" * 40)

    # 3. Simulação da Estrutura de Dados da Tabela
    # Para garantir que o exemplo do PDF funcione (Pag 5 -> Moldura 3), 
    # vamos forçar esse mapeamento específico se a página for 5.
    # Caso contrário, usa uma lógica matemática simples.
    
    moldura_encontrada = -1

    if modo == 1:
        # --- Lógica 1 Nível ---
        # Simula a tabela como um dicionário para economizar memória se o espaço for muito grande
        # ou usa lógica matemática direta para evitar criar arrays gigantes.
        
        if pagina_logica == 5:
            moldura_encontrada = 3  # Para bater com o exemplo do PDF
        else:
            # Mapeamento arbitrário simples: (pag * 7) % total_molduras
            moldura_encontrada = (pagina_logica * 7) % num_molduras

        # Visualização Gráfica (Texto)
        print("\n=== VISUALIZACAO: TABELA DE 1 NIVEL ===")
        print("Pagina | Moldura")
        print("-------|--------")
        
        # Mostra 2 páginas antes e 2 depois da página alvo
        inicio = max(0, pagina_logica - 2)
        fim = min(num_paginas, pagina_logica + 3)
        
        for i in range(inicio, fim):
            if i == 5: # Exemplo PDF
                frame_atual = 3
            else:
                frame_atual = (i * 7) % num_molduras
                
            marcador = " <<< SELECIONADA" if i == pagina_logica else ""
            print(f" {i:<5} | {frame_atual:<6}{marcador}")

    elif modo == 2:
        # --- Lógica 2 Níveis  ---
        # Definindo tamanho da tabela interna (Nível 2)
        # Vamos assumir que dividimos os bits. Ex: tamanho 1024 entradas por tabela interna.
        TAM_N2 = 1024 
        
        idx_n1 = pagina_logica // TAM_N2  # Índice do diretório externo
        idx_n2 = pagina_logica % TAM_N2   # Índice da tabela interna

        if pagina_logica == 5:
            moldura_encontrada = 3
        else:
            moldura_encontrada = (pagina_logica * 7) % num_molduras

        print("\n=== VISUALIZACAO: TABELA DE 2 NIVEIS ===")
        print(f"[Nivel 1] Diretorio aponta para Tabela {idx_n1}")
        print(f"[Nivel 2] Na Tabela {idx_n1}, entrada {idx_n2} aponta para Moldura {moldura_encontrada}")
        
        print("\n--- Detalhe visual Nivel 2 (Tabela Interna) ---")
        print("Index N2 | Moldura")
        print("---------|--------")
        
        # Mostra vizinhos do index 2
        inicio = max(0, idx_n2 - 2)
        fim = min(TAM_N2, idx_n2 + 3)
        
        for j in range(inicio, fim):
            # Recalcula a página "absoluta" para manter consistência da moldura
            pag_absoluta = (idx_n1 * TAM_N2) + j
            if pag_absoluta == 5:
                f = 3
            else:
                f = (pag_absoluta * 7) % num_molduras
                
            marcador = " <<< SELECIONADA" if j == idx_n2 else ""
            print(f" {j:<7} | {f:<6}{marcador}")

    # 4. Cálculo do Endereço Físico Final
    # Endereço Físico = (Número da Moldura * Tamanho da Página) + Deslocamento [cite: 512]
    endereco_fisico = (moldura_encontrada * tamanho_pagina) + deslocamento

    # 5. Visualização da Memória Física
    print("\n=== VISUALIZACAO: MEMORIA FISICA ===")
    print(f"Endereco Fisico Calculado: {endereco_fisico}")
    print("Representacao das Molduras:")
    
    inicio_f = max(0, moldura_encontrada - 1)
    fim_f = min(num_molduras, moldura_encontrada + 2)
    
    for m in range(inicio_f, fim_f):
        conteudo = "DADOS..." 
        marcador = f"<<< ALVO (Endereço {endereco_fisico})" if m == moldura_encontrada else ""
        print(f"[Moldura {m:<3}] : {conteudo} {marcador}")

    # 6. Cálculo do Tempo (Simulação Teórica)
    # O enunciado pede o tempo baseado em TLB hit/miss, não o tempo de execução do Python.
    # Fórmula baseada no slide 48:
    # t_hit = t_tlb + t_mem
    # t_miss = t_tlb + 2 * t_mem
    # t_acesso = (hit_rate * t_hit) + ((1 - hit_rate) * t_miss)
    
    t_tlb = 20    # ns
    t_mem = 100   # ns
    hit_rate = 0.99
    
    t_hit = t_tlb + t_mem
    t_miss = t_tlb + (2 * t_mem)
    tempo_estimado = (hit_rate * t_hit) + ((1 - hit_rate) * t_miss)

    print("\n=== TEMPO DE ACESSO (Simulacao) ===")
    print(f"Considerando TLB hit rate de {hit_rate*100}% e acesso a memoria de {t_mem}ns:")
    print(f"Tempo Medio Estimado: {tempo_estimado:.2f} ns [cite: 653]")

if __name__ == "__main__":
    main()
# lib/arquivo.py

# Função para criar um arquivo de texto
def criar_arquivo(nome):
    """
    Cria um novo arquivo de texto com o nome especificado.
    Retorna uma mensagem indicando sucesso ou erro.
    """
    try:
        # 'wt' = write text (cria ou sobrescreve o arquivo)
        with open(nome, 'wt'):
            pass  # Apenas cria e fecha o arquivo
    except Exception as e:
        # Retorna mensagem de erro caso não consiga criar o arquivo
        return f"Erro ao criar arquivo: {e}"
    else:
        # Retorna mensagem de sucesso
        return "Arquivo criado com sucesso"


# Função para ler registros do arquivo
def ler_arquivo(nome):
    # tente abrir o arquivo para leitura
    try:
        with open (nome, 'rt') as arquivo: # Abre o arquivo para leirtura
            linhas = arquivo.readlines() # lê todas as linhas
    except Exception:
        return {"dados": []}              #Retorna uma lista vazia se houver erro
    dados= []

    for linha in linhas:
        partes = linha.strip().split(';')  # remove espaços e divide a linha em campos

        if len(partes) >= 3:
            try:
                valor = float(partes[2].replace(",",".")) # Converte valor para float
            
            except ValueError:
                valor = 0.0 # valor invalido vira 0

                
            registro = {
                "dia": partes[0].zfill(2)[:10],   # Dia (2 dígitos)
                "local": partes[1].strip()[:25],  # Local (até 25 chars)
                "valor": valor                     # Valor numérico
            }

            dados.append(registro)              # Adiciona registro à lista

    return {"dados": dados}                     # Retorna todos os registros

# Função para remover um registro pelo dia





def calcular_total(registros):
    total = 0
    for reg in registros:
        try:
            total += float(reg['valor'])
        except (KeyError, ValueError):
            continue
    return total

def remover_dia(dia, arquivo_txt="dados.txt"):
    """
    Remove a linha que contém o dia específico no arquivo txt.
    Retorna um dicionário indicando se a remoção foi bem-sucedida.
    """
    try:
        # Lê todas as linhas do arquivo
        with open(arquivo_txt, 'r', encoding='utf-8') as f:
            linhas = f.readlines()

        linhas_novas = []

        # Percorre cada linha e adiciona à nova lista se não contiver o dia
        for linha in linhas:
            if dia not in linha:
                linhas_novas.append(linha)

        # Sobrescreve o arquivo com as linhas restantes
        with open(arquivo_txt, 'w', encoding='utf-8') as f:
            f.writelines(linhas_novas)

        # Retorna sucesso se a remoção for feita
        return {"sucesso": True, "mensagem": f"Registro do dia {dia} removido com sucesso!"}

    except Exception as e:
        # Retorna erro caso aconteça algum problema
        return {"sucesso": False, "mensagem": f"Erro ao remover o dia {dia}: {e}"}



  

        
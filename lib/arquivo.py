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
def remover_dia_flask(nome_arquivo, dia_remover):
    try:
        with open(nome_arquivo, 'rt') as arquivo:
            linhas = arquivo.readlines()
    except Exception as e:
        return {"sucesso": False, "mensagem": f"Erro ao ler o arquivo: {e}"}

    nova_lista = []
    encontrado = False

    for linha in linhas:
        dados = linha.strip().split(';')
        if len(dados) < 1:
            continue

        # Comparação corrigida com zfill(2)
        if dados[0] != str(int(dia_remover)).zfill(2):
            nova_lista.append(linha)
        else:
            encontrado = True

    if not encontrado:
        return {"sucesso": False, "mensagem": f"Nenhum dia encontrado: {dia_remover}"}

    try:
        with open(nome_arquivo, 'wt') as arquivo:
            arquivo.writelines(nova_lista)
        return {"sucesso": True, "mensagem": f"Dia {dia_remover} removido com sucesso"}
    except Exception as e:
        return {"sucesso": False, "mensagem": f"Erro ao sobrescrever o arquivo: {e}"}


def calcular_total(registros):
    total = 0
    for reg in registros:
        try:
            total += float(reg['valor'])
        except (KeyError, ValueError):
            continue
    return total
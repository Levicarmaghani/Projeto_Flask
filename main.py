# ============================================
# app.py — Sistema Flask com gravação em arquivo TXT
# Autor: Levi Agustinho Carmaghani
# Objetivo: Cadastrar, listar e validar dias trabalhados
# ============================================

import os
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, flash
from lib.arquivo import criar_arquivo, ler_arquivo, remover_dia, calcular_total

# ============================================
# Configuração inicial do Flask
# ============================================
app = Flask(__name__)  # Inicializa o Flask
app.secret_key = "chave-secreta-flask"  # Necessário para usar o flash (mensagens temporárias)
ARQUIVO = "dias.txt"   # Nome do arquivo para armazenar os registros

# ============================================
# Cria o arquivo se ele ainda não existir
# ============================================
if not os.path.exists(ARQUIVO):
    criar_arquivo(ARQUIVO)  # Função importada de lib/arquivo.py

# ============================================
# Página inicial (home) — apenas boas-vindas
# ============================================
@app.route("/")
def home():
    return render_template("home.html")

# ============================================
# Página de dias cadastrados
# Mostra todos os registros do arquivo
# ============================================
@app.route("/dias")
def dias():
    resultado = ler_arquivo(ARQUIVO)  # Lê os dados do arquivo TXT
    
    # Pega a data atual (ex: "2025-11-10") para limitar o campo de data no HTML
    data_atual = date.today().isoformat()

    # Envia registros e a data atual para o template index.html
    return render_template(
        "index.html",
        registros=resultado.get("dados", []),
        data_atual=data_atual
    )

# ============================================
# Rota para cadastrar um novo registro
# ============================================
@app.route("/cadastrar", methods=["POST"])
def cadastrar_rota():
    # Captura os valores enviados pelo formulário
    dia = request.form.get("dia", "0")                   # Data escolhida pelo usuário (campo input type="date")
    local = request.form.get("local", "Desconhecido")    # Local de trabalho
    valor = request.form.get("valor", "0")               # Valor recebido

    # ===================== Validação da data =====================
    try:
        # Converte o texto do campo 'dia' em uma data válida (ex: "2025-11-10")
        data_convertida = datetime.strptime(dia, "%Y-%m-%d").date()

        # Verifica se a data informada é maior que a data atual (futuro)
        if data_convertida > date.today():
            flash("A data não pode ser no futuro.", "erro")  # Envia mensagem de erro para o HTML
            return redirect(url_for("dias"))  # Redireciona para a página de dias cadastrados

    except ValueError:
        # Caso o usuário digite uma data inválida (ex: 31/02/2025)
        flash("Data inválida! Por favor, selecione uma data existente.", "erro")
        return redirect(url_for("dias"))

    # ===================== Gravação no arquivo =====================
    try:
        # Abre o arquivo em modo de adição (append)
        with open(ARQUIVO, "a", encoding="utf-8") as f:
            # Escreve os dados formatados:
            #   data no formato DD/MM/YYYY
            #   local (limitado a 25 caracteres)
            #   valor em formato numérico com 2 casas decimais
            f.write(f"{data_convertida.strftime('%d/%m/%Y')};{local[:25]};{float(valor):.2f}\n")

        # Mostra mensagem de sucesso
        flash("Registro adicionado com sucesso!", "sucesso")

    except Exception as e:
        # Caso aconteça algum erro (ex: problema ao abrir ou gravar o arquivo)
        print(f"Erro ao cadastrar: {e}")  # Mostra o erro no terminal
        flash("Ocorreu um erro ao salvar o registro.", "erro")  # Mostra mensagem de erro no site

    # Depois de gravar (ou tratar o erro), volta para a página de dias cadastrados
    return redirect(url_for("dias"))

# ============================================
# Rota para remover um registro existente
# ============================================
@app.route("/remover", methods=["POST"])
def remover_rota():
    dia_input = request.form.get("dia", "").strip()

    # ===================== Verificação se o campo dia está vazio =====================
    if not dia_input:
        flash("Por favor, informe o dia que deseja remover.", "erro")
        return redirect(url_for("dias"))

    try:
        # Converte YYYY-MM-DD para DD/MM/YYYY
        dia_formatado = datetime.strptime(dia_input, "%Y-%m-%d").strftime("%d/%m/%Y")
    except ValueError:
        flash("Data inválida!", "erro")
        return redirect(url_for("dias"))

    # ===================== Chama a função para remover =====================
    resultado = remover_dia(dia_formatado, ARQUIVO)

    if resultado["sucesso"]:
        flash(resultado['mensagem'], 'sucesso')
    else:
        flash(resultado["mensagem"], 'erro')

    # Redireciona para a página de dias cadastrados após remover
    return redirect(url_for("dias"))

# ============================================
# Rota para calcular o total de valores registrados
# ============================================
@app.route("/total")
def total_rota():
    try:
        total = calcular_total(ARQUIVO)  # Função importada da pasta lib
        return {"sucesso": True, "total": total}
    except Exception as e:
        print(f"Erro ao calcular total: {e}")
        return {"sucesso": False, "total": 0.0}

# ============================================
# Execução do aplicativo Flask
# ============================================
if __name__ == "__main__":
    app.run(debug=True)

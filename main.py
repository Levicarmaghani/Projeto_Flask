# app.py
import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from lib.arquivo import criar_arquivo, ler_arquivo, remover_dia_flask, calcular_total

app = Flask(__name__)  # Inicializa o Flask
ARQUIVO = "dias.txt"   # Nome do arquivo para armazenar registros



# Só Cria o arquivo se ele não existir
if not os.path.exists(ARQUIVO):
    criar_arquivo(ARQUIVO)


# Rota principal (home) que exibe os registros
@app.route("/")
def home():
    resultado = ler_arquivo(ARQUIVO)  # Lê os registros do arquivo
    return render_template("index.html", registros=resultado.get("dados", []))  # Envia para o HTML


# Rota para cadastrar um novo registro
@app.route("/cadastrar", methods=["POST"])
def cadastrar_rota():
    dia = request.form.get("dia", "0")         # Captura o dia do formulário
    local = request.form.get("local", "Desconhecido")  # Captura o local
    valor = request.form.get("valor", "0")     # Captura o valor

    try:
        # Adiciona o registro no arquivo
        with open(ARQUIVO, 'at') as f:
            f.write(f"{int(dia):02d};{local.strip()[:25]};{float(valor):.2f}\n")
    except Exception as e:
        print(f"Erro ao cadastrar: {e}")  # Imprime erro no console

    return redirect(url_for("home"))  # Redireciona para página inicial


# Rota para remover um registro pelo dia
# Rota para remover um registro pelo dia
@app.route("/remover", methods=["POST"])
def remover_rota():
    # Captura o dia enviado pelo formulário
    dia = request.form.get("dia")# Pega o dia do formulário do HTML

    if not dia:  # Se não enviar dia, retorna para a home sem fazer nada
        return redirect(url_for("home"))

    # Chama a função de remoção, garantindo que a comparação será com 2 dígitos
    resultado = remover_dia_flask(ARQUIVO, dia)

    #redireciona de volta para a página inicial
    return redirect(url_for("home"))

    # Redireciona de volta para a página principal apó


# Rota para calcular o total dos valores
@app.route("/total", methods=["GET"])
def total_rota():
    resultado = ler_arquivo(ARQUIVO)
    registros = resultado.get("dados",[])

    # Aqui usamos sua função calcular_total
    total = calcular_total(registros)
    return jsonify({"sucesso": True, "total": round(total, 2)})


# Executa o Flask
if __name__ == "__main__":
    app.run(debug=True)

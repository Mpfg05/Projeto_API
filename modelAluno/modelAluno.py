import re  # Importa regex para validar o nome
from flask import Flask, jsonify, request  
from datetime import datetime

dici = {
    "alunos": [
        {
            "id": 1,
            "nome": "Joel",
            "idade": 20,
            "turma_id": 1,
            "data_nascimento": "17/10/2005",
            "nota_primeiro_semestre": 5,
            "nota_segundo_semestre": 5  
        }
    ]
}    

app = Flask(__name__)

def validar_nome(nome):
    return bool(re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ ]+$", nome))


def getAluno():
    dados = dici['alunos']  
    return jsonify(dados)


def getAlunoById(idAluno):
    for aluno in dici["alunos"]:
        if aluno["id"] == idAluno:
            return jsonify(aluno)
        
    return jsonify({"erro": "Aluno não encontrado"}), 404


def createAluno():
    dados = request.json
    campos_obrigatorios = ['nome', 'turma_id', 'data_nascimento', 'nota_primeiro_semestre', 'nota_segundo_semestre']

    if not all(campo in dados for campo in campos_obrigatorios):
        return jsonify({"erro": "Campos obrigatórios faltando. Use o exemplo que esta no GET para ter de exemplo cada entrada para aluno!('nome', 'turma_id', 'data_nascimento', 'nota_primeiro_semestre', 'nota_segundo_semestre')"}), 400

    if not validar_nome(dados["nome"]):
        return jsonify({"erro": "O nome deve conter apenas letras e espaços!"}), 400

    turma_existe = any(turma['id'] == dados['turma_id'] for turma in dici["turmas"])
    if not turma_existe:
        return jsonify({"erro": "Turma não encontrada!"}), 400
    
    novo_id = max([aluno["id"] for aluno in dici["alunos"]], default=0) + 1

    data_nascimento = datetime.strptime(dados["data_nascimento"], "%d/%m/%Y")
    hoje = datetime.now()
    idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) <(data_nascimento.month, data_nascimento.day))

    dados["id"] = novo_id
    dados["idade"] = idade
    dados["media_final"] = (dados["nota_primeiro_semestre"] + dados["nota_segundo_semestre"]) / 2

    dici['alunos'].append(dados)
    return jsonify({"mensagem": "Aluno cadastrado com sucesso!", "aluno": dados}), 201


def deleteAluno(idAluno):
    for aluno in dici["alunos"]:
        if aluno['id'] == idAluno:
            dici["alunos"].remove(aluno)
            return jsonify({'mensagem': 'Aluno removido com sucesso!'})
    
    return jsonify({'erro': 'Aluno não encontrado'}), 404
    

def updateAlunos(idAluno):
    for aluno in dici["alunos"]:
        if aluno['id'] == idAluno:
            dados = request.json
            campos_obrigatorios = ['nome', 'turma_id', 'data_nascimento', 'nota_primeiro_semestre', 'nota_segundo_semestre']

            if not all(campo in dados and dados[campo] not in [None, ""] for campo in campos_obrigatorios):
                return jsonify({"erro": "Todos os campos são obrigatórios para serem preenchidos! ('nome', 'turma_id', 'data_nascimento', 'nota_primeiro_semestre', 'nota_segundo_semestre')"}), 400
            
            if not validar_nome(dados["nome"]):
                return jsonify({"erro": "O nome deve conter apenas letras e espaços!"}), 400
            
            if "id" in dados and dados["id"] != idAluno:
                return jsonify({"erro": "Não é permitido mudar o ID do aluno"}), 400
 
            turma_existe = any(turma['id'] == dados['turma_id'] for turma in dici["turmas"])
            if not turma_existe:
                return jsonify({"erro": "Turma não encontrada!"}), 400

            try:
                data_nascimento = datetime.strptime(dados["data_nascimento"], "%d/%m/%Y")
            except ValueError:
                return jsonify({"erro": "Data de nascimento inválida! O formato deve ser DD/MM/AAAA."}), 400

            hoje = datetime.now()
            idade_calculada = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))

            if dados["idade"] != idade_calculada:
                return jsonify({"erro": f"Idade informada ({dados['idade']}) não bate com a data de nascimento ({dados['data_nascimento']}). Idade correta seria {idade_calculada}."}), 400

            aluno.update({key: value for key, value in dados.items() if key != "id"})

            aluno["media_final"] = (aluno["nota_primeiro_semestre"] + aluno["nota_segundo_semestre"]) / 2

            return jsonify({"mensagem": "Aluno atualizado!", "aluno": aluno})

    return jsonify({"erro": "Aluno não encontrado"}), 404

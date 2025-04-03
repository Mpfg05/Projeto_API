from datetime import datetime
import re

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

def validar_nome(nome):
    return bool(re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ ]+$", nome))

def getAluno():
    return dici["alunos"]

def getAlunoById(idAluno):
    for aluno in dici["alunos"]:
        if aluno["id"] == idAluno:
            return aluno
    return None

def createAluno(dados, turmas):
    campos_obrigatorios = ['nome', 'turma_id', 'data_nascimento', 'nota_primeiro_semestre', 'nota_segundo_semestre']

    if not all(campo in dados for campo in campos_obrigatorios):
        return {"erro": "Campos obrigatórios faltando. Use ('nome', 'turma_id', 'data_nascimento', 'nota_primeiro_semestre', 'nota_segundo_semestre')."}, 400

    if not validar_nome(dados["nome"]):
        return {"erro": "O nome deve conter apenas letras e espaços!"}, 400

    turma_existe = any(turma['id'] == dados['turma_id'] for turma in turmas)
    if not turma_existe:
        return {"erro": "Turma não encontrada!"}, 400

    try:
        data_nascimento = datetime.strptime(dados["data_nascimento"], "%d/%m/%Y")
    except ValueError:
        return {"erro": "Data de nascimento inválida! O formato deve ser DD/MM/AAAA."}, 400

    hoje = datetime.now()
    idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))

    if idade < 5:  
        return {"erro": "Idade inválida! O aluno deve ter pelo menos 5 anos."}, 400

    novo_id = max([aluno["id"] for aluno in dici["alunos"]], default=0) + 1
    dados["id"] = novo_id
    dados["idade"] = idade
    dados["media_final"] = (dados["nota_primeiro_semestre"] + dados["nota_segundo_semestre"]) / 2

    dici['alunos'].append(dados)
    return {"mensagem": "Aluno cadastrado com sucesso!", "aluno": dados}, 201

def updateAlunos(idAluno, novos_dados, turmas):
    aluno = getAlunoById(idAluno)
    if not aluno:
        return {"erro": "Aluno não encontrado"}, 404

    if "nome" in novos_dados and not validar_nome(novos_dados["nome"]):
        return {"erro": "O nome deve conter apenas letras e espaços!"}, 400

    if "turma_id" in novos_dados:
        turma_existe = any(turma['id'] == novos_dados['turma_id'] for turma in turmas)
        if not turma_existe:
            return {"erro": "Turma não encontrada!"}, 400

    if "data_nascimento" in novos_dados:
        try:
            data_nascimento = datetime.strptime(novos_dados["data_nascimento"], "%d/%m/%Y")
        except ValueError:
            return {"erro": "Data de nascimento inválida! O formato deve ser DD/MM/AAAA."}, 400

        hoje = datetime.now()
        idade_calculada = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))

        if "idade" in novos_dados and novos_dados["idade"] != idade_calculada:
            return {"erro": f"Idade incorreta! A idade correta seria {idade_calculada}."}, 400


        aluno["idade"] = idade_calculada

    aluno.update({key: value for key, value in novos_dados.items() if key != "id"})


    if "nota_primeiro_semestre" in novos_dados or "nota_segundo_semestre" in novos_dados:
        aluno["media_final"] = (aluno["nota_primeiro_semestre"] + aluno["nota_segundo_semestre"]) / 2

    return {"mensagem": "Aluno atualizado!", "aluno": aluno}, 200

def deleteAluno(idAluno):
    aluno = getAlunoById(idAluno)
    if aluno:
        dici["alunos"].remove(aluno)
        return {"mensagem": "Aluno removido com sucesso!"}, 200
    return {"erro": "Aluno não encontrado"}, 404

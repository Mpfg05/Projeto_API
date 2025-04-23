import re
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
        }]
}

def validar_nome(nome):
    return bool(re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ ]+$", nome))

def calcular_idade(data_nascimento):
    try:
        nascimento = datetime.strptime(data_nascimento, "%d/%m/%Y")
        hoje = datetime.today()
        idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
        return idade
    except ValueError:
        return None

def getAluno():
    return dici["alunos"]

def getAlunoById(idAluno):
    for aluno in dici["alunos"]:
        if aluno["id"] == idAluno:
            return aluno
    return {"erro": "Aluno não encontrado"}

def createAluno(dados, turmas):  
    campos_obrigatorios = ['nome', 'turma_id', 'data_nascimento', 'nota_primeiro_semestre', 'nota_segundo_semestre']
    if not all(campo in dados for campo in campos_obrigatorios):
        return {"erro": "Campos obrigatórios faltando!"}, 400

    if not validar_nome(dados["nome"]):
        return {"erro": "O nome deve conter apenas letras e espaços!"}, 400

    turma_existe = any(turma['id'] == dados['turma_id'] for turma in turmas)
    if not turma_existe:
        return {"erro": "Turma não encontrada!"}, 400

    idade = calcular_idade(dados["data_nascimento"])
    if idade is None:
        return {"erro": "Data de nascimento inválida. Use o formato DD/MM/AAAA."}, 400

    dados.pop("idade", None) 
    novo_id = max([aluno["id"] for aluno in dici["alunos"]], default=0) + 1
    dados["id"] = novo_id
    dados["idade"] = idade

    dici['alunos'].append(dados)
    return {"mensagem": "Aluno cadastrado com sucesso!", "aluno": dados}, 201

def updateAluno(idAluno, novos_dados):
    aluno = getAlunoById(idAluno)
    if not aluno or "erro" in aluno:
        return {"erro": "Aluno não encontrado"}, 404

    campos_obrigatorios = ['nome', 'turma_id', 'data_nascimento', 'nota_primeiro_semestre', 'nota_segundo_semestre']
    if not all(campo in novos_dados and novos_dados[campo] not in [None, ""] for campo in campos_obrigatorios):
        return {"erro": "Todos os campos são obrigatórios!"}, 400

    if not validar_nome(novos_dados["nome"]):
        return {"erro": "O nome deve conter apenas letras e espaços!"}, 400

    idade = calcular_idade(novos_dados["data_nascimento"])
    if idade is None:
        return {"erro": "Data de nascimento inválida. Use o formato DD/MM/AAAA."}, 400

    novos_dados.pop("idade", None)  # ignora tentativa de alterar idade
    novos_dados["idade"] = idade

    aluno.update({key: value for key, value in novos_dados.items() if key != "id"})

    return {"mensagem": "Aluno atualizado!", "aluno": aluno}

def deleteAluno(idAluno):
    aluno = getAlunoById(idAluno)
    if aluno and "erro" not in aluno:
        dici["alunos"].remove(aluno)
        return {"mensagem": "Aluno removido com sucesso!"}
    return {"erro": "Aluno não encontrado"}, 404

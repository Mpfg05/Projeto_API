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


    turma_existe = any(turma['id'] == dados['turma_id'] for turma in turmas)
    if not turma_existe:
        return {"erro": "Turma não encontrada!"}, 400


    novo_id = max([aluno["id"] for aluno in dici["alunos"]], default=0) + 1
    dados["id"] = novo_id

    dici['alunos'].append(dados)
    return {"mensagem": "Aluno cadastrado com sucesso!", "aluno": dados}, 201

def updateAluno(idAluno, novos_dados):
    aluno = getAlunoById(idAluno)
    if not aluno:
        return {"erro": "Aluno não encontrado"}, 404

    campos_obrigatorios = ['nome', 'turma_id', 'data_nascimento', 'nota_primeiro_semestre', 'nota_segundo_semestre']
    if not all(campo in novos_dados and novos_dados[campo] not in [None, ""] for campo in campos_obrigatorios):
        return {"erro": "Todos os campos são obrigatórios!"}, 400

    aluno.update({key: value for key, value in novos_dados.items() if key != "id"})
    return {"mensagem": "Aluno atualizado!", "aluno": aluno}

def deleteAluno(idAluno):
    aluno = getAlunoById(idAluno)
    if aluno:
        dici["alunos"].remove(aluno)
        return {"mensagem": "Aluno removido com sucesso!"}
    return {"erro": "Aluno não encontrado"}, 404

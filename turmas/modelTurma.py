dici = {
    "turmas": [
        {
            "id": 1,
            "descricao": "APIs 4B manhã",
            "professor_id": 1,
            "ativo": True
        }
    ]
}

def getTurma():
    return dici["turmas"]  # Corrigido: antes estava 'alunos' ao invés de 'turmas'

def getTurmaById(idTurma):
    for turma in dici["turmas"]:
        if turma["id"] == idTurma:
            return turma
    return None

def createTurma(dados, professores):  # Corrigido: nome da função estava errado
    campos_obrigatorios = ['descricao', 'professor_id', 'ativo']
    if not all(campo in dados for campo in campos_obrigatorios):
        return {"erro": "Campos obrigatórios faltando. Use o exemplo que está no GET para ter de exemplo cada entrada para turma ('descricao', 'professor_id', 'ativo')"}, 400
     
    novo_id = max([turma["id"] for turma in dici["turmas"]], default=0) + 1
    dados["id"] = novo_id

    professor_existe = any(professor['id'] == dados['professor_id'] for professor in professores)
    if not professor_existe:
        return {"erro": "Professor não encontrado!"}, 400

    dici['turmas'].append(dados)
    return {"mensagem": "Turma cadastrada com sucesso!", "turma": dados}, 201

def updateTurmas(idTurma, novos_dados):
    turma = getTurmaById(idTurma)
    if not turma:
        return {"erro": "Turma não encontrada"}, 404
    
    campos_obrigatorios = ['descricao', 'professor_id', 'ativo']  # Corrigido: campos estavam errados
    if not all(campo in novos_dados and novos_dados[campo] not in [None, ""] for campo in campos_obrigatorios):
        return {"erro": "Todos os campos são obrigatórios!"}, 400
    
    turma.update({key: value for key, value in novos_dados.items() if key != "id"})
    return {"mensagem": "Turma atualizada!", "turma": turma}

def deleteTurma(idTurma):
    turma = getTurmaById(idTurma)
    if turma:
        dici["turmas"].remove(turma)
        return {"mensagem": "Turma removida com sucesso!"}  # Corrigido: retorno melhorado
    return {"erro": "Turma não encontrada"}, 404

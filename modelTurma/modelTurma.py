from flask import Flask, jsonify, request  






def getTurma():
    dados = dici['turmas']  
    return jsonify(dados)

def getTurmaById(idTurma):
    for turma in dici["turmas"]:
        if turma["id"] == idTurma:
            return jsonify(turma)
        
    return jsonify({"erro": "Turma não encontrada"}), 404


def createTurma():
    dados = request.json

    campos_obrigatorios = ['descricao', 'professor_id', 'ativo']
    if not all(campo in dados for campo in campos_obrigatorios):
        return jsonify({"erro": "Campos obrigatórios faltando. Use o exemplo que esta no GET para ter de exemplo cada entrada para turma('descricao', 'professor_id', 'ativo')"}), 400

    novo_id = max([turma["id"] for turma in dici["turmas"]], default=0) + 1

    dados["id"] = novo_id

    # Verificar se professor_id existe antes de cadastrar a turma
    professor_existe = any(professor['id'] == dados['professor_id'] for professor in dici["professores"])
    if not professor_existe:
        return jsonify({"erro": "Professor não encontrado!"}), 400

    dici['turmas'].append(dados)
    return jsonify({"mensagem": "Turma cadastrada com sucesso!", "turma": dados}), 201

def updateTurmas(idTurma):
    for turma in dici["turmas"]:
        if turma['id'] == idTurma:
            dados = request.json
            campos_obrigatorios = ['descricao', 'professor_id', 'ativo']

            if not all(campo in dados and dados[campo] not in [None, ""] for campo in campos_obrigatorios):
                return jsonify({"erro": "Todos os campos são obrigatórios!"}), 400

            if "id" in dados and dados["id"] != idTurma:
                return jsonify({"erro": "Não é permitido mudar o ID da turma"}), 400

            turma.update({key: value for key, value in dados.items() if key != "id"})

            return jsonify({"mensagem": "Turma atualizada!", "turma": turma})

    return jsonify({"erro": "Turma não encontrada"}), 404


def deleteTurma(idTurma):
    for turma in dici["turmas"]:
        if turma['id'] == idTurma:
            dici["turmas"].remove(turma)
            return jsonify({'mensagem': 'Turma removida com sucesso!'})
    
    return jsonify({'erro': 'Turma não encontrada'}), 404

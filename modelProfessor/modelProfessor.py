import re  # Importa regex para validar o nome
from flask import Flask, jsonify, request  

dici = {
    "professores": [  
        {
            "id": 1,
            "nome": "Cleber Machado",
            "idade": 40,
            "materia": "matemática",
            "observacoes": "um professor muito esperto e reconhecido pelo MEC"
        }
    ]

def getProfessor():
    dados = dici['professores']  
    return jsonify(dados)


def getProfessorById(idProfessor):
    for professor in dici["professores"]:
        if professor["id"] == idProfessor:
            return jsonify(professor)
        
    return jsonify({"erro": "Professor não encontrado"}), 404

def createProfessor():
    dados = request.json
    campos_obrigatorios = ['nome', 'idade', 'materia', 'observacoes']

    if not all(campo in dados for campo in campos_obrigatorios):
        return jsonify({"erro": "Campos obrigatórios faltando. Use o exemplo que esta no GET para ter de exemplo cada entrada para professor!('nome', 'idade', 'materia', 'observacoes')"}), 400

    if not validar_nome(dados["nome"]):
        return jsonify({"erro": "O nome deve conter apenas letras e espaços!"}), 400
    
    if dados['idade'] <= 0:
        return jsonify({"erro": "Idade invalida"})

    if dados['idade'] < 17:
        return jsonify({"erro": "Idade invalida, muito novo para ser professor"})

    novo_id = max([professor["id"] for professor in dici["professores"]], default=0) + 1

    dados["id"] = novo_id

    dici['professores'].append(dados)
    return jsonify({"mensagem": "Professor cadastrado com sucesso!", "professor": dados}), 201

def updateProfessores(idProfessor):
    for professor in dici["professores"]:
        if professor['id'] == idProfessor:
            dados = request.json
            campos_obrigatorios = ['nome', 'idade', 'materia', 'observacoes']

            if not all(campo in dados and dados[campo] not in [None, ""] for campo in campos_obrigatorios):
                return jsonify({"erro": "Todos os campos são obrigatórios para serem preenchidos!('nome', 'idade', 'materia', 'observacoes')"}), 400

            if not validar_nome(dados["nome"]):
                return jsonify({"erro": "O nome deve conter apenas letras e espaços!"}), 400

            if dados['idade'] <= 0:
                return jsonify({"erro": "Idade invalida"})

            if dados['idade'] < 17:
                return jsonify({"erro": "Idade invalida, muito novo para ser professor"})

            if "id" in dados and dados["id"] != idProfessor:
                return jsonify({"erro": "Não é permitido mudar o ID do professor"}), 400

            professor.update({key: value for key, value in dados.items() if key != "id"})

            return jsonify({"mensagem": "Professor atualizado!", "professor": professor})
    
    return jsonify({"erro": "Professor não encontrado"}), 404

def deleteProfessor(idProfessor):
    for professor in dici["professores"]:
        if professor['id'] == idProfessor:
            dici["professores"].remove(professor)
            return jsonify({'mensagem': 'Professor removido com sucesso!'})
    
    return jsonify({'erro': 'Professor não encontrado'}), 404

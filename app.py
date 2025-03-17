###########################################################
#OBROGATÓRIO O USO DO POSTMAN PARA AS REQUISIÇÕES E A ROTA#
#OBROGATÓRIO O USO DO POSTMAN PARA AS REQUISIÇÕES E A ROTA#
#OBROGATÓRIO O USO DO POSTMAN PARA AS REQUISIÇÕES E A ROTA#
#OBROGATÓRIO O USO DO POSTMAN PARA AS REQUISIÇÕES E A ROTA#
###########################################################



#{
#  "nome": "Joel",
#  "id": 2,
#  "idade": 15,
#  "turma_id": 1,
#  "data_nascimento": "17/10/2005",
#  "nota_primeiro_semestre": 8,
#  "nota_segundo_semestre": 9
#}

#{
#  "nome": "Cleber Machado",
#  "idade": 19,
#  "materia": "matemática",
#  "id": 2,
#  "observacoes": "É um professor muito esperto e reconhecido pelo MEC"
#}

#{
#  "id": 2,
#  "descricao": "Sala do nono ano B",
#  "professor_id": 1,
#  "ativo": true
#}



from flask import Flask, jsonify, request  


dici = {
    "alunos": [
        {
            "id": 1,
            "nome": "Caio",
            "idade": 20  
        }
    ],
    "professores": [  
        {
            "id": 1,
            "nome": "Rafael"
        }
    ],
    "turmas": [
        {
            "id": 1,
            "nome": "APIs"
        }
    ],
}

app = Flask(__name__)

#-------------------------------------------------------------------##-------------------------------------------------------------------#


@app.route("/alunos", methods=['GET'])
def getAluno():
    dados = dici['alunos']  
    return jsonify(dados)

@app.route("/alunos/<int:idAluno>", methods=['GET'])
def getAlunoById(idAluno):
    for aluno in dici["alunos"]:
        if aluno["id"] == idAluno:
            return jsonify(aluno)
        
    return jsonify({"erro": "Aluno não encontrado"}), 404

############################################

# Rota POST para adicionar um aluno
@app.route('/alunos', methods=['POST'])
def createAluno():
    dados = request.json  # Recebe o JSON enviado na requisição

    # Valida se os campos obrigatórios foram enviados
    campos_obrigatorios = ['id', 'nome', 'idade', 'turma_id', 'data_nascimento', 'nota_primeiro_semestre', 'nota_segundo_semestre']
    if not all(campo in dados for campo in campos_obrigatorios):
        return jsonify({"erro": "Campos obrigatórios faltando!"}), 400

    # Calcula a média final
    media_final = (dados["nota_primeiro_semestre"] + dados["nota_segundo_semestre"]) / 2
    dados["media_final"] = media_final  # Adiciona a média ao aluno

    # Adiciona o novo aluno à lista
    dici['alunos'].append(dados)
    return jsonify({"mensagem": "Aluno cadastrado com sucesso!", "aluno": dados}), 201

############################################

# Rota PUT para atualizar aluno por ID
@app.route("/alunos/<int:idAluno>", methods=['PUT'])
def updateAlunos(idAluno):
    for aluno in dici["alunos"]:
        if aluno['id'] == idAluno:
            dados = request.json  # Dados atualizados do aluno

            # Atualiza os dados conforme enviados
            aluno["nome"] = dados.get('nome', aluno["nome"])
            aluno["idade"] = dados.get('idade', aluno["idade"])
            aluno["turma_id"] = dados.get('turma_id', aluno.get('turma_id'))
            aluno["data_nascimento"] = dados.get('data_nascimento', aluno.get("data_nascimento"))
            aluno["nota_primeiro_semestre"] = dados.get('nota_primeiro_semestre', aluno.get("nota_primeiro_semestre", 0))
            aluno["nota_segundo_semestre"] = dados.get('nota_segundo_semestre', aluno.get("nota_segundo_semestre", 0))

            # Recalcula a média final
            aluno["media_final"] = (aluno["nota_primeiro_semestre"] + aluno["nota_segundo_semestre"]) / 2

            return jsonify({"mensagem": "Aluno atualizado!", "aluno": aluno})
    
    return jsonify({"erro": "Aluno não encontrado"}), 404  # Retorna erro corretamente

############################################

# Rota DELETE para remover um aluno por ID
@app.route('/alunos/<int:idAluno>', methods=['DELETE'])
def deleteAluno(idAluno):
    for aluno in dici["alunos"]:
        if aluno['id'] == idAluno:
            dici["alunos"].remove(aluno)
            return jsonify({'mensagem': 'Aluno removido com sucesso!'})
    
    return jsonify({'erro': 'Aluno não encontrado'}), 404
    

#-------------------------------------------------------------------##-------------------------------------------------------------------#

@app.route("/professores", methods=['GET'])
def getProfessor():
    dados = dici['professores']  
    return jsonify(dados)

@app.route("/professores/<int:idProfessor>", methods=['GET'])
def getProfessorById(idProfessor):
    for professor in dici["professores"]:
        if professor["id"] == idProfessor:
            return jsonify(professor)
        
    return jsonify({"erro": "Professor não encontrado"}), 404

############################################

@app.route('/professores', methods = ['POST'])
def createProfessor():
    dados = request.json

    campos_obrigatorios = ['id', 'nome', 'idade', 'materia', 'observacoes']
    if not all(campo in dados for campo in campos_obrigatorios):
        return jsonify({"erro": "Campos obrigatórios faltando!"}), 400
    
    dici['professores'].append(dados)
    return jsonify({"mensagem": "Professor cadastrado com sucesso!", "professor": dados}), 201

############################################

@app.route("/professores/<int:idProfessor>", methods=['PUT'])
def updateProfessores(idProfessor):
    for professor in dici["professores"]:
        if professor['id'] == idProfessor:
            dados = request.json 

            # Atualiza os dados conforme enviados
            professor["nome"] = dados.get('nome', professor["nome"])
            professor["idade"] = dados.get('idade', professor["idade"])
            professor["materia"] = dados.get('materia', professor["materia"])
            professor["observacoes"] = dados.get('observacoes',professor["observacoes"])

            return jsonify({"mensagem": "Professor atualizado!", "professor": professor})
    
    return jsonify({"erro": "Professor não encontrado"}), 404  

############################################

@app.route('/professores/<int:idProfessor>', methods=['DELETE'])
def deleteProfessor(idProfessor):
    for professor in dici["professores"]:
        if professor['id'] == idProfessor:
            dici["professores"].remove(professor)
            return jsonify({'mensagem': 'Professor removido com sucesso!'})
    
    return jsonify({'erro': 'Professor não encontrado'}), 404

#-------------------------------------------------------------------##-------------------------------------------------------------------#

@app.route("/turmas", methods=['GET'])
def getTurma():
    dados = dici['turmas']  
    return jsonify(dados)

@app.route("/turmas/<int:idTurma>", methods=['GET'])
def getTurmaById(idTurma):
    for turma in dici["turmas"]:
        if turma["id"] == idTurma:
            return jsonify(turma)
        
    return jsonify({"erro": "Turma não encontrada"}), 404

############################################

@app.route('/turmas', methods = ['POST'])
def createTurma():
    dados = request.json

    campos_obrigatorios = ['id', 'descricao', 'professor_id', 'ativo']
    if not all(campo in dados for campo in campos_obrigatorios):
        return jsonify({"erro": "Campos obrigatórios faltando!"}), 400
    
    dici['turmas'].append(dados)
    return jsonify({"mensagem": "Turma cadastrada com sucesso!", "turma": dados}), 201

############################################

@app.route("/turmas/<int:idTurma>", methods=['PUT'])
def updateTurmas(idTurma):
    for turma in dici["turmas"]:
        if turma['id'] == idTurma:
            dados = request.json 

            # Atualiza os dados conforme enviados
            turma["descricao"] = dados.get('descricao', turma["descricao"])
            turma["professor_id"] = dados.get('professor_id', turma["professor_id"])
            turma["ativo"] = dados.get('ativo', turma["ativo"])


            return jsonify({"mensagem": "Turma atualizada!", "turma": turma})
    
    return jsonify({"erro": "Turma não encontrada"}), 404  

############################################

@app.route('/turmas/<int:idTurma>', methods=['DELETE'])
def deleteTurma(idTurma):
    for turma in dici["turmas"]:
        if turma['id'] == idTurma:
            dici["turmas"].remove(turma)
            return jsonify({'mensagem': 'Turma removida com sucesso!'})
    
    return jsonify({'erro': 'Turma não encontrada'}), 404

#-------------------------------------------------------------------##-------------------------------------------------------------------#
if __name__ == "__main__":
    app.run(debug=True)

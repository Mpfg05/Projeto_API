from flask import Flask, jsonify, request  


dici = {
    "alunos": [
        {
            "id": 1,
            "nome": "Caio",
            "idade": 20  
        }
    ],
    "professor": [  
        {
            "id": 1,
            "nome": "Rafael"
        }
    ],
    "turma": [
        {
            "id": 1,
            "nome": "APIs"
        }
    ],
}

app = Flask(__name__)


@app.route("/alunos", methods=['GET'])
def getAluno():
    dados = dici['alunos']  
    return jsonify(dados)

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

# Rota PUT para atualizar aluno por ID
@app.route("/alunos/<int:idAluno>", methods=['PUT'])
def updateAlunos(idAluno):
    for aluno in dici["alunos"]:
        if aluno['id'] == idAluno:
            dados = request.json  # Dados atualizados do aluno

            # Atualiza os dados conforme enviados
            aluno["nome"] = dados.get('nome', aluno["nome"])
            aluno["idade"] = dados.get('idade', aluno["idade"])
            aluno["turma_id"] = dados.get('turma_id', aluno["turma_id"])
            aluno["data_nascimento"] = dados.get('data_nascimento', aluno["data_nascimento"])
            aluno["nota_primeiro_semestre"] = dados.get('nota_primeiro_semestre', aluno["nota_primeiro_semestre"])
            aluno["nota_segundo_semestre"] = dados.get('nota_segundo_semestre', aluno["nota_segundo_semestre"])

            # Recalcula a média final
            aluno["media_final"] = (aluno["nota_primeiro_semestre"] + aluno["nota_segundo_semestre"]) / 2

            return jsonify({"mensagem": "Aluno atualizado!", "aluno": aluno})
    
    return jsonify({"erro": "Aluno não encontrado"}), 404  # Retorna erro corretamente

# Rota DELETE para remover um aluno por ID
@app.route('/alunos/<int:idAluno>', methods=['DELETE'])
def deleteAluno(idAluno):
    for aluno in dici["alunos"]:
        if aluno['id'] == idAluno:
            dici["alunos"].remove(aluno)
            return jsonify({'mensagem': 'Aluno removido com sucesso!'})
    
    return jsonify({'erro': 'Aluno não encontrado'}), 404
    

#-------------------------------------------------------------------#

@app.route("/professores", methods=['GET'])
def getProfessor():
    dados = dici['professor']  
    return jsonify(dados)


#-------------------------------------------------------------------#

@app.route("/turma", methods=['GET'])
def getTurma():
    dados = dici['turma']  
    return jsonify(dados)

#-------------------------------------------------------------------#
if __name__ == "__main__":
    app.run(debug=True)

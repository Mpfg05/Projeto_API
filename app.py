###########################################################
#OBROGATÓRIO O USO DO POSTMAN PARA AS REQUISIÇÕES E A ROTA#
#OBROGATÓRIO O USO DO POSTMAN PARA AS REQUISIÇÕES E A ROTA#
#OBROGATÓRIO O USO DO POSTMAN PARA AS REQUISIÇÕES E A ROTA#
#OBROGATÓRIO O USO DO POSTMAN PARA AS REQUISIÇÕES E A ROTA#
###########################################################


import re  # Importa regex para validar o nome
from flask import Flask, jsonify, request  


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
    ],
    "professores": [  
        {
            "id": 1,
            "nome": "Cleber Machado",
            "idade": 40,
            "materia": "matemática",
            "observacoes": "um professor muito esperto e reconhecido pelo MEC"
        }
    ],
    "turmas": [
        {
            "id": 1,
            "descricao": "APIs 4B manhã",
            "professor_id": 1,
            "ativo": True
        }
    ],
}

app = Flask(__name__)


# Função para validar nomes (somente letras e espaços)
def validar_nome(nome):
    return bool(re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ ]+$", nome))

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
    dados = request.json
    campos_obrigatorios = ['id', 'nome', 'idade', 'turma_id', 'data_nascimento', 'nota_primeiro_semestre', 'nota_segundo_semestre']

    if not all(campo in dados for campo in campos_obrigatorios):
        return jsonify({"erro": "Campos obrigatórios faltando!"}), 400

    if not validar_nome(dados["nome"]):
        return jsonify({"erro": "O nome deve conter apenas letras e espaços!"}), 400

    if dados['idade'] <= 0:
        return jsonify({"erro": "Idade invalida"})
    
    aluno_existe = any(aluno['id'] == dados['id'] for aluno in dici["alunos"])
    if aluno_existe:
        return jsonify({"erro": "Aluno já existente com esse ID"}), 400

    turma_existe = any(turma['id'] == dados['turma_id'] for turma in dici["turmas"])
    if not turma_existe:
        return jsonify({"erro": "Turma não encontrada!"}), 400

    dados["media_final"] = (dados["nota_primeiro_semestre"] + dados["nota_segundo_semestre"]) / 2

    dici['alunos'].append(dados)
    return jsonify({"mensagem": "Aluno cadastrado com sucesso!", "aluno": dados}), 201


############################################

@app.route("/alunos/<int:idAluno>", methods=['PUT'])
def updateAlunos(idAluno):
    for aluno in dici["alunos"]:
        if aluno['id'] == idAluno:
            dados = request.json
            campos_obrigatorios = ['nome', 'idade', 'turma_id', 'data_nascimento', 'nota_primeiro_semestre', 'nota_segundo_semestre']

            # Verifica se todos os campos obrigatórios estão preenchidos
            if not all(campo in dados and dados[campo] not in [None, ""] for campo in campos_obrigatorios):
                return jsonify({"erro": "Todos os campos são obrigatórios para serem preenchidos!"}), 400
            
            # Verifica se o nome é válido
            if not validar_nome(dados["nome"]):
                return jsonify({"erro": "O nome deve conter apenas letras e espaços!"}), 400
            
            if dados['idade'] <= 0:
                return jsonify({"erro": "Idade invalida"})

            # Impede a alteração do ID para um já existente
            if "id" in dados and dados["id"] != idAluno:
                aluno_existe = any(a['id'] == dados["id"] for a in dici["alunos"])
                if aluno_existe:
                    return jsonify({"erro": "ID já existe para outro aluno!"}), 400
            
            # Atualiza os dados, exceto o ID
            aluno.update({dados: i for dados, i in dados.items() if dados != "id"})

            # Recalcula a média final
            aluno["media_final"] = (aluno["nota_primeiro_semestre"] + aluno["nota_segundo_semestre"]) / 2

            return jsonify({"mensagem": "Aluno atualizado!", "aluno": aluno})
    
    return jsonify({"erro": "Aluno não encontrado"}), 404


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

@app.route('/professores', methods=['POST'])
def createProfessor():
    dados = request.json
    campos_obrigatorios = ['id', 'nome', 'idade', 'materia', 'observacoes']

    if not all(campo in dados for campo in campos_obrigatorios):
        return jsonify({"erro": "Campos obrigatórios faltando!"}), 400

    if not validar_nome(dados["nome"]):
        return jsonify({"erro": "O nome deve conter apenas letras e espaços!"}), 400
    
    if dados['idade'] <= 0:
        return jsonify({"erro": "Idade invalida"})

    if dados['idade'] < 17:
        return jsonify({"erro": "Idade invalida, muito novo para ser professor"})

    professor_existe = any(professor['id'] == dados['id'] for professor in dici["professores"])
    if professor_existe:
        return jsonify({"erro": "Professor já existente com esse ID"}), 400

    dici['professores'].append(dados)
    return jsonify({"mensagem": "Professor cadastrado com sucesso!", "professor": dados}), 201



############################################

@app.route("/professores/<int:idProfessor>", methods=['PUT'])
def updateProfessores(idProfessor):
    for professor in dici["professores"]:
        if professor['id'] == idProfessor:
            dados = request.json
            campos_obrigatorios = ['nome', 'idade', 'materia', 'observacoes']

            if not all(campo in dados and dados[campo] not in [None, ""] for campo in campos_obrigatorios):
                return jsonify({"erro": "Todos os campos são obrigatórios para serem preenchidos!"}), 400

            if not validar_nome(dados["nome"]):
                return jsonify({"erro": "O nome deve conter apenas letras e espaços!"}), 400

            if dados['idade'] <= 0:
                return jsonify({"erro": "Idade invalida"})

            if dados['idade'] < 17:
                return jsonify({"erro": "Idade invalida, muito novo para ser professor"})

            # Impede a alteração do ID para um já existente
            if "id" in dados and dados["id"] != idProfessor:
                professor_existe = any(p['id'] == dados["id"] for p in dici["professores"])
                if professor_existe:
                    return jsonify({"erro": "ID já existe para outro professor!"}), 400

            professor.update({dados: i for dados, i in dados.items() if dados != "id"})

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

@app.route('/turmas', methods=['POST'])
def createTurma():
    dados = request.json

    campos_obrigatorios = ['id', 'descricao', 'professor_id', 'ativo']
    if not all(campo in dados for campo in campos_obrigatorios):
        return jsonify({"erro": "Campos obrigatórios faltando!"}), 400

    turma_existe = any(turma['id'] == dados['id'] for turma in dici["turmas"])
    if turma_existe:
        return jsonify({"erro": "Turma ja existente com esse ID"})

    # Verificar se professor_id existe antes de cadastrar a turma
    professor_existe = any(professor['id'] == dados['professor_id'] for professor in dici["professores"])
    if not professor_existe:
        return jsonify({"erro": "Professor não encontrado!"}), 400

    dici['turmas'].append(dados)
    return jsonify({"mensagem": "Turma cadastrada com sucesso!", "turma": dados}), 201


############################################

@app.route("/turmas/<int:idTurma>", methods=['PUT'])
def updateTurmas(idTurma):
    for turma in dici["turmas"]:
        if turma['id'] == idTurma:
            dados = request.json  
            campos_obrigatorios = ['descricao', 'professor_id', 'ativo']

            if not all(campo in dados and dados[campo] not in [None, ""] for campo in campos_obrigatorios):
                return jsonify({"erro": "Todos os campos são obrigatórios!"}), 400

            # Impede a alteração do ID para um já existente
            if "id" in dados and dados["id"] != idTurma:
                turma_existe = any(t['id'] == dados["id"] for t in dici["turmas"])
                if turma_existe:
                    return jsonify({"erro": "ID já existe para outra turma!"}), 400

            turma.update({dados: i for dados, i in dados.items() if dados != "id"})

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

@app.route("/reset", methods=['POST', 'DELETE'])
def resetar_dados():
    if not dici["alunos"] and not dici["professores"]:
        return jsonify({"mensagem": "As listas de alunos e professores já estão vazias!"})

    dici["alunos"].clear()
    dici["professores"].clear()
    return jsonify({"mensagem": "Listas de alunos e professores foram apagadas com sucesso!"})

#-------------------------------------------------------------------##-------------------------------------------------------------------#

if __name__ == "__main__":
    app.run(debug=True)

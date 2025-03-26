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

############################################

@app.route("/alunos/<int:idAluno>", methods=['PUT'])
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



############################################

@app.route("/professores/<int:idProfessor>", methods=['PUT'])
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


############################################

@app.route("/turmas/<int:idTurma>", methods=['PUT'])
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

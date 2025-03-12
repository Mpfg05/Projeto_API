from flask import Flask, jsonify, request

app = Flask(__name__)

lista = {
    "alunos":[
        {
            "id":1,
            "nome":"caio"
        }
    ],

    "professor":[
        {
            "id":1,
            "nome":"rafael"
        }
    ],

     "turma":[
        {
            "id":1,
            "nome":"apis"
        }
    ],
}

app = Flask(__name__) 

@app.route("/alunos", methods = ['GET']) 
def getAluno(): # função do endpoint "/alunos" com verbo "GET"
    dados=lista['alunos'] # da chave "alunos" me retorna uma lista
    return jsonify(dados) # dicionario to json

@app.route("/professores", methods=['GET'])
def getProfessor():
    dados = lista['professores']
    return jsonify(dados)

@app.route('/alunos',methods=['POST'])
def createAluno():
    dados = request.json
    lista['alunos'].append(dados)
    return jsonify(dados)

@app.route("/alunos/<int:idAluno>", methods=['PUT'])
def updateAlunos(idAluno):
    alunos = lista["alunos"]
    for aluno in alunos:
        if aluno['id'] == idAluno:
            dados = request.json
            aluno["id"] = dados['id']
            aluno['nome'] = dados['nome']
            return jsonify(dados)
        else:
            return jsonify("aluno nao encontrado")


if __name__=="__main__":
    app.run(debug=True)

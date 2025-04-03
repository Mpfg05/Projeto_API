from flask import Blueprint, request, jsonify
from .modelAluno import getAluno, getAlunoById, createAluno, updateAlunos, deleteAluno

alunos_blueprint = Blueprint('alunos', __name__)

@alunos_blueprint.route('/alunos', methods=['GET'])
def get_alunos():
    return jsonify(getAluno())

@alunos_blueprint.route('/alunos/<int:idAluno>', methods = ['GET'])
def get_aluno(idAluno):
    try:
        aluno = getAlunoById(idAluno)
        return jsonify(aluno)
    except:
        return jsonify({"erro": "Aluno não encontrado"}), 404
    
@alunos_blueprint.route('/alunos' , methods =['POST'])
def create_aluno():
    data = request.json
    createAluno(data)
    return jsonify(data), 201

@alunos_blueprint.route('/alunos', methods = ['PUT'])
def update_aluno(idAluno):
    data = request.json
    try:
        updateAlunos(idAluno, data)
        return jsonify(getAlunoById(idAluno))
    except:
        return jsonify({"erro": "Aluno não encontrado"}), 404
    
@alunos_blueprint.route('/alunos/<int:idAluno>', methods = ['DELETE'])
def delete_aluno(idAluno):
    try:
        deleteAluno(idAluno)
        return '', 204
    except:
        return jsonify({"erro": "Aluno não encontrado"}), 404

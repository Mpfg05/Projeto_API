from flask import Blueprint, request, jsonify
from .modelAluno import getAluno, getAlunoById, createAluno, updateAluno, deleteAluno
from turmas.modelTurma import getTurmaById, getTurma

from config import db


alunos_blueprint = Blueprint('alunos', __name__)



@alunos_blueprint.route('/alunos', methods=['GET'])
def get_alunos():
    return jsonify(getAluno())




@alunos_blueprint.route('/alunos/<int:idAluno>', methods=['GET'])
def get_aluno(idAluno):
    aluno = getAlunoById(idAluno)
    if aluno:
        return jsonify(aluno)
    return jsonify({"erro": "Aluno não encontrado"}), 404




@alunos_blueprint.route('/alunos', methods=['POST'])
def create_aluno():
    try:
        data = request.json


        if "nome" not in data or not data["nome"].strip():
            return jsonify({"erro": "O campo 'nome' é obrigatório."}), 400   

        if "turma_id" not in data:
            return jsonify({"erro": "O campo 'turma_id' é obrigatório."}), 400  

        turma = getTurmaById(data["turma_id"])
        if not turma:
            return jsonify({"erro": "Turma não encontrada."}), 400  

        novo_aluno, status = createAluno(data) 
        return jsonify(novo_aluno), status
    except Exception as e:
        return jsonify({"erro": "Erro ao criar aluno", "detalhes": str(e)}), 500




@alunos_blueprint.route('/alunos/<int:idAluno>', methods=['PUT', 'PATCH'])
def update_aluno(idAluno):
    try:
        data = request.json
        aluno_existente = getAlunoById(idAluno)
        if not aluno_existente:
            return jsonify({"erro": "Aluno não encontrado"}), 404

        if "id" in data and data["id"] != idAluno:
            return jsonify({"erro": "Não é permitido alterar o ID do aluno."}), 400

        updateAluno(idAluno, data)  
        return jsonify({"mensagem": "Aluno atualizado!"}), 200
    except Exception as e:
        return jsonify({"erro": "Erro ao atualizar aluno", "detalhes": str(e)}), 500




@alunos_blueprint.route('/alunos/<int:idAluno>', methods=['DELETE'])
def delete_aluno(idAluno):
    try:
        aluno_existente = getAlunoById(idAluno)
        if not aluno_existente:
            return jsonify({"erro": "Aluno não encontrado"}), 404

        deleteAluno(idAluno)
        return jsonify({"mensagem": "Aluno removido com sucesso!"}), 200  
    except Exception as e:
        return jsonify({"erro": "Erro ao deletar aluno", "detalhes": str(e)}), 500

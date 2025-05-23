from flask import Blueprint, request, jsonify
from .modelProfessor import getProfessor, getProfessorById, createProfessor, updateProfessores, deleteProfessor
from turmas.modelTurma import getTurmaByProfessor, deleteTurma  
from alunos.modelAluno import getAlunosByTurma  

from config import db


professores_blueprint = Blueprint('professores', __name__)

@professores_blueprint.route('/professores', methods=['GET'])
def get_professores():
    return jsonify(getProfessor())



@professores_blueprint.route('/professores/<int:idProfessor>', methods=['GET'])
def get_professor(idProfessor):
    professor = getProfessorById(idProfessor)
    if professor is not None:
        return jsonify(professor), 200
    return jsonify({"erro": "Professor não encontrado"}), 404




@professores_blueprint.route('/professores', methods=['POST'])
def create_professor():
    try:
        data = request.json

        if "nome" not in data or not isinstance(data["nome"], str) or data["nome"].strip() == "":
            return jsonify({"erro": "O campo 'nome' é obrigatório e deve ser uma string válida."}), 400

        resposta, status = createProfessor(data)

        return jsonify(resposta), status 
    except Exception as e:
        return jsonify({"erro": "Erro ao criar professor", "detalhes": str(e)}), 500



@professores_blueprint.route('/professores/<int:idProfessor>', methods=['PUT', 'PATCH'])
def update_professor(idProfessor):
    try:
        data = request.json
        professor_existente = getProfessorById(idProfessor)

        if not professor_existente:
            return jsonify({"erro": "Professor não encontrado"}), 404

        if "id" in data and data["id"] != idProfessor:
            return jsonify({"erro": "Não é permitido alterar o ID do professor"}), 400
        
        updateProfessores(idProfessor, data)

        professor_atualizado = getProfessorById(idProfessor)  
        return jsonify({"mensagem": "Professor atualizado!", "professor": professor_atualizado}), 200
    except Exception as e:
        return jsonify({"erro": "Erro ao atualizar professor", "detalhes": str(e)}), 500



@professores_blueprint.route('/professores/<int:idProfessor>', methods=['DELETE'])
def delete_professor(idProfessor):
    professor_existente = getProfessorById(idProfessor)

    if professor_existente is None:
        return jsonify({"erro": "Professor não encontrado"}), 404

    turma_do_professor = getTurmaByProfessor(idProfessor)
    if turma_do_professor:
        alunos_na_turma = getAlunosByTurma(turma_do_professor.id)
        if alunos_na_turma:
            return jsonify({"erro": "A turma ainda possui alunos. Remova os alunos para excluir a turma."}), 400
        else:
            deleteTurma(turma_do_professor.id)


    deleteProfessor(idProfessor)
    return jsonify({"mensagem": "Professor removido com sucesso!"}), 200

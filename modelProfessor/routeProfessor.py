from flask import Blueprint, request, jsonify
from .modelProfessor import getProfessor, getProfessorById, createProfessor, updateProfessores, deleteProfessor

professores_blueprint = Blueprint('professores', __name__)

@professores_blueprint.route('/professores', methods =['GET'])
def get_professores():
    return jsonify(getProfessor())


@professores_blueprint.route('/professores/:<int:idProfessor>', methods = ['GET'])
def get_professor(idProfessor):
    try:
        professor = getProfessorById(idProfessor)
        return jsonify(professor)
    except:
        return jsonify({"erro": "Professor não encontrado"}), 404
    

@professores_blueprint.route('/professores', methods = ['POST'])
def create_professor():
    data = request.json
    createProfessor(data)
    return jsonify(data), 201


@professores_blueprint.route('/professores/:<int:idProfessor>', methods = ['PUT'])
def update_professor(idProfessor):
    data = request.json
    try:
        updateProfessores(idProfessor, data)
        return jsonify(getProfessorById(idProfessor))
    except:
        return jsonify({"erro": "Professor não encontrado"}), 404
    

@professores_blueprint.route('/professores/:<int:idProfessor>', methods = ['DELETE'])
def delete_professor(idProfessor):
    try:
        delete_professor(idProfessor)
        return '', 204
    except:
        return jsonify({"erro": "Professor não encontrado"}), 404

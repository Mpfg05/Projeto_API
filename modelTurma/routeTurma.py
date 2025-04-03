from flask import Blueprint, request, jsonify
from .modelTurma import getTurma, getTurmaById, crateTurma, updateTurmas, deleteTurma

turmas_blueprint = Blueprint('turmas', __name__)

@turmas_blueprint.route('/turmas', methods =['GET'])
def get_turmas():
    return jsonify(getTurma())

@turmas_blueprint.route('/turmas/<int:idTurma>', methods = ['GET'])
def get_turma(idTurma):
    try:
        turma = getTurmaById(idTurma)
        return jsonify(turma)
    except:
        return jsonify({"erro": "Turma não encontrada"}), 404
    
@turmas_blueprint.route('/turmas', methods = ['POST'])
def create_turma():
    data = request.json
    crateTurma(data)
    return jsonify(data), 201

@turmas_blueprint.route('/turmas/<int:idTurma>', methods=['PUT'])
def update_turma(idTurma):
    data = request.json
    try:
        updateTurmas(idTurma, data)
        return jsonify(getTurmaById(idTurma))
    except:
        return jsonify({"erro": "Turma não encontrada"}), 404
    
@turmas_blueprint.route('/turmas/<int:idTurma>', methods=['DELETE'])
def delete_turma(idTurma):
    try:
        delete_turma(idTurma)
        return '', 204
    except:
        return jsonify({"erro": "Turma não encontrada"}), 404

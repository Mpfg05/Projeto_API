from flask import Blueprint, request, jsonify
from .modelTurma import getTurma, getTurmaById, createTurma, updateTurmas, deleteTurma
from professores.modelProfessor import getProfessorById 

turmas_blueprint = Blueprint('turmas', __name__)

@turmas_blueprint.route('/turmas', methods=['GET'])
def get_turmas():
    return jsonify(getTurma()), 200

@turmas_blueprint.route('/turmas/<int:idTurma>', methods=['GET'])
def get_turma(idTurma):
    turma = getTurmaById(idTurma)
    if turma is None:
        return jsonify({"erro": "Turma não encontrada"}), 404
    return jsonify(turma), 200


@turmas_blueprint.route('/turmas', methods=['POST'])
def create_turma():
    try:
        data = request.json


        campos_obrigatorios = ['descricao', 'professor_id', 'ativo']
        for campo in campos_obrigatorios:
            if campo not in data or data[campo] in [None, ""]:
                return jsonify({"erro": f"Campo obrigatório '{campo}' está faltando ou inválido."}), 400


        from professores.modelProfessor import getProfessorById
        professor = getProfessorById(data["professor_id"])
        if not professor:
            return jsonify({"erro": "Professor não encontrado."}), 400


        resultado, status = createTurma(data)


        return jsonify(resultado), status

    except Exception as e:
        return jsonify({"erro": "Erro ao criar turma", "detalhes": str(e)}), 500



@turmas_blueprint.route('/turmas/<int:idTurma>', methods=['PUT', 'PATCH'])
def update_turma(idTurma):
    try:
        data = request.json
        turma_existente = getTurmaById(idTurma)

        if turma_existente is None:
            return jsonify({"erro": "Turma não encontrada."}), 404


        if "id" in data and data["id"] != idTurma:
            return jsonify({"erro": "Não pode alterar o id da turma."}), 400

  
        if request.method == 'PUT':
            campos_obrigatorios = ['descricao', 'professor_id', 'ativo']
            for campo in campos_obrigatorios:
                if campo not in data or data[campo] in [None, ""]:
                    return jsonify({"erro": f"Campo obrigatório '{campo}' está faltando ou inválido."}), 400


        if "professor_id" in data:
            from professores.modelProfessor import getProfessorById
            professor = getProfessorById(data["professor_id"])
            if not professor:
                return jsonify({"erro": "Professor não encontrado."}), 400


        if "descricao" in data and not data["descricao"].strip():
            return jsonify({"erro": "O campo 'descricao' não pode estar vazio."}), 400

        updateTurmas(idTurma, data)

        return jsonify({"mensagem": "Turma atualizada!", "turma": getTurmaById(idTurma)}), 200

    except Exception as e:
        print("Erro ao editar turma:", e)
        return jsonify({"erro": "Erro ao editar turma", "detalhes": str(e)}), 500


@turmas_blueprint.route('/turmas/<int:idTurma>', methods=['DELETE'])
def delete_turma(idTurma):
    try:
        turma_existente = getTurmaById(idTurma)
        if not turma_existente:
            return jsonify({"erro": "Turma não encontrada"}), 404

        deleteTurma(idTurma)  
        return jsonify({"mensagem": "Turma removida com sucesso!"}), 200
    except Exception as e:
        return jsonify({"erro": "Erro ao deletar turma", "detalhes": str(e)}), 500

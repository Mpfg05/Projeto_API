from flask_restx import Namespace, Resource, fields
from turmas.modelTurma import getTurma, getTurmaById, createTurma, updateTurmas, deleteTurma

turmas_ns = Namespace("turmas", description="Operações relacionadas as turmas")

turma_model = turmas_ns.model("Turma", {
    "descricao": fields.String(required=True, description="Descrição da turma"),
    "ativo": fields.Boolean(required=True, description="Turma esta ativada ou desativada"),
    "professor_id": fields.Integer(required=True, description="ID do Professor associado")
})

turma_output_model = turmas_ns.model("TurmaOutput", {
    "id": fields.Integer(description="ID do aluno"),
    "descricao": fields.String(description="Descrição da turma"),
    "ativo": fields.Boolean(description="Turma esta ativada ou desativada"),
    "professor_id": fields.Integer(description="ID do Professor associado")
})


@turmas_ns.route("/")
class AlunosResource(Resource):
    @turmas_ns.marshal_list_with(turma_output_model)
    def get(self):
        return getTurma()

    @turmas_ns.expect(turma_model)
    def post(self):
        data = turmas_ns.payload
        response, status_code = createTurma(data)
        return response, status_code

@turmas_ns.route("/<int:id_turma>")
class AlunoIdResource(Resource):
    @turmas_ns.marshal_with(turma_output_model)
    def get(self, id_turma):
        return getTurmaById(id_turma)

    @turmas_ns.expect(turma_model)
    def put(self, id_turma):
        data = turmas_ns.payload
        updateTurmas(id_turma, data)
        return data, 200

    def delete(self, id_turma):
        deleteTurma(id_turma)
        return {"message": "Turma excluído com sucesso"}, 200

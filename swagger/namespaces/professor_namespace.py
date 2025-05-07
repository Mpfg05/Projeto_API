from flask_restx import Namespace, Resource, fields
from professores.modelProfessor import getProfessor, getProfessorById, createProfessor, updateProfessores, deleteProfessor

professores_ns = Namespace("professores", description="Operações relacionadas aos professores")

professor_model = professores_ns.model("Professor", {
    "nome": fields.String(required=True, description="Nome do professor"),
    "idade": fields.Integer(required=True, description="Idade do professor"),
    "observacoes": fields.String(required=True, description="Observações sobre o professor"),
    "materia": fields.String(required=True, description="Matéria dada pelo professor")

})

professor_output_model = professores_ns.model("ProfessorOutput", {
    "id": fields.Integer(description="ID do professor"),
    "nome": fields.String(description="Nome do professor"),
    "idade": fields.Integer(description="Idade do professor"),
    "materia": fields.String(description="Matéria dada pelo professor"),
    "observacoes": fields.String(description="Observações sobre o professor")
})

@professores_ns.route("/")
class AlunosResource(Resource):
    @professores_ns.marshal_list_with(professor_output_model)
    def get(self):
        return getProfessor()

    @professores_ns.expect(professor_model)
    def post(self):
        data = professores_ns.payload
        response, status_code = createProfessor(data)
        return response, status_code

@professores_ns.route("/<int:id_professor>")
class AlunoIdResource(Resource):
    @professores_ns.marshal_with(professor_output_model)
    def get(self, id_professor):
        return getProfessorById(id_professor)

    @professores_ns.expect(professor_model)
    def put(self, id_professor):
        data = professores_ns.payload
        updateProfessores(id_professor, data)
        return data, 200

    def delete(self, id_professor):
        deleteProfessor(id_professor)
        return {"message": "Professor excluído com sucesso"}, 200

from professores.modelProfessor import Professor
from config import db


class Turma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'), nullable=False)
    ativo = db.Column(db.Boolean, default=True, nullable=False)

    alunos = db.relationship('Aluno', backref='turma', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "descricao": self.descricao,
            "professor_id": self.professor_id,
            "ativo": self.ativo
        }

def getTurma():
    turmas = Turma.query.all()
    return [turma.to_dict() for turma in turmas]

def getTurmaById(idTurma):
    turma = db.session.get(Turma, idTurma)
    return turma.to_dict() if turma else None

def createTurma(dados):
    campos_obrigatorios = ['descricao', 'professor_id', 'ativo']
    if not all(campo in dados for campo in campos_obrigatorios):
        return {"erro": "Campos obrigatórios faltando. Use ('descricao', 'professor_id', 'ativo')."}, 400

    professor = db.session.get(Professor, dados['professor_id'])
    if not professor:
        return {"erro": "Professor não encontrado!"}, 400

    nova_turma = Turma(
        descricao=dados['descricao'],
        professor_id=dados['professor_id'],
        ativo=bool(dados['ativo'])  
    )

    db.session.add(nova_turma)
    db.session.commit()

    return {"mensagem": "Turma cadastrada com sucesso!", "turma": nova_turma.to_dict()}, 201

def updateTurmas(idTurma, novos_dados):
    turma = db.session.get(Turma, idTurma)
    if not turma:
        return {"erro": "Turma não encontrada"}, 404

    campos_obrigatorios = ['descricao', 'professor_id', 'ativo']
    if not all(campo in novos_dados and novos_dados[campo] not in [None, ""] for campo in campos_obrigatorios):
        return {"erro": "Todos os campos são obrigatórios!"}, 400

    professor = db.session.get(Professor, novos_dados['professor_id'])
    if not professor:
        return {"erro": "Professor não encontrado!"}, 400

    turma.descricao = novos_dados['descricao']
    turma.professor_id = novos_dados['professor_id']
    turma.ativo = novos_dados['ativo']

    db.session.commit()
    return {"mensagem": "Turma atualizada!", "turma": turma.to_dict()}

def getTurmaByProfessor(professor_id):
    turma = Turma.query.filter_by(professor_id=professor_id).first()
    return turma


def deleteTurma(idTurma):
    turma = db.session.get(Turma, idTurma)
    if turma:
        db.session.delete(turma)
        db.session.commit()
        return {"mensagem": "Turma removida com sucesso!"}
    return {"erro": "Turma não encontrada"}, 404

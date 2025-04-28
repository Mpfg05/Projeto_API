import re
from datetime import datetime
from config import db

class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)    
    data_nascimento = db.Column(db.String(10), nullable=False)
    materia = db.Column(db.String(100), nullable=False)    
    observacoes = db.Column(db.String(100), nullable=False)

    turmas = db.relationship('Turma', backref='professor', lazy=True)

    def to_dict(self, incluir_turma=False):
        professor_dict = {
            "id": self.id,
            "nome": self.nome,
            "idade": self.idade,
            "data_nascimento": self.data_nascimento,
            "observacoes": self.observacoes,
            "materia": self.materia
        }
        if incluir_turma and hasattr(self, 'turmas'):
            professor_dict["turmas"] = [turma.to_dict() for turma in self.turmas]

        return professor_dict
        
        
def validar_nome(nome):
    return bool(re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ ]+$", nome))

def calcular_idade(data_nascimento):
    try:
        nascimento = datetime.strptime(data_nascimento, "%d/%m/%Y")
        hoje = datetime.today()
        idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
        return idade
    except ValueError:
        return None

def getProfessor():
    professores = Professor.query.all()
    return [professor.to_dict() for professor in professores]    

def getProfessorById(idProfessor):
    professor = db.session.get(Professor, idProfessor)
    return professor.to_dict(incluir_turma=True) if professor else {"erro": "Professor não encontrado"}

def createProfessor(dados):
    campos_obrigatorios = ['nome', 'materia', 'observacoes', 'data_nascimento']
    if not all(campo in dados for campo in campos_obrigatorios):
        return {"erro": "Campos obrigatórios faltando. Use ('nome', 'materia', 'observacoes', 'data_nascimento')."}, 400

    if not validar_nome(dados["nome"]):
        return {"erro": "O nome deve conter apenas letras e espaços!"}, 400

    idade = calcular_idade(dados["data_nascimento"])
    if idade is None or idade < 17:
        return {"erro": "Data de nascimento inválida ou idade insuficiente. Mínimo 17 anos."}, 400

    novo_professor = Professor(
        nome=dados["nome"],
        idade=idade,
        data_nascimento=dados["data_nascimento"],
        observacoes=dados["observacoes"],
        materia=dados["materia"]
    )

    db.session.add(novo_professor)
    db.session.commit()
    return {"mensagem": "Professor cadastrado com sucesso!", "aluno": novo_professor.to_dict()}, 201



def updateProfessores(idProfessor, novos_dados):
    professor = db.session.get(Professor, idProfessor)
    
    if not professor:
        return {"erro": "Professor não encontrado"}, 404

    if "nome" in novos_dados:
        if not validar_nome(novos_dados["nome"]):
            return {"erro": "O nome deve conter apenas letras e espaços!"}, 400
        professor.nome = novos_dados["nome"]

    if "materia" in novos_dados:
        professor.materia = novos_dados["materia"]

    if "observacoes" in novos_dados:
        professor.observacoes = novos_dados["observacoes"]

    if "data_nascimento" in novos_dados:
        idade = calcular_idade(novos_dados["data_nascimento"])
        if idade is None or idade < 17:
            return {"erro": "Data de nascimento inválida ou idade insuficiente. Mínimo 17 anos."}, 400
        professor.data_nascimento = novos_dados["data_nascimento"]
        professor.idade = idade

    db.session.commit()
    return {"mensagem": "Professor atualizado!", "aluno": professor.to_dict()}

def deleteProfessor(idProfessor):
    professor = db.session.get(Professor, idProfessor)
    if professor:
        db.session.delete(professor)
        db.session.commit()
        return {"mensagem": "Professor removido com sucesso!"}
    return {"erro": "Professor não encontrado"}, 404

import re
from datetime import datetime
from config import db
from turmas.modelTurma import Turma


class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id'), nullable=False)
    data_nascimento = db.Column(db.String(10), nullable=False)
    nota_primeiro_semestre = db.Column(db.Float, nullable=False)
    nota_segundo_semestre = db.Column(db.Float, nullable=False)

    def to_dict(self):
        media_final = (self.nota_primeiro_semestre + self.nota_segundo_semestre) / 2
        aluno_dict = {
            "id": self.id,
            "nome": self.nome,
            "idade": self.idade,
            "turma_id": self.turma_id,
            "data_nascimento": self.data_nascimento,
            "nota_primeiro_semestre": self.nota_primeiro_semestre,
            "nota_segundo_semestre": self.nota_segundo_semestre,
            "media_final": media_final  
        }
        if incluir_turma and self.turma:
            aluno_dict["turma"] = self.turma.to_dict()
    
        return aluno_dict

        
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

def getAluno():
    alunos = Aluno.query.all()
    return [aluno.to_dict() for aluno in alunos]

def getAlunoById(idAluno):
    aluno = db.session.get(Aluno, idAluno)
    return aluno.to_dict(incluir_turma=True) if aluno else {"erro": "Aluno não encontrado"}


def createAluno(dados):
    campos_obrigatorios = ['nome', 'turma_id', 'data_nascimento', 'nota_primeiro_semestre', 'nota_segundo_semestre']
    if not all(campo in dados for campo in campos_obrigatorios):
        return {"erro": "Campos obrigatórios faltando!"}, 400

    if not validar_nome(dados["nome"]):
        return {"erro": "O nome deve conter apenas letras e espaços!"}, 400

    turma = db.session.get(Turma, dados['turma_id'])
    if not turma:
        return {"erro": "Turma não encontrada!"}, 400

    idade = calcular_idade(dados["data_nascimento"])
    if idade is None:
        return {"erro": "Data de nascimento inválida. Use o formato DD/MM/AAAA."}, 400

    novo_aluno = Aluno(
        nome=dados["nome"],
        idade=idade,
        turma_id=dados["turma_id"],
        data_nascimento=dados["data_nascimento"],
        nota_primeiro_semestre=dados["nota_primeiro_semestre"],
        nota_segundo_semestre=dados["nota_segundo_semestre"]
    )

    db.session.add(novo_aluno)
    db.session.commit()

    return {"mensagem": "Aluno cadastrado com sucesso!", "aluno": novo_aluno.to_dict()}, 201

def updateAluno(idAluno, novos_dados):
    aluno = db.session.get(Aluno, idAluno)
    if not aluno:
        return {"erro": "Aluno não encontrado"}, 404

    campos_obrigatorios = ['nome', 'turma_id', 'data_nascimento', 'nota_primeiro_semestre', 'nota_segundo_semestre']
    if not all(campo in novos_dados and novos_dados[campo] not in [None, ""] for campo in campos_obrigatorios):
        return {"erro": "Todos os campos são obrigatórios!"}, 400

    if not validar_nome(novos_dados["nome"]):
        return {"erro": "O nome deve conter apenas letras e espaços!"}, 400

    turma = db.session.get(Turma, novos_dados["turma_id"])
    if not turma:
        return {"erro": "Turma inexistente!"}, 400

    idade = calcular_idade(novos_dados["data_nascimento"])
    if idade is None:
        return {"erro": "Data de nascimento inválida. Use o formato DD/MM/AAAA."}, 400


    aluno.nome = novos_dados["nome"]
    aluno.turma_id = novos_dados["turma_id"]
    aluno.data_nascimento = novos_dados["data_nascimento"]
    aluno.nota_primeiro_semestre = novos_dados["nota_primeiro_semestre"]
    aluno.nota_segundo_semestre = novos_dados["nota_segundo_semestre"]
    aluno.idade = idade  

    db.session.commit()

    return {"mensagem": "Aluno atualizado!"}

def getAlunosByTurma(turma_id):
    alunos = Aluno.query.filter_by(turma_id=turma_id).all()
    return alunos


def deleteAluno(idAluno):
    aluno = db.session.get(Aluno, idAluno)
    if aluno:
        db.session.delete(aluno)
        db.session.commit()
        return {"mensagem": "Aluno removido com sucesso!"}
    return {"erro": "Aluno não encontrado"}, 404

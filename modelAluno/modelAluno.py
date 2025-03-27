import re  # Importa regex para validar o nome 
from datetime import datetime


dici = {
    "alunos": [
        {
            "id": 1,
            "nome": "Joel",
            "idade": 20,
            "turma_id": 1,
            "data_nascimento": "17/10/2005",
            "nota_primeiro_semestre": 5,
            "nota_segundo_semestre": 5  
        }
    ],
}


class AlunoNaoEncontrado(Exception):
    pass

def validar_nome(nome):
    return bool(re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ ]+$", nome))


def getAluno():
    dados = dici['alunos']  
    return dici

def getAlunoById(idAluno):
    for aluno in dici["alunos"]:
        if aluno["id"] == idAluno:
            return dici
        
    raise AlunoNaoEncontrado

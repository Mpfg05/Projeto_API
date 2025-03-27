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


def getAluno():
    return dici["alunos"]

def getAlunoById(idAluno):
    for aluno in dici["alunos"]:
        if aluno["id"] == idAluno:
            return dici
    try:
        getAlunoById(idAluno)
        return True
    except AlunoNaoEncontrado:
        return False
        


def createAluno(dict):
    dici["alunos"].append(dict)



def updateAlunos(idAluno, novos_dados):
    aluno = getAlunoById(idAluno)
    aluno.update(novos_dados)


def deleteAluno(idAluno):
    aluno = getAlunoById(idAluno)
    dici['alunos'].remove(aluno)

def reset():
    dici['alunos'] = [] 

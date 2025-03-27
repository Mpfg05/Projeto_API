dici = {
    "alunos": [
        {
            "id": 1,
            "descricao": "APIs 4B manhã",
            "professor_id": 1,
            "ativo": True
        }
    ]
}


class TurmaNaoEncontrado(Exception):
    pass


def getTurma():
    return dici["turmas"]

def getTurmaById(idTurma):
    for turma in dici["turmas"]:
        if turma["id"] == idTurma:
            return dici
    try:
        getTurmaById(idTurma)
        return True
    except TurmaNaoEncontrado:
        return False
        


def createTurma(dict):
    dici["turmas"].append(dict)



def updateTurma(idTurma, novos_dados):
    turma = getTurmaById(idTurma)
    turma.update(novos_dados)


def deleteTurma(idTurma):
    turma = getTurmaById(idTurma)
    dici['turmas'].remove(turma)

def reset():
    dici['turmas'] = [] 

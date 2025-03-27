dici = {
    "alunos": [
        {
            "id": 1,
            "nome": "Cleber Machado",
            "idade": 40,
            "materia": "matemática",
            "observacoes": "um professor muito esperto e reconhecido pelo MEC"
        }
    ]
}


class ProfessorNaoEncontrado(Exception):
    pass


def getProfessor():
    return dici["professores"]

def getProfessorById(idProfessor):
    for professor in dici["professores"]:
        if professor["id"] == idProfessor:
            return dici
    try:
        getProfessorById(idProfessor)
        return True
    except ProfessorNaoEncontrado:
        return False
        


def createProfessor(dict):
    dici["professores"].append(dict)



def updateProfessor(idProfessor, novos_dados):
    professor = getProfessorById(idProfessor)
    professor.update(novos_dados)


def deleteProfessor(idProfessor):
    professor = getProfessorById(idProfessor)
    dici['professores'].remove(professor)

def reset():
    dici['professores'] = [] 

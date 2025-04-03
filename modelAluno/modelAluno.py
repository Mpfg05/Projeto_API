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

    "turmas": [
        {
            "id": 1,
            "descricao": "APIs 4B manhã",
            "professor_id": 1,
            "ativo": True
        }
    ],
}



def getAluno():
    return dici["alunos"]

def getAlunoById(idAluno):
    for aluno in dici["alunos"]:
        if aluno["id"] == idAluno:
            return aluno
    return None

def createAluno(dados):
    novo_id = max([aluno["id"] for aluno in dici["alunos"]], default=0) + 1
    dados["id"] = novo_id

    data_nascimento = datetime.strptime(dados["data_nascimento"], "%d/%m/%Y")
    hoje = datetime.now()
    idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))
    dados["idade"] = idade

    dados["media_final"] = (dados["nota_primeiro_semestre"] + dados["nota_segundo_semestre"]) / 2

    dici["alunos"].append(dados)
    return dados


def updateAlunos(idAluno,novos_dados):
    aluno = getAlunoById(idAluno)
    if aluno:
        aluno.update(novos_dados)
        return aluno
    return None



def deleteAluno(idAluno):
    aluno = getAlunoById(idAluno)
    if aluno:
        dici["alunos"].remove(aluno)
        return True
    return False

import re
dici = {
    "professores": [  
        {
            "id": 1,
            "nome": "Cleber Machado",
            "idade": 40,
            "materia": "matemática",
            "observacoes": "um professor muito esperto e reconhecido pelo MEC"
        }
    ] 
}

def validar_nome(nome):
    return bool(re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ ]+$", nome))

def getProfessor():
    return dici["professores"]

def getProfessorById(idProfessor):
    for professor in dici["professores"]:
        if professor["id"] == idProfessor:
            return professor
    return None

def createProfessor(dados):

    campos_obrigatorios = ['nome', 'idade', 'materia', 'observacoes']


    if not all(campo in dados for campo in campos_obrigatorios):
        return {"erro": "Campos obrigatórios faltando. Use ('nome', 'idade', 'materia', 'observacoes')."}, 400

  
    if not validar_nome(dados["nome"]):
        return {"erro": "O nome deve conter apenas letras e espaços!"}, 400
    
    if dados['idade'] <= 0:
        return {"erro": "Idade inválida"}, 400

    if dados['idade'] < 17:
        return {"erro": "Idade inválida, muito novo para ser professor"}, 400

 
    novo_id = max([prof["id"] for prof in dici["professores"]], default=0) + 1
    dados["id"] = novo_id

    dici['professores'].append(dados)
    return {"mensagem": "Professor cadastrado com sucesso!", "professor": dados}, 201

def updateProfessores(idProfessor, novos_dados):
    professor = getProfessorById(idProfessor)
    if professor:
        professor.update(novos_dados)
        return professor
    return None

def deleteProfessor(idProfessor):
    professor = getProfessorById(idProfessor)
    if professor:
        dici["professores"].remove(professor)
        return True
    return False

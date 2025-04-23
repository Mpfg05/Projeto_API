import re
from datetime import datetime

dici = {
    "professores": [  
        {
            "id": 1,
            "nome": "Cleber Machado",
            "idade": 40,
            "materia": "matemática",
            "observacoes": "um professor muito esperto e reconhecido pelo MEC",
            "data_nascimento": "01/01/1984"
        }
    ] 
}

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
    return dici["professores"]

def getProfessorById(idProfessor):
    for professor in dici["professores"]:
        if professor["id"] == idProfessor:
            return professor
    return {"erro": "Professor não encontrado"}

def createProfessor(dados):
    campos_obrigatorios = ['nome', 'materia', 'observacoes', 'data_nascimento']
    if not all(campo in dados for campo in campos_obrigatorios):
        return {"erro": "Campos obrigatórios faltando. Use ('nome', 'materia', 'observacoes', 'data_nascimento')."}, 400

    if not validar_nome(dados["nome"]):
        return {"erro": "O nome deve conter apenas letras e espaços!"}, 400

    idade = calcular_idade(dados["data_nascimento"])
    if idade is None or idade < 17:
        return {"erro": "Data de nascimento inválida ou idade insuficiente. Mínimo 17 anos."}, 400

    dados.pop("idade", None)
    novo_id = max([prof["id"] for prof in dici["professores"]], default=0) + 1
    dados["id"] = novo_id
    dados["idade"] = idade

    dici['professores'].append(dados)
    return {"mensagem": "Professor cadastrado com sucesso!", "professor": dados}, 201

def updateProfessores(idProfessor, novos_dados):
    professor = getProfessorById(idProfessor)
    if not professor or "erro" in professor:
        return {"erro": "Professor não encontrado"}, 404

    if "nome" in novos_dados and not validar_nome(novos_dados["nome"]):
        return {"erro": "O nome deve conter apenas letras e espaços!"}, 400

    if "data_nascimento" in novos_dados:
        idade = calcular_idade(novos_dados["data_nascimento"])
        if idade is None or idade < 17:
            return {"erro": "Data de nascimento inválida ou idade insuficiente. Mínimo 17 anos."}, 400
        novos_dados["idade"] = idade

    novos_dados.pop("idade", None)  # ignora tentativas de alterar diretamente
    professor.update({k: v for k, v in novos_dados.items() if k != "id"})
    return {"mensagem": "Professor atualizado com sucesso!", "professor": professor}, 200

def deleteProfessor(idProfessor):
    professor = getProfessorById(idProfessor)
    if professor and "erro" not in professor:
        dici["professores"].remove(professor)
        return {"mensagem": "Professor removido com sucesso!"}, 200
    return {"erro": "Professor não encontrado"}, 404

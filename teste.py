import requests
import unittest
import time
import json
from app import app

URL_Base = "http://127.0.0.1:8000"

class TesteAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        time.sleep(1)

      
        resposta_professor = requests.get(f"{URL_Base}/professores")
        professores = resposta_professor.json()
        if professores:
            self.professor_id = professores[0]['id']
        else:
            dados_professor = {
                "nome": "Professor Teste",
                "idade": "30",
                "materia": "Teste",
                "observacoes": "Professor apaixonada pela disciplina."
            }
            resposta = requests.post(f"{URL_Base}/professores", json=dados_professor)
            self.professor_id = resposta.json().get('id', 1)

      
        resposta_turmas = requests.get(f"{URL_Base}/turmas")
        turmas = resposta_turmas.json()
        if turmas:
            self.turma_id = turmas[0]['id']
        else:
            dados_turma = {
                "descricao": "Turma de Teste",
                "professor_id": self.professor_id,
                "ativo": True
            }
            resposta = requests.post(f"{URL_Base}/turmas", json=dados_turma)
            self.turma_id = resposta.json().get('id', 1)

       
        resposta_alunos = requests.get(f"{URL_Base}/alunos")
        alunos = resposta_alunos.json()
        if alunos:
            self.aluno_id = alunos[0]['id']
        else:
            dados_aluno = {
                "nome": "Aluno Teste",
                "turma_id": self.turma_id,
                "data_nascimento": "01/01/2005",
                "nota_primeiro_semestre": 8,
                "nota_segundo_semestre": 8
            }
            resposta = requests.post(f"{URL_Base}/alunos", json=dados_aluno)
            self.aluno_id = resposta.json().get('id', 1)

        time.sleep(0.5)

    

    def test_01p_get_lista_professores(self):
        resposta = requests.get(f"{URL_Base}/professores")
        self.assertIsInstance(resposta.json(), list)

    def test_02p_get_professor_por_id(self):
        resposta = requests.get(f"{URL_Base}/professores/{self.professor_id}")
        self.assertEqual(resposta.status_code, 200)
        self.assertIsInstance(resposta.json(), dict)

    def test_03p_post_professores(self):
        dados = {
            "nome": "Ana Costa",
            "idade": "30",
            "materia": "História",
            "observacoes": "Professora apaixonada pela disciplina."
        }
        resposta = self.app.post('/professores', data=json.dumps(dados), content_type='application/json')
        self.assertEqual(resposta.status_code, 201)
        resposta_json = resposta.get_json()
        self.assertEqual(resposta_json['mensagem'], 'Professor cadastrado com sucesso!')

    def test_04p_put_edita_professor(self):
        dados = {
            "nome": "Ana Costa Editada",
            "idade": "30",
            "materia": "Matemática",
            "observacoes": "Atualizado."
        }
        resposta = self.app.put(f'/professores/{self.professor_id}', data=json.dumps(dados), content_type='application/json')
        self.assertEqual(resposta.status_code, 200)
        resposta_json = resposta.get_json()
        self.assertEqual(resposta_json['mensagem'], 'Professor atualizado!')

    def test_05p_get_professor_inexistente(self):
        resposta = requests.get(f"{URL_Base}/professores/999")
        self.assertEqual(resposta.json(), {"erro": "Professor não encontrado"})

    def test_06p_post_professor_sem_nome(self):
        dados = {
            "nome": "",
            "idade": "30",
            "materia": "Matemática Aplicada",
            "observacoes": "Teste"
        }
        resposta = requests.post(f"{URL_Base}/professores", json=dados)
        self.assertIn("erro", resposta.json())

    

    def test_01t_get_lista_turmas(self):
        resposta = requests.get(f"{URL_Base}/turmas")
        self.assertIsInstance(resposta.json(), list)

    def test_02t_post_cria_turmas(self):
        dados = {
            "descricao": "Turma de ADS",
            "professor_id": self.professor_id,
            "ativo": True
        }
        resposta = requests.post(f"{URL_Base}/turmas", json=dados)
        self.assertEqual(resposta.status_code, 201)

    def test_03t_get_turmas_por_id(self):
        resposta = requests.get(f"{URL_Base}/turmas/{self.turma_id}")
        self.assertEqual(resposta.status_code, 200)
        self.assertIsInstance(resposta.json(), dict)

    def test_04t_put_edita_turma(self):
        dados = {
            "descricao": "Turma Atualizada",
            "professor_id": self.professor_id,
            "ativo": True
        }
        resposta = self.app.put(f'/turmas/{self.turma_id}', data=json.dumps(dados), content_type='application/json')
        self.assertEqual(resposta.status_code, 200)
        resposta_json = resposta.get_json()
        self.assertEqual(resposta_json['mensagem'], 'Turma atualizada!')

    def test_05t_get_turma_inexistente(self):
        resposta = requests.get(f"{URL_Base}/turmas/999")
        self.assertEqual(resposta.json(), {"erro": "Turma não encontrada"})

    def test_06t_post_turma_sem_descricao(self):
        dados = {
            "professor_id": self.professor_id,
            "ativo": True
        }
        resposta = requests.post(f"{URL_Base}/turmas", json=dados)
        self.assertIn("erro", resposta.json())

    

    def test_01a_get_alunos(self):
        resposta = requests.get(f"{URL_Base}/alunos")
        self.assertIsInstance(resposta.json(), list)

    def test_02a_post_alunos(self):
        dados = {
            "nome": "Tatianna",
            "turma_id": self.turma_id,
            "data_nascimento": "01/01/2005",
            "nota_primeiro_semestre": 8,
            "nota_segundo_semestre": 8
        }
        resposta = self.app.post('/alunos', json=dados)
        self.assertEqual(resposta.status_code, 201)
        resposta_json = resposta.get_json()
        self.assertEqual(resposta_json['mensagem'], 'Aluno cadastrado com sucesso!')

    def test_03a_edita_aluno(self):
        dados = {
            "nome": "Tatianna Braga",
            "turma_id": self.turma_id,
            "data_nascimento": "01/01/2005",
            "nota_primeiro_semestre": 10,
            "nota_segundo_semestre": 9
        }
        resposta = self.app.put(f'/alunos/{self.aluno_id}', data=json.dumps(dados), content_type='application/json')
        self.assertEqual(resposta.status_code, 200)
        resposta_json = resposta.get_json()
        if isinstance(resposta_json, list):
            resposta_json = resposta_json[0]
        self.assertEqual(resposta_json.get('mensagem'), 'Aluno atualizado!')

    def test_04a_get_alunos_inexistente(self):
        resposta = requests.get(f"{URL_Base}/alunos/999")
        self.assertEqual(resposta.json(), {"erro": "Aluno não encontrado"})

    def test_05a_post_alunos_sem_nome(self):
        dados = {
            "nome": "",
            "turma_id": self.turma_id,
            "data_nascimento": "01/01/2006",
            "nota_primeiro_semestre": 7,
            "nota_segundo_semestre": 9
        }
        resposta = requests.post(f"{URL_Base}/alunos", json=dados)
        self.assertIn("erro", resposta.json())

    
    def test_delete_alunos(self):
        resposta_lista = requests.get(f"{URL_Base}/alunos").json()
        for aluno in resposta_lista:
            requests.delete(f"{URL_Base}/alunos/{aluno['id']}")

    def test_delete_turma(self):
        
        resposta_lista_alunos = requests.get(f"{URL_Base}/alunos").json()
        for aluno in resposta_lista_alunos:
            if aluno['turma_id'] == self.turma_id:
                requests.delete(f"{URL_Base}/alunos/{aluno['id']}")
        
        resposta_lista_turmas = requests.get(f"{URL_Base}/turmas").json()
        if resposta_lista_turmas:
            turma_id = resposta_lista_turmas[0]['id']
            resposta = requests.delete(f"{URL_Base}/turmas/{turma_id}")
            self.assertEqual(resposta.status_code, 200)
        else:
            self.skipTest("Nenhuma turma para deletar")

    def test_delete_professor(self):
        
        while True:
            resposta_lista_turmas = requests.get(f"{URL_Base}/turmas").json()
            turmas_do_professor = [turma for turma in resposta_lista_turmas if turma['professor_id'] == self.professor_id]

            if not turmas_do_professor:
                break

            for turma in turmas_do_professor:
                
                resposta_lista_alunos = requests.get(f"{URL_Base}/alunos").json()
                for aluno in resposta_lista_alunos:
                    if aluno['turma_id'] == turma['id']:
                        requests.delete(f"{URL_Base}/alunos/{aluno['id']}")
                
                requests.delete(f"{URL_Base}/turmas/{turma['id']}")
    
        
        resposta = requests.delete(f"{URL_Base}/professores/{self.professor_id}")
        self.assertEqual(resposta.status_code, 200)


if __name__ == "__main__":
    unittest.main()

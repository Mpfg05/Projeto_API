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
        

        resposta_professor = requests.get(f"{URL_Base}/professores/1")
        if resposta_professor.status_code != 200:
            dados_professor = {
                "data_nascimento": "17/10/2002",
                "materia": "Teste",
                "nome": "Professor Teste",
                "observacoes": "Professora apaixonada pela disciplina."
            }
            requests.post(f"{URL_Base}/professores", json=dados_professor)
        

        resposta_turma = requests.get(f"{URL_Base}/turmas/1")
        if resposta_turma.status_code != 200:
            dados_turma = {
                "descricao": "Turma de Teste",
                "professor_id": 1, 
                "ativo": "true"
            }
            requests.post(f"{URL_Base}/turmas", json=dados_turma)
        

        resposta_aluno = requests.get(f"{URL_Base}/alunos/1")
        if resposta_aluno.status_code != 200:
            dados_aluno = {
                "nome": "Alunos Teste",
                "turma_id": 1,
                "data_nascimento": "01/01/2005",
                "nota_primeiro_semestre": 8,
                "nota_segundo_semestre": 8
            }
            requests.post(f"{URL_Base}/alunos", json=dados_aluno)
        
        time.sleep(1) 





    def test_01p_get_lista_professores(self):
        resposta = requests.get(f"{URL_Base}/professores")
        resposta_json = resposta.json()
        self.assertIsInstance(resposta_json, list)

    def test_02p_get_professor_por_id(self):
        resposta = requests.get(f"{URL_Base}/professores/1")
        self.assertEqual(resposta.status_code, 200)
        self.assertIsInstance(resposta.json(), dict)

    def test_03p_post_professores(self):
        dados = {
            "nome": "Ana Costa",
            "data_nascimento": "17/10/2000",
            "materia": "História",
            "observacoes": "Professora apaixonada pela disciplina."
        }

        resposta = self.app.post('/professores', data=json.dumps(dados), content_type='application/json')

      
        self.assertEqual(resposta.status_code, 201)
        resposta_json = json.loads(resposta.data)
        self.assertEqual(resposta_json['mensagem'], 'Professor cadastrado com sucesso!')

    def test_04p_put_edita_professor(self):
     
        dados = {
            "data_nascimento": "17/10/2002",
            "materia": "Matemática",
            "nome": "Ana Costa",
            "observacoes": "Professora apaixonada pela disciplina."
        }

        resposta = self.app.put(f'/professores/1', data=json.dumps(dados), content_type='application/json')

      
        self.assertEqual(resposta.status_code, 200)
        resposta_json = json.loads(resposta.data)
        self.assertEqual(resposta_json['mensagem'], 'Professor atualizado!')

    def test_05p_get_professor_inexistente(self):
        resposta = requests.get(f"{URL_Base}/professores/999")  
        self.assertEqual(resposta.json(), {"erro": "Professor não encontrado"})

    def test_06p_post_professor_sem_nome(self):
        dados = {
            "data_nascimento": "17/10/2000",
            "materia": "Matemática Aplicada",
            "nome": "",
            "observacoes": "Professor apaixonada pela disciplina."
        }
        resposta = requests.post(f"{URL_Base}/professores", json=dados)
        self.assertIn("erro", resposta.json())





    def test_01t_get_lista_turmas(self):
        resposta = requests.get(f"{URL_Base}/turmas")
        resposta_json = resposta.json()
        self.assertIsInstance(resposta_json, list)

    def test_02t_post_cria_turmas(self):
        dados = {
            "descricao": "Turma de ADS",
            "professor_id": 1, 
            "ativo": True
        }
        resposta = requests.post(f"{URL_Base}/turmas", json=dados)
        self.assertEqual(resposta.status_code, 201)


    def test_03t_get_turmas_por_id(self):
        if requests.get(f"{URL_Base}/turmas/1").status_code != 200:
            dados_turma = {
                "descricao": "Turma de Teste",
                "professor_id": 1,
                "ativo": True
            }
            requests.post(f"{URL_Base}/turmas", json=dados_turma)

        resposta = requests.get(f"{URL_Base}/turmas/1")
        self.assertEqual(resposta.status_code, 200)
        self.assertIsInstance(resposta.json(), dict)



    def test_04t_put_edita_turma(self):
        dados = {
            "descricao": "APIs 4B tarde",
            "professor_id": 1,
            "ativo": True
        }

        resposta = self.app.put(f'/turmas/1', data=json.dumps(dados), content_type='application/json')

        self.assertEqual(resposta.status_code, 200)
        resposta_json = resposta.get_json()
        self.assertEqual(resposta_json['mensagem'], 'Turma atualizada!')


    def test_05t_get_turma_inexistente(self):
        resposta = requests.get(f"{URL_Base}/turmas/999")  
        self.assertEqual(resposta.json(), {"erro": "Turma não encontrada"})

    def test_06t_post_turma_sem_descricao(self):
        dados = {
            "professor_id": 1,
            "ativo": True
        }
        resposta = requests.post(f"{URL_Base}/turmas", json=dados)
        self.assertIn("erro", resposta.json())      




    def test_01a_get_alunos(self):
        resposta = requests.get(f"{URL_Base}/alunos")
        resposta_json = resposta.json()
        self.assertIsInstance(resposta_json, list)

    def test_02a_post_alunos(self):
        dados = {
            "nome": "Tatianna",
            "turma_id": 1,
            "data_nascimento": "01/01/2005",  
            "nota_primeiro_semestre": 8,
            "nota_segundo_semestre": 8
        }

        resposta = self.app.post(f'{URL_Base}/alunos', json=dados)

        self.assertEqual(resposta.status_code, 201)
        resposta_json = resposta.get_json()
        self.assertEqual(resposta_json['mensagem'], 'Aluno cadastrado com sucesso!')


    def test_03a_edita_aluno(self):
        dados = {
            "nome": "Tatianna Braga",
            "turma_id": 1,
            "data_nascimento": "01/01/2005",
            "nota_primeiro_semestre": 10,
            "nota_segundo_semestre": 8
        }

        resposta = self.app.put('/alunos/1', data=json.dumps(dados), content_type='application/json')

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
            "turma_id": 1,
            "data_nascimento": "01/01/2006",
            "nota_primeiro_semestre": 8,
            "nota_segundo_semestre": 8
        }
        resposta = requests.post(f"{URL_Base}/alunos", json=dados)
        self.assertIn("erro", resposta.json()) 
        
    



 

    def test_06a_delete_alunos(self):
        resposta_lista = requests.get(f"{URL_Base}/alunos").json()
        aluno_id = resposta_lista[0]['id'] if resposta_lista else None
        if aluno_id:
            resposta = requests.delete(f"{URL_Base}/alunos/{aluno_id}")
            self.assertEqual(resposta.status_code, 200)
        else:
            self.skipTest("Nenhum aluno encontrado para deletar")

    def test_07t_delete_turma(self):
        turma = requests.get(f"{URL_Base}/turmas/2").json()
        turma_id = turma.get('id')
        if turma_id:
            resposta = requests.delete(f"{URL_Base}/turmas/{turma_id}")
            self.assertEqual(resposta.status_code, 200)
        else:
            self.skipTest("Nenhuma turma encontrada para deletar")

    def test_07p_delete_professor(self):
        professor = requests.get(f"{URL_Base}/professores/2").json()
        professor_id = professor.get('id')
        if professor_id:
            resposta = requests.delete(f"{URL_Base}/professores/{professor_id}")
            self.assertEqual(resposta.status_code, 200)
        else:
            self.skipTest("Nenhum professor encontrado para deletar")


if __name__ == "__main__":
    unittest.main()

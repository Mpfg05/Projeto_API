import requests
import unittest
import time
import json
from app import app

URL_Base = "http://127.0.0.1:5000"

class TesteAPI(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()  # Inicializa o test client
        self.app.testing = True  # Habilita o modo de teste
        time.sleep(1)
        
        # Garantir que o professor com id=1 exista
        resposta_professor = requests.get(f"{URL_Base}/professores/1")
        if resposta_professor.status_code != 200:
            dados_professor = {
                "id": 1,
                "nome": "Professor Teste",
                "idade": 35,
                "materia": "Matemática",
                "observacoes": "Muito bom"
            }
            requests.post(f"{URL_Base}/professores", json=dados_professor)
        
        # Garantir que a turma com id=1 exista
        resposta_turma = requests.get(f"{URL_Base}/turmas/1")
        if resposta_turma.status_code != 200:
            dados_turma = {
                "id": 1,
                "descricao": "Turma Teste",
                "professor_id": 1,  # Associando o professor com id=1
                "ativo": True
            }
            requests.post(f"{URL_Base}/turmas", json=dados_turma)
        
        # Garantir que o aluno com id=1 exista
        resposta_aluno = requests.get(f"{URL_Base}/alunos/1")
        if resposta_aluno.status_code != 200:
            dados_aluno = {
                "id": 1,
                "nome": "Aluno Teste",
                "idade": 22,
                "turma_id": 1  # Associando a turma com id=1
            }
            requests.post(f"{URL_Base}/alunos", json=dados_aluno)
        
        time.sleep(1)  # Aguarde a criação dos recursos

    # Teste alunos
    def test_get_alunos(self):
        resposta = requests.get(f"{URL_Base}/alunos")
        resposta_json = resposta.json()
        self.assertIsInstance(resposta_json, list)

    def test_post_alunos(self):
        dados = {
            "id": 2,
            "nome": "Maria Oliveira",
            "idade": 19,
            "turma_id": 1,
            "data_nascimento": "01/01/2005",
            "nota_primeiro_semestre": 7,
            "nota_segundo_semestre": 8
                }

        resposta = self.app.post('/alunos', json=dados)

        # Verificar se a resposta foi 201 (criação bem-sucedida)
        self.assertEqual(resposta.status_code, 201)
        resposta_json = resposta.json  # No parentheses here
        self.assertEqual(resposta_json['mensagem'], 'Aluno cadastrado com sucesso!')

    def test_delete_alunos(self):
        resposta_lista = requests.get(f"{URL_Base}/alunos").json()
        aluno_id = resposta_lista[0]['id'] if resposta_lista else None
        if aluno_id:
            resposta = requests.delete(f"{URL_Base}/alunos/{aluno_id}")
            self.assertEqual(resposta.status_code, 200)
        else:
            self.skipTest("Nenhum aluno encontrado para deletar")

    def test_edita_aluno(self):
        dados = {
            "nome": "Joel Lima",
            "idade": 21,
            "turma_id": 1,
            "data_nascimento": "17/10/2004",
            "nota_primeiro_semestre": 6,
            "nota_segundo_semestre": 7
        }

        resposta = self.app.put('/alunos/1', data=json.dumps(dados), content_type='application/json')

        # Verificar se a resposta foi 200 (sucesso)
        self.assertEqual(resposta.status_code, 200)
        resposta_json = json.loads(resposta.data)
        self.assertEqual(resposta_json['mensagem'], 'Aluno atualizado!')

    def test_get_alunos_inexistente(self):
        resposta = requests.get(f"{URL_Base}/alunos/999")  # ID inexistente
        self.assertEqual(resposta.json(), {"erro": "Aluno não encontrado"})

    def test_post_alunos_sem_nome(self):
        dados = {
            "idade": 20,
            "turma_id": 1
        }
        resposta = requests.post(f"{URL_Base}/alunos", json=dados)
        self.assertIn("erro", resposta.json())  # Espera chave 'erro'
        
    # Teste professores
    def test_100_get_lista_professores(self):
        resposta = requests.get(f"{URL_Base}/professores")
        resposta_json = resposta.json()
        self.assertIsInstance(resposta_json, list)

    def test_102_get_professor_por_id(self):
        resposta = requests.get(f"{URL_Base}/professores/1")
        self.assertEqual(resposta.status_code, 200)
        self.assertIsInstance(resposta.json(), dict)

    def test_post_professores(self):
        dados = {
            "id": 2,
            "nome": "Ana Costa",
            "idade": 35,
            "materia": "História",
            "observacoes": "Professor apaixonada pela disciplina."
        }

        resposta = self.app.post('/professores', data=json.dumps(dados), content_type='application/json')

        # Verificar se a resposta foi 201 (criação bem-sucedida)
        self.assertEqual(resposta.status_code, 201)
        resposta_json = json.loads(resposta.data)
        self.assertEqual(resposta_json['mensagem'], 'Professor cadastrado com sucesso!')

    def test_103_delete_professor(self):
        resposta_lista = requests.get(f"{URL_Base}/professores").json()
        professor_id = resposta_lista[0]['id'] if resposta_lista else None
        if professor_id:
            resposta = requests.delete(f"{URL_Base}/professores/{professor_id}")
            self.assertEqual(resposta.status_code, 200)
        else:
            self.skipTest("Nenhum professor encontrado para deletar")

    def test_104_put_edita_professor(self):
        # Supondo que o professor com ID 1 exista
        dados = {
            "nome": "Cleber Machado",
            "idade": 41,
            "materia": "Matemática Avançada",
            "observacoes": "Professor de excelência!"
        }

        resposta = self.app.put('/professores/1', data=json.dumps(dados), content_type='application/json')

        # Verificar se a resposta foi 200 (sucesso)
        self.assertEqual(resposta.status_code, 200)
        resposta_json = json.loads(resposta.data)
        self.assertEqual(resposta_json['mensagem'], 'Professor atualizado!')

    def test_106_get_professor_inexistente(self):
        resposta = requests.get(f"{URL_Base}/professores/999")  # ID inexistente
        self.assertEqual(resposta.json(), {"erro": "Professor não encontrado"})

    def test_107a_post_professor_sem_nome(self):
        dados = {
            "idade": 30,
            "materia": "História",
            "observacoes": "Bom professor"
        }
        resposta = requests.post(f"{URL_Base}/professores", json=dados)
        self.assertIn("erro", resposta.json())

    # Teste turma
    def test_200_get_lista_turmas(self):
        resposta = requests.get(f"{URL_Base}/turmas")
        resposta_json = resposta.json()
        self.assertIsInstance(resposta_json, list)

    def test_202_get_turmas_por_id(self):
        resposta = requests.get(f"{URL_Base}/turmas/1")
        self.assertEqual(resposta.status_code, 200)
        self.assertIsInstance(resposta.json(), dict)

    def test_201_post_cria_turmas(self):
        dados = {
            "id": 2,
            "descricao": "Turma de Teste",
            "professor_id": 1,  # ID do professor que deve estar presente
            "ativo": True
        }
        resposta = requests.post(f"{URL_Base}/turmas", json=dados)
        self.assertEqual(resposta.status_code, 201)

    def test_203_delete_turma(self):
        resposta_lista = requests.get(f"{URL_Base}/turmas").json()
        turma_id = resposta_lista[0]['id'] if resposta_lista else None
        if turma_id:
            resposta = requests.delete(f"{URL_Base}/turmas/{turma_id}")
            self.assertEqual(resposta.status_code, 200)
        else:
            self.skipTest("Nenhuma turma encontrada para deletar")

    def test_204_put_edita_turma(self):
        dados = {
            "descricao": "APIs 4B tarde",
            "professor_id": 1,
            "ativo": True
        }

        resposta = self.app.put('/turmas/1', data=json.dumps(dados), content_type='application/json')

        # Verificar se a resposta foi 200 (sucesso)
        self.assertEqual(resposta.status_code, 200)
        resposta_json = json.loads(resposta.data)
        self.assertEqual(resposta_json['mensagem'], 'Turma atualizada!')

    def test_206_get_turma_inexistente(self):
        resposta = requests.get(f"{URL_Base}/turmas/999")  # ID inexistente
        self.assertEqual(resposta.json(), {"erro": "Turma não encontrada"})

    def test_207a_post_turma_sem_descricao(self):
        dados = {
            "nome": "Turma A"
        }
        resposta = requests.post(f"{URL_Base}/turmas", json=dados)
        self.assertIn("erro", resposta.json())  # Verifica se o campo 'erro' existe


if __name__ == "__main__":
    unittest.main()

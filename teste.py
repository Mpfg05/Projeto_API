import requests
import unittest

'''
Cada aluno será representado por um dicionário JSON como o seguinte: 
    {
        "id": 1,
        "nome": "Joel",
        "idade": 20,
        "turma_id": 1,
        "data_nascimento": "17/10/2005",
        "nota_primeiro_semestre": 5,
        "nota_segundo_semestre": 5  
    }

Testes 0 e 01:
Na URL /alunos, se o verbo for GET, 
retornaremos uma lista com um dicionário para cada aluno.

Na URL /alunos, com o verbo POST, ocorrerá a criação do aluno,
enviando um desses dicionários 

Teste 02
Na URL /alunos/<int:id>, se o verbo for GET, devolveremos o nome, id, idade, turma_id, data de nascimento, nota do primeiro semestre e do segundo, e a média do aluno. 
(exemplo. /alunos/2 devolve o dicionário do aluno(a) de id 2)

Teste 03
Na URL /reset, apagaremos a lista de alunos e professores (essa URL só atende o verbo POST e DELETE).

Teste 04
Na URL /alunos/<int:id>, se o verbo for DELETE, deletaremos o aluno.
(dica: procure lista.remove)

Teste 05
Na URL /alunos/<int:id>, se o verbo for PUT, 
editaremos o aluno, mudando seu nome. 
Para isso, o usuário vai enviar um dicionário 
com a chave nome, que deveremos processar

Se o usuário manda um dicionário {“nome”:”José”} para a url /alunos/40,
com o verbo PUT, trocamos o nome do usuário 40 para José

Tratamento de erros

Testes 06 a 08b: Erros de usuário darão um código de status 400, e retornarão um dicionário descrevendo o erro. 
No teste 06, tentamos fazer GET, PUT e DELETE na URL  /alunos/15, sendo que o aluno de id 15 não existe. Nesse caso, devemos retornar um código de status 400 e um dicionário {“erro”:'aluno nao encontrado'}
No teste 07, tentamos criar dois alunos com a mesma id. Nesse caso, devemos retornar um código de status 400 e um dicionário {‘erro’:'Aluno ja existente com esse ID'}


No teste 08a, tento enviar um aluno sem nome via post. Nesse caso, devemos retornar um código de status 400 e um dicionário {‘erro’:'aluno sem nome'}
No teste 08b, tento editar um aluno, usando o verbo put, mas mando um dicionário sem nome. Nesse caso, devemos retornar um código de status 400 e um dicionário {“erro”:'aluno sem nome'}
No teste 08c, evito que usem o mesmo ID quando se tenta atualizar o aluno, mudando o ID para um ja existente
No teste 09, tento evitar que aluno coloque qualquer caractere em seu nome
No teste 10, não deixo que o aluno coloque uma idade invalida
Testes 11 a 21: Teremos as URLs análogas para professores.
No teste 22, evito que criam uma turma com o mesmo ID
No teste 23, evito que alterem o ID da turma para um ID ja existente.

'''

class TestStringMethods(unittest.TestCase):


    def test_0_alunos_retorna_lista(self):
        #pega a url /alunos, com o verbo get
        r = requests.get('http://localhost:5002/alunos')

        #o status code foi pagina nao encontrada?
        if r.status_code == 404:
            self.fail("voce nao definiu a pagina /alunos no seu server")

        try:
            obj_retornado = r.json()
            #r.json() é o jeito da biblioteca requests
            #de pegar o arquivo que veio e transformar
            #em lista ou dicionario.
            #Vou dar erro se isso nao for possivel
        except:
            self.fail("queria um json mas voce retornou outra coisa")

        #no caso, tem que ser uma lista
        self.assertEqual(type(obj_retornado),type([]))

    def test_01_adiciona_alunos(self):
        #criar dois alunos (usando post na url /alunos)
        r = requests.post('http://localhost:5002/alunos',json={'nome':'fernando','id':1})
        r = requests.post('http://localhost:5002/alunos',json={'nome':'roberto','id':2})
        
        #pego a lista de alunos (do mesmo jeito que no teste 0)
        r_lista = requests.get('http://localhost:5002/alunos')
        lista_retornada = r_lista.json()#le o arquivo que o servidor respondeu
                                        #e transforma num dict/lista de python

 
    def test_02_aluno_por_id(self):
        #cria um aluno 'mario', com id 20
        r = requests.post('http://localhost:5002/alunos',json={'nome':'mario','id':20})

        #consulta a url /alunos/20, pra ver se o aluno está lá
        resposta = requests.get('http://localhost:5002/alunos/20')
        dict_retornado = resposta.json() #pego o dicionario retornado
        self.assertEqual(type(dict_retornado),dict)
        self.assertIn('nome',dict_retornado)#o dicionario dict_retornado, que veio do servidor, 
        #tem que ter a chave nome
        self.assertEqual(dict_retornado['nome'],'mario')  


    #adiciona um aluno, mas depois reset o servidor
    #e o aluno deve desaparecer
    def test_03_reset(self):
        #criei um aluno, com post
        r = requests.post('http://localhost:5002/alunos',json={'nome':'cicero','id':29})
        #peguei a lista
        r_lista = requests.get('http://localhost:5002/alunos')
        #no momento, a lista tem que ter mais de um aluno
        self.assertTrue(len(r_lista.json()) > 0)

        #POST na url reset: deveria apagar todos os dados do servidor
        r_reset = requests.post('http://localhost:5002/reset')

        #estou verificando se a url reset deu pau
        #se voce ainda nao definiu ela, esse cod status nao vai ser 200
        self.assertEqual(r_reset.status_code,200)

        #pego de novo a lista
        r_lista_depois = requests.get('http://localhost:5002/alunos')
        
        #e agora tem que ter 0 elementos
        self.assertEqual(len(r_lista_depois.json()),0)

    #esse teste adiciona 2 alunos, depois deleta 1
    #e verifica que o numero de alunos realmente diminuiu

    def test_04_deleta(self):
        #apago tudo
        r_reset = requests.post('http://localhost:5002/reset')
        self.assertEqual(r_reset.status_code,200)
        #crio 3 alunos
        requests.post('http://localhost:5002/alunos',json={'nome':'cicero','id':29})
        requests.post('http://localhost:5002/alunos',json={'nome':'lucas','id':28})
        requests.post('http://localhost:5002/alunos',json={'nome':'marta','id':27})
        #pego a lista completa
        r_lista = requests.get('http://localhost:5002/alunos')
        lista_retornada = r_lista.json()
        #a lista completa tem que ter 3 elementos
        self.assertEqual(len(lista_retornada),3)
        #faço um request com delete, pra deletar o aluno de id 28
        requests.delete('http://localhost:5002/alunos/28')
        #pego a lista de novo
        r_lista2 = requests.get('http://localhost:5002/alunos')
        lista_retornada2 = r_lista2.json()
        #e vejo que não tem mais o aluno 28
        self.assertEqual(len(lista_retornada2),2) 


    #cria um usuário, depois usa o verbo PUT
    #para alterar o nome do usuário
    def test_05_edita(self):
        #resetei
        r_reset = requests.post('http://localhost:5002/reset')
        #verifiquei se o reset foi
        self.assertEqual(r_reset.status_code,200)

        #criei um aluno
        requests.post('http://localhost:5002/alunos',json={'nome':'lucas','id':28})
        #e peguei o dicionario dele
        r_antes = requests.get('http://localhost:5002/alunos/28')
        #o nome enviado foi lucas, o nome recebido tb
        self.assertEqual(r_antes.json()['nome'],'lucas')
        #vou editar. Vou mandar um novo dicionario p/ corrigir o dicionario
        #que já estava no 28 (note que só mandei o nome)
        #para isso, uso o verbo PUT
        requests.put('http://localhost:5002/alunos/28', json={'nome':'lucas mendes'})
        #pego o novo dicionario do aluno 28
        r_depois = requests.get('http://localhost:5002/alunos/28')
        #agora o nome deve ser lucas mendes
        self.assertEqual(r_depois.json()['nome'],'lucas mendes')
        #mas o id nao mudou
        self.assertEqual(r_depois.json()['id'],28)

    #tenta fazer GET, PUT e DELETE num aluno que nao existe
    def test_06a_id_inexistente_no_put(self):
        #reseto
        r_reset = requests.post('http://localhost:5002/reset')
        #vejo se nao deu pau reset
        self.assertEqual(r_reset.status_code,200)
        #estou tentando EDITAR um aluno que nao existe (verbo PUT)
        r = requests.put('http://localhost:5002/alunos/15',json={'nome':'bowser','id':15})
        #tem que dar erro 400 ou 404
        #ou seja, r.status_code tem que aparecer na lista [400,404]
        self.assertIn(r.status_code,[400,404])
        #qual a resposta que a linha abaixo pede?
        #um json, com o dicionario {"erro":"aluno nao encontrado"}
        self.assertEqual(r.json()['erro'],'aluno nao encontrado')
    

    def test_06b_id_inexistente_no_get(self):
        #reseto
        r_reset = requests.post('http://localhost:5002/reset')
        #vejo se nao deu pau resetr
        self.assertEqual(r_reset.status_code,200)
        #agora faço o mesmo teste pro GET, a consulta por id
        r = requests.get('http://localhost:5002/alunos/15')
        self.assertIn(r.status_code,[400,404])
        #olhando pra essa linha debaixo, o que está especificado que o servidor deve retornar
        self.assertEqual(r.json()['erro'],'aluno nao encontrado')
       
    def test_06c_id_inexistente_no_delete(self):
        #reseto
        r_reset = requests.post('http://localhost:5002/reset')
        #vejo se nao deu pau resetr
        self.assertEqual(r_reset.status_code,200)
        r = requests.delete('http://localhost:5002/alunos/15')
        self.assertIn(r.status_code,[400,404])
        self.assertEqual(r.json()['erro'],'aluno nao encontrado')



    #tento criar 2 caras com a  mesma id
    def test_07_criar_com_id_ja_existente(self):

        #dou reset e confiro que deu certo
        r_reset = requests.post('http://localhost:5002/reset')
        self.assertEqual(r_reset.status_code,200)

        #crio o usuario bond e confiro
        r = requests.post('http://localhost:5002/alunos',json={'nome':'bond','id':7})
        self.assertEqual(r.status_code,200)

        #tento usar o mesmo id para outro usuário
        r = requests.post('http://localhost:5002/alunos',json={'nome':'james','id':7})
        # o erro é muito parecido com o do teste anterior
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'id ja utilizada')


    #cria alunos sem nome, o que tem que dar erro
    def test_08a_post_sem_nome(self):
        r_reset = requests.post('http://localhost:5002/reset')
        self.assertEqual(r_reset.status_code,200)

        #tentei criar um aluno, sem enviar um nome
        r = requests.post('http://localhost:5002/alunos',json={'id':8})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'campo obrigatório')
    
    #tenta editar alunos sem passar nome, o que também
    #tem que dar erro (se vc nao mudar o nome, vai mudar o que?)
    def test_08b_put_sem_nome(self):
        r_reset = requests.post('http://localhost:5002/reset')
        self.assertEqual(r_reset.status_code,200)

        #criei um aluno sem problemas
        r = requests.post('http://localhost:5002/alunos',json={'nome':'maximus','id':7})
        self.assertEqual(r.status_code,200)

        #mas tentei editar ele sem mandar o nome
        r = requests.put('http://localhost:5002/alunos/7',json={'id':7})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'campo obrigatório')

    def test_08c_put_mesmo_id(self):
        r_reset = requests.post('http://localhost:5002/reset')
        self.assertEqual(r_reset.status_code,200)

        #criei dois alunos com IDs diferentes
        r = requests.post('http://localhost:5002/alunos',json={'id':7})
        self.assertEqual(r.status_code,200)
        r = requests.post('http://localhost:5002/alunos',json={'id':6})
        self.assertEqual(r.status_code,200)
        #mas tentei editar ele colocando o mesmo ID
        r = requests.put('http://localhost:5002/alunos/7',json={'id':6})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'ID ja sendo utilizado')
    

        #não deixa colocar caracteres invalidos
    def test_09_nome_invalido(self):
        r_reset = requests.post('http://localhost:5002/reset')
        self.assertEqual(r_reset.status_code,200)   

        #tentei criar um aluno, com ! ? + =
        r = requests.post('http://localhost:5002/alunos',json={'nome':"cleber!"})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'nome invalido!')

    def test_09_nome_invalido(self):
        r_reset = requests.post('http://localhost:5002/reset')
        self.assertEqual(r_reset.status_code,200)   
        #tentei criar um aluno, com idade invalida
        r = requests.post('http://localhost:5002/alunos',json={'idade':-4})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'idade invalida!')    


    def test_11_professores_retorna_lista(self):
        r = requests.get('http://localhost:5002/professores')
        self.assertEqual(type(r.json()),type([]))
    
    def test_11b_nao_confundir_professor_e_aluno(self):
        r_reset = requests.post('http://localhost:5002/reset')
        r = requests.post('http://localhost:5002/alunos',json={'nome':'fernando','id':1})
        self.assertEqual(r.status_code,200)
        r = requests.post('http://localhost:5002/alunos',json={'nome':'roberto','id':2})
        self.assertEqual(r.status_code,200)
        r_lista = requests.get('http://localhost:5002/professores')
        self.assertEqual(len(r_lista.json()),0)
        r_lista_alunos = requests.get('http://localhost:5002/alunos')
        self.assertEqual(len(r_lista_alunos.json()),2)

    def test_12_adiciona_professores(self):
        r = requests.post('http://localhost:5002/professores',json={'nome':'fernando','id':1})
        r = requests.post('http://localhost:5002/professores',json={'nome':'roberto','id':2})
        r_lista = requests.get('http://localhost:5002/professores')

    def test_13_professores_por_id(self):
        r = requests.post('http://localhost:5002/professores',json={'nome':'mario','id':20})
        r_lista = requests.get('http://localhost:5002/professores/20')
        self.assertEqual(r_lista.json()['nome'],'mario')

    
    def test_14_adiciona_e_reset(self):
        r = requests.post('http://localhost:5002/professores',json={'nome':'cicero','id':29})
        r_lista = requests.get('http://localhost:5002/professores')
        self.assertTrue(len(r_lista.json()) > 0)
        r_reset = requests.post('http://localhost:5002/reset')
        self.assertEqual(r_reset.status_code,200)
        r_lista_depois = requests.get('http://localhost:5002/professores')
        self.assertEqual(len(r_lista_depois.json()),0)

    def test_15_deleta(self):
        r_reset = requests.post('http://localhost:5002/reset')
        self.assertEqual(r_reset.status_code,200)
        requests.post('http://localhost:5002/professores',json={'nome':'cicero','id':29})
        requests.post('http://localhost:5002/professores',json={'nome':'lucas','id':28})
        r_lista = requests.get('http://localhost:5002/professores')
        self.assertEqual(len(r_lista.json()),2)
        requests.delete('http://localhost:5002/professores/28')
        r_lista = requests.get('http://localhost:5002/professores')
        self.assertEqual(len(r_lista.json()),1)
    
    def test_16_edita(self):
        r_reset = requests.post('http://localhost:5002/reset')
        self.assertEqual(r_reset.status_code,200)
        requests.post('http://localhost:5002/professores',json={'nome':'lucas','id':28})
        r_antes = requests.get('http://localhost:5002/professores/28')
        self.assertEqual(r_antes.json()['nome'],'lucas')
        requests.put('http://localhost:5002/professores/28', json={'nome':'lucas mendes'})
        r_depois = requests.get('http://localhost:5002/professores/28')
        self.assertEqual(r_depois.json()['nome'],'lucas mendes')

    def test_17_id_inexistente(self):
        r_reset = requests.post('http://localhost:5002/reset')
        self.assertEqual(r_reset.status_code,200)
        r = requests.put('http://localhost:5002/professores/15',json={'nome':'bowser','id':15})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'professor nao encontrado')
        r = requests.get('http://localhost:5002/professores/15')
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'professor nao encontrado')
        r = requests.delete('http://localhost:5002/professores/15')
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'professor nao encontrado')

    def test_18_criar_com_id_ja_existente(self):
        r_reset = requests.post('http://localhost:5002/reset')
        self.assertEqual(r_reset.status_code,200)
        r = requests.post('http://localhost:5002/professores',json={'nome':'bond','id':7})
        self.assertEqual(r.status_code,200)
        r = requests.post('http://localhost:5002/professores',json={'nome':'james','id':7})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'id ja utilizada')

    def test_19_post_ou_put_sem_nome(self):
        r_reset = requests.post('http://localhost:5002/reset')
        self.assertEqual(r_reset.status_code,200)
        r = requests.post('http://localhost:5002/professores',json={'id':8})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'professor sem nome')
        r = requests.post('http://localhost:5002/professores',json={'nome':'maximus','id':7})
        self.assertEqual(r.status_code,200)
        r = requests.put('http://localhost:5002/professores/7',json={'id':7})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'professor sem nome')

    def test_20_nao_confundir_professor_e_aluno(self):
        r_reset = requests.post('http://localhost:5002/reset')
        r = requests.post('http://localhost:5002/professores',json={'nome':'fernando','id':1})
        self.assertEqual(r.status_code,200)
        r = requests.post('http://localhost:5002/professores',json={'nome':'roberto','id':2})
        self.assertEqual(r.status_code,200)
        r_lista = requests.get('http://localhost:5002/professores')
        self.assertEqual(len(r_lista.json()),2)
        r_lista_alunos = requests.get('http://localhost:5002/alunos')
        self.assertEqual(len(r_lista_alunos.json()),0)

    def test_09_nome_invalido(self):
        r_reset = requests.post('http://localhost:5002/reset')
        self.assertEqual(r_reset.status_code,200)   

        #tentei criar um aluno, com idade abaixo de 18 anos
        r = requests.post('http://localhost:5002/professores',json={'idade':17})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'idade invalida!')    


    def test_22_put_com_id_ja_existente_turma(self):
        #criei dois professores com IDs diferentes
        r = requests.post('http://localhost:5002/professores',json={'id':7})
        self.assertEqual(r.status_code,200)
        r = requests.post('http://localhost:5002/professores',json={'id':6})
        self.assertEqual(r.status_code,200)
        #mas tentei editar ele colocando o mesmo ID
        r = requests.put('http://localhost:5002/professores/7',json={'id':6})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'ID ja sendo utilizado')

    def test_23_criar_com_id_ja_existente_turma(self):
        #dou reset e confiro que deu certo
        r_reset = requests.post('http://localhost:5002/reset')
        self.assertEqual(r_reset.status_code,200)

        #crio a turma
        r = requests.post('http://localhost:5002/turmas',json={'id':7})
        self.assertEqual(r.status_code,200)
        #tento usar o mesmo id para outra turma
        r = requests.post('http://localhost:5002/turmas',json={'id':7})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'id ja utilizada')






def runTests():
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestStringMethods)
        unittest.TextTestRunner(verbosity=2,failfast=True).run(suite)


if __name__ == '__main__':
    runTests()

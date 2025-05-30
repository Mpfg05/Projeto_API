## 🏫 Sistema de Gerenciamento

## Minha API

```
https://projeto-api-jdan.onrender.com/
```

## 📝 Descrição da API
Este repositório contém a API do Sistema de Gerenciamento, responsável pelo cadastro e gerenciamento de alunos, professores e turmas. Esta API fornece os dados necessários para integração com os microserviços de Reservas e Atividades, compartilhando os IDs de turmas e professores.
Validações feitas via requisição externa:

- Verifica se a **turma existe**: `GET /turmas/<id>`
- *(Opcional)* Verifica se o aluno existe: `GET /alunos/<id>`

---

## 🚀 Tecnologias Utilizadas

- Python 3.x
- Flask
- SQLAlchemy
- SQLite
- Requests 

---


## 🐳 Instruções de Execução (com Docker)
1. Clone o repositório:
   
```bash
git clone https://github.com/Mpfg05/Projeto_API.git
cd Projeto_API
```
 ---

2. Construa a imagem Docker:

```bash
docker build -t sistema-gerenciamento .
```
---

3. Execute o container:

```bash
docker run -d -p 8000:8000 sistema-gerenciamento
```

---


4. A API estará disponível em:
http://localhost:8000

---


## 🏗️ Explicação da Arquitetura Utilizada

* Padrão MVC (Model-View-Controller):
A aplicação foi estruturada seguindo o padrão de projeto MVC, separando as responsabilidades de modelagem de dados, lógica de negócios e manipulação de rotas.

* Banco de Dados:
A persistência dos dados é realizada utilizando SQLite, que armazena informações de alunos, professores e turmas.

* Rotas:
Implementação de endpoints utilizando os métodos HTTP GET e POST para manipulação dos recursos da aplicação.

* Docker:
A aplicação é containerizada utilizando Docker, facilitando o deploy e garantindo a padronização do ambiente de execução.


---

## 🌐 Descrição do Ecossistema de Microserviços

Este projeto faz parte de um ecossistema de microserviços integrados, composto por três APIs:

1. Sistema de Gerenciamento:
Responsável por fornecer os dados mestres de alunos, professores e turmas.

2. Reservas:
Microserviço que realiza a reserva de salas de aula, utilizando o ID da turma fornecido por esta API.

3. Atividades:
Microserviço que gerencia o controle de atividades, utilizando o ID do professor disponibilizado pela API do Sistema de Gerenciamento.

A integração entre os microserviços ocorre por meio de troca de dados através das APIs RESTful, permitindo uma arquitetura desacoplada e escalável.

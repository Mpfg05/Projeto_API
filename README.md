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


2. Build manual da imagem Docker

```bash

docker build -t reserva-salas .
docker run -p 5001:5001 -e API_ESCOLA_URL=http://host.docker.internal:5000 reserva-salas

```
Nota: A API estará disponível em http://localhost:5001

---


## 🏗️ Arquitetura Utilizada

Microsserviço Flask
-Padrão MVC (Model-View-Controller) adaptado para APIs

  - Models: reserva_model.py

  - Views/Controllers: reserva_route.py

  - Database: database.py

Comunicação entre Serviços
- Síncrona via HTTP REST

  - Circuit Breaker (para resiliência quando a API de turmas estiver indisponível)

  - Cache local de turmas válidas (opcional)

- Banco de Dados
  - SQLite para ambiente de desenvolvimento

  - Configuração pronta para migração para PostgreSQL em produção
    
---

## 🌐 Ecossistema de Microsserviços
Serviços Principais
1. API de Reserva de Salas (este serviço)

  - Responsabilidade única: Gestão de reservas

  - Porta: 5001

2. API de Gerenciamento Escolar

  - Fornece dados de turmas e alunos

  - Porta: 5000

Diagrama de Integração
```[Cliente] 
  │
  ├─▶ [API Reserva] POST /reservas
  │     │
  │     └─▶ [API Escola] GET /turmas/{id} (validação)
  │
  └─▶ [API Escola] GET /alunos (dados complementares)
```

Padrões de Integração
1. Validação Síncrona:

  - Antes de criar reserva, verifica turma na API Escola

2. Cache Local (opcional):

  - Armazena temporariamente turmas válidas para reduzir chamadas

3. Retry Pattern:

  - Tentativas automáticas em caso de falha temporária

## 🚀 Como Executar Localmente
### 1. Clone o repositório

```bash
git clone https://github.com/Mpfg05/Reserva_de_salas_flask.git
cd Reserva_de_salas_flask

2. Crie um ambiente virtual (opcional, mas recomendado)
python -m venv venv
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

3. Instale as dependências
pip install -r requirements.txt

4. Execute a API
python app.py
A aplicação estará disponível em: http://localhost:5001

📝 O banco de dados SQLite é criado automaticamente na primeira execução.

📡 Endpoints Principais
GET /reservas – Lista todas as reservas

POST /reservas – Cria uma nova reserva

DELETE /reservas/<id> – Remove uma reserva

✅ Exemplo de JSON para criação de reserva:

{
  "turma_id": 1,
  "sala": "204",
  "data": "2025-05-21",
  "hora_inicio": "10:00",
  "hora_fim": "12:00"
}
```
---

## 🔗 Dependências Externas

🔗 Dependência Externa
Certifique-se de que a API de Gerenciamento Escolar esteja rodando em:

http://localhost:5000
Ela deve ter os seguintes endpoints funcionais:

GET /turmas/<id>

(opcional) GET /alunos/<id>

📁 Estrutura do Projeto
Reserva_de_salas_flask/
│
├── app.py
├── config.py
├── database.py
├── reserva_model.py
├── reserva_route.py
├── instance/
│   └── reservas.db
└── README.md
🛠️ Futuras Melhorias
Validação de conflito de horário

Integração via RabbitMQ ou outra fila

Autenticação e autorização de usuários

Logs e monitoramento com ferramentas externas




- Explicação arquitetural detalhada

- Visão do ecossistema de microsserviços

from swagger.swagger_config import configure_swagger
import pytest
import sys
import os
from config import app, db
from alunos.routeAluno import alunos_blueprint
from professores.routeProfessor import professores_blueprint
from turmas.routeTurma import turmas_blueprint

app.register_blueprint(alunos_blueprint)
app.register_blueprint(professores_blueprint)
app.register_blueprint(turmas_blueprint)

configure_swagger(app)

with app.app_context():
    db.create_all()

def run_tests():
    os.environ['FLASK_ENV'] = 'testing'
    # Executa os testes e captura o resultado
    result = pytest.main(['--maxfail=1', '--disable-warnings', '--tb=short'])
    return result


if __name__ == '__main__':
  result = run_tests()
    
    if result != 0:
        sys.exit("Testes falharam. A aplicação não será iniciada.")

    app.run(host=app.config["HOST"], port=app.config['PORT'], debug=app.config['DEBUG'])

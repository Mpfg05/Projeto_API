import os
from config import app
from alunos.routeAluno import alunos_blueprint
from professores.routeProfessor import professores_blueprint
from turmas.routeTurma import turmas_blueprint

app.register_blueprint(alunos_blueprint)
app.register_blueprint(professores_blueprint)
app.register_blueprint(turmas_blueprint)

if __name__ == '__main__':
  app.run(host=app.config["HOST"], port = app.config['PORT'],debug=app.config['DEBUG'] )

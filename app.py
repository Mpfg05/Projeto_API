from swagger.swagger_config import configure_swagger
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


if __name__ == '__main__':
    app.run(host=app.config["HOST"], port=app.config['PORT'], debug=app.config['DEBUG'])

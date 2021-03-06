from werkzeug.security import generate_password_hash
from estacao.ext.database import db
from estacao.ext.factories import consolidado_factory
from estacao.models import Consolidado, Pressao, Users, Umidade
from datetime import date, datetime


def create_db():
    """Creates database"""
    db.create_all()


def create_user_db():
    db.create_all(bind=['users'])


def drop_db():
    """Drops database"""
    db.drop_all()


def populate_db():
    data = consolidado_factory(11)
    now = datetime.now()
    curr_date = now.date()
    current_data = consolidado_factory(1, curr_date, curr_date)
    data.append(current_data[0])
    Consolidado.query.session.bulk_save_objects(data)
    Consolidado.query.session.commit()
    return Consolidado


def populate_pressao():
    pressao = Pressao(data=date.fromisoformat('2020-02-01'), pressao=192.5)
    pressao.save()
    return Pressao.query.all()


def populate_users():
    password_hash = generate_password_hash('12345', method='md5')
    users = Users(login='login_test', password=password_hash)
    users.save()
    return users


def populate_umidade():
    umidade = Umidade(data=date.fromisoformat('2020-02-01'), ur=80.4)
    umidade.save()
    return umidade


def init_app(app):
    commands = [
            create_db,
            create_user_db,
            drop_db,
            populate_db,
            populate_pressao,
            populate_users,
            populate_umidade
    ]
    for command in commands:
        app.cli.add_command(app.cli.command()(command))

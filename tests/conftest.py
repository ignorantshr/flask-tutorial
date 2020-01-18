# author        :   ignorantshr
# create_date   :   2020/01/18 13:05
# description   :   固件fixture的配置函数

import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import init_db, get_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    # TESTING tell flask in test mode; DATABASE is overwritten
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions:
    def __init__(self, client):
        self._client = client

    # 在app固件中执行了插入test用户数据
    def login(self, username='test', password='test'):
        # POST
        return self._client.post(
            '/auth/login',
            data = {'username': username, 'password': password}
        )

    def logout(self):
        # GET
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)

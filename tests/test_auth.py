# author        :   ignorantshr
# create_date   :   2020/01/18 13:57
# description   :   测试认证功能

import pytest

from flask import session, g
from flaskr.db import get_db


def test_register(client, app):
    assert client.get('/auth/register').status_code == 200

    response = client.post(
        'auth/register',
        data = {'username': 'a', 'password': 'a'}
    )

    assert response.headers['Location'] == 'http://localhost/auth/login'

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'a'",
        ).fetchone() is not None


@pytest.mark.parametrize(('username', 'password', 'message'),(
        ('', 'a', b'username and password is required.'),
        ('a', '', b'username and password is required.'),
        ('test', 'test', b'has already registered'),
))
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data = {'username': username, 'password': password}
    )

    assert message in response.data


def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    # 这样可以在响应返回之后操作环境变量，在请求之外操作 session 会引发一个异常
    with client:
        client.get('/')
        assert session.get('user_id') == 1
        assert g.user['username'] == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'),(
        ('', 'a', 'username and password is required.'),
        ('a', '', 'username and password is required.'),
        ('b', 'b', 'Incorrect username'),
        ('test', 'b', 'Incorrect password'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    print(response.data)
    assert message in response.get_data(as_text=True)


def test_logout(auth, client):
    response = auth.logout()
    assert response.headers['Location'] == 'http://localhost/'

    with client:
        auth.logout()
        assert 'user_id' not in session

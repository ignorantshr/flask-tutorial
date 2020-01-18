# author        :   ignorantshr
# create_date   :   2020/01/18 14:32
# description   :   测试博客功能

import pytest

from flaskr.db import get_db

def assert_response_data(data, response, is_in=True):
    if is_in:
        assert data in response.data
    else:
        assert data not in response.data


def test_index(client, auth):
    response = client.get('/')
    assert_response_data(b'Log In', response)
    assert_response_data(b'Register', response)

    auth.login()
    response = client.get('/')
    assert_response_data(b'Log Out', response)
    assert_response_data(b'test title', response)
    assert_response_data(b'by test on 2019-01-18', response)
    assert_response_data(b'test\nbody', response)
    assert_response_data(b'href="/1/update', response)


@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
    '/1/delete',
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers['Location'] == 'http://localhost/auth/login'


def test_author_required(app, client, auth):
    with app.app_context():
        db = get_db()
        db.execute('UPDATE post SET author_id = 2 WHERE id = 1')
        db.commit()

    auth.login()
    assert client.post('/1/update').status_code == 403
    assert client.post('/1/delete').status_code == 403
    assert b'href="/1/update"' not in client.get('/').data


@pytest.mark.parametrize('path', (
    '/2/update',
    '/2/delete',
))
def test_exist_required(auth, client, path):
    auth.login()
    assert client.post(path).status_code == 404


def test_create(app, auth, client):
    auth.login()
    assert client.get('/create').status_code == 200
    client.post('/create', data={'title': 'test create', 'body': ''})

    with app.app_context():
        db = get_db()
        assert db.execute('SELECT COUNT(*) FROM post').fetchone()[0] == 2


def test_update(app, auth, client):
    auth.login()
    assert client.get('/1/update').status_code == 200
    client.post('/1/update', data={'title': 'test update', 'body': ''})

    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM post WHERE id=1').fetchone()
        assert post['title'] == 'test update'


@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
))
def test_create_update_validate(auth, client, path):
    auth.login()
    response = client.post(path, data={'title': '', 'body': ''})
    assert b'Title is required.' in response.data


def test_delete(auth, client, app):
    auth.login()
    response = client.post('/1/delete')
    assert response.headers['Location'] == 'http://localhost/'

    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM post WHERE id=1').fetchone()
        assert post is None

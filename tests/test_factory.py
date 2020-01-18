# author        :   ignorantshr
# create_date   :   2020/01/18 13:26
# description   :   测试工厂函数create_app

from flaskr import create_app


def test_conf():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'

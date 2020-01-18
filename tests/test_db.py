# author        :   ignorantshr
# create_date   :   2020/01/18 13:32
# description   :   测试数据库

import sqlite3

import pytest
from flaskr.db import get_db


def test_get_closed_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e.value)


def test_init_db_command(runner, monkeypatch):
    class Recoder():
        called = False

    def fake_init_db():
        Recoder.called = True

    monkeypatch.setattr('flaskr.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recoder.called

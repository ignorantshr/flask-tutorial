## test
``` bash
$ cd flask-tutorial
$ python3 -m venv venv
$ . venv/bin/activate

$ # execute this after modify flaskr code
$ pip install -e .
$ pip install pytest coverage
$ pytest -v
# generate test report
$ coverage run -m pytest
$ coverage report
```

## build
``` bash
$ cd flask-tutorial
$ python3 -m venv build-venv
$ . build-venv/bin/activate

$ pip install wheel
# will generate dir build/ and dist/, flaskr-xxx.whl in dist/
$ python setup.py bdist_wheel
```

## run in container
``` bash
$ cd flaskr-install-test
$ python3 -m venv install-venv
$ . install-venv/bin/activate

$ cp ../flask-tutorial/dist/flaskr-1.0.0-py3-none-any.whl .
$ pip install flaskr-1.0.0-py3-none-any.whl
$ export FLASK_APP=flaskr
$ flask init-db
# generate key
$ python -c 'import os; print(os.urandom(16))'
b'\xd0\xff\xcc7VYY~i\xadX\xe9\xa4C$`'
# write config.py to overwrite the default config
$ vi install-venv/var/flaskr-instance/config.py
SECRET_KEY = b'\xd0\xff\xcc7VYY~i\xadX\xe9\xa4C$`'

$ pip install waitress
$ waitress-serve --call 'flaskr:create_app'
```

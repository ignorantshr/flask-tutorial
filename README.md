## test
``` bash
$ cd flask-tutorial
$ python3 -m venv venv
$ . venv/bin/activate

$ # execute this after modify flaskr code
$ pip3 install -e .
$ pip3 install pytest coverage
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

$ pip3 install wheel
# will generate dir build/ and dist/, flaskr-xxx.whl in dist/
$ python setup.py bdist_wheel
```

## run in container with virtual environment
``` bash
$ cd flaskr-install-test
$ python3 -m venv install-venv
$ . install-venv/bin/activate

$ cp ../flask-tutorial/dist/flaskr-1.0.0-py3-none-any.whl .
$ pip3 install flaskr-1.0.0-py3-none-any.whl
$ export FLASK_APP=flaskr
$ flask init-db
# generate key
$ python -c 'import os; print(os.urandom(16))'
b'\xd0\xff\xcc7VYY~i\xadX\xe9\xa4C$`'
# write config.py to overwrite the default config
$ vi install-venv/var/flaskr-instance/config.py
SECRET_KEY = b'\xd0\xff\xcc7VYY~i\xadX\xe9\xa4C$`'

$ pip3 install waitress
$ waitress-serve --call 'flaskr:create_app'
```

## deploy with uWSGI container
``` bash
$ yum install python3-devel gcc
$ pip3 install flaskr-1.0.0-py3-none-any.whl
$ pip3 install uWSGI

$ export FLASK_APP=flaskr
$ flask init-db
Initialized the database.
# generate key
$ python -c 'import os; print(os.urandom(16))'
b'<\xfa\xe6\x91\x10\x16\xd3\x12Q0A(\xbd\xcfwd'
$ vi /usr/var/flaskr-instance/config.py
SECRET_KEY = b'<\xfa\xe6\x91\x10\x16\xd3\x12Q0A(\xbd\xcfwd'

$ uwsgi --http 127.0.0.1:9002 -s /tmp/flaskr.sock --manage-script-name \
> --mount /=flaskr:app
```

## deploy with uWSGI and nginx
``` bash
# first configure according to the previous section and install nginx

# configure uWSGI
$ cat flaskr.ini
[uwsgi]
uid = root
gid = root
socket = /tmp/flaskr.sock
manage-script-name = true
mount = /=flaskr:app
$ uwsgi --ini flaskr.ini

# configure nginx
$ vi /etc/nginx/nginx.conf
user  root;
.......
$ cd /etc/nginx/conf.d
$ cp default.conf flaskr.conf
$ vi flaskr.conf
server {
    listen       9003;
    server_name  127.0.0.1;

    location / {
        try_files $uri @flaskr;
    }

    location @flaskr {
	include uwsgi_params;
	uwsgi_pass unix:/tmp/flaskr.sock;
    }

    ......
}

# configure SELinux
# open http port
$ semanage port -a -t http_port_t -p tcp 9003
$ ausearch -c 'nginx' --raw | audit2allow -M my-nginx
$ semodule -i my-nginx.pp

$ systemctl restart nginx
```

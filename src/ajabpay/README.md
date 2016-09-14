### Create DB
```sh
$ export DATABASE_URL="postgresql://localhost/yourdb"
$ python manage.py create_db
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py db upgrade
```

### Run Back-End

```sh
$ python manage.py runserver
```

### Test Back-End

```sh
$ python test.py --cov-report=term --cov-report=html --cov=application/ tests/
```
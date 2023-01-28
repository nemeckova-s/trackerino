# Trackerino

Using Python 3.9.9

## To install:
```
$ pip install -r requirements.txt
$ pip install -r requirements-dev.txt
```

## To start a development server:
```
$ python manage.py runserver
```

## To format the code:
```
$ pip install oitnb
$ oitnb .
```

## To lint the code:
```
$ flake8
```

## To run all tests:
```
$ python manage.py test
```

## To update requirements.txt or requirements-dev.txt:
```
$ pip install pip-tools
$ pip-compile
$ pip-compile requirements-dev.txt
```

## To prepare and run migrations: 
```
$ python manage.py makemigrations <app name>
$ python manage.py sqlmigrate <app name> <migration number>
$ python manage.py migrate
```

## To create a new superuser:
```
$ python manage.py createsuperuser
```

## To call the API:
```
$ curl http://localhost:8000/api/issues/ -H "Authorization: Token <auth token>"
$ curl http://localhost:8000/api/issues/<issue ID> -H "Authorization: Token <auth token>"
```

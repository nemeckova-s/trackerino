# Trackerino

Using Python 3.9.9

## To start a development server:
```
$ python manage.py runserver
```

## To format the code:
```
$ pip install oitnb
$ oitnb .
```

## To update requirements.txt:
```
$ pip install pip-tools
$ pip-compile
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

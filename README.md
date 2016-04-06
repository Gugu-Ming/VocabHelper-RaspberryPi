# VocabHelper
The site uses Django 1.9. Make sure you already have Django and python3 installed on your comptuer.
```
$pip install django
```
Run the server by command line with
```
$python manage.py runserver 0.0.0.0:80
```
Initialize up the database by
```
$python manage.py makemigrations vocab
Migrations for 'vocab':
  0001_initial.py:
    - Create model .......
    (Some sh!ts go around here)
$python manage.py migrate
Operations to perform:
  Apply all migrations: ...
Running migrations:
  Rendering model states.. DONE
  Applying ... OK
  (Some sh!ts go around here again)
```
Create superuser for editing database by
```
$python manage.py createsuperuser
Username: (TYPE HERE)
Email address: (CAN LEAVE BLANK)
Password: (TYPE)
Password (again): (TYPE)
Super user created successfully.
```
# Features
* Vocab lists can be add in the management page of Django by accessing /admin/
** Login with the superuser account created before
* Viewers can post their own vocab list
* Support multi-vocab-lists view
* *Vocab lists can be viewed in _Alphabetical_ order*

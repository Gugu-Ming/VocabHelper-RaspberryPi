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
$python manage.py makemigrations
(some sh!ts here)
$python manage.py migrate
```
Create superuser for editing database by
```
$python manage.py create superuser
Username: (TYPE HERE)
Email address: (CAN LEAVE BLANK)
Password: (TYPE)
Password (again): (TYPE)
Super user created successfully.
```

# AutoGOLE Dashboard GUI #

## Install instructions ##

**Debian Jessie**

### Install dependencies ###
```
pip install django
pip install django-mysql
pip install mysql-connector-repackaged
```

### Set-up database ###

**Note: Replace username and password as intended.**

```
create database dashboard_django;
GRANT ALL PRIVILEGES ON dashboard_django.* To 'monitor'@'localhost' IDENTIFIED BY 'monitor_pass';
```
```
python manage.py migrate
```

### Start Dashboard GUI ###

```
python manage.py runserver 0.0.0.0:80
```

**Note: The command above will start the django web server to serve the dashboard GUI. While it is suitable for development, for longer term deployments, a proper web server (e.g. apache) should be used.**
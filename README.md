# Auto post tool

## Version info

## I. Version info

-   Postgresql: 14.5
-   Python: 3.9 (for ubuntu 18.04)
-   Library & Framework: See [requirements.txt](./requirement.txt) (for ubuntu see [requirments_ubuntu.txt](./requirements_ubuntu.txt))

## Create database

```
CREATE USER developer SUPERUSER;

ALTER USER developer WITH PASSWORD 'password';

CREATE DATABASE auto_post_tool_dev WITH OWNER developer;
```

## Install Virtual environment

```
python3 -m venv venv
```

## Activate the virtual environment

```
source venv/bin/activate
```

## Install libraries

```
pip install -r requirements.txt
```

## Run development server

Make sure that virtual environment is activated:

```
python3 manage.py runserver
```

## Backup database

```
python3 manage.py dumpdata --indent 2 > initial_database_dev.json
```

## Restore database

```
python3 manage.py loaddata initial_database.json
```

## Run test

```
Hello Duy
```

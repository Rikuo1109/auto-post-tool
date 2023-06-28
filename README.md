# Auto Post Tool

Auto Post Tool is a Django web application built with Django-Ninja that helps you post your content to social media automatically.

## Version Info

- Python: 3.9 (for Ubuntu 18.04)
- Libraries & Frameworks: See `requirements.txt` (for Ubuntu see `requirements_ubuntu.txt`)
## Setting up the Virtual Environment

Auto Post Tool comes with a `requirements.txt` file containing all the Python packages needed to run the application.

To set up a virtual environment for the application, follow these steps:

1. Install `python3-venv` if it's not already installed.

   ```
   $ sudo apt-get install python3-venv
   ```

2. Create a new virtual environment in the project directory.

   ```
   $ python3 -m venv venv
   ```

3. Activate the virtual environment.

   ```
   $ source venv/bin/activate
   ```

4. Install the required packages.

   ```
   pip install -r requirements.txt
   ```

5. When you're done working with the application, you can deactivate the virtual environment.

   ```
   $ deactivate
   ```


## Setting up the Database

Auto Post Tool now uses SQLite instead of PostgreSQL. By default, Django uses a file-based SQLite database, which is located in the project directory as `db.sqlite3`. To set up the database, do the following:

1. Delete the existing `db.sqlite3` file if it exists:

   ```
   $ rm db.sqlite3
   ```

2. Run the Django migration to create the database tables:

   ```
   $ python3 manage.py makemigrations
   $ python3 manage.py migrate
   ```

## Running the Application

Once you've set up the database and virtual environment, you can run the development server with the following command:

```
$ python3 manage.py runserver
```

This will start the server on your local machine, and you can access it by navigating to `http://localhost:8000` in your web browser.

## Database Backup

You can create a backup of the database by running the following command:

```
$ python3 manage.py dumpdata --indent 2 > initial_database_dev.json
```

This will create a JSON file containing the current state of the database for backup purposes.

## Database Restore

If need to restore the database from a backup file, run the following command:

```
$ python3 manage.py loaddata initial_database_dev.json
```

This will restore the database from the specified file.
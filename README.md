# PreadProfiler

## Application Installation

PreadProfiler is a django project.

1. Set Up Your Development Environment inside your folder.

    ```bash
    python -m venv venv

    source venv/bin/activate
    ```

    if you are not using bash shell, for example, on windows you need this command:

    ```windows
    venv\Scripts\activate.bat
    ```

2. Install the Django and Plotly.

    ```bash
    pip install Django
    pip install plotly==4.14.3
    ```

3. Start the server.

    ```bash
    python manage.py runserver
    ```

    Then, in your browser go to localhost:8000 to check the website.

## Custom Django-admin Commands

There are some custom commands for handling csv files in management/commands folder. For example, load_csv is used to load data to our database. Check here if you want to write custom commands:

<https://docs.djangoproject.com/en/3.1/howto/custom-management-commands/>

## Manage Database for Search App

1. Once you’ve updated the models, you can create the migration files with makemigrations:

    ```bash
    python manage.py makemigrations search
    ```

2. Then migrate the tables.

    ```bash
    python manage.py migrate
    ```

3. Then load data using custom command load_csv.

    ``` bash
    python manage.py load_csv
    ```

## Backup Database

1. Here is one example to backup just one table - publication:

    ```windows
    python manage.py dumpdata about.Publication -o publication.json
    ```

2. Here is one example to load backup data for table - publication:

    ```bash
    python manage.py loaddata publication.json
    ```

3. Here is one example to backup just one table - publication:

    ```windows
    python manage.py dumpdata search -o search.json
    ```

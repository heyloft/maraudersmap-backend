# Marauder’s Map Backend

*Backend for the [Marauder's Map Project](https://github.com/heyloft/maraudersmap)*

[![Built with FastAPI](https://img.shields.io/badge/FastAPI-005571?&logo=fastapi)](https://fastapi.tiangolo.com)
![Python Version](https://img.shields.io/badge/python-3.10-brightgreen)
![License](https://img.shields.io/github/license/heyloft/maraudersmap?color=blue)


## 💻️ Development

This project assumes a Python version of `^3.10`, and has not been tested with any other versions. See [Python docs](https://docs.python.org/3.10/using/index.html) for installation instructions for your system.

#### 📄 A note on `make`
The following setup references some commands that utilize the `make` build tool (available in Unix). These are optional convenience commands that might not fit all systems or use cases. Have a look inside `Makefile` to see what they do. Alternatives are provided for each `make` command.

### ✨ Initial setup
You can quickly set up a dev environment with
```
make init
```

Alternatively, do the following:

1. Install [Poetry](https://python-poetry.org/) for Python package management.
    ```
    curl -sSL https://install.python-poetry.org | python3 -
    ```
    > see [Poetry docs](https://python-poetry.org/docs/#installation) for alternative installation methods
2. (Optional, but recommended)
    
    Tell Poetry to create the virtual environment inside the project directory
    ```
    poetry config --local virtualenvs.in-project true
    ```
    > this makes it easier for development environments like VS Code to recognize the correct Python intepreter for the project
3. Install project dependencies
    ```
    poetry install
    ```
    > if Poetry starts complaining about `psycopg2-binary`, simply run `pip install` manually inside the virtual environment
    > ```
    > poetry run pip install psycopg2-binary==2.9.3
    > ```
4. Install [`pre-commit`](https://pre-commit.com/) hooks
    ```
    poetry run pre-commit install
    ```
    > ensures proper formatting and spots common code bugs when committing code

### 🐚 Virtual environment
Most commands need to be run from inside the Poetry virtual environment. This is done by first entering the environment shell with
```
poetry shell
```
> if the above command fails, try the following instead
>```
>source $(poetry env info --path)/bin/activate
>```

Alternatively: prepend all commands with `poetry run` to run them from inside the virtual environment.

<details><summary>Integration with VS Code</summary>

If you're using VS Code, and did not set `virtualenvs.in-project=true` above, you should tell VS Code where your Poetry virtual 
environment is located

Run
```
make vscode
```
or perform the following steps:
1. `Open Workspace Settings (JSON)` via the command palette (`Ctrl+Shift+P`). This will open `.vscode/settings.json`.
2. Add the following settings
```json
{
    "python.pythonPath": "<Poetry Virtualenv Path>",
    "python.defaultInterpreterPath": "<Poetry Virtualenv Executable>"
}
```
where `<Poetry Virtualenv Path>` and `<Poetry Virtualenv Executable>` need to be replaced with your Poetry env values. These can be found with the following command
```
poetry env info
```
This will display something like
```
...

Virtualenv
Python:         3.10.4
Implementation: CPython
Path:           /home/<user>/.cache/pypoetry/virtualenvs/maraudersmap-ljAqK4qE-py3.10
Executable:     /home/<user>/.cache/pypoetry/virtualenvs/maraudersmap-ljAqK4qE-py3.10/bin/python
Valid:          True

...
```

3. Back in your Workspace Settings, replace `<Poetry Virtualenv Path>` with the value of `Path` and `<Poetry Virtualenv Executable>` with the value of `Executable`. For the above example, it will look like this
```json
{
    "python.pythonPath": "/home/<user>/.cache/pypoetry/virtualenvs/maraudersmap-ljAqK4qE-py3.10",
    "python.defaultInterpreterPath": "/home/<user>/.cache/pypoetry/virtualenvs/maraudersmap-ljAqK4qE-py3.10/bin/python"
}
```
</details>

### 🔡 Environment variables
A template `base.env` file is included inside `/maraudersmap`, which can be copied to a local, gitignored `.env` file. These values are only used for local development (e.g. a local database connection string).
```
cp maraudersmap/base.env maraudersmap/.env
```

### 🗄️ Start database
The project requires a PostgreSQL database.
A quick approach for setting this up is to run the official Docker image. Just make sure you have [installed Docker](https://docs.docker.com/get-docker/) first.

A `make` command is available to initialize and start a database with Docker
```
make db
```
> this command also [applies new migrations](#apply-migrations)

Alternatively, run the following
```
docker run -p 5432:5432 -e POSTGRES_PASSWORD=password -v maraudersmap-data:/var/lib/postgresql/data --name maraudersmap-pg postgres:14.5
```

> you could choose any password for the database, but make sure to update the connection string accordingly

> the above command creates a named volume `maraudersmap-data`, which will persist the database data between image restarts (see [Delete database](#💣️-delete-database) if you need a fresh start...)


### 🚀 Run backend

1. Verify that the connection string inside `.env` points to your running database
1. [Apply any new database migrations](#apply-migrations)
2. Start server with
    ```
    make api
    ```
    or
    ```bash
    cd maraudersmap
    uvicorn main:app --host 0.0.0.0 --reload
    ```
    > must be run from `/maraudersmap` directory to recognize `.env`

    > using `--host 0.0.0.0` seems to be required for accessing the backend from outside `localhost`

### ⏩️ Database Migrations

Any changes to the database schema need to be documented in an Alembic migration file (`maraudersmap/alembic/versions`), which is used to upgrade tables in existing databases. 

#### Create migrations
> make sure the database is running

Migration files can be autogenerated with the following
```
cd maraudersmap 
alembic revision --autogenerate -m "<Some descriptive title>"
```

#### Apply migrations
> make sure the database is running

A database can be upgraded to the latest version with the following
```
cd maraudersmap 
alembic upgrade head
```

### 🌱 Seed database
> make sure the database is running

Your database can be kickstarted by injecting some sample code provided in `seed.sql`
```
make seed
```
or
```
docker exec -i maraudersmap-pg /bin/bash -c "PGPASSWORD=password psql --username postgres postgres" < maraudersmap/database/seed.sql
```
> assumes names and passwords as given in `docker run` above.

#### Update `seed.sql`
If you want to update the sample data, simply replace the file with a dump of your current database
```
make dump
```
or
```
docker exec -i maraudersmap-pg /bin/bash -c "PGPASSWORD=password pg_dump --username postgres postgres" > maraudersmap/database/seed.sql
```

### 💣️ Delete database
The database can be deleted with
```
make nukedb
```
or
```
docker stop maraudersmap-pg
docker rm maraudersmap-pg
docker volume rm maraudersmap-data
```

## 🌐 Deployment (with Fly.io)
The backend can be deployed in a lot of places. We currently use [Fly.io](https://fly.io/) for quick prototyping.

#### Initial setup and database
1. Install [`flyctl`](https://fly.io/docs/hands-on/install-flyctl/)
2. Create an account with `fly auth signup` or login with `fly auth login`
3. Create PostgreSQL cluster app
    ```
    fly postgres create -n <unique-psql-app-name>
    ```

#### Development app

1. Create fly app
    ```
    fly apps create <unique-dev-app-name>
    ```
2. Connect to the PostgreSQL cluster you created above
    ```
    fly postgres attach --app <unique-dev-app-name> <unique-psql-app-name>
    ```
3. Set the `app` property to `<unique-dev-app-name>` in `fly.dev.toml`
4. Deploy
    ```
    fly deploy -c fly.dev.toml
    ```

#### Production app

1. Create fly app
    ```
    fly apps create <unique-prod-app-name>
    ```
2. Connect to the PostgreSQL cluster you created above
    ```
    fly postgres attach --app <unique-prod-app-name> <unique-psql-app-name>
    ```
3. Set the `app` property to `<unique-prod-app-name>` in `fly.prod.toml`
4. Deploy
    ```
    fly deploy -c fly.prod.toml
    ```

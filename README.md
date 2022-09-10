<h1 align="center">
    Marauder’s Map Backend
</h1>

<p align="center">
    <a href="https://fastapi.tiangolo.com" target="_blank">
        <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="Built with FastAPI">
    </a>
</p>


## Development setup

> Assumes Python version `3.10^`

1. Install [`Poetry`](https://python-poetry.org/) for Python package management. The following should work for Linux, macOS and Windows (WSL):
```
curl -sSL https://install.python-poetry.org | python3 -
```
2. Install project dependencies
```
poetry install
```
3. Enter Poetry virtual environment (venv)
```
poetry shell
```
> if the above command returns `Virtual environment already activated`, use the following instead
>```
>source $(poetry env info --path)/bin/activate
>```
4. Install [`pre-commit`](https://pre-commit.com/) hooks
```
pre-commit install
```

### Poetry integration with VS Code
If you're using VS Code, you need to tell it where your Poetry virtualenv is located
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
Path:           /home/mathias/.cache/pypoetry/virtualenvs/maraudersmap-ljAqK4qE-py3.10
Executable:     /home/mathias/.cache/pypoetry/virtualenvs/maraudersmap-ljAqK4qE-py3.10/bin/python
Valid:          True

...
```

3. Back in your Workspace Settings, replace `<Poetry Virtualenv Path>` with the value of `Path` and `<Poetry Virtualenv Executable>` with the value of `Executable`. For the above example, it will look like this
```json
{
    "python.pythonPath": "/home/mathias/.cache/pypoetry/virtualenvs/maraudersmap-ljAqK4qE-py3.10",
    "python.defaultInterpreterPath": "/home/mathias/.cache/pypoetry/virtualenvs/maraudersmap-ljAqK4qE-py3.10/bin/python"
}
```

## Run backend
```bash
uvicorn maraudersmap.main:app --reload
```
> omit `--reload` to disable *auto-reload*
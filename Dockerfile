FROM python:3.10.4

WORKDIR /app

RUN pip install "poetry==1.2.0"

COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY . .
 
CMD ["poetry", "run", "uvicorn", "maraudersmap.main:app", "--host", "0.0.0.0", "--port", "8080"]

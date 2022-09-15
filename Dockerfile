FROM python:3.10.4

WORKDIR /app

RUN pip install "poetry==1.2.0"

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false

RUN poetry install

COPY . .

ENV PYTHONPATH=/app

RUN chmod +x entrypoint.sh
CMD ["/bin/bash", "entrypoint.sh"]

FROM python:3.10.4

WORKDIR /app

RUN curl -sSL https://install.python-poetry.org | python3 - -y --version 1.2.0

RUN /root/.local/bin/poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN /root/.local/bin/poetry install

COPY . .

ENV PYTHONPATH=/app

RUN chmod +x entrypoint.sh
CMD ["/bin/bash", "entrypoint.sh"]

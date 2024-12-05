FROM python:3.11.5

WORKDIR /midnite/

RUN pip install poetry
COPY pyproject.toml poetry.lock* /midnite/
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . /midnite/

ENV PYTHONPATH=/
EXPOSE 80
EXPOSE 8000

ENV NAME World

# Access container: docker exec -it midnite_backend_container /bin/sh

FROM python:3.10-slim
COPY . /app
WORKDIR /app
RUN pip install poetry
RUN poetry install -E api
EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "qm9star_query.run_api_server:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

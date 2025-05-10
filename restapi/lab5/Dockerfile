ARG PYTHON_TAG=3.11-slim
FROM python:${PYTHON_TAG}

WORKDIR /service

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.entry:service", "--host", "0.0.0.0", "--port", "8000"]

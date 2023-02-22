FROM python:3.10-buster
WORKDIR /src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./src/requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./src/app .

#CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

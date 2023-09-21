#Stage 1
FROM python:3.11

RUN mkdir -p /app

WORKDIR /app

COPY . .

RUN pip install --upgrade pip

RUN pip install -r ./requirements.txt
#
#CMD ["python", "manage.py", "makemigrations"]
#CMD ["python", "manage.py", "migrate"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "footy.wsgi"]

#Stage 2

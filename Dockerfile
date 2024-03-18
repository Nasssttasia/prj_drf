FROM python:3.10

WORKDIR /app

COPY ./requirements.txt .

RUN python -m pip install --upgrade pip

RUN pip install --no-cache-dir -r ./requirements.txt

COPY . .

#CMD ["python", "manage.py", "runserver"] запускаем в docker-compose
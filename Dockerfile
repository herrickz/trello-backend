FROM python:3.7-slim

WORKDIR /trello-app

COPY . /trello-app

RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8000

RUN python3 manage.py makemigrations

RUN python3 manage.py migrate

# CMD [ "ls" ]

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000"]
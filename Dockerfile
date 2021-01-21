FROM python:3-alpine

ENV SELENIUM_HOST=http://localhost:4444/wd/hub

WORKDIR /usr/src/selenium-test

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY main.py main.py

CMD ["python3", "main.py"]
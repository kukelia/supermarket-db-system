FROM python:latest

WORKDIR /supermarket_app/

ENV POSTGRES_DB=database
ENV POSTGRES_USER=username
ENV POSTGRES_PASSWORD=secret

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY supermarket_menu.py .

CMD [ "python","supermarket_menu.py"]
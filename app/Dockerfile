FROM python:latest

WORKDIR /supermarket_app/

ENV POSTGRES_DB=database
ENV POSTGRES_USER=username
ENV POSTGRES_PASSWORD=secret

COPY requirements.txt supermarket_menu.py ./
RUN pip install -r requirements.txt

CMD [ "python","supermarket_menu.py"]
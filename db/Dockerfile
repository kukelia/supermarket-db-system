FROM postgres:latest

ENV POSTGRES_DB=database
ENV POSTGRES_USER=username
ENV POSTGRES_PASSWORD=secret

COPY ddl.sql /docker-entrypoint-initdb.d/ddl.sql
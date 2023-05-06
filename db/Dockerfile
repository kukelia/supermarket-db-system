FROM postgres:latest

ENV POSTGRES_DB=database
ENV POSTGRES_USER=username
ENV POSTGRES_PASSWORD=secret
# WHEN updating ddl, image must be built again
COPY ddl.sql /docker-entrypoint-initdb.d/ddl.sql
FROM postgres:16.3-alpine
COPY init.sql /docker-entrypoint-initdb.d/

ENV POSTGRES_PASSWORD = "temppass"
ENV POSTGRES_USER = "postgres"
ENV POSTGRES_DB = "postgres"
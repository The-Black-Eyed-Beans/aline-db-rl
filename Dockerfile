FROM mysql:8

COPY aline-db-schema.sql /docker-entrypoint-initdb.d
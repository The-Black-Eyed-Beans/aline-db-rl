FROM mysql

COPY aline-db-schema.sql /docker-entrypoint-initdb.d

ENV MYSQL_ROOT_PASSWORD=password


